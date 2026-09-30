"""Better Digital – cinematic intro v2 (45 s). Score + sound design synced to intro2.html.
usage: python3 intro2_sfx.py out.wav"""
import numpy as np, wave, sys
from scipy.signal import fftconvolve, butter, sosfilt, lfilter

SR = 48000; DUR = 45.0; N = int(DUR * SR)
rng = np.random.default_rng(2026)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)

    def add(s, sig, at, g=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        if np.ndim(pan):  # pan curve
            p = np.asarray(pan)[:j - i]
            s.L[i:j] += seg * np.sqrt(.5 * (1 - p)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + p)) * 1.414
        else:
            s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


# A = chaos (hard cut at 5.4) · M = music (sidechained) · X = hits/drums/SFX
A, Aw, M, Mw, X, Xw = Bus(), Bus(), Bus(), Bus(), Bus(), Bus()


def T(d): return np.arange(int(d * SR)) / SR
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def noise(d): return rng.standard_normal(int(d * SR))


def env(d, a, dec, rel=None):
    t = T(d); e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
    if rel: e *= np.clip((d - t) / rel, 0, 1)
    return e


def put(bus, wet, sig, at, g, pan=0.0, w=0.3):
    bus.add(sig, at, g, pan)
    if w: wet.add(sig, at, g * w, pan)


def sweep_bp(x, f0, f1, q=1.2, curve=1.0, blk=256):
    """band-pass with a moving centre frequency (log sweep f0 -> f1)"""
    y = np.zeros_like(x); zi = np.zeros(2); n = len(x)
    for s in range(0, n, blk):
        u = min(1, (s + blk / 2) / n) ** curve
        f = f0 * (f1 / f0) ** u; w0 = 2 * np.pi * min(f, SR * .45) / SR; al = np.sin(w0) / (2 * q)
        b = np.array([al, 0, -al]) / (1 + al); a = np.array([1, -2 * np.cos(w0) / (1 + al), (1 - al) / (1 + al)])
        y[s:s + blk], zi = lfilter(b, a, x[s:s + blk], zi=zi)
    return y


def saw(f, d, c0=.05, c1=.4, tau=.8, fmax=7000):
    t = T(d); c = c1 + (c0 - c1) * np.exp(-t / tau); out = np.zeros_like(t)
    ph = 2 * np.pi * f * t + rng.random() * 6
    for k in range(1, int(fmax / f) + 1):
        out += np.sin(k * ph) / k * np.exp(-(k - 1) * c)
    return out


# ------------------------------------------------------------------ instruments
def whoosh(bus, wet, at, d=.45, g=.3, f0=400, f1=5000, pan0=0.0, pan1=0.0, peak=.55, q=.9, w=.4):
    """at = moment of the peak"""
    t = T(d); x = t / d
    e = np.where(x < peak, (x / peak) ** 2.2, np.exp(-(x - peak) / (1 - peak) * 3.2))
    s = sweep_bp(noise(d), f0, f1, q) * e + lp(noise(d), 300) * e * .25
    pan = np.clip(pan0 + (pan1 - pan0) * x, -1, 1)
    bus.add(s, at - d * peak, g, pan); wet.add(s, at - d * peak, g * w, pan)


def impact(bus, wet, at, g=1.0, crash=True, sub=38, w=.5):
    d = 2.8; t = T(d)
    f = sub + 95 * np.exp(-t / .055)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .75)
    s += lp(noise(d), 2400) * env(d, .001, .08) * .85
    s += bp(noise(d), 100, 900) * env(d, .001, .25) * .35
    if crash: s += hp(noise(d), 4200) * env(d, .002, .9) * .2
    put(bus, wet, s, at, g, 0, w)


def braam(bus, wet, at, f0, d=4.0, g=1.0, fifth=True, bright=.03, w=.55):
    parts = [(f0, 1), (f0 * 1.006, .8), (f0 * .994, .8), (f0 * 2, .55), (f0 * 2 * 1.004, .4)]
    if fifth: parts += [(f0 * 3, .3), (f0 * 3 * .997, .2)]
    s = sum(saw(f, d, bright, .6, .45) * a for f, a in parts) * env(d, .03, 1.5, .6)
    t = T(d); sb = np.sin(2 * np.pi * np.cumsum(f0 * (1 + .7 * np.exp(-t / .07))) / SR) * env(d, .004, 1.3, .5)
    s = s * .17 + sb * .85 + lp(noise(d), 1800) * env(d, .002, .06) * .5
    put(bus, wet, s, at, g, 0, w)


