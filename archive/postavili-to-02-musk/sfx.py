"""POSTAVILI TO #02 – Elon Musk: hudba, zvuky a hlas. Časy z timeline.json (voice/timeline.py), stejné jako v reel.html.
Temný elektronický podkres v a moll, 100 BPM. Úvod: dron, tep, výbuchy tří raket, odpočet T−5…0, ticho a start
(dunění + úder). Příběh: synthwave arpeggio a lehký groove, 8bit střelba u Blastaru, počítadla a cinknutí.
2008: hudba spadne do temného dronu a alarmu. Čtvrtý start: rozřešení v C dur a „úspěšný“ zvonek. Šílená fakta:
plné bicí, rychlé arpeggio, motory, přistání, kovové chycení. Kontroverze: temnější groove (d moll – E), glitch,
razítko, prasknutí. Bilion: velký akord. Mars: klavír a smyčce, dunění, „žuch“ na pointu. Konec: lehký outro groove.
Zvuky k animacím: fx.json = události z reel.html (export_ev.py). Hudba uhýbá hlasu (~−8 dB), hlas ~9 dB nad hudbou.
usage: python3 sfx.py out.wav [PRE]"""
import sys, wave, json, os
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt, sawtooth
from scipy.ndimage import maximum_filter1d, minimum_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'timeline.json'))); S = TL['S']
CK = {}
for sid, i, txt, a, b in TL['chunks']: CK.setdefault(sid, {})[i] = a
st = lambda s: S[s][0]; en = lambda s: S[s][1]; ck = lambda s, i: CK[s][i]
SR = 48000; DUR = TL['END']; N = int(DUR * SR)
rng = np.random.default_rng(55)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)
B = 60 / 100; ST = B / 4
K_PAD, K_ARP, K_PIANO, K_808, K_KICK, K_DRONE = 3.0, 3.0, 2.2, .32, .7, .45


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, at, g=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


M, Mw, D, Dw, X, Xw = Bus(), Bus(), Bus(), Bus(), Bus(), Bus()
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


# ---------------------------------------------------------------- nástroje
def kick(at, g=1.0, f0=170, f1=54, dec=.22):
    d = .7; t = T(d); f = f1 + (f0 - f1) * np.exp(-t / .028)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, dec) + bp(noise(d), 2500, 7000) * env(d, .0004, .005) * .6
    put(D, Dw, np.tanh(s * 1.4), at, g * K_KICK, 0, .04)
def clap(at, g=1.0, pan=0.0):
    d = .35; s = np.zeros(int(d * SR))
    for k, o in enumerate([0, .009, .019, .028]):
        i = int(o * SR); n = bp(noise(d), 900, 4200) * env(d, .0005, .011 if k < 3 else .085); s[i:] += n[:len(s) - i]
    put(D, Dw, s, at, g, pan, .4)
def snare(at, g=1.0):
    d = .22; t = T(d); s = bp(noise(d), 1400, 7500) * env(d, .001, .055) + np.sin(2 * np.pi * 185 * t) * env(d, .001, .035) * .6
    put(D, Dw, s, at, g, 0, .25)
def hat(at, g=1.0, open_=False, pan=.22):
    d = .45 if open_ else .08; put(D, Dw, hp(noise(d), 7500) * env(d, .0005, .13 if open_ else .016), at, g, pan, .08)
def b808(at, note, d, g=1.0, glide=0.0):
    t = T(d); f = hz(note) * 2 ** (glide / 12 * np.exp(-t / .07))
    s = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 4.0) / np.tanh(4.0)
    e = np.minimum(1, t / .004) * np.exp(-t / max(d * .7, .25)) * np.clip((d - t) / .05, 0, 1)
    put(D, Dw, lp(s * e, 1400), at, g * K_808, 0, 0)
def piano(at, note, g=1.0, d=2.6, pan=0.0, bright=1.0):
    f = hz(note); t = T(d); s = np.zeros_like(t)
    for k in range(1, 10):
        fk = f * k * np.sqrt(1 + .0004 * k * k)
        if fk > 11000: break
        s += (1 / k ** 1.15) * (1 if k == 1 else .65 * bright) * np.sin(2 * np.pi * fk * t + k) * np.exp(-t * (.55 + k * .5))
    s += bp(noise(d), 1500, 5000) * env(d, .0005, .01) * .07
    s *= np.minimum(1, t / .003) * np.clip((d - t) / .25, 0, 1)
    put(M, Mw, s, at, g * K_PIANO, pan, .6)
