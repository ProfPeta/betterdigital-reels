#!/usr/bin/env bash
# Stáhne Whisper large-v3-turbo pro sherpa-onnx (~1 GB) do engine/tools/sherpa-onnx-whisper-turbo (gitignore).
# Potřebuje: pip install --break-system-packages sherpa-onnx soundfile scipy
# Stahování trvá déle než 2 min – spouštěj na pozadí: nohup bash engine/tools/get_whisper.sh > /tmp/whisper_dl.log 2>&1 &
set -e
cd "$(dirname "$0")"
[ -d sherpa-onnx-whisper-turbo ] && { echo "už staženo"; exit 0; }
curl -sSL -o turbo.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2
tar xjf turbo.tar.bz2 && rm turbo.tar.bz2 && echo hotovo
