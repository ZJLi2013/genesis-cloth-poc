# feature1：环境就绪 + 最小布料 smoke

状态：**as-built ✅（2026-06-18，R9700 验证通过）**

端到端验证：`gs.amdgpu` 原生生效；PBD 布料 step 稳定无 NaN；EGL GPU 离屏渲染出图。详见 `../part1-exp.md`。
实现：`scripts/00_env_check.py`、`scripts/10_cloth_smoke.py`、`scripts/run_feature1.sh`。

## 核心判断

先确认 RDNA4（R9700）上 Genesis 能：选对计算后端、建 `PBD.Cloth` 场景、`step` 不崩、GPU 渲染出非空图像。这是后续一切的地基，不引入任何资产/机器人。

## Scope

做：
- `scripts/00_env_check.py`：初始化 Genesis，打印实际生效 backend、GPU、ROCm 信息。
- `scripts/10_cloth_smoke.py`：程序生成一块网格布，在重力下下落到地面，PBD 求解；挂相机渲染若干帧存 PNG，验证 GPU 光栅化。

不做（留后续 feature）：
- 真实毛巾/衣物资产导入（feature2）
- 物性精细标定（feature2）
- 机器人 / 夹爪 / 抓取（feature3）
- 状态录制回放（feature4）

## Problem / 不确定项

- `gs.amdgpu`（ROCm/HIP）与 `gs.vulkan` 在 R9700 上哪个能跑计算、哪个能渲染，需实测。
- 是否需 `HSA_OVERRIDE_GFX_VERSION`（ROCm gfx 匹配）。
- Genesis 版本与 API 漂移（`add_entity` / `PBD.Cloth` / camera 签名）。

## Design

- 布料网格：脚本内程序生成 N×N 平面 OBJ（不依赖外部资产），避免与 feature2 的资产导入耦合。
- 场景：`gs.morphs.Plane()` 地面 + 程序布料悬空下落。
- 后端：默认 `gs.amdgpu`，命令行可切 `gs.vulkan` / `gs.cpu` 作回退。
- 渲染：`scene.add_camera(GUI=False)` 离屏渲染，每隔若干步存 PNG。

## 影响范围

新建 `scripts/00_env_check.py`、`scripts/10_cloth_smoke.py`、`assets/cloth/_grid_autogen.obj`（运行时生成）。无既有代码改动。

## Tests / 验收

1. `00_env_check.py` 打印的 backend 与预期一致（非回退到 CPU）。
2. `10_cloth_smoke.py` 连续 step 1000 次不崩、无 NaN。
3. 输出 PNG 非全黑（GPU 渲染生效），布料呈现下落+铺展的合理形态。

## 边界 / 回退

- `gs.amdgpu` 渲染异常 → 切 `gs.vulkan`。
- gfx 报 "invalid device function" → 设 `HSA_OVERRIDE_GFX_VERSION`（如 `11.0.0`）。
- API 不匹配 → 记录实际签名到 `part1-exp.md`，修正脚本。