def pad(at, notes, d, g=1.0, a=.5, r=.7, fc=1600, pan=.0):
    t = T(d); s = np.zeros_like(t)
    for j, n in enumerate(notes):
        for k, det in enumerate((-.09, 0, .09)):
            ph = rng.uniform(0, 2 * np.pi)
            s += sawtooth(2 * np.pi * hz(n + det) * t + ph) * (.5 if det else .7)
    s = lp(s, fc, 2) / (len(notes) * 1.7)
    s *= np.clip(t / a, 0, 1) * np.clip((d - t) / r, 0, 1)
    put(M, Mw, s, at, g * K_PAD, pan, .8)
def pluck(at, note, g=1.0, d=.55, pan=0.0, fc=2800, dec=.17):
    f = hz(note); t = T(d); s = sawtooth(2 * np.pi * f * t) * .5 + np.sin(2 * np.pi * f * t)
    put(M, Mw, lp(s * np.minimum(1, t / .002) * np.exp(-t / dec), fc), at, g, pan, .5)
def bell(at, note, g=1.0, d=1.8, pan=0.0):
    f = hz(note); t = T(d)
    s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (1.1 / r ** .5)) for r, a in [(1, 1), (2.0, .4), (2.76, .2), (5.4, .07)])
    put(M, Mw, s * np.minimum(1, t / .002), at, g, pan, .6)
def drone(at, d, notes, g=1.0):
    t = T(d); s = sum(np.sin(2 * np.pi * hz(n) * t + i) for i, n in enumerate(notes))
    s += .3 * np.sin(2 * np.pi * hz(notes[0]) * 2 * t) * (1 + .3 * np.sin(2 * np.pi * .7 * t))
    put(M, Mw, s * np.clip(t / 1.2, 0, 1) * np.clip((d - t) / .3, 0, 1) / len(notes), at, g * K_DRONE, 0, .3)

def impact(at, g=1.0, dec=1.4, crash=.15):
    d = 3.2; t = T(d); f = 29 + 95 * np.exp(-t / .05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, dec * .5)
    s = s * .6 + lp(noise(d), 3200) * env(d, .001, .11) * .9 + hp(noise(d), 4500) * env(d, .002, .7) * crash
    put(X, Xw, hp(np.tanh(s * 1.6), 35), at, g, 0, .55)
def stamp(at, g=1.0):
    d = 1.2; t = T(d); f = 42 + 70 * np.exp(-t / .03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .18) + lp(noise(d), 1800) * env(d, .001, .05) * 1.2
    put(X, Xw, np.tanh(s * 1.8), at, g, 0, .35)
def rev(at_end, d=.6, g=.3, lo=2500):
    t = T(d); x = t / d; put(X, Xw, hp(noise(d), lo) * x ** 3 * np.clip((d - t) / .01, 0, 1), at_end - d, g, 0, .4)
def riser(at_end, d=1.8, g=.25, f0=180, f1=1500):
    t = T(d); x = t / d; f = f0 * (f1 / f0) ** x
    s = sawtooth(2 * np.pi * np.cumsum(f) / SR) * .25 + np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * .25 + hp(noise(d), 1500) * .5
    put(X, Xw, lp(s, 7000) * x ** 2.2 * np.clip((d - t) / .015, 0, 1), at_end - d, g, 0, .5)
def whoosh(at, d=.35, g=.2, f0=500, f1=6000, peak=.6):
    t = T(d); x = t / d; e = np.where(x < peak, (x / peak) ** 2, np.exp(-(x - peak) / (1 - peak) * 3))
    put(X, Xw, bp(noise(d), min(f0, f1), max(f0, f1)) * e, at - d * peak, g, 0, .4)
def glitch(at, d=.38, g=.3):
    n = int(d * SR); s = np.zeros(n); r = np.random.default_rng(7); seg = int(.028 * SR)
    for i in range(0, n, seg):
        L = min(seg, n - i)
        if r.random() < .78:
            f = r.uniform(180, 1800); tt = np.arange(L) / SR
            s[i:i + L] += (np.sign(np.sin(2 * np.pi * f * tt)) * .55 + r.standard_normal(L) * .35) * (1 - i / n)
    s = np.round(s * 5) / 5
    put(X, Xw, lp(s, 7000), at, g, 0, .15)
def click(at, g=.2, pan=0.0):
    d = .03; t = T(d); s = bp(noise(d), 2000, 8000) * env(d, .0003, .004) + np.sin(2 * np.pi * 1700 * t) * env(d, .0004, .003) * .3
    put(X, Xw, s, at, g, pan, .05)
def mouse(at, g=.22):
    d = .05; t = T(d); s = bp(noise(d), 1500, 6000) * env(d, .0002, .003) + np.sin(2 * np.pi * 3200 * t) * env(d, .0002, .002) * .4
    put(X, Xw, s, at, g, .1, .05); put(X, Xw, s * .6, at + .045, g, .1, .05)