def pulse(bus, wet, at, g=1.0, f0=44, w=.2):
    d = .7; t = T(d); f = f0 + 48 * np.exp(-t / .045)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .2) + lp(noise(d), 1100) * env(d, .001, .012) * .45
    put(bus, wet, s, at, g, 0, w)


def snare(bus, wet, at, g=1.0, w=.7):
    d = .9; t = T(d)
    s = bp(noise(d), 700, 7500) * env(d, .001, .09) * .9 + np.sin(2 * np.pi * 185 * t) * env(d, .001, .05) * .6
    s += bp(noise(d), 1500, 4000) * env(d, .001, .018) * .8
    put(bus, wet, s, at, g, 0, w)


def tom(bus, wet, at, g=1.0, f0=100, w=.45):
    d = .6; t = T(d); f = f0 * .65 + f0 * .6 * np.exp(-t / .04)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .18) + bp(noise(d), 150, 2500) * env(d, .001, .03) * .5
    put(bus, wet, s, at, g, rng.uniform(-.35, .35), w)


def hat(bus, wet, at, g=1.0, dec=.018, w=.12):
    d = .09; s = hp(noise(d), 7000) * env(d, .0005, dec)
    put(bus, wet, s, at, g, rng.uniform(-.35, .35), w)


def riser(bus, wet, a, b, g=1.0, f0=180, f1=1500, w=.6):
    d = b - a; t = T(d); x = t / d
    nz = sweep_bp(noise(d), 600, 9000, .7, 1.5) * x ** 3
    f = f0 * (f1 / f0) ** (x ** 1.6)
    tone = sum(np.sin(2 * np.pi * np.cumsum(f * m) / SR) * wt for m, wt in [(1, 1), (1.5, .5), (2, .35)]) * x ** 2.5
    rum = lp(noise(d), 200) * x ** 2 * 1.4
    s = (nz * .55 + tone * .11 + rum * .55) * np.clip((d - t) / .012, 0, 1)
    put(bus, wet, s, a, g, 0, w)


def revcym(bus, wet, end, d=1.2, g=.5, w=.5):
    t = T(d); x = t / d
    s = hp(noise(d), 3500) * x ** 3.5 + bp(noise(d), 800, 3000) * x ** 5 * .5
    s *= np.clip((d - t) / .008, 0, 1)
    put(bus, wet, s, end - d, g, 0, w)


def bell(bus, wet, at, f, g=1.0, d=3.0, pan=0.0, w=.8):
    t = T(d); s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (1.2 / r ** .5)) for r, a in [(1, 1), (2.0, .5), (2.76, .25), (5.4, .12)])
    s *= np.minimum(1, t / .004); put(bus, wet, s, at, g, pan, w)


def pad(bus, wet, at, notes, d, g=1.0, att=.9, rel=1.1, w=.9):
    for n in notes:
        f = hz(n); t = T(d)
        s = sum(np.sin(2 * np.pi * f * dt * t + rng.random() * 6) for dt in (1, 1.004, .996)) / 3
        s += .35 * np.sin(2 * np.pi * 2 * f * t) + .12 * np.sin(2 * np.pi * 3 * f * t)
        s *= np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
        p = rng.uniform(-.55, .55); bus.add(s, at, g * .55, p); wet.add(s, at, g * w, -p)


def strings(bus, wet, at, notes, d, g=1.0, att=.5, rel=.9, bright=.35, w=.8):
    """warm saw ensemble (low-passed), for the finale"""
    for n in notes:
        f = hz(n); s = sum(saw(f * dt, d, .5 - bright, .5 - bright, 1, 4000) for dt in (1, 1.005, .995)) / 3
        s = lp(s, 2600 + 2500 * bright)
        t = T(d); s *= np.minimum(1, t / att) * np.clip((d - t) / rel, 0, 1)
        p = rng.uniform(-.6, .6); bus.add(s, at, g * .5, p); wet.add(s, at, g * w, -p)


def pluck(bus, wet, at, f, g=1.0, w=.6):
    d = .8; t = T(d); s = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.5 * np.exp(-t * (4 + k * 1.6)) for k in range(1, 7))
    s *= np.minimum(1, t / .003); p = rng.uniform(-.45, .45); bus.add(s, at, g, p); wet.add(s, at, g * w, -p)


