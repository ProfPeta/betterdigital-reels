"""Hlasovka „Kubíčka“ jako skutečná hlasová zpráva z telefonu: vyděšené dítě, které nemůže mluvit nahlas.

Styly (--style):
  whisper  šepot (výchozí). Bez hlasivek, takže nezbude syntetická intonace ani „vokodérový“ bzukot, který
           u převodu dospělého TTS na dětský hlas zní uměle. Sedí na „Nemůžu volat.“ a podvodníci šepot
           i pláč používají, protože se hlas hůř pozná.
  hushed   přidušený, dýchavý dětský hlas (trochu hlasivek, hodně vzduchu).
  voice    normální dětský hlas (WORLD: ~265 Hz, formanty ×1,27).

Postup:
1. Neuronové TTS Piper cs_CZ-jirka-medium (offline přes sherpa-onnx). Pro každou větu se vygeneruje 8 variant.
2. Převod vokodérem WORLD (časování se nemění): formanty ×1,25 (hlasové ústrojí zhruba desetiletého dítěte),
   podle stylu šepot / dýchavý hlas / hlas, chvění strachem.
3. Kontrola srozumitelnosti Whisperem (volitelně, --asr). Nesrozumitelná varianta se nahradí další v pořadí.
4. Časy slov: DTW zarovnání věty s toutéž větou složenou ze samostatně vyslovených slov (MFCC).
5. Lidské zvuky: šustnutí telefonu na začátku a na konci, roztřesené nádechy, popotáhnutí nosem, výdech.
6. Telefon: EQ mikrofonu, automatické zesílení (komprese, víc slyšet okolí), tichá ulice, kodek Opus 24 kb/s
   jako u hlasových zpráv v messengerech.

Výstup: voice.wav (48 kHz mono) a words.json (časy slov od začátku souboru, pro přepis v reel.html).
Modely: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-cs_CZ-jirka-medium.tar.bz2
        https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2
usage: python3 make_voice.py <model TTS> [--asr <sherpa-onnx-whisper-turbo>] [--style whisper|hushed|voice] [--out <složka>]
Pozn.: VITS dává při každém běhu jiné varianty, zdrojem pravdy je uložený voice.wav.
"""
import argparse, json, os, re, subprocess, sys, tempfile
import numpy as np, soundfile as sf, pyworld as pw, librosa
from scipy.signal import butter, sosfilt, resample_poly, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
A = argparse.ArgumentParser()
A.add_argument('tts'); A.add_argument('--asr'); A.add_argument('--out', default=HERE)
A.add_argument('--style', default='whisper', choices=['whisper', 'hushed', 'voice']); A.add_argument('--seed', type=int, default=7)
ARGS = A.parse_args()
D = ARGS.tts.rstrip('/') + '/'; STYLE = ARGS.style
SR = 48000
#        text v přepisu            text pro TTS              rychlost  co následuje po větě (druh, délka v s)
SENT = [('Mami, to jsem já.',       'Mamí, to sem já.',       1.12,   ('pause', .16)),
        ('Měl jsem nehodu.',        'Měl sem nehodu.',        1.18,   ('shaky', .26)),
        ('Potřebuju hned peníze.',  'Potřebuju hned peníze.', 1.20,   ('sniff', .24)),
        ('Nemůžu volat.',           'Nemůžu volat.',          1.15,   None)]
# Pozn.: Piper vyslovuje „jsem“ s j („Měli jsem“, „to i sem“) a krátké „Mami“ zní jako „Máme“. Hovorové „sem“ a protažené
#       „Mamí“ (dítě volá mámu) znějí přirozeněji a přepisují se správně. V přepisu ve videu zůstává spisovný text.
N_CAND = 8                 # variant TTS na větu
F0_TARGET = 262.0          # Hz, medián výšky pro styl voice (kluci 8–11 let ~240–270 Hz)
FORMANT = 1.25             # posun formantů (dospělý muž -> dítě ~1,25–1,35; žena ~1,15)
RANGE = 1.30               # rozšíření melodie kolem trendu věty (voice)
FP = 5.0                   # WORLD frame period (ms)
rng = np.random.default_rng(ARGS.seed)

import sherpa_onnx
tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
    model=D + 'cs_CZ-jirka-medium.onnx', lexicon='', data_dir=D + 'espeak-ng-data', tokens=D + 'tokens.txt',
    noise_scale=.8, noise_scale_w=1.0), num_threads=2), max_num_sentences=1))
