"""JEDNA VĚTA #01 – Kalkulačka porad: hudba, zvuky a hlas. Časy z timeline.json (voice/timeline.py) a fx.json (export_ev.py),
stejné jako v reel.html. Svižný elektronický podkres v F dur, 116 BPM.
Háček: úder a basa na první snímek, „slam“ na Hotová aplikace. Zadání: lehký groove, klávesnice synchronně se psaním.
Stavba: plný groove, šestnáctinové arpeggio, „datový“ šum psaní kódu, zvonek na Hotovo, spuštění. Bez řádku: pauza
v bicích, odpočet, razítko na nulu. Ukázka: lehký groove a ťuknutí. Start: náboj, oheň (praskání) a plný groove;
zrychlená hodina: náběh, zrychlující se cinkání mincí a pokladna na konci. Výzva: lehký outro groove a závěrečný akord.
Hudba uhýbá hlasu (~−8 dB), hlas ~9 dB nad hudbou.
usage: python3 sfx.py out.wav [PRE]"""
import sys, wave, json, os
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt, sawtooth
from scipy.ndimage import maximum_filter1d, minimum_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, 'timeline.json'))); S = TL['S']
CK = {}
for sid, i, txt, a, b in TL['chunks']: CK.setdefault(sid, {})[i] = (a, b)
st = lambda s: S[s][0]; en = lambda s: S[s][1]; ck = lambda s, i: CK[s][i][0]
APP = json.loads(open(os.path.join(HERE, 'app_data.js'), encoding='utf-8').read()[len('window.APP='):].rstrip().rstrip(';'))
SR = 48000; DUR = TL['END']; N = int(DUR * SR)
rng = np.random.default_rng(116)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)
B = 60 / 116; ST = B / 4
K_PAD, K_ARP, K_808, K_KICK = 2.6, 2.8, .32, .7

# hranice scén – stejné vzorce jako v reel.html
HOOK_END, PROMPT_END, BUILD_END = st('s3') - .06, st('s5') - .06, st('s6') - .06
ZERO_END, DEMO_END, SHARE_END = st('s7') - .06, st('s10') - .06, st('s11') - .06
GO, FF0, FF1, V0 = APP['go'], APP['ff0'], APP['ff1'], APP['v0']


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


# ---------------------------------------------------------------- nástroje (knihovna z Postavili to #01/#02)
def kick(at, g=1.0, f0=170, f1=54, dec=.22):
    d = .7; t = T(d); f = f1 + (f0 - f1) * np.exp(-t / .028)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, dec) + bp(noise(d), 2500, 7000) * env(d, .0004, .005) * .6
    put(D, Dw, np.tanh(s * 1.4), at, g * K_KICK, 0, .04)
def clap(at, g=1.0, pan=0.0):
    d = .35; s = np.zeros(int(d * SR))
    for k, o in enumerate([0, .009, .019, .028]):
        i = int(o * SR); n = bp(noise(d), 900, 4200) * env(d, .0005, .011 if k < 3 else .085); s[i:] += n[:len(s) - i]
    put(D, Dw, s, at, g, pan, .4)
def hat(at, g=1.0, open_=False, pan=.22):
    d = .45 if open_ else .08; put(D, Dw, hp(noise(d), 7500) * env(d, .0005, .13 if open_ else .016), at, g, pan, .08)
def shaker(at, g=.05, pan=-.25):
    d = .09; put(D, Dw, bp(noise(d), 5000, 11000) * env(d, .012, .03), at, g, pan, .05)
def b808(at, note, d, g=1.0, glide=0.0):
    t = T(d); f = hz(note) * 2 ** (glide / 12 * np.exp(-t / .07))
    s = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 4.0) / np.tanh(4.0)
    e = np.minimum(1, t / .004) * np.exp(-t / max(d * .7, .25)) * np.clip((d - t) / .05, 0, 1)
    put(D, Dw, lp(s * e, 1400), at, g * K_808, 0, 0)
def pad(at, notes, d, g=1.0, a=.5, r=.7, fc=1600, pan=.0):
    t = T(d); s = np.zeros_like(t)
    for n in notes:
        for det in (-.09, 0, .09):
            s += sawtooth(2 * np.pi * hz(n + det) * t + rng.uniform(0, 2 * np.pi)) * (.5 if det else .7)
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
def impact(at, g=1.0, dec=1.4, crash=.15):
    d = 3.2; t = T(d); f = 29 + 95 * np.exp(-t / .05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, dec * .5)
    s = s * .6 + lp(noise(d), 3200) * env(d, .001, .11) * .9 + hp(noise(d), 4500) * env(d, .002, .7) * crash
    put(X, Xw, hp(np.tanh(s * 1.6), 35), at, g, 0, .55)
