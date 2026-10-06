"""Manifest „Postav si to.“ – hudba a zvuky (42,6 s), časy podle reel.html (S, ERR_T, TYPED).
100 BPM (doba 0,6 s). Úvod: temný dron a tikání, „Byli / sakra“ dva údery, „NAŠTVANÍ.“ velký úder s glitchem.
Příběhy (4,2–18,6): trap groove v a moll (Am–F–Dm–E–Am–F), na každé jméno firmy úder, UI zvuky (klikání myší,
chybová hlášení, tiskárna účtenek, rychle tikající hodiny). Zlom (18,6–22,2): jen piano, náběh do „DOST.“, kde
všechno ztichne kromě úderu s dozvukem. „Postavím si to sám.“ = C dur, pak světlejší groove (F–G–Am–F–G), krátká
pauza na „Ale upřímně?“, údery na profese, gradace s vířením a ukazatelem „Stavím…“, drop na „TEĎ.“ (C dur),
psaní komentáře a podpis. Konec doznívá do ticha (smyčka začne znovu tichým úvodem).
usage: python3 sfx.py out.wav"""
import sys, wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt, sawtooth

SR = 48000; DUR = 42.6; N = int(DUR * SR)
rng = np.random.default_rng(42)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)
B = .6; ST = B / 4                                    # doba a šestnáctina
# mix pro reproduktory telefonů: subbasy dolů, středy (akordy, piano, arpeggio) nahoru
K_PAD, K_ARP, K_PIANO, K_808, K_KICK, K_DRONE = 3.4, 3.4, 2.0, .32, .7, .4


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, at, g=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


M, Mw, D, Dw, X, Xw = Bus(), Bus(), Bus(), Bus(), Bus(), Bus()   # hudba (tóny), bicí, efekty + jejich dozvuky
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

# časy scén (stejné jako S v reel.html)
S = dict(H1=0.0, H2=1.2, H3=2.4, H4=3.0, A1=4.2, A2=6.0, A3=7.2, B1=8.4, B2=10.2, B3=11.4, C1=12.6, C2=14.4, C3=16.8,
         P1=18.6, P2=19.8, P3=21.0, P4=21.6, P5=22.2, P6=23.4, V1=25.2, V2=27.6, V3=28.2, Y1=30.0, Y2=30.9, Y3=31.5,
         Y4=32.1, Y5=32.7, Y6=33.6, Y7=34.8, Y8=36.0, Y9=37.2, E1=38.4, E2=40.2)
ERR_T = [.06 + i * .085 for i in range(10)]
TYPED = 'přepisování faktur do Excelu 😤'; TY0, TYC = .35, 19


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

# ---------------------------------------------------------------- akordy (MIDI) a basové tóny
CH = dict(Am=[57, 60, 64], F=[53, 57, 60], Dm=[50, 53, 57], E=[52, 56, 59], C=[48, 52, 55, 60], G=[55, 59, 62])
BS = dict(Am=33, F=29, Dm=38, E=40, C=36, G=31)
ARP = [0, 1, 2, 3, 2, 1, 2, 3]
def arp(at, ch, g=.1, oct_=12, fc=2600, dec=.17, steps=8):
    notes = CH[ch] + [CH[ch][0] + 12]
    for k in range(steps):
        pluck(at + k * 2 * ST, notes[ARP[k % 8]] + oct_, g * K_ARP * (1 if k % 2 == 0 else .75), .5, (k % 3 - 1) * .3, fc, dec)

