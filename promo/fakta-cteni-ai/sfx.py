"""„Tohle přečetla AI.“ – zvuk (14,5 s), časy podle reel.html.
Lo-fi podkres (88 BPM, teplé akordy, měkký beat) hraje od prvního snímku, cvakání klávesnice přesně na psané znaky
(stejný rozvrh a jitter jako TYPE v reel.html), tikání počítadla jako u automatu, cink na 377 000 let,
basový úder na zvrat „dřív, než existoval člověk“, pop na výzvu ke sdílení. Konec navazuje na začátek (smyčka).
usage: python3 sfx.py out.wav"""
import sys, wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000; DUR = 14.5; N = int(DUR * SR)
rng = np.random.default_rng(31)
hz = lambda n: 440 * 2 ** ((n - 69) / 12)


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, at, g=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(N, i + len(sig)); seg = sig[:j - i] * g
        s.L[i:j] += seg * np.sqrt(.5 * (1 - pan)) * 1.414; s.R[i:j] += seg * np.sqrt(.5 * (1 + pan)) * 1.414


M, Mw, X, Xw = Bus(), Bus(), Bus(), Bus()
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


# ---------------------------------------------------------------- lo-fi podkres
BPM = 88; B = 60 / BPM
def kick(at, g=1.0):
    d = .5; t = T(d); f = 48 + 70 * np.exp(-t / .035)
    put(M, Mw, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .16), at, g, 0, .05)
def snap(at, g=1.0):
    d = .25; s = bp(noise(d), 1200, 6000) * env(d, .001, .045) + bp(noise(d), 300, 900) * env(d, .001, .02) * .5
    put(M, Mw, s, at, g, .1, .5)
def hat(at, g=1.0, pan=.25):
    d = .08; put(M, Mw, hp(noise(d), 7000) * env(d, .0005, .018), at, g, pan, .1)
def rhodes(at, n, g=1.0, d=2.6, pan=0.0):
    f = hz(n); t = T(d)
    s = (np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * t) * np.exp(-t / .5)) * np.exp(-t / 1.4)
         + .25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / .5))
    s *= np.minimum(1, t / .006) * np.clip((d - t) / .3, 0, 1) * (1 + .12 * np.sin(2 * np.pi * 4.5 * t))
    put(M, Mw, lp(s, 2600), at, g, pan, .7)
def bass(at, n, d, g=1.0):
    t = T(d); s = np.sin(2 * np.pi * hz(n) * t) + .15 * np.sin(2 * np.pi * 2 * hz(n) * t)
    put(M, Mw, lp(s * np.minimum(1, t / .01) * np.clip((d - t) / .08, 0, 1), 300), at, g, 0, 0)

CHORDS = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]   # Fmaj7 Em7 Dm7 Cmaj7
ROOTS = [41, 40, 38, 36]
bar = 4 * B; nb = int(np.ceil(DUR / bar)) + 1
for k in range(nb):
    at = k * bar; ch = CHORDS[k % 4]
    for i, n in enumerate(ch): rhodes(at + i * .018, n, .16 * (1 - .06 * i), 3.2, (i / 3 - .5) * .6)
    bass(at, ROOTS[k % 4], bar * .92, .42)
    for b in range(4):
        tb = at + b * B
        if b in (0, 2): kick(tb, .55 if b == 0 else .42)
        if b in (1, 3): snap(tb, .30)
        hat(tb + B / 2, .12); hat(tb, .07, -.2)
    kick(at + 3.5 * B, .28)
# vinylový šum
t_ = np.arange(N) / SR; crackle = hp(noise(DUR), 2500) * .004
pops = np.zeros(N); idx = rng.integers(0, N, 120); pops[idx] = rng.uniform(-.25, .25, 120); pops = lp(pops, 6000)
M.add(crackle + pops * .5, 0, 1.0)

# ---------------------------------------------------------------- klávesnice (stejný rozvrh jako reel.html)
TYPE = [('Llama 3 od Mety: přes 15 bilionů tokenů ≈ 11 bilionů slov.', 2.25, 40),
        ('Ty čteš 238 slov za minutu.', 3.95, 36),
        ('8 hodin denně, 5 dní v týdnu.', 4.9, 36),
        ('Četl bys:', 5.75, 30),
        ('Homo sapiens je na Zemi asi 300 000 let.', 7.95, 40),
        ('A to je jen jedna AI. 😅', 10.35, 30)]
