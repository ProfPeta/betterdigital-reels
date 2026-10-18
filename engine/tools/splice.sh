#!/usr/bin/env bash
# Vloží přerenderovaný úsek snímků do celého raw videa (bez renderu celého videa znovu).
# usage: bash engine/tools/splice.sh raw.mp4 seg.mp4 F0 F1 out.mp4
#   seg.mp4 = python3 engine/tools/render_range.py reel.html seg.mp4 F0 F1   (F0, F1 = čísla snímků při 30 fps)
set -e
RAW=$1; SEG=$2; F0=$3; F1=$4; OUT=$5
A=$(python3 -c "print(f'{$F0/30-0.0167:.4f}')"); B=$(python3 -c "print(f'{$F1/30-0.0167:.4f}')")
ffmpeg -v error -y -i "$RAW" -i "$SEG" -filter_complex "[1:v]setpts=PTS-STARTPTS+$F0/30/TB[s];[0:v][s]overlay=eof_action=pass:enable='between(t,$A,$B)'[v]" \
  -map "[v]" -c:v libx264 -preset medium -crf 18 -bf 0 -pix_fmt yuv420p "$OUT"
echo "ok $OUT"
