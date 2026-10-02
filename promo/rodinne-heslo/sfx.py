"""„Tvoje máma nepozná tvůj hlas od AI.“ – zvuk (28,8 s), časy podle reel.html.
Hlasovka je mladý kluk z ElevenLabs (voice/voice.wav, viz voice/process_take.py), časy slov sedí na přepis v reel.html.
Všechno od 7,3 s se posouvá o SHIFT (2,8 s), než hlas doběhne – stejně jako v reel.html.
Pak glitch, napětí pod fakty, ticho, když „syn“ přestane psát, a rozřešení v dur.
usage: python3 sfx.py out.wav"""
import sys
import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt, lfilter

SR = 48000; SHIFT = 2.8; HOLD = 7.3; DUR = 26 + SHIFT; N = int(DUR * SR)   # events from 7.3 s on are delayed by SHIFT
rng = np.random.default_rng(909)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)

    def add(s, sig, at, g=1.0, pan=0.0, hold=False):          # hold=True: čas výstupu (uvnitř zastaveného obrazu), bez posunu
        i = int(round(at * SR))
        if at >= HOLD and not hold: i = int(round((at + SHIFT) * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


M, Mw, X, Xw, Vb = Bus(), Bus(), Bus(), Bus(), Bus()   # music, fx, voice


def T(d): return np.arange(int(d * SR)) / SR
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))


def env(d, a, dec, rel=None):
    t = T(d); e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
    if rel: e *= np.clip((d - t) / rel, 0, 1)
    return e


def put(bus, wet, sig, at, g, pan=0.0, w=.3, hold=False):
    bus.add(sig, at, g, pan, hold)
    if w: wet.add(sig, at, g * w, pan, hold)


def sweep_bp(x, f0, f1, q=1.0, blk=256):
    y = np.zeros_like(x); zi = np.zeros(2); n = len(x)
    for s in range(0, n, blk):
        u = min(1, (s + blk / 2) / n); f = f0 * (f1 / f0) ** u; w0 = 2 * np.pi * min(f, SR * .45) / SR; al = np.sin(w0) / (2 * q)
        b = np.array([al, 0, -al]) / (1 + al); a = np.array([1, -2 * np.cos(w0) / (1 + al), (1 - al) / (1 + al)])
        y[s:s + blk], zi = lfilter(b, a, x[s:s + blk], zi=zi)
    return y


# ================================================================ THE VOICE MESSAGE (real speech, neural TTS)
import os
HERE = os.path.dirname(os.path.abspath(__file__))
with wave.open(os.path.join(HERE, 'voice', 'voice.wav')) as w_:
    voice = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(float) / 32768
FILE0 = 2.66                                    # = VF v reel.html: hned po ťuknutí na Přehrát (2.62 s), první slovo ve 2.71 s
Vb.add(voice, FILE0, 1.2, 0)                    # hlas nad hudbou (ducking níž), viz kontrola odstupu v README

# ================================================================ instruments
def tick_ui(at, g=.3, f=2600):
    d = .03; t = T(d); s = bp(noise(d), 1800, 8000) * env(d, .0002, .002) + np.sin(2 * np.pi * f * t) * env(d, .0002, .004) * .3
    put(X, Xw, s, at, g, 0, .1)

def key(at, g=.25):
    d = .04; t = T(d); s = bp(noise(d), 1800, 6500) * env(d, .0003, .004) * .7 + np.sin(2 * np.pi * rng.uniform(170, 230) * t) * env(d, .001, .01) * .4
    put(X, Xw, s, at, g * rng.uniform(.7, 1), rng.uniform(-.2, .2), .05)

def pop(at, f=900, g=.25):
    d = .12; t = T(d); fr_ = f * (1 + .7 * np.exp(-t / .012)); s = np.sin(2 * np.pi * np.cumsum(fr_) / SR) * env(d, .001, .03)
    put(X, Xw, s, at, g, 0, .3)

def whoosh(at, d=.4, g=.3, f0_=400, f1_=6000, peak=.6, pan0=0, pan1=0):
    t = T(d); x = t / d; e = np.where(x < peak, (x / peak) ** 2, np.exp(-(x - peak) / (1 - peak) * 3))
    s = sweep_bp(noise(d), f0_, f1_, .9) * e
    X.add(s, at - d * peak, g, 0); Xw.add(s, at - d * peak, g * .4, 0)

def buzz(at, d, g=.5):
    t = T(d); f = 168 + 5 * np.sin(2 * np.pi * 7 * t)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 + np.sin(2 * np.pi * np.cumsum(2 * f) / SR) * .3
    s = lp(s, 1500) * (.8 + .2 * np.sin(2 * np.pi * 29 * t)); s *= np.minimum(1, t / .01) * np.clip((d - t) / .02, 0, 1)
    put(X, Xw, s, at, g, .1, .05)

def bell(at, f, g=1.0, d=1.6, pan=0.0, w=.6):
    t = T(d); s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (1.0 / r ** .5)) for r, a in [(1, 1), (2.0, .45), (2.76, .2), (5.4, .08)])
    put(X, Xw, s * np.minimum(1, t / .003), at, g, pan, w)