jit = lambda i: .012 * np.sin(i * 12.9898 + .5)
def click(at, g=.2, space=False):
    d = .035; t = T(d)
    s = bp(noise(d), 1800 if not space else 900, 7000 if not space else 4000) * env(d, .0003, .006)
    s += np.sin(2 * np.pi * (1500 if not space else 700) * t) * env(d, .0005, .004) * .25
    put(X, Xw, s, at, g * rng.uniform(.75, 1.0), rng.uniform(-.15, .15), .05)
for txt, st, cps in TYPE:
    for i, ch in enumerate(txt):
        click(st + i / cps + jit(i), .17, space=ch in '  ')

# ---------------------------------------------------------------- efekty
def whoosh(at, d=.35, g=.2, f0=500, f1=6000, peak=.6):
    t = T(d); x = t / d; e = np.where(x < peak, (x / peak) ** 2, np.exp(-(x - peak) / (1 - peak) * 3))
    s = bp(noise(d), min(f0, f1), max(f0, f1)) * e
    put(X, Xw, s, at - d * peak, g, 0, .4)
def pop(at, f=900, g=.22):
    d = .12; t = T(d); fr = f * (1 + .7 * np.exp(-t / .012))
    put(X, Xw, np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(d, .001, .03), at, g, 0, .3)
def bell(at, f, g=1.0, d=1.6):
    t = T(d); s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (1.0 / r ** .5)) for r, a in [(1, 1), (2.0, .45), (2.76, .2), (5.4, .08)])
    put(X, Xw, s * np.minimum(1, t / .003), at, g, 0, .6)
def tick(at, g=.1, f=2400):
    d = .025; t = T(d)
    put(X, Xw, (bp(noise(d), 2000, 8000) * env(d, .0002, .003) + np.sin(2 * np.pi * f * t) * env(d, .0002, .004) * .4), at, g, 0, .05)
def boom(at, g=1.0):
    d = 2.2; t = T(d); f = 34 + 70 * np.exp(-t / .06)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .55) + lp(noise(d), 2000) * env(d, .001, .05) * .6
    put(X, Xw, s, at, g, 0, .45)

whoosh(2.1, .3, .10, 300, 3000)                     # klávesnice vyjede
# počítadlo jako automat: cvak při každé změně zobrazené hodnoty (po snímcích)
C0, C1 = 5.95, 7.65; prev = -1
for f in range(int(C0 * 30), int(C1 * 30) + 1):
    tt = f / 30; p = 1 - (1 - min(1, max(0, (tt - C0) / (C1 - C0)))) ** 3; v = round(377 * p)
    if v != prev: tick(tt, .07 + .05 * p, 2000 + 900 * p); prev = v
bell(7.65, hz(88), .12, 1.6); bell(7.68, hz(95), .06, 1.4); pop(7.65, 1100, .16)
boom(9.15, .75); whoosh(9.15, .4, .16, 6000, 400)  # zvrat
pop(12.0, 980, .2); whoosh(11.55, .3, .08, 3000, 300)

# ---------------------------------------------------------------- mix
def ir(seed, d=1.6, tau=.4):
    r = np.random.default_rng(seed); t = T(d); x = r.standard_normal(len(t)) * np.exp(-t / tau)
    x = lp(x, 6000); x[:int(.012 * SR)] = 0; return x / np.sqrt(np.sum(x ** 2))
IRL, IRR = ir(1), ir(2)
ML = M.L + fftconvolve(Mw.L, IRL)[:N] * .5; MR = M.R + fftconvolve(Mw.R, IRR)[:N] * .5
XL = X.L + fftconvolve(Xw.L, IRL)[:N]; XR = X.R + fftconvolve(Xw.R, IRR)[:N]
ML, MR = lp(ML, 9000), lp(MR, 9000)                 # teplý lo-fi charakter
duck = 1 - .25 * np.clip((t_ - 9.15) / .03, 0, 1) * np.clip((9.9 - t_) / .5, 0, 1)   # hudba uhne zvratu
L_ = ML * duck + XL; R_ = MR * duck + XR
fade = np.clip(t_ / .02, 0, 1) * np.clip((DUR - t_) / .35, 0, 1); L_ *= fade; R_ *= fade
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = np.tanh(L_ / pk * 1.6), np.tanh(R_ / pk * 1.6)
pk = max(np.abs(L_).max(), np.abs(R_).max()); L_, R_ = L_ / pk * .65, R_ / pk * .65   # ~-14 LUFS
out = sys.argv[1] if len(sys.argv) > 1 else 'fakta.wav'
with wave.open(out, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L_, R_], 1) * 32767).astype(np.int16).tobytes())
m = (L_ + R_) / 2
print(' '.join(f'{s}:{20*np.log10(np.sqrt(np.mean(m[s*SR:(s+1)*SR]**2))+1e-9):.0f}' for s in range(int(DUR))))
