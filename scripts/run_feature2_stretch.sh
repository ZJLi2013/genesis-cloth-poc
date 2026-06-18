#!/usr/bin/env bash
# feature2 补充：stretch_compliance 扫描（验证拉伸是否为有效旋钮）。
# 单边悬臂竖直悬挂时，软拉伸→自重下伸长→sag 超过布宽、pull_in 变化。
set -uo pipefail
export PYOPENGL_PLATFORM=egl

BACKEND="${1:-amdgpu}"
OUT="output/feature2_stretch"
mkdir -p "$OUT"
LOG="$OUT/run.log"
echo "=== feature2-stretch run @ $(date -u) backend=$BACKEND ===" | tee "$LOG"

for S in 1e-9 1e-5 1e-2; do
  TAG="s${S}"
  echo "--- drape stretch=$S (bending fixed 1e-5) ---" | tee -a "$LOG"
  python3 scripts/20_cloth_drape.py --backend "$BACKEND" --stretch "$S" --bending 1e-5 \
    --size 0.2 --rho 1.0 --steps 1200 --render-every 600 --out "$OUT/$TAG" 2>&1 | tee -a "$LOG"
done

echo "=== feature2-stretch done @ $(date -u) ===" | tee -a "$LOG"
grep -a drape-metric "$LOG" | tee -a "$LOG"