def ostinato(bus, wet, at, f, g=1.0, bright=.5, w=.1):
    d = .3; s = saw(f, d, .6 - .5 * bright, .7 - .5 * bright, 1.0, 3200) * env(d, .008, .22, .05)
    put(bus, wet, s, at, g, 0, w)


def sub(bus, at, f, d, g=1.0):
    t = T(d); s = np.tanh(1.6 * np.sin(2 * np.pi * f * t)) * np.minimum(1, t / .05) * np.clip((d - t) / .15, 0, 1)
    bus.add(s, at, g)


def blip(bus, wet, at, f, g=1.0, d=.12, pan=None, w=.35):
    t = T(d); s = (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t)) * env(d, .002, .035)
    put(bus, wet, s, at, g, rng.uniform(-.25, .25) if pan is None else pan, w)


def key(bus, wet, at, g=.5):
    d = .04; t = T(d)
    s = bp(noise(d), 1800, 6500) * env(d, .0003, .004) * .7 + np.sin(2 * np.pi * rng.uniform(170, 230) * t) * env(d, .001, .01) * .4
    put(bus, wet, s, at, g * rng.uniform(.7, 1), rng.uniform(-.2, .2), .08)


def typing(a, b, rate=20, g=.3):
    t = a
    while t < b: key(X, Xw, t, g); t += 1 / rate * rng.uniform(.65, 1.35)


def mclick(at, g=.55):  # mouse click: press + release
    for k, dt in enumerate((0, .07)):
        d = .025; t = T(d); s = bp(noise(d), 2000, 9000) * env(d, .0002, .0017) + np.sin(2 * np.pi * 2600 * t) * env(d, .0002, .002) * .3
        put(X, Xw, s, at + dt, g * (1 if k == 0 else .55), 0, .1)


def press(at, g=.4):  # soft UI button press
    d = .08; t = T(d); s = lp(noise(d), 3000) * env(d, .0005, .006) + np.sin(2 * np.pi * 320 * t) * env(d, .001, .02) * .6
    put(X, Xw, s, at, g, 0, .15)


def pop(at, f, g=.3):  # bubbly pop for UI elements appearing
    d = .12; t = T(d); fr = f * (1 + .6 * np.exp(-t / .015))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(d, .001, .03)
    put(X, Xw, s, at, g, rng.uniform(-.3, .3), .35)


def sparkle(at, n=10, span=.35, g=.05):
    for i in range(n):
        bell(X, Xw, at + span * (i / n) ** 1.3 + rng.uniform(0, .02), rng.uniform(2600, 6200), g * (1 - .6 * i / n), .6, rng.uniform(-.7, .7), .9)


def shing(at, g=.18):  # metallic accent for word-mark slams
    d = 1.2; s = sum(bp(noise(d), f * .97, f * 1.03) * a for f, a in [(5200, 1), (7400, .7), (9800, .5)]) * env(d, .001, .28)
    put(X, Xw, s, at, g, 0, .8)


def heartbeat(at, g=1.0):
    for dt, gg, f0 in ((0, 1, 58), (.17, .7, 52)):
        d = .5; t = T(d); f = f0 + 30 * np.exp(-t / .03)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .003, .09) + lp(noise(d), 400) * env(d, .002, .02) * .3
        put(X, Xw, s, at + dt, g * gg, 0, .35)


def ping(at, kind, g=.2):
    """notification sounds for the chaos cards"""
    b = (A, Aw)
    if kind == 'mail': bell(*b, at, 1318.5, g, .8, -.4); bell(*b, at + .07, 1760, g * .7, .8, -.4)
    elif kind == 'alert':
        for i, f in enumerate((1760, 1318.5, 1760)): blip(*b, at + i * .06, f, g * 1.3, .07, .45)
    elif kind == 'chat':
        d = .12; t = T(d); s = np.sin(2 * np.pi * np.cumsum(500 + 900 * (t / d) ** .6) / SR) * env(d, .004, .05); put(*b, s, at, g * 1.6, -.2, .3)
    elif kind == 'error':
        d = .18; t = T(d); s = np.sign(np.sin(2 * np.pi * 330 * t)) * env(d, .002, .06); put(*b, lp(s, 2500), at, g * .9, .3, .3)
    elif kind == 'phone':
        for i in range(6): blip(*b, at + i * .045, 1400 if i % 2 else 1800, g * 1.1, .05, .2)
    elif kind == 'cal': bell(*b, at, 1046.5, g, .9, .45); bell(*b, at + .1, 1318.5, g * .8, .9, .45)
    elif kind == 'box': bell(*b, at, 1568, g, .8, -.3)