def ding(at, g=.12):
    for k, (n, o) in enumerate([(88, 0), (84, .09)]):
        d = .5; t = T(d); put(X, Xw, np.sin(2 * np.pi * hz(n) * t) * env(d, .002, .12), at + o, g, 0, .4)
def bonk(at, f=380, g=.14, pan=0.0):
    d = .17; t = T(d); w = np.sign(np.sin(2 * np.pi * f * t)) * .4 + np.sin(2 * np.pi * f * t) * .6
    w2 = np.sign(np.sin(2 * np.pi * f * .75 * t)) * .4 + np.sin(2 * np.pi * f * .75 * t) * .6
    s = w * env(d, .001, .035) + np.concatenate([np.zeros(int(.055 * SR)), (w2 * env(d, .001, .05))[:len(t) - int(.055 * SR)]])
    put(X, Xw, lp(s, 3000), at, g, pan, .15)
def printer(at, d=.45, g=.1):
    t = T(d); buzz = (np.sin(2 * np.pi * 95 * t) > .55).astype(float) * rng.uniform(.6, 1, len(t))
    s = bp(buzz * noise(d), 900, 5000) * np.clip(t / .02, 0, 1) * np.clip((d - t) / .03, 0, 1) * (1 + .4 * np.sin(2 * np.pi * 11 * t))
    put(X, Xw, s, at, g, -.2, .2)
def paper(at, g=.18, pan=0.0):
    d = .14; s = bp(noise(d), 1800, 7500) * env(d, .002, .03) + lp(noise(d), 300) * env(d, .001, .02) * .8
    put(X, Xw, s, at, g, pan, .2)
def tick(at, g=.1, f=2600):
    d = .025; t = T(d)
    put(X, Xw, bp(noise(d), 2000, 8000) * env(d, .0002, .003) + np.sin(2 * np.pi * f * t) * env(d, .0002, .004) * .4, at, g, 0, .05)
def pop(at, f=900, g=.2):
    d = .12; t = T(d); fr = f * (1 + .7 * np.exp(-t / .012))
    put(X, Xw, np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(d, .001, .03), at, g, 0, .3)

# ---------------------------------------------------------------- další zvuky
def heartbeat(at, g=.5):
    for o, k in ((0, 1), (.19, .6)):
        d = .35; t = T(d); f = 48 + 30 * np.exp(-t / .03)
        put(D, Dw, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .07) * k, at + o, g, 0, .05)
def shutter(at, g=.25):
    for o in (0, .045):
        d = .04; put(X, Xw, bp(noise(d), 1500, 7000) * env(d, .0003, .006), at + o, g, .2, .1)
def pen(at, d, g=.12):
    t = T(d); am = np.clip(np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * 1.3 * t + 1) * 1.6, 0, 1)
    put(X, Xw, bp(noise(d), 2500, 8000) * am * np.clip(t / .05, 0, 1) * np.clip((d - t) / .1, 0, 1), at, g, -.15, .1)
def swish(at, g=.12):
    d = .12; t = T(d); put(X, Xw, bp(noise(d), 1800, 6000) * np.sin(np.pi * t / d) ** 2, at, g, .1, .1)
def projector(at, d, g=.08):
    t = T(d); cl = (np.sin(2 * np.pi * 24 * t) > .92).astype(float)
    s = bp(noise(d) * cl, 800, 5000) + .3 * np.sin(2 * np.pi * 120 * t) * .2
    put(X, Xw, s * np.clip(t / .1, 0, 1) * np.clip((d - t) / .2, 0, 1), at, g, .2, .1)
def vhs(at, d, g=.06):
    t = T(d); s = hp(noise(d), 3000) * .6 + .5 * np.sin(2 * np.pi * 60 * t) + .3 * np.sin(2 * np.pi * 180 * t)
    put(X, Xw, s * (1 + .3 * np.sin(2 * np.pi * .7 * t)) * np.clip(t / .05, 0, 1) * np.clip((d - t) / .1, 0, 1), at, g, 0, .05)
def rip(at, g=.25):
    d = .3; t = T(d); x = t / d; s = bp(noise(d), 1000, 7000) * (1 - x) ** 2 * (np.sin(2 * np.pi * 70 * t) > 0)
    put(X, Xw, s, at, g, 0, .2)
def strings(at, notes, d, g=1.0, a=.9, r=.9, fc=1900):
    t = T(d); s = np.zeros_like(t)
    for n in notes:
        for det in (-.07, 0, .07):
            vib = 1 + .004 * np.sin(2 * np.pi * 5.2 * t + rng.uniform(0, 6))
            s += sawtooth(2 * np.pi * np.cumsum(hz(n + det) * vib) / SR) * (.5 if det else .7)
    s = lp(s, fc, 2) / (len(notes) * 1.7) * np.clip(t / a, 0, 1) * np.clip((d - t) / r, 0, 1)
    put(M, Mw, s, at, g * K_PAD, 0, .9)