# ---------------------------------------------------------------- 0–4,2 úvod
drone(0, 4.3, [33, 45, 52], .12)                                 # A1 A2 E3
pad(0, [45, 48, 52], 4.2, .045, a=1.5, r=.3, fc=900)
for k in range(4): tick(k * B, .08 + .02 * k, 2200)               # tikání (napětí)
piano(0, 45, .17, 3.0); piano(0, 57, .09, 3.0); piano(1.2, 52, .11, 2.4); piano(1.2, 64, .06, 2.4)
paper(.0, .14); paper(1.2, .16, .1); whoosh(1.2, .25, .07, 3000, 600)
kick(S['H3'], .8); b808(S['H3'], 33, .3, .55)                    # „Byli“
kick(S['H3'] + .3, .9); b808(S['H3'] + .3, 33, .3, .6); clap(S['H3'] + .3, .25)   # „sakra“
rev(S['H4'], .6, .28)
impact(S['H4'], .95, 1.6, .2); b808(S['H4'], 33, 1.1, .75, 7)    # „NAŠTVANÍ.“
glitch(S['H4'] + .02, .4, .26)
riser(S['A1'], .8, .1, 300, 2400)

# ---------------------------------------------------------------- 4,2–18,6 příběhy: groove v a moll
PROG_A = ['Am', 'F', 'Dm', 'E', 'Am', 'F']
for bi, ch in enumerate(PROG_A):
    at = S['A1'] + bi * 4 * B
    pad(at, CH[ch], 4 * B + .05, .085, a=.08, r=.12, fc=2600)
    arp(at, ch, .085, 12, 4200, .15)
    kicks = [0, 6, 10] + ([14] if bi % 2 else [])
    for j, k in enumerate(kicks):
        nxt = (kicks + [16])[j + 1]
        kick(at + k * ST, .85 if k == 0 else .65)
        b808(at + k * ST, BS[ch], (nxt - k) * ST, .5 if k == 0 else .42, 5 if (k == 0 and bi in (2, 4)) else 0)
    for k in (4, 12): clap(at + k * ST, .32)
    for k in range(0, 16, 2): hat(at + k * ST, .09 if k % 4 else .12)
    if bi % 2: hat(at + 13 * ST, .07); hat(at + 15 * ST, .08)
    if bi == 5:
        for q in range(6): hat(at + 12 * ST + q * (4 * ST / 6), .06 + .01 * q)
# A – Canva
paper(S['A1'], .15); whoosh(S['A1'] + .3, .3, .06, 4000, 900)
for o in (.1, .2, .3): mouse(S['A2'] + o, .2)
mouse(S['A2'] + .62, .18); mouse(S['A2'] + .9, .18); ding(S['A2'] + .55, .1)
rev(S['A3'], .6, .22); impact(S['A3'], .7, 1.0, .14)
# B – Shopify
whoosh(S['B1'] + .25, .45, .14, 300, 2500); paper(S['B1'], .1)
for i, e in enumerate(ERR_T): bonk(S['B2'] + e, 380 + 25 * (i % 4), .13, (i % 5 - 2) * .15)
rev(S['B3'], .6, .22); impact(S['B3'], .7, 1.0, .14); whoosh(S['B3'] + .35, .3, .08, 600, 5000)
# C – Mews
printer(S['C1'] + .15, .5, .09); paper(S['C1'], .1)
for k in range(int(2.3 / .075)): tick(S['C2'] + k * .075, .045 + .02 * (k % 2), 2900)   # hodiny letí dvě hodiny
for i in range(9): paper(S['C2'] + i * .2 + .05, .12, (i % 3 - 1) * .3)
printer(S['C2'] + .3, .35, .07); printer(S['C2'] + 1.3, .35, .07)
rev(S['C3'], .6, .24); stamp(S['C3'], .9); impact(S['C3'], .45, .8, .1)

# ---------------------------------------------------------------- 18,6–23,4 zlom: piano, náběh, DOST
for o, ch in [(0, 'Am'), (1.2, 'F'), (2.4, 'Dm')]:
    for n in CH[ch]: piano(S['P1'] + o, n, .07, 2.2)
    piano(S['P1'] + o, BS[ch] + 12, .1, 2.2)
pad(S['P1'], [45, 52], 3.6, .03, a=.8, r=.4, fc=700)
for k in range(12): tick(S['P3'] + k * .045, .05 + .004 * k, 2400 + 40 * k)       # počítadlo dnů
riser(S['P5'] - .02, 2.2, .11, 150, 1800); rev(S['P5'] - .04, .6, .2, 1500)
impact(S['P5'], 1.0, 2.2, .3); b808(S['P5'], 28, 1.6, .7, 12)      # „DOST.“

