#!/usr/bin/env bash
# feature1 runner: 在容器内顺序跑 env_check + cloth_smoke，全部日志写到 output/。
# 设计为可 detach 执行（docker run -d ... bash -lc 'scripts/run_feature1.sh <backend>'）。
set -uo pipefail

BACKEND="${1:-amdgpu}"
# RDNA4 headless 渲染走 EGL（radeonsi GPU 光栅化），否则 pyrender 退回 glx 无显示报错。
export PYOPENGL_PLATFORM="${PYOPENGL_PLATFORM:-egl}"
OUT="output/feature1"
mkdir -p "$OUT"
LOG="$OUT/run.log"

echo "=== feature1 run @ $(date -u) backend=$BACKEND ===" | tee "$LOG"

echo "--- Exp 1.1 env_check ---" | tee -a "$LOG"
python3 scripts/00_env_check.py --backend "$BACKEND" 2>&1 | tee -a "$LOG"
EC1=${PIPESTATUS[0]}
echo "env_check exit=$EC1" | tee -a "$LOG"

echo "--- Exp 1.2 cloth_smoke ---" | tee -a "$LOG"
python3 scripts/10_cloth_smoke.py --backend "$BACKEND" --steps 1000 --out "$OUT/smoke" 2>&1 | tee -a "$LOG"
EC2=${PIPESTATUS[0]}
echo "cloth_smoke exit=$EC2" | tee -a "$LOG"

echo "=== feature1 done @ $(date -u) env_check=$EC1 smoke=$EC2 ===" | tee -a "$LOG"