def tick(at, hi, g=.12):
    d = .03; t = T(d); f = 3200 if hi else 2500
    s = bp(noise(d), f * .7, f * 1.4) * env(d, .0003, .003) + np.sin(2 * np.pi * f * .6 * t) * env(d, .0003, .006) * .5
    put(A, Aw, s, at, g, .15 if hi else -.15, .15)


# ================================================================== ACT 1 · CHAOS (0 – 5.4)
t = T(5.6); x = t / 5.4
dr = (saw(55, 5.6, .9, .9, 1, 1400) + saw(58.27, 5.6, .9, .9, 1, 1400) * .7) * .25 + np.sin(2 * np.pi * 27.5 * t) * .5
dr = lp(dr, 300) + hp(lp(dr, 1800), 300) * x ** 2
dr *= np.clip(t / .15, 0, 1) * (.45 + .55 * x ** 1.5)
put(A, Aw, dr, 0, .3, 0, .25)
tt = T(3.2); hi = sum(np.sin(2 * np.pi * f * tt + rng.random() * 6) for f in (hz(81), hz(82), hz(88), hz(89))) / 4
hi *= (1 + .5 * np.sin(2 * np.pi * 11 * tt)) * np.clip(tt / 3.0, 0, 1) ** 2
put(A, Aw, hi, 2.2, .06, 0, .6)
# opening: a soft swell so the first frame isn't dead
whoosh(A, Aw, .25, .5, .12, 200, 1500)
# clock: 8ths, then 16ths when time starts racing
k = 0; tc = .35
while tc < 5.4:
    tick(tc, k % 2 == 0, .1 + .12 * tc / 5.4); k += 1; tc += .25 if tc < 2.6 else .125
# card slams on the beat
BEATS = [.6, 1.1, 1.6, 2.1, 2.6, 3.1, 3.6, 4.1]
KIND = ['mail', 'alert', 'chat', 'error', 'phone', 'cal', 'box', 'mail']
for i, b in enumerate(BEATS):
    whoosh(A, Aw, b + .03, .28, .16, 700, 4500, .8 if i % 2 == 0 else -.8, 0, .7)
    pulse(A, Aw, b, .55 + .35 * i / 7)
    d = .1; tt = T(d); thud = lp(noise(d), 900) * env(d, .001, .015); put(A, Aw, thud, b + .04, .35, 0, .2)
    ping(b + .05, KIND[i], .17 + .05 * i / 7)
pulse(A, Aw, 4.6, .9)
# text slams (off-beat)
for i, at in enumerate([1.35, 2.35, 3.35, 4.3]):
    big = i == 3
    braam(A, Aw, at, 55 if i < 3 else 51.9, 1.3 if not big else 1.6, .45 + .12 * i, fifth=False)
    impact(A, Aw, at, .5 + .12 * i, crash=big)
    d = .2; c = hp(noise(d), 2500) * env(d, .0005, .025); put(A, Aw, c, at, .5, 0, .5)
# glitch before the cut
for kk in range(14):
    at = 4.85 + kk * .039 + rng.uniform(0, .01); d = rng.uniform(.018, .035); tt = T(d)
    if kk % 3 == 0: s = np.sign(np.sin(2 * np.pi * rng.uniform(200, 1800) * tt))
    else: s = bp(noise(d), 1000, 9000)
    s = np.round(s * 6) / 6 * env(d, .0005, .02); put(A, Aw, s, at, .22, rng.uniform(-.8, .8), .1)
tt = T(.55); wh = np.sin(2 * np.pi * np.cumsum(900 * 3 ** (tt / .55)) / SR) * (1 + np.sign(np.sin(2 * np.pi * 24 * tt))) * .5 * (tt / .55) ** 1.5
put(A, Aw, wh, 4.85, .08, 0, .3)
riser(A, Aw, 4.5, 5.4, .45, 200, 2200)

