# part2 实验记录：布料 + compliance 物性标定

目标：建立「材质参数 → 布料行为」的标定方法论，并验证 RDNA4 上结果稳定可控。
脚本：`scripts/20_cloth_drape.py`（悬臂垂坠）、`scripts/21_cloth_over_cylinder.py`（搭圆柱）、`scripts/run_feature2.sh`。

## 实验矩阵与结果

| 轮次 | 构型 | 扫描 | 关键指标 | 结果 |
|------|------|------|----------|------|
| 2.1 | 单边悬臂，0.4m，rho=4 | bending 1e-6/1e-4/1e-2 | sag | 三者 sag≈0.396（=布宽），**无差别** |
| 2.2 | 单边悬臂，0.2m，rho=1 | bending 1e-12/1e-9/1e-6/1e-3 | sag | 全部 sag≈0.2002（=布宽），**无差别** |
| 2.3 | 搭水平圆柱，0.4m | bending 1e-10/1e-6(/1e-3/1e-1 被中断) | half_width / bottom_z | 0.2149 vs 0.2160，**无差别**；bottom_z=0.005(触地) |

| 2.4 | 单边悬臂，0.2m | stretch 1e0/1e2/1e4 | sag | **有效**：0.255 / 0.995 / 0.995（详见下表） |

所有轮次 `finite=True`（无 NaN/爆飞），`fix_particles` 钉固定端稳定。

## 2.4 大范围 stretch 扫描（找到工作区间）

| stretch_compliance | sag | 说明 |
|--------------------|-----|------|
| 1e-9 ~ 1e-2 | 0.2002~0.2008 | 不可伸长（=布宽），等效刚性 |
| 1e0 | 0.2549 | 开始伸长 |
| 1e2 | 0.9946 | 强烈伸长，垂到地面 |
| 1e4 | 0.9949（pull_in<0 摊开） | 橡皮筋式 |

→ **`stretch_compliance` 是有效旋钮，转折点在 ~1e-1…1e0**。

## 社区参考（回应"有没有 sample 参数"）

- 官方示例 `examples/tutorials/pbd_cloth.py`：**直接用默认 `PBD.Cloth()`**，`dt=4e-3, substeps=10`，
  不调 compliance；靠 **mesh + 钉点** 出效果。钉点用 `cloth.fix_particles(cloth.find_closest_particle((x,y,z)))`。
- 默认值（v1.0/1.1，readthedocs 确认）：`rho=4.0, stretch_compliance=1e-7, bending_compliance=1e-5,
  stretch_relaxation=0.3, bending_relaxation=0.1, static/kinetic_friction=0.15, air_resistance=1e-3`。
- 自带真实布料网格：`genesis/assets/meshes/cloth.obj`（可直接 `gs.morphs.Mesh(file="meshes/cloth.obj")`）。
- 额外旋钮：`stretch_relaxation`/`bending_relaxation`，"值越小约束越弱"。

## 关键结论（重要，影响后续 feature）

1. **为何小范围 compliance 扫描无效（solver 数学）**：`pbd_solver.py:421` 用
   `alpha = compliance / substep_dt²`，`dp = -C/(w1+w2+alpha)·relaxation`。`substep_dt=dt/substeps=4e-4` →
   `substep_dt²=1.6e-7`。对轻布每粒子逆质量 `w≈3e4`，只有当 `alpha≳w`（即 **compliance ≳ ~1e-2**）才进入软区。
   1e-12~1e-2 全在「alpha≪w → 等效刚性」区，故无差别。**这不是 build 的 bug，是 XPBD 的正常缩放**。
2. **默认值是刻意的「近乎不可伸长」**：真实布料拉伸刚度极高、弯曲很软；官方默认 stretch=1e-7 即落在刚性区。
3. **标定建议**：
   - 拉伸：日常布料保持默认（1e-7，不可伸长）；要"弹性布/橡皮"用 1e0~1e2。
   - 弯曲：默认 1e-5 偏硬；要更软的垂坠/折叠，bending_compliance 同样需推到 ~1e-2 以上（且需用强制曲率的构型才看得出，见下）。
   - 钉点优先用 `find_closest_particle`，比手动按坐标筛索引稳。
4. **单边平面布的 bending 测试天然无效**：平衡态是平整竖直（曲率=0、弯曲能=0），与 bending 刚度无关。
   要标定 bending 必须用搭圆柱/折叠等强制曲率构型，且 compliance 要进入软区。

## 踩坑

- 2.3 圆柱过高 + 布过长 → 两侧垂到地面（bottom_z=0.005），指标被地面接触污染。后续抬高 cylinder 或缩短布。
- 仿真链路稳定，全程无 NaN/发散。

## Next Step

- feature2 收尾：标定图谱与方法论已建立（stretch 工作区间明确）。
- feature2.1（后置增强）：用 `meshes/cloth.obj` 真实网格 + `find_closest_particle` 复跑，并把 bending 推到软区
  （搭圆柱构型）做一次弯曲标定确认。
- 进入 feature3：机器人 + 夹爪抓布接触验证。