def impact(at, g=1.0, sub=36, crash=False):
    d = 2.6; t = T(d); f = sub + 90 * np.exp(-t / .05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .7) + lp(noise(d), 2400) * env(d, .001, .07) * .75
    if crash: s += hp(noise(d), 4500) * env(d, .002, .8) * .18
    put(X, Xw, s, at, g, 0, .45)

def pad(at, notes, d, g=1.0, att=.6, rel=.8, bus=M, wet=Mw):
    for n in notes:
        t = T(d); f = hz(n)
        s = sum(np.sin(2 * np.pi * f * dt * t + rng.random() * 6) for dt in (1, 1.0035, .9965)) / 3 + .25 * np.sin(2 * np.pi * 2 * f * t)
        s *= np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1); p = rng.uniform(-.5, .5)
        bus.add(s, at, g * .45, p); wet.add(s, at, g * .8, -p)

def piano(at, n, g=1.0, d=3.0, pan=0.0):
    f = hz(n); t = T(d); s = np.zeros_like(t)
    for k in range(1, 11):
        fk = k * f * np.sqrt(1 + .00035 * k * k)
        if fk > 8000: break
        s += np.sin(2 * np.pi * fk * t + rng.random()) / k ** 1.25 * np.exp(-t * (.9 + .55 * k) * (1 + f / 900))
    s = lp(s * np.minimum(1, t / .004), 3200) * np.clip((d - t) / .4, 0, 1)
    put(M, Mw, s, at, g, pan, .8)

def chord(at, notes, g=1.0, d=3.5):
    for i, n in enumerate(notes): piano(at + i * .012, n, g * (1 - .05 * i), d, (i / max(1, len(notes) - 1) - .5) * .6)

def pulse(at, g=1.0):
    d = .6; t = T(d); f = 46 + 50 * np.exp(-t / .04)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .18) + lp(noise(d), 1000) * env(d, .001, .01) * .4
    put(X, Xw, s, at, g, 0, .15)

def heartbeat(at, g=1.0, hold=False):
    for dt, gg, f00 in ((0, 1, 58), (.16, .7, 52)):
        d = .45; t = T(d); f = f00 + 28 * np.exp(-t / .03)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .003, .09); put(X, Xw, s, at + dt, g * gg, 0, .2, hold)

# ================================================================ TIMELINE
# lock screen: vibration + chime, quiet unease
buzz(0.0, .3, .5); buzz(.42, .3, .45)
bell(.02, hz(88), .07, 1.2, .2); bell(.12, hz(93), .05, 1.2, .2)
t = T(3.2); dr = (np.sin(2 * np.pi * hz(38) * t) + .4 * np.sin(2 * np.pi * hz(45) * t) + .25 * np.sin(2 * np.pi * hz(50) * t)) * np.minimum(1, t / .3) * np.clip((3.2 - t) / .6, 0, 1)
put(M, Mw, lp(dr, 500), 0, .14, 0, .2)
tick_ui(1.52, .35); whoosh(1.88, .35, .12, 3000, 500)
# chat: message bubble, tap on play, the voice
pop(2.42, 820, .22); tick_ui(2.62, .3); tick_ui(FILE0, .12, 3200)
pad(2.5, [50, 57, 62, 65], 5.6 + SHIFT, .04, 1.0, .8)              # D minor, low and soft under the voice
import json as _j
VEND_WORDS = FILE0 + _j.load(open(os.path.join(HERE, 'voice', 'words.json')))['lastWordEnd']
for k in range(12):                                                   # tlukot srdce pod celou hlasovkou (i v zastaveném obrazu)
    if 3.1 + k * .86 < VEND_WORDS: heartbeat(3.1 + k * .86, min(.38, .24 + .03 * k), hold=True)
pop(7.42, 760, .22); pop(7.72, 760, .2)
tt = 7.88
while tt < 8.13: key(tt, .22); tt += .035 * rng.uniform(.7, 1.3)
tick_ui(8.1, .3)
# GLITCH: crack, stutter of the voice, tape-stop, shock silence
d = .025; put(X, Xw, bp(noise(d), 800, 9000) * env(d, .0003, .01), 8.2, .7, 0, .1)
seg = voice[int(5.1 * SR):int(5.1 * SR) + int(.05 * SR)]            # a slice of „peníze“
for k in range(8):
    rate = 1 - .07 * k; s = np.interp(np.arange(0, len(seg) - 1, rate), np.arange(len(seg)), seg)
    s = np.round(s * 7) / 7; put(X, Xw, s * np.hanning(len(s)), 8.22 + k * .05, .55, (-1) ** k * .4, .1)
for k in range(10):
    d = rng.uniform(.012, .03); s = np.sign(np.sin(2 * np.pi * rng.uniform(300, 2400) * T(d))) * env(d, .0004, .02)
    put(X, Xw, s, 8.2 + rng.uniform(0, .4), .12, rng.uniform(-.8, .8), .05)