FS = 22050                 # nativní vzorkovací frekvence modelu
ASR = None
if ARGS.asr:
    W = ARGS.asr.rstrip('/') + '/'
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
    """Bez úletů výšky. Šepot: nejsvižnější varianta. Hlas: nejživější intonace (mírně preferuje svižnější)."""
    med = np.median([c['dur'] for c in cands])
    score = (lambda c: -c['dur']) if STYLE == 'whisper' else (lambda c: c['sd'] - 2.0 * (c['dur'] / med - 1))
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


def smooth(x, n): return np.convolve(x, np.ones(n) / n, 'same')


def convert(x, ratio, first_word_boost=0.0, fw_len=.36):
    """WORLD: dětské formanty + styl (šepot / dýchavý hlas / hlas) + chvění strachem. Délka a časování zůstávají."""
    f0, t = pw.harvest(x, FS, f0_floor=70, f0_ceil=420, frame_period=FP)
    sp = pw.cheaptrick(x, f0, t, FS); ap = pw.d4c(x, f0, t, FS)
    v = f0 > 0; n = len(t)
    freqs = np.arange(sp.shape[1]) * FS / ((sp.shape[1] - 1) * 2)
    sp2 = np.exp(warp(np.log(sp + 1e-12), FORMANT)); ap2 = warp(ap, FORMANT)
    vg = smooth(v.astype(float), 9)                                   # „znělost“ snímku, plynule
    if STYLE == 'whisper':
        f0n = np.zeros(n); ap2 = np.ones_like(ap2)
        tilt = np.interp(freqs, [0, 250, 500, 900, 1500, 3000, 5000, 7000, 11025], [-26, -22, -12, -4, 0, 2, 3, 1, -3])
        sp2 *= 10 ** (tilt / 10)                                       # šepot nemá basy hlasivek, víc vzduchu ve výškách
        sp2 *= 10 ** (-7 * vg / 10)[:, None]                           # samohlásky v šepotu slabší vůči sykavkám
    else:
        lf = np.log2(np.where(v, f0, 1.0))
        tv = t[v]; M = np.vstack([tv, np.ones_like(tv)]).T; coef = np.linalg.lstsq(M, lf[v], rcond=None)[0]
        trend = np.vstack([t, np.ones_like(t)]).T @ coef
        rg, r = (RANGE, ratio) if STYLE == 'voice' else (.85, ratio * .93)
        lf2 = trend + (lf - trend) * rg + np.log2(r)
        if first_word_boost:                                          # „Mami“ jako zavolání: o kousek výš
            on = t[v][0]; w = np.clip((t - on) / .06, 0, 1) * np.clip((on + fw_len - t) / .12, 0, 1)
            lf2 += first_word_boost / 12 * w
        trem = .0095 * np.sin(2 * np.pi * (5.8 + .4 * np.sin(2 * np.pi * .7 * t)) * t + rng.uniform(0, 6))
        jit = smooth(rng.standard_normal(n), 6) * .007
        f0n = np.where(v, 2 ** lf2 * (1 + trem + jit), 0.0)
        if STYLE == 'voice':
            b = .28 * np.clip((freqs - 1500) / 4500, 0, 1)
            ap2 = np.clip(1 - (1 - ap2) * (1 - b), 0, 1)
        else:                                                         # hushed: hodně vzduchu, hlasivky jen naznačené
            ap2 = np.maximum(ap2, np.interp(freqs, [0, 1000, 3000, 11025], [.55, .78, .93, .98]))
            sp2 *= 10 ** (np.interp(freqs, [0, 250, 500, 900, 1500, 3000, 5000, 11025], [-10, -8, -4, -1, 0, 1, 2, -2]) / 10)
            sp2 *= 10 ** (-3 * vg / 10)[:, None]
    y = pw.synthesize(f0n, sp2, ap2, FS, FP)[:len(x)]
    y = np.pad(y, (0, len(x) - len(y)))
    depth = .08 if STYLE != 'voice' else .05                           # chvění strachem (hlasitost)
    amp = 1 + depth * np.sin(2 * np.pi * 5.6 * np.arange(len(y)) / FS + rng.uniform(0, 6))
    return y * amp, sp2[v].mean(0)


