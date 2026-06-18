# part5 实验记录：可重复衣物操作任务 + 成功率

最初要解决的问题：定义**一个可重复、可量化成功率的衣物操作任务**，作为 feature6 合成数据的专家轨迹来源。
设计依据 `design/feature5_garment_task.md`。脚本 `scripts/50_garment_pick_place.py`。

## 总览表

| Exp | 假设 | 状态 | 关键结果 | 结论 |
|-----|------|------|----------|------|
| 5.1 | 专家 pick-and-place 在多 (garment_x,target) 上高成功率 | ⏳ 待实验 | — | — |

## 任务

衣物（tube 筒裙）悬挂 → 专家：自标定水平抓取 rim + attach + 解钉顶 rim + 抬起 +
移到目标上方 + 下降 + 松开 → 衣物落到目标。
`success = 质心到目标水平距离 < tol(0.10) 且 finite`。

## Phase 0（面向 feature6）

专家用 GT 状态，本实验良定。**为 feature6 预埋**：action 依赖 garment 形态 + target 位姿，
录制时 observation 必须含此二者，否则 π 非单值（skill Phase 0 教训）。

## Exp 5.1：pick-and-place 成功率

### 方案
- N=6 确定性 episode，覆盖 garment_x ∈ {0.40,0.42,0.44} × target 近/远/左/右。
- 判据：success rate、平均 place_err、lifted。

### 结果
（待实验）

### 分析
（待实验）

### 结论与 Next Step
（待实验）