def stamp(at, g=1.0):
    d = 1.2; t = T(d); f = 42 + 70 * np.exp(-t / .03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .18) + lp(noise(d), 1800) * env(d, .001, .05) * 1.2
    put(X, Xw, np.tanh(s * 1.8), at, g, 0, .35)
def riser(at_end, d=1.8, g=.25, f0=180, f1=1500):
    t = T(d); x = t / d; f = f0 * (f1 / f0) ** x
    s = sawtooth(2 * np.pi * np.cumsum(f) / SR) * .25 + np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * .25 + hp(noise(d), 1500) * .5
    put(X, Xw, lp(s, 7000) * x ** 2.2 * np.clip((d - t) / .015, 0, 1), at_end - d, g, 0, .5)
def whoosh(at, d=.35, g=.2, f0=500, f1=6000, peak=.6):
    t = T(d); x = t / d; e = np.where(x < peak, (x / peak) ** 2, np.exp(-(x - peak) / (1 - peak) * 3))
    put(X, Xw, bp(noise(d), min(f0, f1), max(f0, f1)) * e, at - d * peak, g, 0, .4)
def click(at, g=.2, pan=0.0):
    d = .03; t = T(d); s = bp(noise(d), 2000, 8000) * env(d, .0003, .004) + np.sin(2 * np.pi * 1700 * t) * env(d, .0004, .003) * .3
    put(X, Xw, s, at, g, pan, .05)
def ding(at, g=.12):
    for n, o in [(88, 0), (84, .09)]:
        d = .5; t = T(d); put(X, Xw, np.sin(2 * np.pi * hz(n) * t) * env(d, .002, .12), at + o, g, 0, .4)
def tick(at, g=.1, f=2600):
    d = .025; t = T(d)
    put(X, Xw, bp(noise(d), 2000, 8000) * env(d, .0002, .003) + np.sin(2 * np.pi * f * t) * env(d, .0002, .004) * .4, at, g, 0, .05)
def pop(at, f=900, g=.2):
    d = .12; t = T(d); fr = f * (1 + .7 * np.exp(-t / .012))
    put(X, Xw, np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(d, .001, .03), at, g, 0, .3)
def swish(at, g=.12):
    d = .12; t = T(d); put(X, Xw, bp(noise(d), 1800, 6000) * np.sin(np.pi * t / d) ** 2, at, g, .1, .1)
def power(at, g=.14):
    d = .26; t = T(d); f = 90 * (2200 / 90) ** (t / d) ** 1.4
    s = (np.sin(2 * np.pi * np.cumsum(f) / SR) * .6 + hp(noise(d), 2500) * .3) * (t / d) ** 2
    put(X, Xw, s * np.clip((d - t) / .01, 0, 1), at, g, 0, .4)
def notif(at, g=.12):
    for o, n in ((0, 88), (.09, 95)):
        d = .35; t = T(d); put(X, Xw, (np.sin(2 * np.pi * hz(n) * t) + .3 * np.sin(4 * np.pi * hz(n) * t)) * env(d, .002, .08), at + o, g, .1, .3)
def tap(at, k=0, g=.15):
    d = .08; t = T(d); put(X, Xw, bp(noise(d), 800, 4000) * env(d, .0005, .008) + np.sin(2 * np.pi * (180 + 30 * k) * t) * env(d, .001, .02) * .6, at, g, 0, .1)
def success(at, g=.07):
    for i, n in enumerate((72, 76, 79, 84)): bell(at + i * .06, n, g * (1 - i * .1), 1.8, (i - 1.5) * .2)
def thud(at, g=.35):
    d = .5; t = T(d); f = 90 * np.exp(-t / .12) + 40
    put(X, Xw, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .15) + lp(noise(d), 500) * env(d, .001, .03), at, g, 0, .2)
def ticks_eo(at, d, n=26, g=.05, f0=2400):
    for i in range(n): tick(at + d * (1 - (1 - i / n) ** (1 / 3)), g, f0 + 40 * i)

