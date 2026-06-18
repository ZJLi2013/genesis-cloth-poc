#!/usr/bin/env bash
# feature2.1: 真实 cloth.obj 桌沿悬臂 + bending 软区扫描。
# 预期：bending 进入软区(≳~1e-3)后，droop 随 compliance 单调增大。
set -uo pipefail
export PYOPENGL_PLATFORM=egl

BACKEND="${1:-amdgpu}"
OUT="output/feature2_1"
mkdir -p "$OUT"
LOG="$OUT/run.log"
echo "=== feature2.1 run @ $(date -u) backend=$BACKEND ===" | tee "$LOG"

# bending 从刚性区跨到软区。
for B in 1e-4 1e-2 1e0 1e2; do
  TAG="b${B}"
  echo "--- real-cloth cantilever bending=$B ---" | tee -a "$LOG"
  python3 scripts/22_real_cloth_bending.py --backend "$BACKEND" --bending "$B" --stretch 1e-7 \
    --scale 0.4 --steps 1500 --render-every 500 --out "$OUT/$TAG" 2>&1 | tee -a "$LOG"
done

echo "=== feature2.1 done @ $(date -u) ===" | tee -a "$LOG"
grep -a f21-metric "$LOG" | tee -a "$LOG"
