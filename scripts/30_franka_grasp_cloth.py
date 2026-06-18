"""feature3: Franka 夹爪抓取悬挂布料的接触验证。

布料顶边钉住成竖直窗帘；Franka 顶向下接近、闭合手指夹住布面、抬起。
验证 PBD 布料 ↔ 刚性夹爪接触链路：手指接触力非零、被夹区域随夹爪上升、全程 finite。

用法:
    python scripts/30_franka_grasp_cloth.py --backend amdgpu --out output/feature3/grasp
"""
import argparse
import os

os.environ["PYOPENGL_PLATFORM"] = "egl"

import numpy as np
import genesis as gs

BACKENDS = {"amdgpu": lambda: gs.amdgpu, "vulkan": lambda: gs.vulkan,
            "cuda": lambda: gs.cuda, "cpu": lambda: gs.cpu}


def _save_png(arr, path):
    arr = np.asarray(arr)
    if arr.dtype != np.uint8:
        arr = (np.clip(arr, 0, 1) * 255).astype(np.uint8)
    try:
        from PIL import Image
        Image.fromarray(arr).save(path)
    except Exception:  # noqa: BLE001
        np.save(path.replace(".png", ".npy"), arr)


def _to_np(t):
    return t.cpu() if hasattr(t, "cpu") else t


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--backend", default="amdgpu", choices=list(BACKENDS))
    p.add_argument("--scale", type=float, default=0.3)
    p.add_argument("--out", default="output/feature3/grasp")
    # 抓取点（布面附近），可调
    p.add_argument("--gx", type=float, default=0.45)
    p.add_argument("--gy", type=float, default=0.0)
    p.add_argument("--gz", type=float, default=0.65)
    args = p.parse_args()
    os.makedirs(args.out, exist_ok=True)

    gs.init(backend=BACKENDS[args.backend]())
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(dt=4e-3, substeps=10),
        pbd_options=gs.options.PBDOptions(
            particle_size=0.01, max_stretch_solver_iterations=8, max_bending_solver_iterations=4
        ),
        show_viewer=False,
    )
    scene.add_entity(gs.morphs.Plane())
    franka = scene.add_entity(gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"))
    # 竖直窗帘：原平面布(XY,法向Z)绕 X 转 90° → XZ 平面、法向 Y，悬于 y≈0。
    cloth = scene.add_entity(
        gs.morphs.Mesh(file="meshes/cloth.obj", scale=args.scale,
                       pos=(args.gx, 0.0, 0.7), euler=(90.0, 0.0, 0.0)),
        material=gs.materials.PBD.Cloth(stretch_compliance=1e-7, bending_compliance=1e-4,
                                        static_friction=0.6, kinetic_friction=0.6),
    )
    cam = scene.add_camera(res=(640, 480), pos=(1.3, 1.0, 0.9),
                           lookat=(0.4, 0.0, 0.5), fov=45, GUI=False)
    scene.build()

    motors = np.arange(7)
    fingers = np.arange(7, 9)
    franka.set_dofs_kp(np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]))
    franka.set_dofs_kv(np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]))
    hand = franka.get_link("hand")

    # 顶边(布面初始 z 最大)钉住成窗帘
    cpos0 = np.asarray(_to_np(cloth.get_particles_pos()))
    top = np.nonzero(cpos0[:, 2] >= cpos0[:, 2].max() - 0.01)[0].astype(np.int32)
    cloth.fix_particles(particles_idx_local=top)
    print(f"[grasp] cloth n={cpos0.shape[0]} pinned_top={top.size} "
          f"z=[{cpos0[:,2].min():.3f},{cpos0[:,2].max():.3f}]")

    grasp_q = np.array([0.0, 1.0, 0.0, 0.0])  # 手心朝下

    def ik_to(pos, w=0.04):
        q = franka.inverse_kinematics(link=hand, pos=np.array(pos), quat=grasp_q)
        q = np.asarray(_to_np(q)).copy(); q[-2:] = w
        return q

    def render(tag):
        rgb = cam.render(rgb=True)
        arr = rgb[0] if isinstance(rgb, (tuple, list)) else rgb
        _save_png(arr, os.path.join(args.out, f"{tag}.png"))

    def step_hold(steps, arm_q, finger_w, tag=None, every=80):
        for s in range(steps):
            franka.control_dofs_position(arm_q[:7], motors)
            franka.control_dofs_position(np.array([finger_w, finger_w]), fingers)
            scene.step()
            if tag and s % every == 0:
                render(f"{tag}_{s:04d}")

    # 0) 布料静置（机械臂保持初始姿态，远离布）
    q_home = np.asarray(_to_np(franka.get_dofs_position())).copy()
    step_hold(300, q_home, 0.04, tag="00_settle", every=150)

    # 1) 瞬移到抓取位（手指张开骑跨薄布面，避免臂扫掠把布打飞）
    q_grasp = ik_to([args.gx, args.gy, args.gz], w=0.04)
    franka.set_dofs_position(q_grasp, zero_velocity=True)
    scene.step(); render("01_teleport")
    z_before = np.asarray(_to_np(cloth.get_particles_pos()))[:, 2].copy()

    # 2) 闭合手指夹住
    step_hold(300, q_grasp, 0.0, tag="02_close", every=80)
    f_force = np.asarray(_to_np(franka.get_links_net_contact_force()))

    # 3) 抬起（IK 缓慢上移）
    q_lift = ik_to([args.gx, args.gy, args.gz + 0.18], w=0.0)
    step_hold(500, q_lift, 0.0, tag="03_lift", every=80)

    cpos = np.asarray(_to_np(cloth.get_particles_pos()))
    finite = bool(np.isfinite(cpos).all())
    # 被夹区域：抓取点附近粒子
    near = np.nonzero(np.linalg.norm(cpos0[:, [0, 2]] - np.array([args.gx, args.gz]), axis=1) < 0.08)[0]
    dz = float(cpos[near, 2].mean() - z_before[near].mean()) if near.size else float("nan")
    print(f"[grasp-metric] finite={finite} near={near.size} grasp_region_dz={dz:.4f} "
          f"cloth_zmax={cpos[:,2].max():.4f} max_finger_contact={np.abs(f_force).max():.4f}")


if __name__ == "__main__":
    main()