# ---------------------------------------------------------------- retro (8bit) zvuky k animacím
def sqw(f, t): return np.sign(np.sin(2 * np.pi * f * t))
def blip(at, k=0, g=.1):
    f = [880, 988, 1175, 1319, 1568, 1760][int(k) % 6]; d = .075; t = T(d)
    put(X, Xw, lp(sqw(f, t) * .5 * env(d, .001, .028), 5000), at, g, (k % 3 - 1) * .15, .15)
def pop2(at, g=.14): blip(at, 0, g); blip(at + .055, 3, g * .75)
def alert(at, g=.15, lo=False):
    for o, f in ((0, 440 if lo else 660), (.12, 330 if lo else 880)):
        d = .13; t = T(d); s = (sqw(f, t) * .6 + np.sin(2 * np.pi * f * t) * .4) * env(d, .002, .07) * np.clip((d - t) / .01, 0, 1)
        put(X, Xw, lp(s, 4500), at + o, g, 0, .2)
def glide(at, f0, f1, d, g, w=.15, pan=0.0):
    t = T(d); f = f0 * (f1 / f0) ** (t / d)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 * np.minimum(1, t / .004) * np.clip((d - t) / .03, 0, 1)
    put(X, Xw, lp(s, 4000), at, g, pan, w)
def thunk(at, g=1.0):
    d = .25; t = T(d); f = 95 + 70 * np.exp(-t / .02)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .06) + lp(noise(d), 900) * env(d, .001, .02) * .6
    put(X, Xw, s, at, .3 * g, 0, .15)
def roll(at, d, g=.12):
    t = T(d); rat = (np.sin(2 * np.pi * 21 * t) > .7).astype(float)
    s = lp(noise(d), 260) * 1.3 + bp(noise(d) * rat, 1200, 5000) * .6
    put(X, Xw, s * np.clip(t / .08, 0, 1) * np.clip((d - t) / .12, 0, 1), at, g, 0, .2)
def typerun(at, d, rate=17, g=.09):
    r = np.random.default_rng(int(at * 1000))
    for i in range(max(1, int(d * rate))): click(at + i / rate + r.uniform(-.006, .006), g * r.uniform(.7, 1.1), r.uniform(-.25, .25))
def crush(at, d=.3, g=.12):
    n = int(d * SR); s = noise(d); h = int(SR / 2600); s = np.repeat(s[::h], h)[:n]; s = np.round(s * 3) / 3
    put(X, Xw, lp(s * np.sin(np.pi * np.arange(n) / n) ** 1.5, 6500), at, g, 0, .1)
def staticb(at, d=.26, g=.12): put(X, Xw, hp(noise(d), 1500) * np.sin(np.pi * T(d) / d), at, g, 0, .05)
def rewind(at, g=.07):
    for i in range(9): glide(at + i * .034, 2600, 900, .03, g, 0)
def sparkle(at, g=.045):
    r = np.random.default_rng(int(at * 100))
    for i in range(10): bell(at + i * .042 + r.uniform(0, .02), 84 + int(r.integers(0, 12)), g * r.uniform(.5, 1), .7, r.uniform(-.5, .5))
def coin(at, g=.1): ding(at, g); bell(at + .02, 96, g * .5, 1.2); bell(at + .1, 100, g * .45, 1.4)
def ticks_eo(at, d, n=26, g=.05, f0=2400):
    for i in range(n): tick(at + d * (1 - (1 - i / n) ** (1 / 3)), g, f0 + 40 * i)
def blips(at, d, n=14, g=.05):
    r = np.random.default_rng(3)
    for i in range(n): blip(at + r.uniform(0, d), int(r.integers(0, 6)), g * r.uniform(.6, 1))
def drip(at, g=.08): pop(at, 1500, g); pop(at + .13, 1150, g * .7)
def chatter(at, d, g=.035):
    r = np.random.default_rng(11); t = at
    while t < at + d: glide(t, r.uniform(500, 2500), r.uniform(500, 2500), .025, g, 0, r.uniform(-.3, .3)); t += .03 + r.uniform(0, .03)
def coinrain(at, g=.05):
    r = np.random.default_rng(5)
    for i in range(10): bell(at + i * .07 + r.uniform(0, .03), 88 + int(r.integers(0, 8)), g * r.uniform(.5, 1), .5, r.uniform(-.6, .6))
