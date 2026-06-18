# feature4：真实衣物资产 + 自碰撞稳定性 + 抓取迁移

状态：**进行中（2026-06-18）**

## 目标

把 feature3 的 flat-cloth 抓取 baseline 推广到**非平面衣物形状**，打掉迁向「真衣服」最大的未知——
**PBD 自碰撞（self-collision）在 RDNA4 上是否稳定、可接受**。衣物一旦自折叠必然自接触，
这是后续操作任务 / 数据生成的地基。

## 关键背景（源码侦察结论）

- Genesis 没有自带衣物 mesh（仅平面 `cloth.obj`）。
- **PBD 自碰撞是内禀的**：`PBDSolver` 用空间哈希做粒子-粒子碰撞，源码 `solvers.py` 中
  `# self collision` 注释正位于 `particle_size` 上方 → **`particle_size` 即自碰撞半径**，
  `hash_grid_cell_size = 1.25 * particle_size`。没有独立开关，碰撞随粒子距离 < particle_size 触发。
  → 自碰撞实验的核心旋钮 = `particle_size`（碰撞半径）+ 网格密度。

## 资产决策（KISS）

用户选「公开单件衣物 OBJ，最省事」。但稳定的可直链下载 OBJ 难找、且容器联网不确定。
折中：**脚本内程序化生成一个最简衣物形——开口圆筒（tube，= 筒裙/无袖筒身）**。理由：
- 是真正的非平面 3D 衣物拓扑（前后两层壁面），抓一点提起 / 压扁时两层壁面必然自接触
  → 天然的自碰撞测试体，比平面方布更接近衣物。
- 零下载依赖、完全可复现。
- 脚本同时支持 `--mesh <path>` 外部 OBJ，后续可无缝换真实衣物资产。

## 实验设计

脚本：`scripts/40_garment_selfcollision_grasp.py`

### Exp 4.1：衣物垂坠 + 自碰撞稳定性
- 生成 tube（半径 r、高 h、周向/纵向分段），竖直悬挂（钉一圈顶 rim），重力下自然垂坠。
- 再把底 rim 往上推 / 抓顶 rim 提起，制造**自折叠**让前后壁接触。
- 扫 `particle_size ∈ {0.008, 0.012, 0.02}`（碰撞半径由小到大）。
- 判据（量化）：
  - `finite=True`（无 NaN/爆飞）——硬性。
  - `penetration_ratio` = 非相邻粒子对中距离 < 0.5·particle_size 的比例（O(N²)，N~1k 可算）；
    自碰撞有效 → 比例低；失效（穿插）→ 比例高。
  - `step_ms` 平均单步耗时（性能可接受性）。

### Exp 4.2：抓取迁移
- 把 feature3 的自标定水平抓取 + `fix_particles_to_link` attach + 解钉，直接迁到 tube 上，
  抓 rim 一点提起。
- 判据：`finite=True`、`cloth_zmin_rise > 0`（整体被拎起）、流程不挂。

## 预期

- 假设成立：存在某个 `particle_size`（预计 ~0.012–0.02）下 `finite=True`、`penetration_ratio` 低、
  `step_ms` 可接受；抓取迁移成功。
- 假设不成立：自折叠下爆飞（finite=False）或穿插率高且无参数可救 → 记录为 PBD 自碰撞在 RDNA4 的限制，
  触发 pivot（换 solver / 降规模 / 加厚度建模）。

## 不做

- 不接真实 USD 资产（后置，脚本已留 `--mesh` 口）。
- 不做衣物操作任务（feature5）/ 数据录制（feature6）。
- 不追求物性精确，只验证「自碰撞稳定 + 抓取可迁移」。
