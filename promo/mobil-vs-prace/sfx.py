"""„Na mobilu strávíš víc času než v práci.“ – hudba a zvuky (22,5 s), časy podle reel.html.
Hook začíná vibrací telefonu, plnění mřížky má kaskády tiků (spánek nízko, práce středně, mobil vysoko),
u rodičů hudba spadne na klavír a „Zavolej jim.“ podbarví vyzváněcí tón (425 Hz).
usage: python3 sfx.py out.wav"""
import sys
import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt, lfilter

SR = 48000; DUR = 22.5; N = int(DUR * SR)
rng = np.random.default_rng(1122)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)

    def add(s, sig, at, g=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


D, Dw = Bus(), Bus()


def T(d): return np.arange(int(d * SR)) / SR
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))


def env(d, a, dec, rel=None):
    t = T(d); e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
    if rel: e *= np.clip((d - t) / rel, 0, 1)
    return e


def put(sig, at, g, pan=0.0, w=.3):
    D.add(sig, at, g, pan)
    if w: Dw.add(sig, at, g * w, pan)


def sweep_bp(x, f0, f1, q=1.0, blk=256):
    y = np.zeros_like(x); zi = np.zeros(2); n = len(x)
    for s in range(0, n, blk):
        u = min(1, (s + blk / 2) / n); f = f0 * (f1 / f0) ** u; w0 = 2 * np.pi * min(f, SR * .45) / SR; al = np.sin(w0) / (2 * q)
        b = np.array([al, 0, -al]) / (1 + al); a = np.array([1, -2 * np.cos(w0) / (1 + al), (1 - al) / (1 + al)])
        y[s:s + blk], zi = lfilter(b, a, x[s:s + blk], zi=zi)
    return y


# ---------------------------------------------------------------- instruments
def piano(at, n, g=1.0, d=3.5, pan=0.0, w=.8):
    """soft felt piano: slightly inharmonic partials, per-partial decay, hammer thump"""
    f = hz(n); t = T(d); s = np.zeros_like(t); B = .00035
    for k in range(1, 12):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 9000: break
        s += np.sin(2 * np.pi * fk * t + rng.random()) * (1 / k ** 1.25) * np.exp(-t * (.9 + .55 * k) * (1 + f / 900))
    s *= np.minimum(1, t / .004); s = lp(s, 3200)
    s += lp(noise(d), 900) * env(d, .001, .012) * .08
    put(s * np.clip((d - t) / .4, 0, 1), at, g, pan, w)


def chord(at, notes, g=1.0, d=3.5, spread=.012):
    for i, n in enumerate(notes): piano(at + i * spread, n, g * (1 - .06 * i), d, (i / max(1, len(notes) - 1) - .5) * .6)


def pad(at, notes, d, g=1.0, att=.6, rel=.8):
    for n in notes:
        t = T(d); f = hz(n)
        s = sum(np.sin(2 * np.pi * f * dt * t + rng.random() * 6) for dt in (1, 1.0035, .9965)) / 3 + .25 * np.sin(2 * np.pi * 2 * f * t)
        s *= np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1); p = rng.uniform(-.5, .5)
        D.add(s, at, g * .45, p); Dw.add(s, at, g * .8, -p)


def impact(at, g=1.0, crash=True, sub=36):
    d = 2.6; t = T(d); f = sub + 90 * np.exp(-t / .05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .7) + lp(noise(d), 2400) * env(d, .001, .07) * .75
    if crash: s += hp(noise(d), 4500) * env(d, .002, .9) * .18
    put(s, at, g, 0, .45)


def tick(at, f, g=1.0, dec=.05, pan=0.0):
    d = .2; t = T(d)
    s = np.sin(2 * np.pi * f * t) * env(d, .0006, dec) + np.sin(2 * np.pi * f * 3.9 * t) * env(d, .0004, dec * .2) * .3
    s += bp(noise(d), 2000, 9000) * env(d, .0002, .0012) * .35
    put(s, at, g, pan, .25)


