#!/usr/bin/env bash
# 把帧序列(frame_%05d.png)合成 mp4。用法: bash scripts/make_video.sh <frames_dir> <out.mp4> [fps]
set -e
DIR="${1:-output/feature3/grasp}"
OUT="${2:-output/feature3/feature3_grasp.mp4}"
FPS="${3:-20}"
FFMPEG="$(command -v ffmpeg || echo /usr/bin/ffmpeg)"
"$FFMPEG" -y -framerate "$FPS" -i "$DIR/frame_%05d.png" \
    -c:v libx264 -pix_fmt yuv420p "$OUT"
ls -la "$OUT"
