"""„ZASTAV VIDEO“ – hudba a zvuky (15 s, 112,5 BPM: šestnáctina = 4 snímky = jedna karta).
Tiky jsou přesně na změnách karet ze schedule.json (export z reel.html). Jackpot má vlastní „cink“,
aby se ho diváci naučili poznat a zkoušeli na něm zastavit. Konec plynule navazuje na začátek (smyčka).
usage: python3 sfx.py out.wav"""
import json, os, sys
import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt, lfilter

SR = 48000; FPS = 30; DUR = 15.0; N = int(DUR * SR)
rng = np.random.default_rng(930)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)
HERE = os.path.dirname(os.path.abspath(__file__))
SCHED = json.load(open(os.path.join(HERE, 'schedule.json')))
BEAT = 60 / 112.5; S16 = BEAT / 4; BAR = BEAT * 4
T_FAST, T_SLOW, T_JACK, T_CTA = 48 / FPS, 272 / FPS, 332 / FPS, 380 / FPS


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)

    def add(s, sig, at, g=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


M, Mw, X, Xw = Bus(), Bus(), Bus(), Bus()      # music (ducked by the kick) / drums + ticks + fx


def T(d): return np.arange(int(d * SR)) / SR
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))


def env(d, a, dec, rel=None):
    t = T(d); e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
    if rel: e *= np.clip((d - t) / rel, 0, 1)
    return e


def put(bus, wet, sig, at, g, pan=0.0, w=.3):
    bus.add(sig, at, g, pan)
    if w: wet.add(sig, at, g * w, pan)


def sweep_bp(x, f0, f1, q=1.0, blk=256):
    y = np.zeros_like(x); zi = np.zeros(2); n = len(x)
    for s in range(0, n, blk):
        u = min(1, (s + blk / 2) / n); f = f0 * (f1 / f0) ** u; w0 = 2 * np.pi * min(f, SR * .45) / SR; al = np.sin(w0) / (2 * q)
        b = np.array([al, 0, -al]) / (1 + al); a = np.array([1, -2 * np.cos(w0) / (1 + al), (1 - al) / (1 + al)])
        y[s:s + blk], zi = lfilter(b, a, x[s:s + blk], zi=zi)
    return y


def saw(f, d, bright=.3, fmax=6000):
    t = T(d); out = np.zeros_like(t); ph = 2 * np.pi * f * t + rng.random() * 6
    for k in range(1, int(fmax / f) + 1): out += np.sin(k * ph) / k * np.exp(-(k - 1) * (.5 - .45 * bright))
    return out


# ---------------------------------------------------------------- drums
kicks = []
def kick(at, g=1.0):
    d = .45; t = T(d); f = 46 + 110 * np.exp(-t / .035)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .16) + lp(noise(d), 3000) * env(d, .0005, .004) * .5
    put(X, Xw, np.tanh(s * 1.4), at, g, 0, .05); kicks.append(at)

def clap(at, g=1.0):
    d = .5; s = np.zeros(int(d * SR))
    for k, dt in enumerate((0, .011, .022)):
        i = int(dt * SR); seg = bp(noise(d - dt), 900, 6000) * env(d - dt, .0005, .012 if k < 2 else .09); s[i:] += seg[:len(s) - i]
    put(X, Xw, s, at, g, 0, .5)

def hat(at, g=1.0, open_=False):
    d = .3 if open_ else .06; s = hp(noise(d), 7500) * env(d, .0005, .09 if open_ else .014)
    put(X, Xw, s, at, g, rng.uniform(-.3, .3), .1)

def snare(at, g=1.0):
    d = .25; t = T(d); s = bp(noise(d), 800, 7000) * env(d, .0008, .05) + np.sin(2 * np.pi * 190 * t) * env(d, .001, .03) * .6
    put(X, Xw, s, at, g, rng.uniform(-.2, .2), .25)


