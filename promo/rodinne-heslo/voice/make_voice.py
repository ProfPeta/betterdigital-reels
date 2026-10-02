"""Hlasovka „Kubíčka“: dětský, přirozeně znějící hlas jako hlasová zpráva nahraná telefonem venku v noci.

1. Neuronové TTS Piper cs_CZ-jirka-medium (offline přes sherpa-onnx). Pro každou větu se vygeneruje několik variant
   s živější prozodií (vyšší noise_scale) a vybere se nejvýraznější intonace bez úletů výšky.
2. Časy slov: DTW zarovnání věty s toutéž větou složenou ze samostatně vyslovených slov (MFCC), takže přepis
   v reel.html sedí na hlas i uvnitř vět.
3. Převod na dětský hlas vokodérem WORLD (časování se nemění): výška ~265 Hz, formanty ×1,27 (hlasové ústrojí
   zhruba desetiletého kluka), širší melodie (×1,3), dýchavost ve výškách, jemné chvění hlasu, „Mami“ jako zavolání.
4. Rytmus: různě dlouhé pauzy a roztřesené nádechy mezi větami.
5. Zvuk telefonu: EQ mikrofonu, jemná komprese, tichá ulice, krátký prostor.

Výstup: voice.wav (48 kHz mono) a words.json (časy slov od začátku souboru, pro přepis v reel.html).
Model: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-cs_CZ-jirka-medium.tar.bz2
usage: python3 make_voice.py <složka s modelem vits-piper-cs_CZ-jirka-medium> [<složka sherpa-onnx-whisper-turbo>]
       S Whisperem (https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2)
       se každá věta po převodu ověří přepisem a nesrozumitelná varianta se nahradí další v pořadí.
Pozn.: VITS dává při každém běhu jiné varianty, zdrojem pravdy je uložený voice.wav.
"""
import json, os, re, sys
import numpy as np, soundfile as sf, pyworld as pw, librosa
from scipy.signal import butter, sosfilt, resample_poly, fftconvolve

D = sys.argv[1].rstrip('/') + '/'
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
#        text v přepisu            text pro TTS                                   rychlost  (pauza po větě v s, nádech?)
SENT = [('Mami, to jsem já.',       'Mamí, to sem já.',                            1.12,   (.10, False)),
        ('Měl jsem nehodu.',        'Měl sem nehodu.',                             1.20,   (.19, True)),
        ('Potřebuju hned peníze.',  'Potřebuju hned peníze.',                      1.22,   (.07, False)),
        ('Nemůžu volat.',           'Nemůžu volat.',                               1.18,   None)]
# Pozn.: Piper vyslovuje „jsem“ s j („Měli jsem“, „to i sem“) a krátké „Mami“ zní jako „Máme“. Hovorové „sem“ a protažené
#       „Mamí“ (dítě volá mámu) znějí přirozeněji a přepisují se správně. V přepisu ve videu zůstává spisovný text.
N_CAND = 8                 # variant TTS na větu
F0_TARGET = 262.0          # Hz, medián výšky (kluci 8–11 let ~240–270 Hz)
FORMANT = 1.27             # posun formantů (dospělý muž -> dítě ~1,25–1,35; žena ~1,15)
RANGE = 1.30               # rozšíření melodie kolem trendu věty
BREATHY = .28              # přidaná dýchavost nad ~1,5 kHz
FP = 5.0                   # WORLD frame period (ms)
rng = np.random.default_rng(7)

import sherpa_onnx
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
    model=D + 'cs_CZ-jirka-medium.onnx', lexicon='', data_dir=D + 'espeak-ng-data', tokens=D + 'tokens.txt',
    noise_scale=.8, noise_scale_w=1.0), num_threads=2), max_num_sentences=1)
tts = sherpa_onnx.OfflineTts(cfg)
FS = 22050                 # nativní vzorkovací frekvence modelu
ASR = None
if len(sys.argv) > 2:
    W = sys.argv[2].rstrip('/') + '/'
    ASR = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=W + 'turbo-encoder.int8.onnx', decoder=W + 'turbo-decoder.int8.onnx',
                                                     tokens=W + 'turbo-tokens.txt', language='cs', task='transcribe', num_threads=2)