# ================================================================== ACT 2 · SILENCE → LOGO
heartbeat(5.85, .95); bell(X, Xw, 5.87, hz(93), .045, 3.5, 0, 1)
heartbeat(6.45, 1.15)
riser(X, Xw, 6.2, 7.35, .8, 120, 1600)
revcym(X, Xw, 7.35, 1.3, .45)
whoosh(X, Xw, 7.0, .6, .12, 2000, 9000, -.3, .3, .8, 2.5, .6)      # ring draws
whoosh(X, Xw, 7.3, .28, .12, 900, 7000, -.5, .5, .85)             # line
# THE REVEAL
impact(X, Xw, 7.35, 1.35)
braam(X, Xw, 7.35, 55, 5.5, 1.15)
d = 2.4; s = hp(noise(d), 1500) * env(d, .01, .45); put(X, Xw, s, 7.35, .3, 0, .5)
tt = T(1.8); sd = np.sin(2 * np.pi * np.cumsum(60 * .5 ** (tt / 1.2)) / SR) * env(1.8, .005, .7); put(X, Xw, sd, 7.35, .7, 0, 0)
for k, n in enumerate([81, 88, 93, 100]): bell(X, Xw, 7.38 + k * .07, hz(n), .045, 3, rng.uniform(-.5, .5))
shing(7.42, .16)
pad(M, Mw, 7.35, [45, 52, 57, 60, 64], 2.6, .1, .4)
whoosh(X, Xw, 9.2, .5, .32, 250, 7000, 0, 0, .8)                  # zoom through the dot
for at in (8.9, 9.0, 9.08): whoosh(X, Xw, at + .1, .3, .08, 1500, 9000, -.8, .8, .5)

# ================================================================== MUSIC BED (120 BPM from 7.35)
BEAT = .5; BAR = 2.0
Am = (45, [57, 60, 64, 69]); F = (41, [57, 60, 65, 69]); C = (48, [55, 60, 64, 67]); G = (43, [55, 59, 62, 67])
CH = [(9.35, Am), (11.35, F), (13.35, C), (15.35, G), (17.35, Am), (19.35, F), (21.35, C), (23.35, G),
      (25.35, Am), (27.35, F), (29.35, C), (30.35, G)]
END_BED = 31.3
for i, (st, (bs, notes)) in enumerate(CH):
    en = CH[i + 1][0] if i + 1 < len(CH) else END_BED
    lvl = clampv = min(1, (st - 9.35) / 20)
    pad(M, Mw, st, notes, en - st + .9, .11 + .06 * lvl, .5 if st > 9.4 else 1.0, .8)
    sub(M, st, hz(bs - 12), en - st, .14 + .06 * lvl)
    # ostinato 8ths on the root
    tt = st
    while tt < en - 1e-3:
        beat = int(round((tt - 7.35) / .25)) % 4
        ostinato(M, Mw, tt, hz(bs), (.07 + .07 * lvl) * (1.25 if beat == 0 else 1), .3 + .5 * lvl)
        ostinato(M, Mw, tt, hz(bs - 12), (.055 + .06 * lvl), .2 + .4 * lvl)
        tt += .25
    # arp 16ths from the services scene on
    if st >= 11.35:
        arp = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[3] + 12, notes[2] + 12, notes[1] + 12]
        step = .25 if st < 17.3 else .125
        tt = st; k = 0
        while tt < en - 1e-3:
            if not (16.9 < tt < 17.3):
                pluck(M, Mw, tt, hz(arp[k % 6]), (.05 + .045 * lvl) * (1.3 if k % 4 == 0 else 1))
            k += 1; tt += step
# ostinato into the logo (soft)
tt = 7.85
while tt < 9.35 - 1e-3:
    ostinato(M, Mw, tt, hz(45), .035 + .03 * (tt - 7.85) / 1.5, .3); tt += .25
# drums
kick_times = []
tt = 9.35
while tt < 31.3 - 1e-3:
    bi = int(round((tt - 7.35) / BEAT))
    if tt < 17.3:
        if bi % 2 == 0: pulse(X, Xw, tt, .52 + .1 * (tt - 9.35) / 8); kick_times.append(tt)
        if tt >= 12.2: hat(X, Xw, tt + .25, .065)
    else:
        pulse(X, Xw, tt, .6 + .12 * min(1, (tt - 17.35) / 12)); kick_times.append(tt)
        if bi % 2 == 1 and tt >= 19.3: snare(X, Xw, tt, .27 + .08 * min(1, (tt - 19.35) / 10))
        for q in (.125, .25, .375): hat(X, Xw, tt + q, .05 if q != .25 else .08)
    tt += BEAT