# ---------------------------------------------------------------- nové zvuky pro JEDNA VĚTA
def key(at, i=0, g=.11):
    """mechanická klávesa: cvaknutí + tlumené „ťuk“ (mezerník hlubší)"""
    r = np.random.default_rng(1000 + int(i)); sp = r.random() < .12
    d = .07; t = T(d); f = (95 if sp else 140) * r.uniform(.92, 1.08)
    s = bp(noise(d), 1800, 6500) * env(d, .0004, .006) * r.uniform(.7, 1) + np.sin(2 * np.pi * f * t) * env(d, .001, .018) * (.9 if sp else .55)
    put(X, Xw, s, at, g * r.uniform(.75, 1.05), r.uniform(-.2, .2), .06)
def datastream(at, d, g=.035):
    """psaní kódu ve zrychlení: hustý proud krátkých tónů a cvaknutí"""
    r = np.random.default_rng(42); t = at
    while t < at + d:
        x = (t - at) / d; f = r.choice([1320, 1480, 1760, 1980, 2220, 2640]) * (1 + .15 * x)
        dd = .022; tt = T(dd); s = np.sign(np.sin(2 * np.pi * f * tt)) * .4 * env(dd, .0005, .008)
        put(X, Xw, lp(s, 6000), t, g * r.uniform(.5, 1) * (.6 + .4 * np.sin(np.pi * x)), r.uniform(-.5, .5), .1)
        if r.random() < .55: click(t + .01, .05 * r.uniform(.6, 1), r.uniform(-.3, .3))
        t += 1 / 26 + r.uniform(-.006, .006)
def crackle(at, d, g=.09):
    """oheň: náhodné praskání + tiché dunění"""
    r = np.random.default_rng(9); n = int(d * SR); s = np.zeros(n); k = 0.0
    while True:
        k += r.exponential(1 / 34)
        if k >= d - .05: break
        L = int(r.uniform(.002, .012) * SR); i = int(k * SR); a = r.uniform(.2, 1) ** 2
        s[i:i + L] += r.standard_normal(min(L, n - i)) * a * np.exp(-np.arange(min(L, n - i)) / (L / 3))
    s = bp(s, 900, 7500) * 1.1 + lp(noise(d), 260) * .35 * (1 + .3 * np.sin(2 * np.pi * .9 * T(d)))
    tt = T(d); s *= np.clip(tt / .5, 0, 1) * np.clip((d - tt) / .4, 0, 1)
    put(X, Xw, s, at, g, .1, .25)
def coinrun(at, d, g=.05):
    """mince zrychlující se během zrychlené hodiny"""
    r = np.random.default_rng(3); t = at
    while t < at + d:
        x = (t - at) / d; bell(t, int(r.choice([91, 93, 96, 98, 100])), g * (.5 + .5 * x) * r.uniform(.6, 1), .45, r.uniform(-.6, .6))
        t += lerp(.24, .035, x ** .7)
def tape(at, d, g=.06):
    """„převíjení“ – tón zrychluje, jako by se pouštěla páska rychleji"""
    t = T(d); x = t / d; f = 220 * (1760 / 220) ** (x ** 1.3)
    s = sawtooth(2 * np.pi * np.cumsum(f) / SR) * .3 + np.sin(2 * np.pi * np.cumsum(f * .5) / SR) * .4
    put(X, Xw, lp(s, 3500) * np.clip(t / .3, 0, 1) * np.clip((d - t) / .05, 0, 1) * (.4 + .6 * x), at, g, 0, .3)
def cash(at, g=.12):
    """pokladna: cvaknutí šuplíku + zvonek"""
    d = .25; put(X, Xw, bp(noise(d), 600, 3500) * env(d, .001, .04) + lp(noise(d), 400) * env(d, .001, .06), at, g * 1.2, 0, .2)
    for i, (n, o) in enumerate([(96, .06), (100, .1), (103, .13)]): bell(at + o, n, g * (.9 - .15 * i), 1.4, (i - 1) * .3)
    ding(at + .05, g * .7)
def lerp(a, b, p): return a + (b - a) * p

# ---------------------------------------------------------------- akordy (F dur)
CH = dict(F=[53, 57, 60], C=[52, 55, 60], Dm=[50, 53, 57], Bb=[50, 53, 58], Am=[52, 57, 60], Gm=[50, 55, 58])
BS = dict(F=41, C=36, Dm=38, Bb=34, Am=33, Gm=31)
def bars(t0, t1, prog, fn):
    k = 0; t = t0
    while t < t1 - .05:
        fn(t, prog[k % len(prog)], min(4 * B, t1 - t), k); t += 4 * B; k += 1
