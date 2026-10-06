"""Hlas z ElevenLabs (take_elevenlabs.mp3, 62,3 s) -> voice.wav + segments.json.
Zrychlení 1,08× (ffmpeg atempo, výška hlasu beze změny) a zkrácení dlouhých pauz mezi větami na max. 0,30 s
(ořezává se jen ticho uprostřed pauzy, s 15ms prolnutím). Pauzy kolem „Dost.“ zůstávají delší (dramatický zlom).
Pak HPF 70 Hz, jemná komprese a normalizace. usage: python3 prep.py"""
import json, os, subprocess, tempfile
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000; TEMPO = 1.08
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
CAP = .30; KEEP = {19: .42, 20: .48}                  # index pauzy (před segmentem) -> délka: před „Dost.“ a po něm
out = [x[:seg[0][1]]]; new = [[seg[0][0] / SR, seg[0][1] / SR]]; pos = seg[0][1]
fade = int(.015 * SR)
for k in range(1, len(seg)):
    a, b = seg[k]; gap = (a - seg[k - 1][1]) / SR; want = KEEP.get(k, CAP)
    g = x[seg[k - 1][1]:a]
    if gap > want:
        keep = int(want * SR); h = keep // 2
        left, right = g[:h], g[len(g) - (keep - h):]
        if len(left) > fade and len(right) > fade:
            r = np.linspace(0, 1, fade); m = left[-fade:] * (1 - r) + right[:fade] * r
            g = np.concatenate([left[:-fade], m, right[fade:]])
        else: g = np.concatenate([left, right])
    out.append(g); cur = sum(len(o) for o in out); out.append(x[a:b])
    new.append([cur / SR, (cur + b - a) / SR])
out.append(x[seg[-1][1]:seg[-1][1] + int(.3 * SR)])
v = np.concatenate(out)
v = sosfilt(butter(2, 70, 'high', fs=SR, output='sos'), v)
env = np.sqrt(np.convolve(v ** 2, np.ones(int(.03 * SR)) / int(.03 * SR), 'same')) + 1e-6
thr = .25 * env.max(); v = v * np.minimum(1, (thr / env) ** .3)
v = v / np.abs(v).max() * .89
sf.write(os.path.join(HERE, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
json.dump({'tempo': TEMPO, 'duration': round(len(v) / SR, 3), 'segments': [[round(a, 3), round(b, 3)] for a, b in new]},
          open(os.path.join(HERE, 'segments.json'), 'w'), indent=1)
print(len(new), 'segments, duration', round(len(v) / SR, 2))
for i, (a, b) in enumerate(new): print(i + 1, round(a, 2), round(b, 2))