def cascade(t0, t1, n, notes, g, dec):
    for i in range(n):
        at = t0 + (t1 - t0) * (i + rng.uniform(0, .6)) / n
        tick(at, hz(notes[rng.integers(len(notes))]), g * rng.uniform(.7, 1), dec, rng.uniform(-.6, .6))


def bell(at, f, g=1.0, d=2.0, pan=0.0):
    t = T(d); s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (1.1 / r ** .5)) for r, a in [(1, 1), (2.0, .45), (2.76, .2), (5.4, .08)])
    put(s * np.minimum(1, t / .003), at, g, pan, .8)


def whoosh(at, d=.4, g=1.0, f0=400, f1=6000, peak=.6):
    t = T(d); x = t / d; e = np.where(x < peak, (x / peak) ** 2, np.exp(-(x - peak) / (1 - peak) * 3))
    put(sweep_bp(noise(d), f0, f1, .9) * e, at - d * peak, g, 0, .4)


def buzz(at, d, g=1.0):
    """phone vibrating on a table"""
    t = T(d); f = 172 + 6 * np.sin(2 * np.pi * 7 * t)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 + np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * .3
    s = lp(s, 1600) * (.8 + .2 * np.sin(2 * np.pi * 31 * t)) + bp(noise(d), 1500, 5000) * .12 * (np.sin(2 * np.pi * 172 * t) > .6)
    s *= np.minimum(1, t / .01) * np.clip((d - t) / .02, 0, 1)
    put(s, at, g, .1, .1)


def clock(at, g=1.0, hi=True):
    d = .05; t = T(d); f = 2900 if hi else 2300
    s = bp(noise(d), f * .7, f * 1.4) * env(d, .0003, .004) + np.sin(2 * np.pi * f * .5 * t) * env(d, .0003, .008) * .4
    put(s, at, g, .2 if hi else -.2, .15)


# ================================================================ HOOK (0 – 2.35)
buzz(0.0, .32, .55); buzz(.46, .32, .5)
impact(.02, .75, crash=False, sub=34)
t = T(2.6); dr = (np.sin(2 * np.pi * hz(38) * t) + .5 * np.sin(2 * np.pi * hz(45) * t)) * np.minimum(1, t / .3) * np.clip((2.6 - t) / .5, 0, 1)
put(lp(dr, 400), 0, .22, 0, .2)
for k in range(1, 5): clock(k * .5, .18 + .04 * k, k % 2 == 0)
whoosh(2.3, .35, .18, 3000, 400)

# ================================================================ ONE WEEK → WHOLE LIFE (2.35 – 5.65)
piano(2.36, 69, .5, 3.2)                                   # one week
d = 1.6; t = T(d); x = t / d                                # pull back: swell
sw = sweep_bp(noise(d), 300, 7000, .7) * x ** 2.2 * .55 + lp(noise(d), 180) * x ** 2 * .6
put(sw * np.clip((d - t) / .01, 0, 1), 3.35, .45, 0, .6)
pad(3.4, [53, 60, 65, 69], 2.3, .1, 1.2, .5)
for i in range(26):                                         # cells multiplying: shimmer
    at = 3.5 + 1.45 * (i / 26) ** .8; bell(at, rng.uniform(1800, 5200), .025 + .02 * i / 26, .5, rng.uniform(-.8, .8))
impact(4.95, .55, crash=False, sub=40)
chord(4.95, [41, 53, 60, 65, 69, 72, 79], .34, 4.0)
pad(4.95, [41, 53, 60, 67, 72], 1.2, .1, .05, .6)
d = .7; s = hp(noise(d), 5000) * np.sin(np.pi * T(d) / d) ** 2; put(s, 4.98, .07, 0, .5)   # shimmer sweep