def arp(at, ch, d, g=.07, oct_=12, fc=3800, step=None):
    step = step or B / 2; notes = CH[ch] + [CH[ch][0] + 12]; pat = [0, 1, 2, 3, 2, 1, 2, 3]
    for i in range(int(d / step + 1e-6)): pluck(at + i * step, notes[pat[i % 8]] + oct_, g * (1 if i % 2 == 0 else .7) * K_ARP, .45, (i % 3 - 1) * .3, fc, .16)
def groove(at, ch, d, k, light=False, kick_g=.75, four=False):
    ks = [0, 4, 8, 12] if four else ([0, 6, 10] if not light else [0, 8])
    for s16 in ks:
        if s16 * ST < d - .05: kick(at + s16 * ST, kick_g if s16 == 0 else kick_g * .82); b808(at + s16 * ST, BS[ch], min(4 * ST * (4 if four else 2), d - s16 * ST), .45)
    if not light:
        for s16 in (4, 12):
            if s16 * ST < d - .05: clap(at + s16 * ST, .24)
    for s16 in range(0, 16, 2):
        if s16 * ST < d - .05: hat(at + s16 * ST, .065 if s16 % 4 else .085)
    for s16 in range(1, 16, 2):
        if s16 * ST < d - .05: shaker(at + s16 * ST, .035)

# A: háček – akord, basa, třpyt
pad(0, CH['F'] + [65], HOOK_END + .3, .07, a=.02, r=.4, fc=2400)
b808(0, BS['F'], 1.6, .9)
for i, n in enumerate((77, 81, 84, 89)): bell(.02 + i * .05, n, .045 * (1 - i * .12), 1.5, (i - 1.5) * .25)
arp(st('s2') - .02, 'F', HOOK_END - st('s2') + .02, .05, 12, 4200, B / 4)
riser(HOOK_END, .9, .12, 300, 2400)

# B: zadání – lehký groove, „přemýšlivé“ arpeggio
def think(at, ch, d, k):
    pad(at, CH[ch], d + .05, .045, a=.25, r=.3, fc=1500)
    arp(at, ch, d, .035, 12, 3000, B)
    groove(at, ch, d, k, light=True, kick_g=.4)
bars(HOOK_END, PROMPT_END, ['F', 'C', 'Dm', 'Bb'], think)

# C: stavba – plný groove, šestnáctinové arpeggio
def build(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.05, r=.2, fc=2200)
    arp(at, ch, d, .045, 12, 4500, B / 4)
    groove(at, ch, d, k, kick_g=.7, four=True)
bars(PROMPT_END, BUILD_END, ['Dm', 'Bb', 'F', 'C'], build)

# D: bez řádku od nás – pauza v bicích
pad(BUILD_END, CH['Bb'] + [65], ZERO_END - BUILD_END + .1, .06, a=.08, r=.3, fc=1800)
b808(BUILD_END, BS['Bb'], ZERO_END - BUILD_END, .6)

# E: ukázka – lehký groove
def demo(at, ch, d, k):
    pad(at, CH[ch], d + .05, .04, a=.1, r=.3, fc=1700)
    arp(at, ch, d, .04, 12, 3400, B / 2)
    groove(at, ch, d, k, light=True, kick_g=.5)
bars(ZERO_END, GO, ['F', 'C', 'Dm', 'Bb'], demo)

# F: start → hoří → zrychlená hodina → výsledek; pak výzva ke sdílení
def burn(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.05, r=.2, fc=2300)
    arp(at, ch, d, .05, 12, 4800, B / 4)
    groove(at, ch, d, k, kick_g=.72, four=True)
bars(GO, SHARE_END, ['Dm', 'Bb', 'F', 'C'], burn)

# G: výzva – outro a závěrečný akord
def outro(at, ch, d, k):
    pad(at, CH[ch], d + .05, .05, a=.1, r=.3, fc=2000); arp(at, ch, d, .04, 12, 3200, B / 2)
    if at < DUR - 1.6: groove(at, ch, d, k, light=True, kick_g=.45)
bars(SHARE_END, DUR - 1.4, ['F', 'C', 'Bb', 'F'], outro)
pad(DUR - 1.45, CH['F'] + [65, 69], 1.45, .07, a=.05, r=.8, fc=2200)
for i, n in enumerate((65, 69, 72, 77)): bell(DUR - 1.45 + i * .07, n, .05 * (1 - i * .12), 1.6, (i - 1.5) * .25)

