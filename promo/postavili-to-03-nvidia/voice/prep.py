"""Hlas z ElevenLabs (take_elevenlabs.mp3) -> voice.wav + segments.json.
Mírné zrychlení (ffmpeg atempo, výška hlasu beze změny) a zkrácení dlouhých pauz mezi větami na max. CAP
(ořezává se jen ticho uprostřed pauzy, s 15ms prolnutím). Pauzy delší než 0,8 s (záměrné [pause]) se zkrátí na 0,5 s.
Pak HPF 70 Hz, jemná komprese a normalizace. usage: python3 prep.py [TEMPO] [CAP]"""
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.05
CAP = float(sys.argv[2]) if len(sys.argv) > 2 else .32
with tempfile.TemporaryDirectory() as d:
    w = os.path.join(d, 'v.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(HERE, 'take_elevenlabs.mp3'), '-af', f'atempo={TEMPO}', '-ac', '1', '-ar', str(SR), w], check=True)
    x, _ = sf.read(w)
def segments(x):
    win = int(.02 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, 'same')); db = 20 * np.log10(e + 1e-9)
    on = db > db.max() - 38; segs = []; i = 0; n = len(on); hold = int(.12 * SR)
    while i < n:
        if on[i]:
            j = i
            while j < n and (on[j] or on[j:j + hold].any()): j += 1
            segs.append([i, j]); i = j
        else: i += 1
    return segs
seg = segments(x)
out = [x[:seg[0][1]]]; new = [[seg[0][0] / SR, seg[0][1] / SR]]; fade = int(.015 * SR); gaps = []
for k in range(1, len(seg)):
    a, b = seg[k]; gap = (a - seg[k - 1][1]) / SR; want = .5 if gap > .8 else CAP; gaps.append(round(gap, 2))
    g = x[seg[k - 1][1]:a]
    if gap > want:
        keep = int(want * SR); h = keep // 2; left, right = g[:h], g[len(g) - (keep - h):]
        if len(left) > fade and len(right) > fade:
            r = np.linspace(0, 1, fade); g = np.concatenate([left[:-fade], left[-fade:] * (1 - r) + right[:fade] * r, right[fade:]])
        else: g = np.concatenate([left, right])
    out.append(g); cur = sum(len(o) for o in out); out.append(x[a:b]); new.append([cur / SR, (cur + b - a) / SR])
out.append(x[seg[-1][1]:seg[-1][1] + int(.3 * SR)])
v = sosfilt(butter(2, 70, 'high', fs=SR, output='sos'), np.concatenate(out))
env = np.sqrt(np.convolve(v ** 2, np.ones(int(.03 * SR)) / int(.03 * SR), 'same')) + 1e-6
v = v * np.minimum(1, (.25 * env.max() / env) ** .3); v = v / np.abs(v).max() * .89
sf.write(os.path.join(HERE, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
json.dump({'tempo': TEMPO, 'cap': CAP, 'duration': round(len(v) / SR, 3), 'segments': [[round(a, 3), round(b, 3)] for a, b in new]},
          open(os.path.join(HERE, 'segments.json'), 'w'), indent=1)
print(len(new), 'segmentů, délka', round(len(v) / SR, 2), 's; původní pauzy:', gaps)
for i, (a, b) in enumerate(new): print(i + 1, round(a, 2), round(b, 2), round(b - a, 2))