# ================================================================ FILLS
chord(5.7, [38, 50, 57, 62, 65], .22, 2.2); pad(5.7, [50, 57, 62, 65], 2.0, .07, .3, .5)          # Dm – spánek
cascade(5.7, 6.7, 60, [50, 53, 55, 57, 60], .22, .06)
chord(7.7, [34, 46, 53, 58, 62], .22, 2.2); pad(7.7, [46, 53, 58, 62], 2.0, .07, .3, .5)          # Bb – práce
cascade(7.7, 8.5, 46, [62, 65, 67, 69, 72], .2, .045)
chord(9.7, [36, 48, 55, 60, 67], .22, 2.0); pad(9.7, [48, 55, 60, 65, 67], 1.75, .08, .3, .2)     # C(sus) – mobil
cascade(9.7, 11.0, 96, [84, 86, 88, 91, 93, 96], .15, .03)
for i in range(6): tick(9.7 + i * .22, hz(96 + i), .12, .08)                                        # notification-like pings
d = 1.7; t = T(d); x = t / d
rs = sweep_bp(noise(d), 500, 9000, .8) * x ** 2.6 * .5 + np.sin(2 * np.pi * np.cumsum(220 * 8 ** (x ** 1.4)) / SR) * x ** 2 * .1
put(rs * np.clip((d - t) / .01, 0, 1), 11.4 - d, .5, 0, .5)
# SLAM – „Víc než v práci.“
impact(11.4, 1.1)
buzz(11.4, .25, .45)
for n in (38, 50, 57, 62, 65): piano(11.4, n, .32, 2.2)
d = 1.4; t = T(d); rum = lp(noise(d), 160) * env(d, .01, .5); put(rum, 11.4, .5, 0, .2)

# ================================================================ PARENTS (12.95 – 17.2)
piano(12.98, 69, .34, 3.5); piano(13.62, 65, .24, 3.0)
for j, n in enumerate([62, 65, 69, 72, 74, 77, 81]):     # the 7 weeks light up
    bell(14.2 + j * .09, hz(n + 12), .05, 1.6, -.5 + j / 6); piano(14.2 + j * .09, n, .12, 2.2)
chord(14.28, [38, 50, 57, 62], .2, 4.0)
pad(14.3, [50, 57, 62, 65], 2.9, .045, .8, .8)
for k, n in enumerate([69, 67, 65, 64]): piano(15.1 + k * .42, n, .2, 2.6)
chord(16.6, [34, 46, 53, 58, 62], .2, 3.0)

# ================================================================ ENDING (17.2 – 22.5)
chord(17.22, [34, 46, 53, 58, 62, 65], .26, 2.2)            # Bb
chord(17.85, [36, 48, 55, 60, 64, 67], .24, 1.6)            # C
impact(18.3, .45, crash=False, sub=40)                       # „Zavolej jim.“ – F
chord(18.3, [29, 41, 53, 57, 60, 65, 69, 72], .34, 4.5)
pad(18.3, [41, 53, 57, 60, 65, 72], 4.2, .1, .5, 1.4)
t = T(1.0); ring = (np.sin(2 * np.pi * 425 * t) + .15 * np.sin(2 * np.pi * 850 * t)) * np.minimum(1, t / .02) * np.clip((1.0 - t) / .03, 0, 1)
put(bp(ring, 300, 3400), 18.75, .06, 0, .3)                  # outgoing call (CZ ringback 425 Hz)
bell(20.5, hz(84), .09, 2.0); bell(20.55, hz(91), .05, 2.0)
for k, n in enumerate([77, 72, 69]): piano(20.6 + k * .3, n, .14, 1.9)

# ================================================================ MIX
def ir(seed, d=2.6, tau=.7):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 5500); x[:int(.015 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
L = D.L + fftconvolve(Dw.L, ir(1))[:N]; R = D.R + fftconvolve(Dw.R, ir(2))[:N]
tt = np.arange(N) / SR; fade = np.clip((DUR - tt) / .5, 0, 1) * np.clip(tt / .003, 0, 1); L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = np.tanh(L / pk * 2.2), np.tanh(R / pk * 2.2)
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * .93, R / pk * .93
out = sys.argv[1] if len(sys.argv) > 1 else 'mobil.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
m = (L + R) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(23)))