# ---------------------------------------------------------------- 23,4–42,6 světlá část
pad(S['P6'], CH['C'] + [64], 1.85, .085, a=.25, r=.15, fc=2200)
for n in [36, 48, 55, 60, 64]: piano(S['P6'], n, .085, 2.4, bright=1.2)
bell(S['P6'] + .3, 76, .05); bell(S['P6'] + .9, 79, .04)
riser(S['V1'], 1.2, .08, 250, 2000)
PROG_B = [(25.2, 'F'), (27.6, 'G'), (30.0, 'Am'), (32.4, 'F'), (34.8, 'G'), (37.2, 'C'), (39.6, 'F'), (42.0, 'C')]
for at, ch in PROG_B:
    d = min(4 * B, DUR - at)
    drop = at >= 37.2
    pad(at, CH[ch] + [CH[ch][0] + 12], d + .05, .13 if drop else .11, a=.06, r=.15, fc=3800 if drop else 3000)
    if at != 42.0: arp(at, ch, .1 if drop else .1, 24 if drop else 12, 6000 if drop else 4800, .2)
    if at == 42.0: continue
    if at == 34.8:                                               # gradace
        for k in (0, 4, 8, 12): kick(at + k * ST, .7); b808(at + k * ST, BS[ch], 4 * ST, .38)
        continue
    kicks = [0, 6, 10] if drop else [0, 7, 10]
    for j, k in enumerate(kicks):
        nxt = (kicks + [16])[j + 1]; tt = at + k * ST
        if 27.6 <= tt < 28.2: continue                           # pauza na „Ale upřímně?“
        kick(tt, .85 if k == 0 else .7); b808(tt, BS[ch], (nxt - k) * ST, .5)
    for k in (4, 12):
        tt = at + k * ST
        if not (27.6 <= tt < 28.2): clap(tt, .36 if drop else .34)
    for k in range(0, 16, 1 if drop else 2):
        tt = at + k * ST
        if not (27.6 <= tt < 28.2): hat(tt, (.08 if k % 2 == 0 else .05) if drop else .09, pan=.25 if k % 2 else -.1)
# „Ale upřímně?“ – krátké nadechnutí (tape stop / vzduch)
whoosh(S['V2'] + .05, .4, .1, 3000, 400); rev(S['V3'], .5, .12)
# profese: údery na každý střih
for k, key in enumerate(['Y1', 'Y2', 'Y3', 'Y4']):
    at = S[key]; impact(at, .22 + .05 * k, .35, .05); clap(at, .25)
    for n in CH['Am'] if key in ('Y1', 'Y2', 'Y3') else CH['F']: pluck(at, n + 12, .07, .4, 0, 3500, .12)
whoosh(S['Y5'] + .28, .3, .1, 800, 6000)                         # škrtnutí „programovat“
# gradace 34,8–37,2: víření, náběh, ukazatel „Stavím…“
roll = [S['Y7'] + i * .3 for i in range(4)] + [S['Y7'] + 1.2 + i * .15 for i in range(6)] + [S['Y8'] + .3 + i * .075 for i in range(12)]
for i, tt in enumerate(roll): snare(tt, .12 + .2 * i / len(roll))
for k in range(16): kick(S['Y8'] + k * .075, .25 + .02 * k) if k % 2 == 0 else None
for k in range(20): tick(S['Y8'] + .15 + k * .05, .03 + .002 * k, 3000 + 60 * k)
riser(S['Y9'] - .05, 2.4, .14, 200, 3000); rev(S['Y9'] - .03, .8, .22)
# DROP „TEĎ.“
impact(S['Y9'], 1.0, 1.8, .35); b808(S['Y9'], 36, 1.2, .7, 12); hat(S['Y9'], .25, True)
LEAD = [(0, 72), (.3, 76), (.6, 79), (1.2, 81), (1.5, 79), (1.8, 76), (2.4, 77), (2.7, 76), (3.0, 72), (3.6, 74), (4.2, 72)]
for o, n in LEAD: bell(S['Y9'] + o, n, .07, 1.4, .1)
# CTA: psaní komentáře, odeslání, podpis
for i, ch in enumerate(TYPED):
    click(S['E2'] + TY0 + i / TYC, .12, (i % 3 - 1) * .1)
