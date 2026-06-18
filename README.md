# genesis-cloth-poc

在 AMD RDNA4（R9700）上用 Genesis 做布料/衣物仿真的 POC，验证具身操作场景「单资产 → 抓取 → 数据录制 → 数据生成 → 闭环评估」全链路。

背景与可行性分析见 lehome 仓库 `exp/study.md`（本 repo 不依赖 lehome 代码，仅复用其结论与资产网格）。

## 环境

- 硬件：AMD R9700（RDNA4），ROCm 7.x，radeonsi GPU 硬件光栅化。
- 物理：Genesis `PBDSolver` + `PBD.Cloth`；强接触备选 `IPC(uipc)`。
- 后端：`gs.init(backend=gs.amdgpu)`（计算）/ `gs.vulkan`（渲染），实测确认见 `exp/part1-exp.md`。

## 开发方法

feature-dev-pipeline：backlog（`exp/overall_todo.md`）→ 设计（`exp/design/`）→ 实现+实验（`exp/partN-exp.md`）→ 回填结论（本 README「结论速查」）。

## 结论速查（conclusions-log）

> 每完成一个 feature 回填一行：结论 + 关键证据 + 对后续影响 + 指回 partN。

（暂无）