# ---------------------------------------------------------------- tonal
def bass(at, n, d, g=1.0):
    s = lp(saw(hz(n), d, .25, 2500), 900) * env(d, .004, d * .9, .03) + np.sin(2 * np.pi * hz(n) * T(d)) * env(d, .004, d, .03) * .6
    M.add(np.tanh(s * 1.3), at, g)

def pad(at, notes, d, g=1.0, att=.25, rel=.4):
    for n in notes:
        t = T(d); f = hz(n)
        s = sum(np.sin(2 * np.pi * f * dt * t + rng.random() * 6) for dt in (1, 1.004, .996)) / 3 + .3 * np.sin(2 * np.pi * 2 * f * t)
        s *= np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1); p = rng.uniform(-.5, .5)
        M.add(s, at, g * .5, p); Mw.add(s, at, g * .7, -p)

def stab(at, notes, g=1.0, d=.9, bright=.8):
    for n in notes:
        s = saw(hz(n) * rng.uniform(.998, 1.002), d, bright, 7000); s = lp(s, 5500) * env(d, .003, .28, .1)
        p = rng.uniform(-.5, .5); X.add(s, at, g * .3, p); Xw.add(s, at, g * .4, -p)

def tick(at, n, g=1.0, pan=0.0):
    """marimba-like tick – one per card"""
    d = .22; t = T(d); f = hz(n)
    s = np.sin(2 * np.pi * f * t) * env(d, .0006, .07) + np.sin(2 * np.pi * f * 3.93 * t) * env(d, .0004, .012) * .35
    s += bp(noise(d), 2500, 9000) * env(d, .0002, .0015) * .5
    put(X, Xw, s, at, g, pan, .18)

def clack(at, n, g=1.0):
    """heavier wooden tick for the slowdown"""
    d = .35; t = T(d); f = hz(n)
    s = np.sin(2 * np.pi * f * t) * env(d, .0005, .1) + np.sin(2 * np.pi * f * 2.7 * t) * env(d, .0004, .03) * .4
    s += lp(noise(d), 3500) * env(d, .0003, .004) * .9
    put(X, Xw, s, at, g, 0, .3)

def bell(at, f, g=1.0, d=1.5, pan=0.0, w=.6):
    t = T(d); s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (1.0 / r ** .5)) for r, a in [(1, 1), (2.0, .5), (2.76, .25), (5.4, .1)])
    put(X, Xw, s * np.minimum(1, t / .003), at, g, pan, w)

def ding(at, g=1.0):
    """the jackpot cue"""
    bell(at, hz(100), g, 1.1, .2, .7); bell(at + .012, hz(107), g * .5, 1.0, -.2, .7)
    d = .5; s = hp(noise(d), 6000) * env(d, .002, .12); put(X, Xw, s, at, g * .25, 0, .6)


# ---------------------------------------------------------------- fx
def impact(at, g=1.0, crash=True):
    d = 2.2; t = T(d); f = 38 + 90 * np.exp(-t / .05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .6) + lp(noise(d), 2400) * env(d, .001, .07) * .8
    if crash: s += hp(noise(d), 4500) * env(d, .002, .8) * .22
    put(X, Xw, s, at, g, 0, .45)

def riser(a, b, g=1.0, f0=200, f1=2000):
    d = b - a; t = T(d); x = t / d
    s = sweep_bp(noise(d), 500, 9000, .8) * x ** 2.6 * .6 + np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (x ** 1.5)) / SR) * x ** 2.2 * .12
    s += lp(noise(d), 200) * x ** 2 * .5
    put(X, Xw, s * np.clip((d - t) / .01, 0, 1), a, g, 0, .5)

def whoosh(at, d=.35, g=1.0, f0=500, f1=6000, peak=.6):
    t = T(d); x = t / d; e = np.where(x < peak, (x / peak) ** 2, np.exp(-(x - peak) / (1 - peak) * 3))
    put(X, Xw, sweep_bp(noise(d), f0, f1, .9) * e, at - d * peak, g, 0, .4)

