"""POSTAVILI TO #01 – Steve Jobs: hudba, zvuky a hlas. Časy z timeline.json (voice/timeline.py), stejné jako v reel.html.
Dokumentární podkres v d moll / F dur, 92 BPM (úvod s tepem, mládí s klavírem, Apple groove, ticho po vyhazovu,
nadějný puls NeXT/Pixar, VHS krize 1997, drop po iPhonu, klavír u smrti, smyčce u citátu, rozřešení Stay hungry).
Zvuky k animacím (retro verze): fx.json = události z reel.html (export_ev.py) – kliknutí myši, 8bit blipy oken
a dialogů, „zoom“ při otevírání oken, pípnutí dialogu, duhové přechody, pixelové rozpuštění, VHS šum, psaní na
klávesnici, vrata garáže, počítadla, konfety. Hudba uhýbá hlasu (~−8 dB), hlas ~9 dB nad hudbou.
Bez voice/voice.wav vznikne jen podkres (náhled).
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
B = 60 / 92; ST = B / 4
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

# ---------------------------------------------------------------- A: úvod a odhalení jména
drone(0, st('s3') + .3, [38, 45, 50], .14)
t = 0.0
while t < st('s2') - .3: heartbeat(t, .35 + .25 * t / max(1, st('s2'))); t += .75
th = ck('s1', 1) + .1; impact(th, .75, 1.2, .15); glitch(th + .02, .22, .1)            # dialog VYHOZEN.
rev(st('s2') - .03, .7, .2)
impact(st('s2') - .03, .42, 1.4, .25)                                                  # duhový pás + jméno
pad(st('s2'), CH['Dm'] + [74], st('s3') - st('s2') + .6, .08, a=.05, r=.5, fc=2400)
bell(st('s2') + .05, 74, .06); bell(st('s2') + .35, 81, .04)

# ---------------------------------------------------------------- B: mládí (Reed, kaligrafie, písma)
def youth(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.3, r=.3, fc=1500); arp(at, ch, d, .055, 12, 3200)
    piano(at, BS[ch] + 12, .09, min(d + .3, 2.6))
bars(st('s3') - .06, st('s6') - .06, ['Dm', 'Bb', 'F', 'C'], youth)

# ---------------------------------------------------------------- C: Apple (garáž, dvě miliardy)
def apple(at, ch, d, k):
    pad(at, CH[ch] + [CH[ch][0] + 12], d + .05, .07, a=.08, r=.2, fc=2800); arp(at, ch, d, .07, 12, 4200)
    groove(at, ch, d, k, light=k == 0)
bars(st('s6') - .06, st('s8') - .06, ['F', 'C', 'Dm', 'Bb'], apple)
impact(st('s6') - .06, .35, .6, .08)
riser(st('s8') - .03, 1.2, .1, 200, 2200)

# ---------------------------------------------------------------- D: vyhazov, „Nevzdal to.“
tf = ck('s8', 1) + .04; impact(tf, 1.0, 1.8, .25)
for n in (50, 57, 62): piano(st('s9') - .02, n, .1, 2.6)

# ---------------------------------------------------------------- E: NeXT, Pixar, Toy Story
def hope(at, ch, d, k):
    pad(at, CH[ch], d + .05, .07, a=.15, r=.2, fc=2600); arp(at, ch, d, .065, 12, 3800)
    groove(at, ch, d, k, light=True, kick_g=.6)
bars(st('s10') - .06, st('s12') - .06, ['F', 'C', 'Dm', 'Bb'], hope)
impact(st('s10') - .06, .4, .9, .12)                                                   # restart (bílý záblesk)
projector(st('s11') - .06, st('s12') - st('s11'), .07)

# ---------------------------------------------------------------- F: 1997 a Michael Dell
c0, c1 = st('s12') - .06, st('s14') - .06
vhs(c0, c1 - c0, .05)
drone(c0, c1 - c0, [26, 27, 38], .15)                              # rozladěné basy (D1, Eb1)
for o in (.3, 1.1, 1.9): glitch(c0 + o, .15, .07)
whoosh(c0 + .5, 1.6, .12, 3000, 200, .2)
strings(st('s13') - .06, [38, 45, 51], c1 - st('s13') + .3, .085, a=1.0, r=.3, fc=1200)

# ---------------------------------------------------------------- G: iMac, iPod, iPhone, #1
for i, tt in enumerate([ck('s14', 1), st('s15') - .02, st('s16') - .02]):
    impact(tt, .5 + .1 * i, .7, .12); ch = ['F', 'C', 'Dm'][i]
    for n in CH[ch]: pluck(tt, n + 12, .1, .6, 0, 5000, .25)
    bell(tt, CH[ch][0] + 24, .05)
rev(st('s17') - .05, .6, .2)
def top(at, ch, d, k):
    pad(at, CH[ch] + [CH[ch][0] + 12], d + .05, .1, a=.05, r=.3, fc=3600); arp(at, ch, d, .08, 24, 6000)
    groove(at, ch, d, k)
    for s16 in range(1, 16, 2):
        if s16 * ST < d - .05: hat(at + s16 * ST, .05, pan=.3)
bars(st('s17') - .06, st('s18') - .06, ['F', 'C', 'Dm', 'Bb'], top)
t1h = ck('s17', 2); bell(t1h, 81, .07); bell(t1h + .3, 84, .05)

# ---------------------------------------------------------------- H: smrt, citát
for o, n in ((0, 62), (.9, 65), (1.8, 69), (2.7, 74)): piano(st('s18') - .06 + o, n, .09, 3.2)
piano(st('s18') - .06, 38, .08, 4)
def warm(at, ch, d, k):
    strings(at, CH[ch], d + .4, .07, a=.8, r=.6, fc=2200); piano(at, CH[ch][0], .07, 2.6); piano(at, CH[ch][2] + 12, .05, 2.6)
bars(st('s19') - .06, st('s20') - .06, ['F', 'C', 'Dm', 'Bb'], warm)

# ---------------------------------------------------------------- I: Stay hungry. Stay foolish.
for tt, ch in ((st('s20') - .06, 'F'), (st('s21') - .06, 'C')):
    rev(tt, .5, .12); strings(tt, CH[ch] + [CH[ch][0] + 12], 1.6, .09, a=.1, r=.8, fc=2600)
    for n in CH[ch]: piano(tt, n, .07, 2.4)
    bell(tt + .05, CH[ch][0] + 24, .05)

# ---------------------------------------------------------------- J: další díl a výzva
def outro(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.1, r=.3, fc=2000); arp(at, ch, d, .05, 12, 3000)
    groove(at, ch, d, k, light=True, kick_g=.45)
bars(st('s22') - .06, DUR, ['F', 'C', 'Dm', 'Bb'], outro)

# ---------------------------------------------------------------- K: zvuky k animacím (fx.json z reel.html)
FX = json.load(open(os.path.join(HERE, 'fx.json')))['events']
def P(e, i, d): return e[i] if len(e) > i else d
for e in FX:
    at, ty = e[0], e[1]
    if ty in ('inv', 'shk'): continue                                # jen obraz
    elif ty == 'click': mouse(at, .24)
    elif ty == 'tick': tick(at, .07)
    elif ty == 'blip': blip(at, P(e, 2, 0), .1)
    elif ty == 'pop': pop(at, 950, .15)
    elif ty == 'pop2': pop2(at, .13)
    elif ty == 'zoom': glide(at, 320, 1250, .13, .045)
    elif ty == 'zoomout': glide(at, 1150, 300, .13, .045)
    elif ty == 'alert': alert(at, .15)
    elif ty == 'alert2': alert(at, .17, lo=True)
    elif ty == 'slam': impact(at, P(e, 2, .4), .8, .1)
    elif ty == 'stamp': stamp(at, P(e, 2, .4))
    elif ty == 'glitch': glitch(at, P(e, 2, .3), .14)
    elif ty == 'swish': swish(at, .13)
    elif ty == 'swoosh': whoosh(at + .12, .36, .14, 500, 5500, .4)
    elif ty == 'wipe': whoosh(at + .2, .42, .17, 300, 5200, .5); whoosh(at + .44, .3, .1, 5200, 900, .3)
    elif ty == 'hit': impact(at, .22, .45, .05)
    elif ty == 'thunk': thunk(at, P(e, 2, 1))
    elif ty == 'roll': roll(at, P(e, 2, .8), .13)
    elif ty == 'type': typerun(at, P(e, 2, .5))
    elif ty == 'pen': pen(at, P(e, 2, 1.0), .15)
    elif ty == 'drip': drip(at)
    elif ty == 'dis': crush(at, .32, .13)
    elif ty == 'static': staticb(at, .26, .14)
    elif ty == 'rew': rewind(at)
    elif ty == 'rip': rip(at, .25)
    elif ty == 'sparkle': sparkle(at)
    elif ty == 'shimmer': shimmer(at)
    elif ty == 'coin': coin(at, .1)
    elif ty == 'count': ticks_eo(at, P(e, 2, .7))
    elif ty == 'race': ticks_eo(at, P(e, 2, 1.2), 30, .045, 1800)
    elif ty == 'blips': blips(at, P(e, 2, .5))
    elif ty == 'flip': paper(at, .2)
    elif ty == 'load': chatter(at, P(e, 2, .8))
    elif ty == 'coins': coinrain(at)
    elif ty == 'power': power(at)
    elif ty == 'ding': ding(at, .12)
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
for at in (th, tf, ck('s14', 1), t1h):
    duck *= 1 - .35 * np.clip((t_ - at) / .01, 0, 1) * np.clip((at + .35 - t_) / .3, 0, 1)
# ticho po vyhazovu (do „Nevzdal to.“) a jen klavír po smrti
mute = 1 - np.clip((t_ - (st('s8') - .1)) / .05, 0, 1) * np.clip((st('s9') - .1 - t_) / .03, 0, 1) * .97
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
PRE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.8
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