pop(S['E2'] + TY0 + len(TYPED) / TYC + .05, 1050, .16)
bell(S['E2'] + .5, 84, .05, 1.6); bell(S['E2'] + .53, 91, .03, 1.4)
pad(42.0, CH['C'] + [64], .6, .08, a=.02, r=.55, fc=1800)

# ---------------------------------------------------------------- mix
def ir(seed, d=1.8, tau=.45):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 6500); x[:int(.015 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
IRL, IRR = ir(1), ir(2)
t_ = np.arange(N) / SR
wet = lambda b, g: (fftconvolve(b.L, IRL)[:N] * g, fftconvolve(b.R, IRR)[:N] * g)
mL, mR = wet(Mw, .55); dL, dR = wet(Dw, .5); xL, xR = wet(Xw, .9)
ML, MR = M.L + mL, M.R + mR; ML, MR = ML + .5 * bp(ML, 1200, 5000), MR + .5 * bp(MR, 1200, 5000); DL, DR = D.L + dL, D.R + dR; XL, XR = X.L + xL, X.R + xR
# hudba uhne úderům; na „DOST.“ hudba úplně ztichne (zůstane jen úder a jeho dozvuk)
duck = np.ones(N)
for at in (S['H4'], S['A3'], S['B3'], S['C3'], S['Y9']):
    duck *= 1 - .35 * np.clip((t_ - at) / .01, 0, 1) * np.clip((at + .35 - t_) / .3, 0, 1)
mute = 1 - np.clip((t_ - (S['P5'] - .06)) / .05, 0, 1) * np.clip((S['P6'] - .02 - t_) / .02, 0, 1)
L_ = (ML + DL) * duck * mute + XL; R_ = (MR + DR) * duck * mute + XR
L_, R_ = hp(L_, 38), hp(R_, 38)                     # bez infrazvuku
eq = lambda x: x - .5 * lp(x, 90, 2) + .4 * bp(x, 300, 3200, 1)   # EQ pro telefon: −6 dB pod 90 Hz, středy +3 dB
L_, R_ = eq(L_), eq(R_)
fade = np.clip(t_ / .01, 0, 1) * np.clip((DUR - t_) / .5, 0, 1); L_ *= fade; R_ *= fade
# limiter s předstihem 4 ms (místo tvrdého tanh): zesílí celek na ~-14 LUFS, špičky drží pod -2,4 dBFS (true peak pod -1 dB)
from scipy.ndimage import maximum_filter1d, minimum_filter1d
PRE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.55
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = L_ / pk * PRE, R_ / pk * PRE
CEIL = .76; W = int(.004 * SR)
need = np.minimum(1, CEIL / np.maximum(np.maximum(np.abs(L_), np.abs(R_)), 1e-9))
g1 = minimum_filter1d(need, 2 * W + 1)              # zeslabení začne W vzorků před špičkou
g = np.empty(N); cur = 1.0; rel = 1 / (.12 * SR)
for i, v in enumerate(g1):                          # pozvolné uvolnění (~120 ms), nikdy nad g1
    cur = min(v, cur + (1 - cur) * rel * 5); g[i] = cur
g = np.convolve(g, np.ones(W) / W, 'same')          # plynulý nástup; průměr okna W zůstává pod potřebným ziskem
L_, R_ = L_ * g, R_ * g
out = sys.argv[1] if len(sys.argv) > 1 else 'manifest.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L_, R_], 1) * 32767).astype(np.int16).tobytes())
m = (L_ + R_) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(int(DUR))))