for k in range(8): tom(X, Xw, 29.35 + 1.5 + k * .0625 * 2, .18 + .3 * k / 7, 105)   # fill into recap

# ================================================================== UI SOUND DESIGN (demo)
# 3 · Co kdyby stačilo / to říct?
whoosh(X, Xw, 9.35, .45, .16, 6000, 400, 0, 0, .3)
typing(9.3, 10.0, 22, .28)
whoosh(X, Xw, 10.35, .3, .15, 600, 6000, 0, 0, .9)
impact(X, Xw, 10.35, .55, crash=False); braam(X, Xw, 10.35, 55, 1.8, .35, bright=.1)
for k, n in enumerate([88, 93, 100]): bell(X, Xw, 10.38 + k * .05, hz(n), .04, 2.2, rng.uniform(-.4, .4))
whoosh(X, Xw, 12.22, .4, .3, 300, 6000, .8, -.8, .6)               # whip out / in
for at in (12.1, 12.15): whoosh(X, Xw, at + .2, .3, .06, 2000, 9000, -.9, .9)
# 4 · služby
for k, at in enumerate([12.6, 12.85, 13.1]): pop(at + .05, [880, 1046.5, 1318.5][k], .16)
for k, at in enumerate([13.35, 13.85, 14.35]):
    press(at, .3); bell(X, Xw, at, hz([76, 79, 84][k]), .06, 1.4, .2)
whoosh(X, Xw, 15.28, .4, .3, 300, 8000, 0, 0, .85)                  # zoom through
# 5 · prompt + CLICK
whoosh(X, Xw, 15.45, .4, .08, 3000, 400, 0, 0, .35)
typing(15.7, 16.95, 23, .3)
blip(X, Xw, 16.97, 1568, .07, .14, 0)
d = .38; s = bp(noise(d), 1500, 5000) * np.sin(np.pi * T(d) / d) ** 2; put(X, Xw, s, 16.95, .025, np.linspace(.6, .2, len(s)), .1)
mclick(17.35, .6)
whoosh(X, Xw, 17.48, .35, .2, 800, 9000, 0, 0, .35)
sparkle(17.37, 12, .4, .045)
impact(X, Xw, 17.35, .38, crash=True)
whoosh(X, Xw, 17.62, .35, .12, 700, 7000, 0, 0, .5)                 # text flies up
whoosh(X, Xw, 18.95, .45, .28, 300, 8000, 0, 0, .7)                 # up and out
# 6 · web
pop(19.07, 700, .18)
whoosh(X, Xw, 19.9, 1.6, .06, 250, 1200, 0, 0, .5)                  # dolly back
for k, at in enumerate([19.25, 19.45, 19.6, 19.75, 19.9, 20.1, 20.2, 20.3]):
    blip(X, Xw, at, hz([81, 84, 86, 88, 91, 93, 96, 98][k]), .055, .1)
    d = .06; s = hp(noise(d), 5000) * env(d, .001, .015); put(X, Xw, s, at, .05, rng.uniform(-.5, .5), .2)
whoosh(X, Xw, 20.95, .35, .14, 600, 5000, -.5, 0, .5)
typing(21.05, 21.35, 26, .26); typing(21.4, 21.75, 28, .26)
press(21.9, .45)
bell(X, Xw, 22.35, hz(88), .12, 1.8, .3); bell(X, Xw, 22.43, hz(93), .1, 1.8, .3)
whoosh(X, Xw, 22.4, .3, .1, 5000, 800, .3, .3, .4)
whoosh(X, Xw, 23.72, .4, .3, 300, 6000, .8, -.8, .6)               # whip
for at in (23.55, 23.6): whoosh(X, Xw, at + .2, .3, .06, 2000, 9000, -.9, .9)
# 7 · automatizace
typing(23.85, 24.55, 28, .26)
press(24.65, .4); blip(X, Xw, 24.66, 1568, .06, .12, 0)
whoosh(X, Xw, 24.9, .45, .12, 200, 2500, 0, 0, .7)                 # push in
for k, at in enumerate([24.85, 25.15, 25.45, 25.75]):
    pop(at, [440, 523.3, 659.3, 880][k], .2); bell(X, Xw, at + .01, hz([81, 84, 88, 93][k]), .045, 1.2, -.4 + .27 * k)
