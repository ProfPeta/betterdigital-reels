"""Hlasovka „Kuby“: neuronové TTS (Piper cs_CZ-jirka-medium přes sherpa-onnx), zpracované jako hlasová zpráva
nahraná telefonem venku v noci (nádech, EQ, komprese, lehké chvění, tichá ulice, krátký prostor).
Výstup: voice.wav (48 kHz mono) a words.json (časy slov od začátku souboru, pro přepis v reel.html).

Model: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-cs_CZ-jirka-medium.tar.bz2
usage: python3 make_voice.py <složka s modelem vits-piper-cs_CZ-jirka-medium>
"""
import json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly, fftconvolve

D = sys.argv[1].rstrip('/') + '/'
HERE = os.path.dirname(os.path.abspath(__file__))
SENT = ['Mami, to jsem já.', 'Měl jsem nehodu.', 'Potřebuju hned peníze.', 'Nemůžu volat.']
GAPS = [.16, .13, .11]          # pauzy mezi větami
SPEED = 1.3                     # spěch, panika
SR = 48000
rng = np.random.default_rng(42)

import sherpa_onnx
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
    model=D + 'cs_CZ-jirka-medium.onnx', lexicon='', data_dir=D + 'espeak-ng-data', tokens=D + 'tokens.txt'), num_threads=4), max_num_sentences=1)
tts = sherpa_onnx.OfflineTts(cfg)


def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)


def sentence(text):
    a = tts.generate(text, sid=0, speed=SPEED)
    x = np.array(a.samples, dtype=np.float64)
    x = resample_poly(x, 320, 147) if a.sample_rate == 22050 else resample_poly(x, SR, a.sample_rate)
    e = np.abs(x); thr = .02 * e.max(); idx = np.where(e > thr)[0]
    s, t = max(0, idx[0] - int(.01 * SR)), min(len(x), idx[-1] + int(.03 * SR))
    return x[s:t]


def breath(d, g):
    n = int(d * SR); t = np.arange(n) / n
    return bp(rng.standard_normal(n), 400, 2600) * np.sin(np.pi * t) ** 1.6 * g


def syllables(w):
    v = 'aáeéěiíoóuůúyý'; n, prev = 0, False
    for ch in w.lower():
        isv = ch in v; n += isv and not prev; prev = isv
    return max(1, n)


# --- assemble with timing ---
LEAD = .30
parts, words, t = [breath(.26, .05), np.zeros(int((LEAD - .26) * SR))], [], LEAD
for i, s in enumerate(SENT):
    x = sentence(s); d = len(x) / SR
    ws = s.split(); wgt = np.array([syllables(w) + .35 for w in ws], float); wgt /= wgt.sum()
    edges = t + np.concatenate([[0], np.cumsum(wgt)]) * (d - .03)
    for j, w in enumerate(ws): words.append([w, round(float(edges[j]), 3), round(float(edges[j + 1]), 3)])
    parts.append(x); t += d
    if i < len(GAPS):
        g = GAPS[i]; parts.append(breath(g, .025) if i == 1 else np.zeros(int(g * SR))); t += g
parts.append(np.zeros(int(.25 * SR)))
v = np.concatenate(parts)
# snap word boundaries to energy dips (better sync of the transcript highlight)
E = np.sqrt(np.convolve(v ** 2, np.ones(int(.015 * SR)) / int(.015 * SR), mode='same'))
def dip(tc, w=.09):
    i0, i1 = int((tc - w) * SR), int((tc + w) * SR); return (i0 + int(np.argmin(E[i0:i1]))) / SR
for k in range(len(words) - 1):
    if words[k][2] == words[k + 1][1]:                       # boundary inside a sentence
        b_ = round(dip(words[k][2]), 3); words[k][2] = b_; words[k + 1][1] = b_
on = np.where(E[int((LEAD - .06) * SR):] > .06 * E.max())[0]
if len(on): words[0][1] = round(LEAD - .06 + on[0] / SR, 3)

# --- shaky voice: tiny pitch wobble via modulated delay ---
n = np.arange(len(v)); dl = (.00018 * SR) * (1 + np.sin(2 * np.pi * 5.6 * n / SR + .7)) + (.00006 * SR) * np.sin(2 * np.pi * 9.3 * n / SR)
v = np.interp(n - dl, n, v)
# --- phone voice-message character: mic EQ, presence, compression, slight saturation ---
v = hp(v, 160); v = lp(v, 7600, 4); v = v + .35 * bp(v, 1800, 3600)
env = np.sqrt(np.convolve(v ** 2, np.ones(int(.02 * SR)) / int(.02 * SR), mode='same')) + 1e-6
gain = np.minimum(1, (.12 / env) ** .45); v = v * gain
v = np.tanh(v / np.abs(v).max() * 1.6)
# --- night street: low rumble, a distant car, a little wind on the mic ---
L = len(v); tt = np.arange(L) / SR
rumble = lp(np.cumsum(rng.standard_normal(L)) / 300, 120); rumble -= rumble.mean()
car = bp(rng.standard_normal(L), 300, 2500) * np.exp(-((tt - (L / SR) * .62) / .9) ** 2) * .5
wind = lp(rng.standard_normal(L), 300) * (.5 + .5 * np.sin(2 * np.pi * .7 * tt) ** 2)
amb = rumble / (np.abs(rumble).max() + 1e-9) * .05 + car * .03 + wind * .04
# --- short space (car / street), then normalize ---
ir_n = int(.22 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / (.05 * SR)); ir = lp(ir, 5000); ir[:int(.004 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
v = v + fftconvolve(v, ir)[:L] * .12 + amb
v = v / np.abs(v).max() * .9
sf.write(os.path.join(HERE, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
json.dump({'duration': round(L / SR, 3), 'firstWord': words[0][1], 'lastWordEnd': words[-1][2], 'words': words},
          open(os.path.join(HERE, 'words.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({'duration': L / SR, 'speech': [words[0][1], words[-1][2]], 'words': words}, ensure_ascii=False))