# ---------- lidské a telefonní zvuky ----------
def shaped_noise(n, env_sp):
    H = np.sqrt(env_sp / env_sp.max()); h = np.fft.irfft(H); h = np.roll(h, len(h) // 2) * np.hanning(len(h))
    x = resample_poly(fftconvolve(rng.standard_normal(int(n * FS / SR) + 64), h, 'same'), 320, 147)[:n]
    return np.pad(x, (0, n - len(x)))


def breath(d, g, env_sp, shaky=False):
    """Nádech ústy: šum tvarovaný hlasovým traktem + vzduch ve výškách; roztřesený = trhaný."""
    n = int(d * SR); x = hp(shaped_noise(n, env_sp), 450); x = x + .35 * np.std(x) * bp(rng.standard_normal(n), 2500, 7000)
    tt = np.arange(n) / n; e = np.sin(np.pi * tt ** .7) ** 1.4
    if shaky: e *= .55 + .45 * np.abs(np.sin(np.pi * 3.5 * tt))
    s_ = x * e; return s_ / (np.abs(s_).max() + 1e-9) * g


def sniff(d, g):
    """Popotáhnutí nosem (pláč na krajíčku): dva krátké nosní nádechy."""
    n = int(d * SR); tt = np.arange(n) / n
    e = np.exp(-((tt - .3) / .09) ** 2) + .75 * np.exp(-((tt - .68) / .1) ** 2)
    x = bp(rng.standard_normal(n), 700, 4200) * e; return x / (np.abs(x).max() + 1e-9) * g


def exhale(d, g, env_sp):
    n = int(d * SR); tt = np.arange(n) / n
    x = lp(hp(shaped_noise(n, env_sp), 300), 2500) * (np.minimum(1, tt / .15) * (1 - tt) ** 1.5)
    return x / (np.abs(x).max() + 1e-9) * g


def rustle(d, g):
    """Šustnutí a ťuknutí prstem o telefon (začátek a konec nahrávání)."""
    n = int(d * SR); x = np.zeros(n)
    for _ in range(int(rng.integers(6, 12))):
        L = int(rng.integers(80, 700)); i = int(rng.integers(0, max(1, n - L)))
        x[i:i + L] += rng.standard_normal(L) * np.hanning(L) * rng.uniform(.25, 1)
    x = bp(x, 900, 6000) + .7 * lp(x, 220); return x / (np.abs(x).max() + 1e-9) * g


def opus(x):
    """Kodek hlasových zpráv: Opus 24 kb/s, 16 kHz (voip). Vrací signál zarovnaný na původní délku."""
    with tempfile.TemporaryDirectory() as d:
        a, b, c = (os.path.join(d, f) for f in ('in.wav', 'v.ogg', 'out.wav'))
        sf.write(a, (x / (np.abs(x).max() + 1e-9) * .9).astype(np.float32), SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-ar', '16000', '-c:a', 'libopus', '-b:a', '24k', '-application', 'voip', b], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', b, '-ar', str(SR), c], check=True)
        y, _ = sf.read(c)
    y = np.pad(y, (0, max(0, len(x) + 2000 - len(y))))
    ex = smooth(np.abs(x), 96); ey = smooth(np.abs(y[:len(x) + 2000]), 96)       # zarovnání obálek (pre-skip, filtry)
    lags = np.arange(-2000, 2001); m = len(x) - 4000
    k = int(lags[np.argmax([np.dot(ex[2000:2000 + m], ey[2000 + l:2000 + l + m]) for l in lags])])
    y = y[k:] if k >= 0 else np.concatenate([np.zeros(-k), y])
    y = y[:len(x)]; return np.pad(y, (0, len(x) - len(y)))


# --- 1) + 2) varianty, převod, kontrola srozumitelnosti, hranice slov ---
gen = [[candidate(say, speed) for _ in range(N_CAND)] for _, say, speed, _ in SENT]
ratio = F0_TARGET / np.median([c['f0med'] for cs in gen for c in cs])
chosen, segs, envs = [], [], []
for i, ((text, say, speed, _), cs) in enumerate(zip(SENT, gen)):
    first = None
    for k, c in enumerate(rank(cs)):
        y, env = convert(c['x'], ratio, first_word_boost=1.6 if i == 0 else 0.0)
        first = first or (c, y, env)
        h = heard(y, FS) if ASR else text
        if norm(h) == norm(text): break
        print(f'   varianta {k + 1} zamítnuta, Whisper slyší: „{h}“')
    else:
        c, y, env = first; print('   žádná varianta nebyla přepsána přesně, beru první v pořadí')
    c['bounds'] = word_bounds(c['x'], say, speed); chosen.append(c)
    segs.append(resample_poly(y, 320, 147)); envs.append(env)
    print(f'{text:26s} vybráno: {c["dur"]:.2f} s | slova:', ' '.join(f'{b:.2f}' for b in c['bounds']))