whoosh(X, Xw, 25.4, 1.3, .05, 300, 1500, -.6, .6, .5)                # tracking pan
whoosh(X, Xw, 26.3, .7, .1, 1800, 250, 0, 0, .45)                   # pull back
tt = 25.95
while tt < 27.1:
    blip(X, Xw, tt, rng.uniform(2500, 4500), .012, .04); tt += rng.uniform(.03, .06)
prev = 0
for i in range(1, 2000):
    tt = 26.2 + i / 2000 * .9; x_ = (tt - 26.2) / .9; e_ = 4 * x_ ** 3 if x_ < .5 else 1 - (-2 * x_ + 2) ** 3 / 2
    n_ = min(30, int(30 * e_))
    if n_ > prev: prev = n_; blip(X, Xw, tt, 1500 + 40 * n_, .03, .035, .1)
for k, n in enumerate([84, 88, 91, 96]): bell(X, Xw, 27.1 + k * .045, hz(n), .065, 2.0, rng.uniform(-.3, .3))
whoosh(X, Xw, 27.9, .4, .2, 5000, 400, 0, 0, .7)                    # zoom out / in
# 8 · školení
typing(28.0, 28.55, 26, .26)
press(28.65, .4); whoosh(X, Xw, 28.75, .35, .12, 500, 4000, 0, 0, .45)
for k in range(6): pop(28.8 + k * .06, 600 * 2 ** (k / 12 * 2), .12)
for k, at in enumerate([29.35, 29.85, 30.35]):
    pop(at, 900, .16); bell(X, Xw, at + .01, hz([84, 88, 91][k]), .075, 1.4, .25)

# ================================================================== RECAP (31.3 – 34.3)
REC = [(31.35, 45), (32.35, 41), (33.35, 43)]
for i, (at, root) in enumerate(REC):
    whoosh(X, Xw, at + .02, .3, .22, 500, 7000, .8, 0, .7)
    impact(X, Xw, at, .85 + .1 * i)
    braam(X, Xw, at, hz(root - 12), 1.7, .8 + .1 * i)
    snare(X, Xw, at, .3)
    pop(at + .08, 520, .22); bell(X, Xw, at + .08, hz([84, 81, 83][i]), .06, 1.6)
    whoosh(X, Xw, at + .9, .28, .1, 1000, 6000, 0, -.8, .5)
    notes = {45: [57, 60, 64, 69], 41: [57, 60, 65, 69], 43: [55, 59, 62, 67]}[root]
    strings(M, Mw, at, [n - 12 for n in notes], 1.05, .07, .02, .15, .5)
    for k in range(4):   # driving toms between hits
        tom(X, Xw, at + .5 + k * .125, .16 + .05 * k, 95 + 10 * k)
    for k in range(8): ostinato(M, Mw, at + k * .125, hz(root), .07, .8)
for i in range(28):  # snare roll into the drop
    at = 33.85 + 1.0 * (1 - (1 - i / 28) ** 1.35)
    d = .08; s = bp(noise(d), 900, 7000) * env(d, .001, .022); put(X, Xw, s, at, .08 + .26 * i / 27, rng.uniform(-.3, .3), .15)
riser(X, Xw, 33.6, 34.85, .9, 220, 2400)
revcym(X, Xw, 34.85, 1.0, .5)
for at in (34.55, 34.62): whoosh(X, Xw, at + .2, .3, .07, 2000, 9000, .9, -.9)

