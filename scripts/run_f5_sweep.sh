#!/usr/bin/env bash
# feature5: N=6 episode pick-and-place 成功率扫描 (单进程/episode, 不渲染)
set -e
cd "$(dirname "$0")/.."
R=output/feature5/sweep.log
mkdir -p output/feature5
rm -f "$R"

# ep garment_x target_x target_y
run() {
  PYOPENGL_PLATFORM=egl python scripts/50_garment_pick_place.py \
    --ep "$1" --garment-x "$2" --target-x "$3" --target-y "$4" \
    --out "output/feature5/ep$1" 2>&1 | grep -E -e f5-ep -e Traceback | tee -a "$R"
}

run 0 0.42 0.75 0.02
run 1 0.42 0.68 0.12
run 2 0.40 0.72 -0.10
run 3 0.44 0.80 0.00
run 4 0.40 0.65 0.08
run 5 0.44 0.78 -0.06

echo "=== sweep done ==="
cat "$R"
python - "$R" <<'PY'
import sys, re
lines = open(sys.argv[1]).read().splitlines()
eps = [l for l in lines if "f5-ep" in l]
succ = sum(1 for l in eps if "success=True" in l)
errs = [float(re.search(r"place_err=([0-9.]+)", l).group(1)) for l in eps if "place_err=" in l and "nan" not in l]
print(f"[f5-summary] episodes={len(eps)} success={succ} rate={succ/max(1,len(eps)):.2f} "
      f"mean_place_err={sum(errs)/max(1,len(errs)):.4f}")
PY