EQUIV = {'sem': 'jsem', 'potřebuji': 'potřebuju', 'mamí': 'mami'}   # hovorové a spisovné tvary jsou pro kontrolu totéž
def norm(s): return ' '.join(EQUIV.get(w, w) for w in re.sub(r'[^\w\s]', ' ', s.lower()).split())


def heard(y, fs):
    z = resample_poly(y, 16000, fs).astype(np.float32); z = z / (np.abs(z).max() + 1e-9) * .5
    st = ASR.create_stream(); st.accept_waveform(16000, np.concatenate([np.zeros(8000, np.float32), z, np.zeros(16000, np.float32)]))
    ASR.decode_stream(st); return st.result.text.strip()


def bp(x, lo, hi, fs=SR, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=fs, output='sos'), x)
def hp(x, f, fs=SR, o=2): return sosfilt(butter(o, f, 'high', fs=fs, output='sos'), x)
def lp(x, f, fs=SR, o=2): return sosfilt(butter(o, f, 'low', fs=fs, output='sos'), x)


def trim(x, fs, pre=.012, post=.035):
    e = np.abs(x); idx = np.where(e > .02 * e.max())[0]
    return x[max(0, idx[0] - int(pre * fs)):min(len(x), idx[-1] + int(post * fs))]


def synth(text, speed):
    a = tts.generate(text, sid=0, speed=speed); assert a.sample_rate == FS
    return np.array(a.samples, dtype=np.float64)


def candidate(text, speed):
    x = trim(synth(text, speed), FS)
    f0, t = pw.harvest(x, FS, f0_floor=70, f0_ceil=420, frame_period=FP)
    v = f0[f0 > 0]; st = 12 * np.log2(v / np.median(v))
    return {'x': x, 'dur': len(x) / FS, 'sd': float(st.std()), 'rng': float(np.percentile(st, 95) - np.percentile(st, 5)),
            'jump': float(np.max(np.abs(np.diff(12 * np.log2(v))))) if len(v) > 2 else 0.0, 'f0med': float(np.median(v))}


def rank(cands):
    """Pořadí: nejživější intonace bez úletů výšky (mírně preferuje svižnější variantu), pak ostatní."""
    med = np.median([c['dur'] for c in cands])
    score = lambda c: c['sd'] - 2.0 * (c['dur'] / med - 1)
    ok = [c for c in cands if abs(c['dur'] / med - 1) < .12 and c['rng'] < 13 and c['jump'] < 7]
    ids = {id(c) for c in ok}
    return sorted(ok, key=score, reverse=True) + sorted([c for c in cands if id(c) not in ids], key=score, reverse=True)


HOP = 110                  # 5 ms při 22,05 kHz
def feats(x):
    m = librosa.feature.mfcc(y=x.astype(np.float32), sr=FS, n_mfcc=20, n_fft=512, hop_length=HOP, win_length=441)[1:]
    f = np.vstack([m, librosa.feature.delta(m)])
    return (f - f.mean(1, keepdims=True)) / (f.std(1, keepdims=True) + 1e-6)


def word_bounds(x, text, speed):
    """Hranice slov ve větě x: DTW proti referenci složené ze samostatně vyslovených slov."""
    refs = [trim(synth(w.strip(',.'), speed), FS, .0, .0) for w in text.split()]
    ref = np.concatenate(refs); er = np.cumsum([0] + [len(r) for r in refs])
    _, wp = librosa.sequence.dtw(X=feats(ref), Y=feats(x), metric='cosine'); wp = wp[::-1]
    out = [0.0]
    for e in er[1:-1]:
        rf = int(round(e / HOP)); tg = wp[wp[:, 0] == rf][:, 1]
        if not len(tg): tg = wp[[np.argmin(np.abs(wp[:, 0] - rf))], 1]
        out.append(float(tg.mean()) * HOP / FS)
    return out + [len(x) / FS]


