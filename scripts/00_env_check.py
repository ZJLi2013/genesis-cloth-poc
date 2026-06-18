"""feature1 Exp 1.1: 确认 Genesis 在 RDNA4 上的计算后端是否正确生效。

用法:
    python scripts/00_env_check.py --backend amdgpu
"""
import argparse

import genesis as gs

BACKENDS = {
    "amdgpu": lambda: gs.amdgpu,
    "vulkan": lambda: gs.vulkan,
    "cuda": lambda: gs.cuda,
    "cpu": lambda: gs.cpu,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend", default="amdgpu", choices=list(BACKENDS), help="Genesis 计算后端"
    )
    args = parser.parse_args()

    # gs.init 会在日志中打印实际生效的 backend、GPU 名与显存。
    # 若回退到 CPU，说明该后端在本节点不可用（见 part1-exp 回退项）。
    gs.init(backend=BACKENDS[args.backend]())
    print(f"[env-check] 请求 backend={args.backend}；以上 Genesis 日志为实际生效结果。")


if __name__ == "__main__":
    main()
