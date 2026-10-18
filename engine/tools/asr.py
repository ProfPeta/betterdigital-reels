"""Kontrola srozumitelnosti hlasovky: Whisper large-v3-turbo (sherpa-onnx), čeština.
usage: python3 asr.py file1.wav [file2.wav ...] [--start s --end s]"""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import resample_poly
import sherpa_onnx

D = os.environ.get('WHISPER_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sherpa-onnx-whisper-turbo')).rstrip('/') + '/'
args = sys.argv[1:]
st = en = None
if '--start' in args:
    i = args.index('--start'); st = float(args[i + 1]); del args[i:i + 2]
if '--end' in args:
    i = args.index('--end'); en = float(args[i + 1]); del args[i:i + 2]
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=D + 'turbo-encoder.int8.onnx', decoder=D + 'turbo-decoder.int8.onnx',
    tokens=D + 'turbo-tokens.txt', language='cs', task='transcribe', num_threads=8)
for f in args:
    x, sr = sf.read(f, dtype='float32', always_2d=True)
    x = x.mean(1)
    if st is not None or en is not None:
        x = x[int((st or 0) * sr):int(en * sr) if en else None]
    if sr != 16000:
        from math import gcd
        g = gcd(16000, sr); x = resample_poly(x, 16000 // g, sr // g).astype(np.float32)
    x = np.concatenate([np.zeros(8000, np.float32), x, np.zeros(16000, np.float32)])
    s = rec.create_stream(); s.accept_waveform(16000, x); rec.decode_stream(s)
    print(f'{os.path.basename(f)}: {s.result.text.strip()}')
