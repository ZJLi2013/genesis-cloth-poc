# part4 实验记录：真实衣物资产 + 自碰撞稳定性 + 抓取迁移

最初要解决的问题：flat-cloth 抓取 baseline（feature3）→「真衣服」之间，最大未知是
**PBD 自碰撞在 RDNA4 上是否稳定可用**。本 feature 用最简非平面衣物（开口圆筒 tube）打掉这个未知。
设计依据见 `design/feature4_garment_asset.md`。脚本 `scripts/40_garment_selfcollision_grasp.py`。

## 总览表

| Exp | 假设 | 状态 | 关键结果 | 结论 |
|-----|------|------|----------|------|
| 4.1 | 存在 particle_size 使自折叠 finite + 低穿插 + 可接受耗时 | ⏳ 待实验 | — | — |
| 4.2 | feature3 抓取 attach 流程可迁到 tube（zmin_rise>0） | ⏳ 待实验 | — | — |

## Phase 0 确认（well-posedness）

本 feature 非策略学习（不涉及 π(obs)→action 单值性），Phase 0 落点在**实验良定性**：
- 4.1 的判据 `finite` / `penetration_ratio` / `step_ms` 均可直接从粒子状态计算，无歧义。
- `penetration_ratio` 定义清晰（非相邻粒子对 < 0.5·particle_size 的比例），能区分「自碰撞生效 vs 穿插」。

## Exp 4.1：衣物垂坠 + 自碰撞稳定性

### 假设
存在某个 `particle_size`（预计 0.012–0.02）下，tube 自折叠时 `finite=True`、`penetration_ratio` 低、
`step_ms` 可接受。

### 方案
- 脚本：`scripts/40_garment_selfcollision_grasp.py`，程序生成 tube（开口圆筒），钉顶 rim，
  重力垂坠 + 制造自折叠。
- 扫描：`particle_size ∈ {0.008, 0.012, 0.02}`。
- 判据：`finite`（硬）、`penetration_ratio`、`step_ms`。

### 结果
（待实验）

### 分析
（待实验）

### 结论与 Next Step
（待实验）

## Exp 4.2：抓取迁移

### 假设
feature3 的自标定水平抓取 + `fix_particles_to_link` attach + 解钉，可直接迁到 tube，抓 rim 提起。

### 方案
- 复用 feature3 抓取流程，目标点改为 tube 的某个 rim 粒子。
- 判据：`finite=True`、`cloth_zmin_rise > 0`、流程不挂。

### 结果
（待实验）

### 分析
（待实验）

### 结论与 Next Step
（待实验）
