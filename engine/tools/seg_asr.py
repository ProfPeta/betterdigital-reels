"""Přepis každého segmentu hlasu zvlášť (Whisper turbo, sherpa-onnx) – pro mapu vět. usage: python3 -I seg_asr.py voice.wav segments.json out.json"""
import sys, os, json, numpy as np, soundfile as sf
from math import gcd
from scipy.signal import resample_poly
import sherpa_onnx
D = os.environ.get('WHISPER_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sherpa-onnx-whisper-turbo')).rstrip('/') + '/'
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=D + 'turbo-encoder.int8.onnx', decoder=D + 'turbo-decoder.int8.onnx',
    tokens=D + 'turbo-tokens.txt', language='cs', task='transcribe', num_threads=8)
x, sr = sf.read(sys.argv[1], dtype='float32'); seg = json.load(open(sys.argv[2]))['segments']; out = []
g = gcd(16000, sr)
for k, (a, b) in enumerate(seg):
    y = x[int(max(0, a - .05) * sr):int((b + .08) * sr)]
    y = resample_poly(y, 16000 // g, sr // g).astype(np.float32)
    y = np.concatenate([np.zeros(4000, np.float32), y, np.zeros(8000, np.float32)])
    s = rec.create_stream(); s.accept_waveform(16000, y); rec.decode_stream(s)
    out.append([k + 1, round(a, 2), round(b, 2), s.result.text.strip()]); print(out[-1], flush=True)
json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False, indent=0)