def warp(rows, alpha):
    k = np.arange(rows.shape[1]); src = k / alpha
    return np.array([np.interp(src, k, r) for r in rows])


def kid(x, ratio, first_word_boost=0.0, fw_len=.36):
    """WORLD: výška, melodie, formanty, dýchavost, chvění. Délka a časování zůstávají."""
    f0, t = pw.harvest(x, FS, f0_floor=70, f0_ceil=420, frame_period=FP)
    sp = pw.cheaptrick(x, f0, t, FS); ap = pw.d4c(x, f0, t, FS)
    v = f0 > 0
    lf = np.log2(np.where(v, f0, 1.0))
    tv = t[v]; A = np.vstack([tv, np.ones_like(tv)]).T; coef = np.linalg.lstsq(A, lf[v], rcond=None)[0]
    trend = np.vstack([t, np.ones_like(t)]).T @ coef
    lf2 = trend + (lf - trend) * RANGE + np.log2(ratio)
    if first_word_boost:                                    # „Mami“ jako zavolání: o kousek výš, plynule
        on = t[v][0]; w = np.clip((t - on) / .06, 0, 1) * np.clip((on + fw_len - t) / .12, 0, 1)
        lf2 += first_word_boost / 12 * w
    n = len(t)                                              # jemné chvění: tremolo ~5,8 Hz + jitter
    trem = .0095 * np.sin(2 * np.pi * (5.8 + .4 * np.sin(2 * np.pi * .7 * t)) * t + rng.uniform(0, 6))
    jit = np.convolve(rng.standard_normal(n), np.ones(6) / 6, 'same') * .007
    f0n = np.where(v, 2 ** lf2 * (1 + trem + jit), 0.0)
    sp2 = np.exp(warp(np.log(sp + 1e-12), FORMANT))
    ap2 = warp(ap, FORMANT)
    freqs = np.arange(sp.shape[1]) * FS / ((sp.shape[1] - 1) * 2)
    b = BREATHY * np.clip((freqs - 1500) / 4500, 0, 1)
    ap2 = np.clip(1 - (1 - ap2) * (1 - b), 0, 1)
    y = pw.synthesize(f0n, sp2, ap2, FS, FP)[:len(x)]
    y = np.pad(y, (0, len(x) - len(y)))
    amp = 1 + .05 * np.sin(2 * np.pi * 5.8 * np.arange(len(y)) / FS + 1.3)   # lehké kolísání hlasitosti
    return y * amp, sp2[v].mean(0)