env_sp = np.mean(envs, 0)
pk = max(np.abs(x).max() for x in segs); segs = [x / pk * .8 for x in segs]   # řeč na společnou úroveň (špička 0,8)
LOUD = .6 if STYLE == 'voice' else 1.0                                # úroveň lidských zvuků vůči řeči (šepot: dech je slyšet víc)

# --- 3) skladba: šustnutí, nádech, věty s pauzami a zvuky, výdech, šustnutí ---
parts = [rustle(.12, .08 * LOUD), breath(.16, .13 * LOUD, env_sp)]
t = sum(len(p) for p in parts) / SR; LEAD = t; words = []
for (text, _, _, gap), x, c in zip(SENT, segs, chosen):
    b = c['bounds']; sc = (len(x) / SR) / b[-1]
    for j, w in enumerate(text.split()): words.append([w, round(t + b[j] * sc, 3), round(t + b[j + 1] * sc, 3)])
    parts.append(x); t += len(x) / SR
    if gap:
        kind, g = gap
        s_ = {'pause': lambda: np.zeros(int(g * SR)), 'shaky': lambda: breath(g, .11 * LOUD, env_sp, shaky=True),
              'sniff': lambda: sniff(g, .09 * LOUD), 'breath': lambda: breath(g, .10 * LOUD, env_sp)}[kind]()
        parts.append(s_); t += len(s_) / SR
parts += [exhale(.22, .07 * LOUD, env_sp), rustle(.10, .06 * LOUD), np.zeros(int(.06 * SR))]
v = np.concatenate(parts)
E = np.sqrt(np.convolve(v ** 2, np.ones(int(.015 * SR)) / int(.015 * SR), mode='same'))
on = np.where(E[int((LEAD - .04) * SR):] > .08 * E.max())[0]          # skutečný nástup prvního slova
if len(on): words[0][1] = round(LEAD - .04 + on[0] / SR, 3)

# --- 4) telefon: EQ mikrofonu, automatické zesílení, okolí, prostor, kodek ---
v = hp(v, 140 if STYLE == 'whisper' else 170); v = lp(v, 7600, o=4); v = v + .30 * bp(v, 1900, 4200)
env = np.sqrt(np.convolve(v ** 2, np.ones(int(.03 * SR)) / int(.03 * SR), mode='same')) + 1e-6
thr = .3 * env.max(); v = v * np.minimum(1, (thr / env) ** (.5 if STYLE != 'voice' else .4))
v = np.tanh(v / np.abs(v).max() * 1.1)
L = len(v); tt = np.arange(L) / SR
rumble = lp(np.cumsum(rng.standard_normal(L)) / 300, 120); rumble -= rumble.mean()
car = bp(rng.standard_normal(L), 300, 2500) * np.exp(-((tt - (L / SR) * .62) / .9) ** 2) * .5
wind = lp(rng.standard_normal(L), 300) * (.5 + .5 * np.sin(2 * np.pi * .7 * tt) ** 2)
agc = 1.6 if STYLE != 'voice' else 1.0                                 # tichá řeč -> telefon zesílí i okolí
amb = (rumble / (np.abs(rumble).max() + 1e-9) * .045 + car * .028 + wind * .03 + hp(rng.standard_normal(L), 3000) * .004) * agc
ir_n = int(.22 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / (.05 * SR)); ir = lp(ir, 5000)
ir[:int(.004 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
v = v + fftconvolve(v, ir)[:L] * .08 + amb
v = opus(v); v = v / np.abs(v).max() * .9
os.makedirs(ARGS.out, exist_ok=True)
sf.write(os.path.join(ARGS.out, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
json.dump({'style': STYLE, 'duration': round(L / SR, 3), 'firstWord': words[0][1], 'lastWordEnd': words[-1][2],
           'formant': FORMANT, 'words': words}, open(os.path.join(ARGS.out, 'words.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({'style': STYLE, 'duration': L / SR, 'speech': [words[0][1], words[-1][2]], 'words': words}, ensure_ascii=False))
if ASR: print('Whisper (celá hlasovka):', heard(v, SR))
