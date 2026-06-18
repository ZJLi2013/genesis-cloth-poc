#!/usr/bin/env bash
# feature2 补充：stretch_compliance 扫描（验证拉伸是否为有效旋钮）。
# 单边悬臂竖直悬挂时，软拉伸→自重下伸长→sag 超过布宽、pull_in 变化。
set -uo pipefail
export PYOPENGL_PLATFORM=egl

BACKEND="${1:-amdgpu}"
OUT="output/feature2_stretch2"
mkdir -p "$OUT"
LOG="$OUT/run.log"
echo "=== feature2-stretch(large) run @ $(date -u) backend=$BACKEND ===" | tee "$LOG"

# 大范围 compliance：定位「软区」。XPBD 的 α 受 dt² 缩放，小值全等效刚性。
for S in 1e0 1e2 1e4; do
  TAG="s${S}"
  echo "--- drape stretch=$S (bending fixed 1e-5) ---" | tee -a "$LOG"
  python3 scripts/20_cloth_drape.py --backend "$BACKEND" --stretch "$S" --bending 1e-5 \
    --size 0.2 --rho 1.0 --steps 1200 --render-every 600 --out "$OUT/$TAG" 2>&1 | tee -a "$LOG"
done

echo "=== feature2-stretch done @ $(date -u) ===" | tee -a "$LOG"
grep -a drape-metric "$LOG" | tee -a "$LOG"