# ================================================================== TAGLINE (34.85 – 38.75)
impact(X, Xw, 34.85, 1.4)
braam(X, Xw, 34.85, hz(29), 3.2, 1.2)
d = 2.6; s = hp(noise(d), 1500) * env(d, .01, .5); put(X, Xw, s, 34.85, .32, 0, .5)
whoosh(X, Xw, 35.1, .9, .3, 300, 4000, .85, -.2, .35)               # the words swing in
strings(M, Mw, 34.85, [53, 57, 60, 65, 69, 72], 1.65, .1, .08, .4, .7)
pad(M, Mw, 34.85, [41, 53, 57, 60, 65, 72], 1.7, .1, .05, .5)
sub(M, 34.85, hz(29), 1.5, .16)
for k, n in enumerate([84, 89, 93, 96]): bell(X, Xw, 34.88 + k * .06, hz(n), .05, 2.6, rng.uniform(-.5, .5))
sparkle(34.9, 14, .7, .035)
# "My to postavíme." + lock-up
whoosh(X, Xw, 36.36, .3, .2, 600, 7000, 0, 0, .8)
impact(X, Xw, 36.35, 1.1)
braam(X, Xw, 36.35, hz(31), 3.0, 1.0)
snare(X, Xw, 36.35, .35)
shing(36.37, .15)
strings(M, Mw, 36.35, [55, 59, 62, 67, 71, 74], 2.9, .085, .05, .45, .8)
pad(M, Mw, 36.35, [43, 55, 59, 62, 67, 74], 3.0, .085, .05, .6)
sub(M, 36.35, hz(31), 2.6, .16)
tt = 35.35
while tt < 38.75 - 1e-3:   # pulse + 8th ostinato under the tagline
    if tt >= 36.8: pulse(X, Xw, tt, .5); kick_times.append(tt)
    for q in (0, .25):
        if tt + q >= 35.35: ostinato(M, Mw, tt + q, hz(43 if tt >= 36.35 else 41), .05, .75)
    tt += BEAT
for k in range(6): tom(X, Xw, 38.1 + k * .09, .18 + .06 * k, 95 + 8 * k)
riser(X, Xw, 38.2, 39.35, .55, 300, 2400)
revcym(X, Xw, 39.35, .9, .45)
for at in (38.55, 38.62): whoosh(X, Xw, at + .2, .3, .07, 2000, 9000, -.9, .9)

# ================================================================== END CARD – resolution in C
whoosh(X, Xw, 39.1, .5, .07, 2500, 9000, -.3, .3, .8, 2.5, .6)     # ring draws
whoosh(X, Xw, 39.33, .22, .09, 900, 7000, -.5, .5, .85)
impact(X, Xw, 39.35, .6, crash=False, sub=42)
braam(X, Xw, 39.35, hz(36), 4.5, .55, bright=.12)
for k, n in enumerate([84, 88, 91, 96]): bell(X, Xw, 39.36 + k * .05, hz(n), .09, 4.2, [-.4, -.1, .1, .4][k])
pad(M, Mw, 39.35, [36, 48, 55, 60, 64, 67, 72], 5.65, .12, .3, 1.6)
strings(M, Mw, 39.35, [48, 55, 60, 64], 5.65, .05, .6, 1.8, .2)
sub(M, 39.35, hz(36), 5.0, .1)
shing(39.52, .12)
pop(39.92, 1046.5, .1); pop(40.32, 1318.5, .1)
for k, n in enumerate([72, 76, 79, 84, 79, 76, 72, 76]):
    pluck(M, Mw, 40.85 + k * .5, hz(n), .045 * (1 - k / 10))

# ================================================================== MIX
def ir(seed, d=3.2, tau=.8):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 5500); x[:int(.018 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2)) * 1.15
IRL, IRR = ir(11), ir(12)
def mix(dry, wet): return dry.L + fftconvolve(wet.L, IRL)[:N], dry.R + fftconvolve(wet.R, IRR)[:N]
AL, AR = mix(A, Aw); ML, MR = mix(M, Mw); XL, XR = mix(X, Xw)
cut = int(5.4 * SR); ga = np.ones(N); ga[cut:] = 0; ga[cut - 240:cut] = np.linspace(1, 0, 240)
# sidechain: music ducks under every pulse/kick
tt = np.arange(N) / SR; duck = np.ones(N)
for k in kick_times:
    i = int(k * SR); j = min(N, i + int(.35 * SR)); duck[i:j] = np.minimum(duck[i:j], 1 - .45 * np.exp(-(tt[i:j] - k) / .11))
L = AL * ga + ML * duck + XL; R = AR * ga + MR * duck + XR
fade = np.clip((DUR - tt) / 1.2, 0, 1) * np.clip(tt / .02, 0, 1)
L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = np.tanh(L / pk * 2.2), np.tanh(R / pk * 2.2)
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * .93, R / pk * .93
out = sys.argv[1] if len(sys.argv) > 1 else 'intro2.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
m = (L + R) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(45)))