def breath(d, g, env_sp, shaky=False):
    """Nádech: šum tvarovaný průměrnou obálkou (dětského) hlasového traktu + vzduch ve výškách."""
    n = int(d * SR)
    H = np.sqrt(env_sp / env_sp.max()); h = np.fft.irfft(H); h = np.roll(h, len(h) // 2) * np.hanning(len(h))
    x = resample_poly(fftconvolve(rng.standard_normal(int(d * FS) + 64), h, 'same'), 320, 147)[:n]
    x = np.pad(x, (0, n - len(x)))
    x = hp(x, 450) + .35 * np.std(x) * bp(rng.standard_normal(n), 2500, 7000)
    tt = np.arange(n) / n; e = np.sin(np.pi * tt ** .7) ** 1.4
    if shaky: e *= .7 + .3 * np.abs(np.sin(np.pi * 3 * tt))   # roztřesený, trhaný nádech
    s_ = x * e; return s_ / (np.abs(s_).max() + 1e-9) * g


# --- 1) + 2) varianty, výběr, dětský hlas, kontrola srozumitelnosti, hranice slov ---
gen = [[candidate(say, speed) for _ in range(N_CAND)] for _, say, speed, _ in SENT]
ratio = F0_TARGET / np.median([c['f0med'] for cs in gen for c in cs])
chosen, segs, envs = [], [], []
for i, ((text, say, speed, _), cs) in enumerate(zip(SENT, gen)):
    first = None
    for k, c in enumerate(rank(cs)):
        y, env = kid(c['x'], ratio, first_word_boost=1.6 if i == 0 else 0.0)
        first = first or (c, y, env)
        h = heard(y, FS) if ASR else text
        if norm(h) == norm(text): break
        print(f'   varianta {k + 1} zamítnuta, Whisper slyší: „{h}“')
    else:
        c, y, env = first; print('   žádná varianta nebyla přepsána přesně, beru nejlepší podle intonace')
    c['bounds'] = word_bounds(c['x'], say, speed); chosen.append(c)
    segs.append(resample_poly(y, 320, 147)); envs.append(env)
    print(f'{text:26s} vybráno: {c["dur"]:.2f} s, sd {c["sd"]:.2f} st, rozsah {c["rng"]:.1f} st | varianty sd:',
          ' '.join(f'{q["sd"]:.1f}' for q in cs), '| slova:', ' '.join(f'{b:.2f}' for b in c['bounds']))
env_sp = np.mean(envs, 0)

# --- 3) skladba s pauzami a nádechy ---
LEAD = .17                                                            # krátký zalapavý nádech hned po ťuknutí na Přehrát
parts, words, t = [breath(.14, .07, env_sp), np.zeros(int((LEAD - .14) * SR))], [], LEAD
for (text, _, _, gap), x, c in zip(SENT, segs, chosen):
    b = c['bounds']; sc = (len(x) / SR) / b[-1]
    for j, w in enumerate(text.split()): words.append([w, round(t + b[j] * sc, 3), round(t + b[j + 1] * sc, 3)])
    parts.append(x); t += len(x) / SR
    if gap:
        g, br = gap
        parts.append(breath(g, .045, env_sp, shaky=True) if br else np.zeros(int(g * SR))); t += g
parts.append(np.zeros(int(.25 * SR)))
v = np.concatenate(parts)
E = np.sqrt(np.convolve(v ** 2, np.ones(int(.015 * SR)) / int(.015 * SR), mode='same'))
on = np.where(E[int((LEAD - .06) * SR):] > .06 * E.max())[0]           # skutečný nástup prvního slova
if len(on): words[0][1] = round(LEAD - .06 + on[0] / SR, 3)

# --- 4) zvuk telefonu: EQ mikrofonu, presence, jemná komprese, jen lehké zaoblení špiček ---
v = hp(v, 170); v = lp(v, 7800, o=4); v = v + .30 * bp(v, 1900, 4200)
env = np.sqrt(np.convolve(v ** 2, np.ones(int(.02 * SR)) / int(.02 * SR), mode='same')) + 1e-6
thr = .35 * env.max(); v = v * np.minimum(1, (thr / env) ** .4)
v = np.tanh(v / np.abs(v).max() * 1.15)
# tichá noční ulice: hukot, vzdálené auto, trocha větru do mikrofonu
L = len(v); tt = np.arange(L) / SR
rumble = lp(np.cumsum(rng.standard_normal(L)) / 300, 120); rumble -= rumble.mean()
car = bp(rng.standard_normal(L), 300, 2500) * np.exp(-((tt - (L / SR) * .62) / .9) ** 2) * .5
wind = lp(rng.standard_normal(L), 300) * (.5 + .5 * np.sin(2 * np.pi * .7 * tt) ** 2)
amb = rumble / (np.abs(rumble).max() + 1e-9) * .045 + car * .028 + wind * .03
ir_n = int(.22 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / (.05 * SR)); ir = lp(ir, 5000)
ir[:int(.004 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
v = v + fftconvolve(v, ir)[:L] * .10 + amb
v = v / np.abs(v).max() * .9
sf.write(os.path.join(HERE, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
json.dump({'duration': round(L / SR, 3), 'firstWord': words[0][1], 'lastWordEnd': words[-1][2], 'f0': F0_TARGET,
           'formant': FORMANT, 'words': words}, open(os.path.join(HERE, 'words.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({'duration': L / SR, 'speech': [words[0][1], words[-1][2]], 'ratio': round(ratio, 3), 'words': words},
                 ensure_ascii=False))
if ASR: print('Whisper (celá hlasovka):', heard(v, SR))