def uiclick(at, g=1.0):
    d = .03; t = T(d); s = bp(noise(d), 2000, 9000) * env(d, .0002, .0018) + np.sin(2 * np.pi * 2400 * t) * env(d, .0002, .003) * .4
    put(X, Xw, s, at, g, 0, .1)


# ================================================================ HOOK (0 – 1.6)
Am9 = [45, 52, 57, 60, 64, 71]
impact(0.0, .9); kick(0.0, 1.0); clap(0.0, .7); stab(0.0, Am9, .9, 1.1); uiclick(0.0, .8)
d = .9; t = T(d); sub = np.sin(2 * np.pi * np.cumsum(55 * .5 ** (t / .9)) / SR) * env(d, .004, .5); X.add(sub, 0.0, .5)
for k in range(1, 12):                                  # tension pulse (8ths), filter opening
    at = k * BEAT / 2
    if at >= T_FAST - .01: break
    dd = BEAT / 2; s = lp(saw(hz(33), dd, .2 + .06 * k, 2500), 250 + 220 * k) * env(dd, .004, .12)
    M.add(s, at, .22 + .03 * k)
for k in range(12):
    hat(k * S16, .05 + .06 * k / 11)
kick(BEAT, .65); kick(2 * BEAT, .75)
for i in range(10):                                     # snare roll into the drop
    at = 1.07 + i * (T_FAST - 1.07) / 10; snare(at, .12 + .35 * i / 9)
riser(.75, T_FAST, .55)
whoosh(T_FAST - .02, .3, .35, 400, 7000)                # card slides in

# ================================================================ SPIN (1.6 – 9.067)
PROG = [('Am', 45, [57, 60, 64]), ('F', 41, [57, 60, 65]), ('C', 48, [55, 60, 64]), ('G', 43, [55, 59, 62])]
ARP = {'Am': [69, 72, 76, 81, 84, 81, 76, 72], 'F': [69, 72, 77, 81, 84, 81, 77, 72],
       'C': [67, 72, 76, 79, 84, 79, 76, 72], 'G': [67, 71, 74, 79, 83, 79, 74, 71]}