impact(8.62, 1.0, 34, crash=False)
t = T(1.6); ring = np.sin(2 * np.pi * 3900 * t) * np.exp(-t / .6) * np.minimum(1, t / .05); put(X, Xw, ring, 8.66, .02, 0, 0)  # tinnitus
# reveal hits
impact(8.68, .55, 40); pad(8.68, [38, 50, 53], 2.2, .07, .02, .6)
impact(9.5, .8, 36, crash=True)
for n in (50, 51, 57, 62, 63): piano(9.5, n, .22, 2.2)                # dissonant cluster
# facts: tense pulse (80 BPM) + whooshes and data ticks
B = .75
for k in range(int((17.7 - 10.25) / B)):
    at = 10.25 + k * B; pulse(at, .42 + .1 * (k % 2 == 0))
    d = .06; put(X, Xw, hp(noise(d), 7000) * env(d, .0005, .015), at + B / 2, .06, rng.uniform(-.3, .3), .1)
pad(10.25, [38, 45, 50, 53], 7.5, .06, 1.2, 1.0)
for at in (11.0, 13.3, 15.6): whoosh(at + .05, .4, .22, 500, 7000)
bell(11.5, hz(84), .07, 1.0); whoosh(12.15, .5, .12, 2000, 300)
for k in range(12): tick_ui(11.95 + abs(k - 6) * .022 + k * .004, .06, 2000 + 120 * k)
for i in range(7): pop(13.75 + i * .09, 600 * 2 ** (i / 12 * 2), .12)
for i in range(1, 19): tick_ui(15.75 + .9 * (i / 19) ** .7, .07, 1800 + 60 * i)
bell(16.65, hz(81), .08, 1.4)
# the fix: mom asks for the password, the "son" starts typing… and stops
whoosh(17.75, .45, .18, 5000, 500)
tt = 17.85
while tt < 18.12: key(tt, .2); tt += .028 * rng.uniform(.7, 1.3)
tick_ui(18.1, .3); whoosh(18.25, .3, .14, 900, 7000); pop(18.22, 980, .18)
pad(17.8, [50, 55, 57, 62], 2.7, .05, .6, .3)
for k in range(5): heartbeat(18.85 + k * .25, .25 + .06 * k)          # suspense speeds up
d = 1.2; t = T(d); rs = sweep_bp(noise(d), 400, 4000, 1.2) * (t / d) ** 2 * np.clip((d - t) / .01, 0, 1); put(X, Xw, rs, 18.85, .12, 0, .3)
# 20.05 – 20.45: silence. Then resolution in D major.
impact(20.5, .45, 42); chord(20.5, [38, 50, 57, 62, 66, 69], .3, 3.5)
pad(20.5, [50, 57, 62, 66], 5.2, .07, .4, 1.0)
bell(21.25, hz(86), .09, 1.6); bell(21.3, hz(93), .05, 1.6)
# end
chord(22.7, [43, 55, 59, 62, 67], .26, 3.0)                           # G (IV) → D
chord(24.0, [38, 50, 57, 62, 66], .22, 2.5)
bell(23.9, hz(81), .06, 1.8)

# ================================================================ MIX
def ir(seed, d=1.8, tau=.45):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 6000); x[:int(.012 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
IRL, IRR = ir(1), ir(2)
ML = M.L + fftconvolve(Mw.L, IRL)[:N]; MR = M.R + fftconvolve(Mw.R, IRR)[:N]
XL = X.L + fftconvolve(Xw.L, IRL)[:N]; XR = X.R + fftconvolve(Xw.R, IRR)[:N]
VL = Vb.L + fftconvolve(Vb.L, IRL)[:N] * .08; VR = Vb.R + fftconvolve(Vb.R, IRR)[:N] * .08
tt_ = np.arange(N) / SR
duck = 1 - .68 * np.clip((tt_ - 2.45) / .1, 0, 1) * np.clip((HOLD + SHIFT + .1 - tt_) / .1, 0, 1)   # music ducks under the voice
L_ = ML * duck + XL + VL; R_ = MR * duck + XR + VR
silence = 1 - np.clip((tt_ - 20.0 - SHIFT) / .05, 0, 1) * np.clip((20.45 + SHIFT - tt_) / .05, 0, 1) * .85  # the dramatic pause (20.0–20.45 in t)
L_ *= silence; R_ *= silence
fade = np.clip((DUR - tt_) / .45, 0, 1) * np.clip(tt_ / .003, 0, 1); L_ *= fade; R_ *= fade
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = np.tanh(L_ / pk * 2.5), np.tanh(R_ / pk * 2.5)
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = L_ / pk * .84, R_ / pk * .84   # ~-13.7 LUFS, true peak < -1 dBTP (rezerva pro AAC)
out = sys.argv[1] if len(sys.argv) > 1 else 'heslo.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L_, R_], 1) * 32767).astype(np.int16).tobytes())
m = (L_ + R_) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(int(DUR))))