# ---------------------------------------------------------------- K: zvuky k animacím (fx.json z reel.html)
FX = json.load(open(os.path.join(HERE, 'fx.json')))['events']
def P(e, i, d): return e[i] if len(e) > i else d
HITS = []
for e in FX:
    at, ty = e[0], e[1]
    if ty == 'hit':
        if at < .05: impact(at, .6, 1.4, .2); HITS.append(at)
        else: impact(at, .28, .6, .06)
    elif ty == 'slam': impact(at, .45, .8, .12); clap(at, .3); HITS.append(at)
    elif ty == 'slam2': impact(at, .3, .6, .08); clap(at, .22)
    elif ty == 'whoosh': whoosh(at + .1, .36, .15, 500, 6000, .45)
    elif ty == 'pop': pop(at, 900 + 110 * P(e, 2, 0), .13)
    elif ty == 'key': key(at, P(e, 2, 0))
    elif ty == 'send': tap(at, 2, .2); whoosh(at + .12, .3, .12, 700, 6500, .4); pop(at + .02, 1300, .1)
    elif ty == 'dark': thud(at, .35); impact(at, .22, .5, .04)
    elif ty == 'code': datastream(at, P(e, 2, 2.5))
    elif ty == 'success': success(at, .085); HITS.append(at)
    elif ty == 'launch': power(at - .2, .12); pop(at, 1000, .14); pop(at + .07, 1450, .11); whoosh(at + .1, .3, .1, 800, 6000, .4)
    elif ty == 'count': ticks_eo(at, P(e, 2, .85), 26, .045)
    elif ty == 'stamp': stamp(at, .5); impact(at, .25, .5, .05); HITS.append(at)
    elif ty == 'tap': tap(at, P(e, 2, 0), .2); click(at + .005, .08)
    elif ty == 'power': power(at, .15); thud(at + .12, .3); HITS.append(at)
    elif ty == 'fire': crackle(at, P(e, 2, 5), .08)
    elif ty == 'ff':
        d = P(e, 2, 3); riser(at + d, d, .2, 160, 2600); tape(at, d, .05); coinrun(at + .1, d - .15, .045)
    elif ty == 'cash': cash(at, .12); impact(at, .35, .9, .14); HITS.append(at)
    elif ty == 'plane': whoosh(at + .35, .8, .17, 350, 7000, .45)
    elif ty == 'notif': notif(at)
    elif ty == 'flash': swish(at, .08)
    else: print('POZOR: neznámá událost', ty)

# ---------------------------------------------------------------- mix
def ir(seed, d=2.2, tau=.55):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 6500); x[:int(.018 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
IRL, IRR = ir(1), ir(2)
t_ = np.arange(N) / SR
wet = lambda b, g: (fftconvolve(b.L, IRL)[:N] * g, fftconvolve(b.R, IRR)[:N] * g)
mL, mR = wet(Mw, .55); dL, dR = wet(Dw, .4); xL, xR = wet(Xw, .8)
ML, MR = M.L + mL, M.R + mR; ML, MR = ML + .5 * bp(ML, 1200, 5000), MR + .5 * bp(MR, 1200, 5000)
DL, DR = D.L + dL, D.R + dR; XL, XR = X.L + xL, X.R + xR
duck = np.ones(N)
for at in HITS:
    duck *= 1 - .35 * np.clip((t_ - at) / .01, 0, 1) * np.clip((at + .35 - t_) / .3, 0, 1)
eq = lambda x: x - .5 * lp(x, 90, 2) + .4 * bp(x, 300, 3200, 1)
musL = eq(hp((ML + DL) * duck, 38)); musR = eq(hp((MR + DR) * duck, 38))
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
PRE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.32
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = L_ / pk * PRE, R_ / pk * PRE
CEIL = .76; W = int(.004 * SR)
need = np.minimum(1, CEIL / np.maximum(np.maximum(np.abs(L_), np.abs(R_)), 1e-9))
g1 = minimum_filter1d(need, 2 * W + 1); g = np.empty(N); cur = 1.0; rel = 1 / (.12 * SR)
for i, v in enumerate(g1): cur = min(v, cur + (1 - cur) * rel * 5); g[i] = cur
g = np.convolve(g, np.ones(W) / W, 'same'); L_, R_ = L_ * g, R_ * g
out = sys.argv[1] if len(sys.argv) > 1 else 'audio.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L_, R_], 1) * 32767).astype(np.int16).tobytes())
m = (L_ + R_) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(int(DUR))))
