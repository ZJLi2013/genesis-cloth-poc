# part1 实验记录：环境就绪 + 最小布料 smoke

| Exp | 目标 | 状态 | 结论 |
|-----|------|------|------|
| 1.1 | R9700 上 `00_env_check` 确认 backend | 待跑 | - |
| 1.2 | `10_cloth_smoke` step 不崩 + 渲染出图 | 待跑 | - |

## 环境

- 节点：AMD R9700（RDNA4），ROCm 7.x。
- 安装：`pip install git+https://github.com/Genesis-Embodied-AI/Genesis@main`；torch(ROCm) 按节点版本装。
- 执行方式：本地改 → push → 节点 pull → 跑（local-push-remote-pull-test）。

## 命令

```bash
python scripts/00_env_check.py --backend amdgpu
python scripts/10_cloth_smoke.py --backend amdgpu --steps 1000 --out output/smoke
```

## Exp 1.1 — env check

- 假设：`gs.init(backend=gs.amdgpu)` 在 R9700 正常生效，不回退 CPU。
- 预期：日志显示 `backend gs.amdgpu` + GPU 名 `AMD Radeon ...`。
- 实际：_（待回填）_
- 分析 / 结论：_（待回填）_

## Exp 1.2 — cloth smoke

- 假设：PBD 布料场景能 build + step 1000 次，相机渲染出非空图。
- 预期：无崩溃/NaN；PNG 显示布料下落铺展。
- 实际：_（待回填）_
- 分析 / 结论：_（待回填）_

## Next Step

_（待回填：feature1 完成后回填结论到 README 结论速查，并拆 feature2。）_