def power(at, g=.14):
    d = .26; t = T(d); f = 90 * (2200 / 90) ** (t / d) ** 1.4
    s = (np.sin(2 * np.pi * np.cumsum(f) / SR) * .6 + hp(noise(d), 2500) * .3) * (t / d) ** 2
    put(X, Xw, s * np.clip((d - t) / .01, 0, 1), at, g, 0, .4)
def shimmer(at, g=.06):
    for i, n in enumerate((77, 81, 84, 89)): bell(at + i * .07, n, g * (1 - i * .12), 1.6, (i - 1.5) * .25)

CH = dict(Dm=[62, 65, 69], Bb=[58, 62, 65], F=[60, 65, 69], C=[60, 64, 67], Gm=[55, 58, 62], Am=[57, 60, 64])
BS = dict(Dm=38, Bb=34, F=41, C=36, Gm=43, Am=33)
def bars(t0, t1, prog, fn):
    k = 0; t = t0
    while t < t1 - .05:
        fn(t, prog[k % len(prog)], min(4 * B, t1 - t), k); t += 4 * B; k += 1
def arp(at, ch, d, g=.07, oct_=12, fc=3800):
    notes = CH[ch] + [CH[ch][0] + 12]; pat = [0, 1, 2, 3, 2, 1, 2, 3]
    for i in range(int(d / (B / 2))): pluck(at + i * B / 2, notes[pat[i % 8]] + oct_, g * (1 if i % 2 == 0 else .7) * K_ARP, .5, (i % 3 - 1) * .3, fc, .18)
def groove(at, ch, d, k, light=False, kick_g=.75):
    for j, s16 in enumerate([0, 6, 10] if not light else [0, 8]):
        if s16 * ST < d - .05: kick(at + s16 * ST, kick_g if s16 == 0 else kick_g * .8); b808(at + s16 * ST, BS[ch], min(4 * ST * 2, d - s16 * ST), .45)
    for s16 in (4, 12):
        if s16 * ST < d - .05: clap(at + s16 * ST, .26 if not light else .18)
    for s16 in range(0, 16, 2):
        if s16 * ST < d - .05: hat(at + s16 * ST, .07 if s16 % 4 else .09)

# ---------------------------------------------------------------- akordy a nástroje pro #02 (a moll)
CH = dict(Am=[57, 60, 64], F=[53, 57, 60], C=[55, 60, 64], G=[55, 59, 62], Dm=[50, 53, 57], E=[52, 56, 59], Em=[52, 55, 59])
BS = dict(Am=33, F=29, C=36, G=31, Dm=38, E=28, Em=28)
def beep(at, k=0, g=.11):
    f, d = (1500, .32) if k else (1000, .12); t = T(d)
    put(X, Xw, np.sin(2 * np.pi * f * t) * np.minimum(1, t / .003) * np.clip((d - t) / .02, 0, 1) * (1 if k else .9), at, g, 0, .25)
def boom(at, g=1.0):
    impact(at, .55 * g, 1.1, .12); d = 1.4; t = T(d)
    s = np.tanh(lp(noise(d), 900) * 2.5) * env(d, .002, .28)
    put(X, Xw, s, at, .35 * g, 0, .5)
def rumble(at, d, g=.4):
    t = T(d); n = lp(noise(d), 160) * 3 + lp(noise(d), 900) * .5 * (1 + .5 * np.sin(2 * np.pi * 7 * t))
    put(X, Xw, np.tanh(n) * np.clip(t / .25, 0, 1) * np.clip((d - t) / .6, 0, 1), at, g, 0, .35)
def launch(at): rumble(at - .05, 2.6, .55); impact(at, .7, 1.6, .3); whoosh(at + .15, .6, .16, 300, 4000, .3)
def thrust(at, d): rumble(at, max(.3, d), .3); put(X, Xw, bp(noise(max(.3, d)), 2000, 7000) * .25 * np.clip(T(max(.3, d)) / .1, 0, 1), at, .25, 0, .2)
def touch(at, g=.4):
    d = .5; t = T(d); f = 60 + 40 * np.exp(-t / .04)
    put(X, Xw, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .12) + lp(noise(d), 1200) * env(d, .002, .08) * .7, at, g, 0, .3)
def clank(at, g=.25):
    d = 1.2; t = T(d); s = sum(np.sin(2 * np.pi * f * t) * a * np.exp(-t / dec) for f, a, dec in [(210, 1, .5), (517, .6, .35), (893, .4, .25), (1420, .3, .18)])
    put(X, Xw, s * np.minimum(1, t / .001) + bp(noise(d), 1500, 6000) * env(d, .0005, .02), at, g, 0, .4)
def crack(at, g=.3):
    d = .4; t = T(d); s = hp(noise(d), 2500) * env(d, .0003, .03) + np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t / .05) + 80) / SR) * env(d, .001, .06) * .5
    put(X, Xw, s, at, g, 0, .3)
