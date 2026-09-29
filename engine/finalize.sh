#!/usr/bin/env bash
# Mux rendered video + synthesized audio into an Instagram-API-safe MP4:
# H.264 video copied as is, AAC 128 kb/s 48 kHz, moov atom first, no edit lists.
# Usage: engine/finalize.sh raw.mp4 audio.wav episodes/dil-XX-slug/video.mp4
set -euo pipefail
ffmpeg -v error -y -i "$1" -i "$2" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -ar 48000 -shortest \
  -movflags +faststart -use_editlist 0 "$3"
python3 - "$3" <<'EOF'
import sys
d = open(sys.argv[1], 'rb').read()
m = d.find(b'mdat')
assert 0 <= d.find(b'moov') < m, 'moov atom is not at the front'
assert d[:m].count(b'elst') == 0, 'edit list present'
print('OK', sys.argv[1], f'{len(d)/1e6:.1f} MB')
EOF
