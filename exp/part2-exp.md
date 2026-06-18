# part2 实验记录：布料 + compliance 物性标定

目标：建立「材质参数 → 布料行为」的标定方法论，并验证 RDNA4 上结果稳定可控。
脚本：`scripts/20_cloth_drape.py`（悬臂垂坠）、`scripts/21_cloth_over_cylinder.py`（搭圆柱）、`scripts/run_feature2.sh`。

## 实验矩阵与结果

| 轮次 | 构型 | 扫描 | 关键指标 | 结果 |
|------|------|------|----------|------|
| 2.1 | 单边悬臂，0.4m，rho=4 | bending 1e-6/1e-4/1e-2 | sag | 三者 sag≈0.396（=布宽），**无差别** |
| 2.2 | 单边悬臂，0.2m，rho=1 | bending 1e-12/1e-9/1e-6/1e-3 | sag | 全部 sag≈0.2002（=布宽），**无差别** |
| 2.3 | 搭水平圆柱，0.4m | bending 1e-10/1e-6(/1e-3/1e-1 被中断) | half_width / bottom_z | 0.2149 vs 0.2160，**无差别**；bottom_z=0.005(触地) |

所有轮次 `finite=True`（无 NaN/爆飞），`fix_particles` 钉固定端稳定。

## 关键结论（重要，影响后续 feature）

1. **`bending_compliance` 在该 Genesis 1.1.1 build 中对宏观垂坠几乎无影响**（1e-12~1e-1 全程一致）。
   即使 1e-12（近似刚性）也无法让布料抗弯——布料表现为**近似纯膜**（membrane），弯曲约束基本不生效。
2. **物理洞察（2.1/2.2 为何无效）**：单边钉住的平面布，平衡态是「平整竖直悬挂」，
   竖直平面布**曲率为零 → 弯曲能为零**，故 bending 刚度天然不参与。必须用强制曲率的构型
   （搭圆柱）才可能体现 bending——但 2.3 显示即便强制曲率，该 build 的 bending 仍无判别力。
3. **标定方法论已建立且有效**：用「参数扫描 + 可量化几何指标（sag / half_width / bottom_z）+ 单调性检查 + 侧视渲染人工核对」即可标定。问题不在方法，而在 bending 这个旋钮本身在该 build 失效。

## 踩坑

- 2.3 圆柱过高 + 布过长 → 两侧垂到地面（bottom_z=0.005），指标被地面接触污染。后续应抬高 cylinder 或缩短布，使布悬空不触地。
- 仿真链路稳定，没有数值发散问题。

## Next Step（feature2 收尾前）

- bending 不是可用旋钮 → 需验证 **`stretch_compliance` 是否为有效旋钮**（拉伸/回缩 pull_in 应随之变化），
  给 feature2 至少留一个可标定的物性维度。
- 真实 towel USD 资产导入仍后置（feature2.1）。
- 风险记录：若要真实「软/硬布」差异，可能需排查 PBD bending 约束是否随网格生成、或换更高网格分辨率 / 更新版 Genesis。