def notif(at, g=.12):
    for o, n in ((0, 88), (.09, 95)):
        d = .35; t = T(d); put(X, Xw, (np.sin(2 * np.pi * hz(n) * t) + .3 * np.sin(4 * np.pi * hz(n) * t)) * env(d, .002, .08), at + o, g, .1, .3)
def tap(at, k=0, g=.15):
    d = .08; t = T(d); put(X, Xw, bp(noise(d), 800, 4000) * env(d, .0005, .008) + np.sin(2 * np.pi * (180 + 30 * k) * t) * env(d, .001, .02) * .6, at, g, 0, .1)
def jet(at, d, g=.12):
    t = T(d); x = t / d; f0 = 400 + 2200 * np.sin(np.pi * x)
    s = bp(noise(d), 300, 6000) * (.4 + .6 * np.sin(np.pi * x)); put(X, Xw, lp(s, 4000) * np.clip(t / .2, 0, 1) * np.clip((d - t) / .3, 0, 1), at, g, -.3, .3)
def alarm(at, d, g=.06):
    k = 0; tt = at
    while tt < at + d:
        f = 820 if k % 2 == 0 else 615; dd = .12; t = T(dd)
        put(X, Xw, lp(np.sign(np.sin(2 * np.pi * f * t)) * .5 * np.clip((dd - t) / .01, 0, 1), 3000), tt, g, 0, .15); tt += .14; k += 1
def success(at, g=.07):
    for i, n in enumerate((72, 76, 79, 84)): bell(at + i * .06, n, g * (1 - i * .1), 1.8, (i - 1.5) * .2)
def scanfx(at, g=.12):
    d = .3; t = T(d); x = t / d; put(X, Xw, hp(noise(d), 3000) * x ** 2 * np.clip((d - t) / .02, 0, 1), at, g, 0, .2)
def zap(at, k=0, g=.07):
    d = .13; t = T(d); f = (1900 - 300 * k) * np.exp(-t / .05) + 250
    put(X, Xw, lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 * env(d, .001, .05), 5000), at, g, (k - 1) * .2, .15)
def hum(at, d, g=.035):
    t = T(d); s = sum(np.sin(2 * np.pi * 60 * h * t) / h for h in (1, 2, 3, 5)) * (1 + .2 * np.sin(2 * np.pi * .5 * t))
    put(X, Xw, s * np.clip(t / .3, 0, 1) * np.clip((d - t) / .2, 0, 1), at, g, 0, .1)
def thud(at, g=.35):
    d = .5; t = T(d); f = 90 * np.exp(-t / .12) + 40
    put(X, Xw, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .15) + lp(noise(d), 500) * env(d, .001, .03), at, g, 0, .2)
def scratch(at, g=.14): d = .22; t = T(d); put(X, Xw, bp(noise(d), 2500, 8000) * np.sin(np.pi * t / d) ** 1.5, at, g, -.1, .1)

# ---------------------------------------------------------------- A: háček (tři selhání, odpočet) a start
S3 = st('s3') - .06
drone(0, S3 + .2, [33, 40, 45], .16)
t = .0
while t < st('s2') - .1: heartbeat(t, .3 + .2 * t / max(1, st('s2'))); t += .6
for i in range(int((S3 - .3) / (B / 2))): hat(i * B / 2, .03 if i % 2 else .045)
riser(S3 - .02, 1.6, .12, 150, 2200)
pad(S3, [57, 64, 67, 71], 2.2, .09, a=.03, r=1.2, fc=3000); bell(S3 + .05, 81, .06); bell(S3 + .3, 88, .045)

# ---------------------------------------------------------------- B: příběh (Blastar, Stanford, Zip2, X.com, líbánky)
def story(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.2, r=.25, fc=1800); arp(at, ch, d, .055, 12, 3400)
    groove(at, ch, d, k, light=True, kick_g=.5)
bars(st('s4') - .06, st('s10') - .06, ['Am', 'F', 'C', 'G'], story)

# ---------------------------------------------------------------- C: SpaceX a Tesla
def build(at, ch, d, k):
    pad(at, CH[ch] + [CH[ch][0] + 12], d + .05, .07, a=.08, r=.2, fc=2800); arp(at, ch, d, .065, 12, 4200)
    groove(at, ch, d, k, kick_g=.6)
bars(st('s10') - .06, st('s13') - .06, ['F', 'C', 'G', 'Am'], build)

# ---------------------------------------------------------------- D: rok 2008 (temný dron, alarm z fx.json)
d0, d1 = st('s13') - .06, st('s15') - .06
drone(d0, d1 - d0 + .2, [33, 34, 45], .2); strings(d0, [45, 52, 58], d1 - d0 + .2, .07, a=.3, r=.2, fc=1100)
t = d0
while t < d1 - .1: kick(t, .45, 120, 45, .3); t += B