def chord_at(t):
    k = int((t - T_FAST) // BAR) % 4
    return PROG[max(0, k)]
bt = T_FAST; bi = 0
while bt < T_SLOW - 1e-3:
    name, root, tri = chord_at(bt + 1e-3)
    kick(bt, .95)
    if bi % 2 == 1: clap(bt, .55)
    hat(bt + BEAT / 2, .12, open_=True)
    for q in (1, 3): hat(bt + q * S16, .06)
    for q in (0, 2):                                     # bass 8ths, octave pump
        bass(bt + q * S16, root - 12 + (12 if q == 2 else 0), S16 * 1.9, .34)
    if bi % 4 == 0: pad(bt, tri, BAR + .1, .085)
    bt += BEAT; bi += 1
# ticks: one per card, arpeggio of the current chord; jackpot gets its own ding
fast = [s for s in SCHED if s.get('fast')]
for i, s in enumerate(fast):
    at = s['f'] / FPS; name, _, _ = chord_at(at + 1e-3)
    if s['c'] == 'J': ding(at, .55); tick(at, ARP[name][i % 8], .3)
    else: tick(at, ARP[name][i % 8], .62 if i % 4 == 0 else .46, .25 * np.sin(i * 1.3))
for bar_at in (T_FAST + BAR - .05, T_FAST + 2 * BAR - .05, T_FAST + 3 * BAR - .05):   # bar turnarounds
    snare(bar_at - S16, .12); snare(bar_at, .16)

# ================================================================ SLOWDOWN (9.067 – 11.067)
slow = [s for s in SCHED if not s.get('fast') and not s.get('land')]
notes = [76, 74, 72, 71, 69, 68, 67, 64]
for i, s in enumerate(slow):
    clack(s['f'] / FPS, notes[i], .5 + .05 * i)
bass(T_SLOW, 40, T_JACK - T_SLOW, .4)                    # E pedal = tension
pad(T_SLOW, [56, 59, 64, 68], T_JACK - T_SLOW + .1, .09, .3, .1)
riser(T_SLOW + .1, T_JACK, .75, 150, 2400)
d = .9; t = T(d); rc = hp(noise(d), 4000) * (t / d) ** 4 * np.clip((d - t) / .006, 0, 1); put(X, Xw, rc, T_JACK - d, .45, 0, .4)
for k in range(4): kick(T_SLOW + k * BEAT, .32 - .05 * k)

# ================================================================ JACKPOT (11.067 – 12.667)
A = [45, 52, 57, 61, 64, 69]
impact(T_JACK, 1.0); kick(T_JACK, 1.0); clap(T_JACK, .6); stab(T_JACK, A, 1.0, 1.3, .95)
for i, n in enumerate([81, 85, 88, 93, 97, 100, 105]): bell(T_JACK + .02 + i * .045, hz(n), .16, 1.4, rng.uniform(-.5, .5))
for i in range(34):                                       # coin shower
    at = T_JACK + .05 + 1.3 * (i / 34) ** 1.4 + rng.uniform(0, .02)
    bell(at, rng.uniform(2400, 5200), .07 * (1 - .6 * i / 34), .35, rng.uniform(-.8, .8), .5)
pad(T_JACK, [57, 61, 64, 69], T_CTA - T_JACK + .3, .12, .02, .4)
bass(T_JACK, 33, BEAT * 1.9, .45)
for k in range(1, 3): kick(T_JACK + k * BEAT, .8); hat(T_JACK + k * BEAT + BEAT / 2, .12, open_=True)
bass(T_JACK + 2 * BEAT, 40, BEAT * .9, .4)

# ================================================================ CTA (12.667 – 15.0) → loops into the hook
whoosh(T_CTA + .1, .35, .35, 6000, 500)
tt = T_CTA; bi = 0
while tt < DUR - 1e-3:
    kick(tt, .8 if bi % 2 == 0 else .6)
    if bi % 2 == 1: clap(tt, .45)
    hat(tt + BEAT / 2, .1, open_=True)
    bass(tt, 33 if tt < T_CTA + 2 * BEAT else 29, BEAT * .9, .34)
    tt += BEAT; bi += 1
pad(T_CTA, [57, 60, 64], 2 * BEAT + .1, .09); pad(T_CTA + 2 * BEAT, [57, 60, 65], DUR - T_CTA - 2 * BEAT, .09, .1, .05)
bell(T_CTA + .2, hz(88), .1, 1.2); bell(T_CTA + .25, hz(93), .07, 1.2)
for i in range(12):                                        # roll back into the start (loop)
    at = DUR - .55 + i * .55 / 12; snare(at, .1 + .35 * i / 11)
riser(DUR - 1.0, DUR, .45)

# ================================================================ MIX
def ir(seed, d=1.8, tau=.45):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 6000); x[:int(.012 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
IRL, IRR = ir(1), ir(2)
ML = M.L + fftconvolve(Mw.L, IRL)[:N]; MR = M.R + fftconvolve(Mw.R, IRR)[:N]
XL = X.L + fftconvolve(Xw.L, IRL)[:N]; XR = X.R + fftconvolve(Xw.R, IRR)[:N]
tt = np.arange(N) / SR; duck = np.ones(N)
for k in kicks:
    i = int(k * SR); j = min(N, i + int(.3 * SR)); duck[i:j] = np.minimum(duck[i:j], 1 - .4 * np.exp(-(tt[i:j] - k) / .09))
L = ML * duck + XL; R = MR * duck + XR
L *= np.clip(tt / .004, 0, 1); R *= np.clip(tt / .004, 0, 1)
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = np.tanh(L / pk * 2.3), np.tanh(R / pk * 2.3)
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * .93, R / pk * .93
out = sys.argv[1] if len(sys.argv) > 1 else 'zastav.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
m = (L + R) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(15)))