# ---------------------------------------------------------------- E: čtvrtý start vyšel, NASA
def hope(at, ch, d, k):
    pad(at, CH[ch] + [CH[ch][0] + 12], d + .05, .09, a=.05, r=.3, fc=3200); arp(at, ch, d, .07, 24, 5200)
    groove(at, ch, d, k, light=k == 0, kick_g=.6)
bars(st('s15') - .06, st('s17') - .06, ['C', 'G', 'Am', 'F'], hope)

# ---------------------------------------------------------------- F: šílená fakta (plné bicí)
def mont(at, ch, d, k):
    pad(at, CH[ch] + [CH[ch][0] + 12], d + .05, .08, a=.03, r=.2, fc=3800); arp(at, ch, d, .075, 24, 6000)
    groove(at, ch, d, k, kick_g=.8)
    for s16 in range(1, 16, 2):
        if s16 * ST < d - .05: hat(at + s16 * ST, .05, pan=.3)
bars(st('s17') - .06, st('s20') - .06, ['Am', 'F', 'C', 'G'], mont)
rev(st('s17') - .05, .6, .2)

# ---------------------------------------------------------------- G: kontroverze (temnější groove)
def dark(at, ch, d, k):
    pad(at, CH[ch], d + .05, .07, a=.1, r=.2, fc=1600); arp(at, ch, d, .05, 12, 2600)
    groove(at, ch, d, k, kick_g=.7)
bars(st('s20') - .06, st('s24') - .06, ['Dm', 'Am', 'E', 'Am'], dark)

# ---------------------------------------------------------------- H: první bilionář
b0 = st('s24') - .06
pad(b0, [57, 64, 69, 72, 76], st('s25') - b0 + .3, .1, a=.15, r=.4, fc=4200); strings(b0, [45, 52, 57], st('s25') - b0 + .3, .07, a=.3, r=.4, fc=2400)
bell(ck('s24', 1), 81, .06); bell(ck('s24', 1) + .25, 88, .05)

# ---------------------------------------------------------------- I: Mars (klavír, smyčce)
def mars(at, ch, d, k):
    strings(at, CH[ch], d + .4, .075, a=.6, r=.6, fc=2200); piano(at, CH[ch][0], .08, 2.6); piano(at, CH[ch][2] + 12, .06, 2.6)
bars(st('s25') - .06, st('s27') - .06, ['F', 'C', 'Am', 'G'], mars)

# ---------------------------------------------------------------- J: anketa a výzva
def outro(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.1, r=.3, fc=2000); arp(at, ch, d, .05, 12, 3000)
    groove(at, ch, d, k, light=True, kick_g=.45)
bars(st('s27') - .06, DUR, ['F', 'C', 'G', 'Am'], outro)

# ---------------------------------------------------------------- K: zvuky k animacím (fx.json z reel.html)
FX = json.load(open(os.path.join(HERE, 'fx.json')))['events']
def P(e, i, d): return e[i] if len(e) > i else d
HITS = []
for e in FX:
    at, ty = e[0], e[1]
    if ty in ('inv', 'shk'): continue
    elif ty == 'hum': hum(at, P(e, 2, 3))
    elif ty == 'boom': boom(at, P(e, 2, 1)); HITS.append(at)
    elif ty == 'beep': beep(at, P(e, 2, 0))
    elif ty == 'launch': launch(at); HITS.append(at)
    elif ty == 'blip': pop(at, [900, 1000, 1100, 1200, 1350, 1500][int(P(e, 2, 0)) % 6], .12)
    elif ty == 'zap': zap(at, P(e, 2, 0))
    elif ty == 'stamp': stamp(at, P(e, 2, .4))
    elif ty == 'coin': ding(at, .11); bell(at + .02, 96, .05, 1.2)
    elif ty == 'count':
        d = P(e, 2, .7); n = 24
        for i in range(n): tick(at + d * (1 - (1 - i / n) ** (1 / 3)), .05, 2400 + 40 * i)
    elif ty == 'whoosh': whoosh(at + .12, .34, .14, 500, 5500, .4)
    elif ty == 'swish': swish(at, .13)
    elif ty == 'scanfx': scanfx(at)
    elif ty == 'scratch': scratch(at)
    elif ty == 'pop': pop(at, 950, .14)
    elif ty == 'pop2': pop(at, 900, .13); pop(at + .06, 1300, .1)
    elif ty == 'slam': impact(at, P(e, 2, .4), .8, .1); HITS.append(at)
    elif ty == 'jet': jet(at, P(e, 2, 2))
    elif ty == 'notif': notif(at)
    elif ty == 'rumble': rumble(at, P(e, 2, 1.5), .3)
    elif ty == 'alarm': alarm(at, P(e, 2, 2))
    elif ty == 'success': success(at); HITS.append(at)
    elif ty == 'thrust': thrust(at, P(e, 2, 1))
    elif ty == 'touch': touch(at)
    elif ty == 'clamp': clank(at)
    elif ty == 'crack': crack(at); glitch(at, .2, .1)
    elif ty == 'glitch': glitch(at, P(e, 2, .25), .12)
    elif ty == 'hit': impact(at, .25, .5, .06)
    elif ty == 'tap': tap(at, P(e, 2, 0))
    elif ty == 'type':
        d = P(e, 2, 1); r = np.random.default_rng(int(at * 1000))
        for i in range(int(d * 14)): click(at + i / 14 + r.uniform(-.006, .006), .09, r.uniform(-.25, .25))
    elif ty == 'thud': thud(at)
    else: print('POZOR: neznámá událost', ty)

# ---------------------------------------------------------------- mix
def ir(seed, d=2.2, tau=.55):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 6500); x[:int(.018 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
IRL, IRR = ir(1), ir(2)
t_ = np.arange(N) / SR
wet = lambda b, g: (fftconvolve(b.L, IRL)[:N] * g, fftconvolve(b.R, IRR)[:N] * g)
mL, mR = wet(Mw, .6); dL, dR = wet(Dw, .45); xL, xR = wet(Xw, .9)
ML, MR = M.L + mL, M.R + mR; ML, MR = ML + .5 * bp(ML, 1200, 5000), MR + .5 * bp(MR, 1200, 5000)
DL, DR = D.L + dL, D.R + dR; XL, XR = X.L + xL, X.R + xR
duck = np.ones(N)
for at in HITS:
    duck *= 1 - .35 * np.clip((t_ - at) / .01, 0, 1) * np.clip((at + .35 - t_) / .3, 0, 1)
# krátké ticho těsně před startem (T−0)
mute = 1 - np.clip((t_ - (en('s2') - .2)) / .05, 0, 1) * np.clip((st('s3') - .08 - t_) / .02, 0, 1) * .97
eq = lambda x: x - .5 * lp(x, 90, 2) + .4 * bp(x, 300, 3200, 1)
musL = eq(hp((ML + DL) * duck * mute, 38)); musR = eq(hp((MR + DR) * duck * mute, 38))
fxL, fxR = eq(hp(XL, 38)), eq(hp(XR, 38))
vp = os.path.join(HERE, 'voice', 'voice.wav'); VO = np.zeros(N)
if os.path.exists(vp):
    vo, _ = sf.read(vp); VO[:min(N, len(vo))] = vo[:N]
    ve = np.sqrt(np.convolve(VO ** 2, np.ones(int(.05 * SR)) / int(.05 * SR), 'same'))
    act = np.clip(ve / (.12 * ve.max()), 0, 1); act = maximum_filter1d(act, int(.25 * SR))
    act = np.convolve(act, np.ones(int(.06 * SR)) / int(.06 * SR), 'same')
    musL, musR = musL * (1 - .6 * act), musR * (1 - .6 * act); fxL, fxR = fxL * (1 - .3 * act), fxR * (1 - .3 * act)
    on = act > .5
    gv = np.sqrt(np.mean(((musL + musR) / 2)[on] ** 2)) * 10 ** (9 / 20) / np.sqrt(np.mean(VO[on] ** 2))
else:
    gv = 0; print('POZOR: chybí voice/voice.wav – jen podkres (náhled)')
L_ = musL + fxL + VO * gv; R_ = musR + fxR + VO * gv
fade = np.clip(t_ / .01, 0, 1) * np.clip((DUR - t_) / .6, 0, 1); L_ *= fade; R_ *= fade
PRE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.45
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = L_ / pk * PRE, R_ / pk * PRE
CEIL = .76; W = int(.004 * SR)
need = np.minimum(1, CEIL / np.maximum(np.maximum(np.abs(L_), np.abs(R_)), 1e-9))
g1 = minimum_filter1d(need, 2 * W + 1); g = np.empty(N); cur = 1.0; rel = 1 / (.12 * SR)
for i, v in enumerate(g1): cur = min(v, cur + (1 - cur) * rel * 5); g[i] = cur
g = np.convolve(g, np.ones(W) / W, 'same'); L_, R_ = L_ * g, R_ * g
out = sys.argv[1] if len(sys.argv) > 1 else 'jobs.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L_, R_], 1) * 32767).astype(np.int16).tobytes())
m = (L_ + R_) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(int(DUR))))
