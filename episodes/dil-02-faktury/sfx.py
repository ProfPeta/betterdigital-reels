import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; DUR = 23.2; N = int(DUR * SR)
rng = np.random.default_rng(12)
L = np.zeros(N); R = np.zeros(N); WL = np.zeros(N); WR = np.zeros(N)
def T(d): return np.arange(int(d * SR)) / SR
def env(d, a, dec): t = T(d); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, fc): return sosfilt(butter(2, fc, 'low', fs=SR, output='sos'), x)
def hp(x, fc): return sosfilt(butter(2, fc, 'high', fs=SR, output='sos'), x)
def add(sig, at, g=1.0, pan=0.0, wet=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); s = sig[:j - i] * g
    l, r = np.sqrt(.5 * (1 - pan)) * 1.414, np.sqrt(.5 * (1 + pan)) * 1.414
    L[i:j] += s * l; R[i:j] += s * r
    if wet: WL[i:j] += s * l * wet; WR[i:j] += s * r * wet

def key(at, g=1.0):      # keyboard keystroke
    d = .05; t = T(d)
    s = bp(rng.standard_normal(len(t)), 1800, 6500) * env(d, .0003, .004) * .8
    s += np.sin(2 * np.pi * rng.uniform(170, 240) * t) * env(d, .001, .012) * .5
    add(s, at, g * rng.uniform(.7, 1.0), rng.uniform(-.25, .25), .05)
def typing(a, b, rate=15, g=.5):
    t = a
    while t < b:
        key(t, g); t += 1 / rate * rng.uniform(.6, 1.4)
def click(at, g=.6, pan=0):
    for k, dt in enumerate((0, .07)):
        d = .02; t = T(d); s = bp(rng.standard_normal(len(t)), 2000, 8000) * env(d, .0002, .0018) + np.sin(2 * np.pi * 3200 * t) * env(d, .0002, .002) * .3
        add(s, at + dt, g * (1 if k == 0 else .6), pan, .08)
def scroll(a, b, g=.18):
    t = a
    while t < b:
        d = .012; tt = T(d); add(bp(rng.standard_normal(len(tt)), 3000, 9000) * env(d, .0002, .0015), t, g, -.2); t += .035
def swish(at, g=.25, d=.22):
    t = T(d); x = t / d; s = bp(rng.standard_normal(len(t)), 600, 5000) * np.sin(np.pi * x) ** 2
    add(s, at - d * .5, g, 0, .2)
def blip(at, f, g=.3, d=.18):
    t = T(d); s = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t)) * env(d, .002, .045)
    add(s, at, g, .1, .35)
def chime(at, notes, g=.3, gap=.07):
    for k, f in enumerate(notes):
        d = 1.6; t = T(d); s = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t / (.7 / r ** .5)) for r, a in [(1, 1), (2, .4), (3, .15)])
        add(s * np.minimum(1, t / .003), at + k * gap, g, 0, .6)
def thud(at, g=.8):
    d = .9; t = T(d); f = 50 + 90 * np.exp(-t / .04)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .16) + lp(rng.standard_normal(len(t)), 1500) * env(d, .001, .03) * .6
    add(s, at, g, 0, .3)
def impact(at, g):
    d = 2.2; t = T(d); f = 36 + 95 * np.exp(-t / .05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .55) + lp(rng.standard_normal(len(t)), 2400) * env(d, .001, .06) * .9 + hp(rng.standard_normal(len(t)), 5000) * env(d, .002, .35) * .15
    add(s, at, g, 0, .45)


def err(at, g=.35):
    for k, f in enumerate((233, 175)):
        d = .14; t = T(d); s = lp(np.sign(np.sin(2 * np.pi * f * t)), 1800) * env(d, .003, .06)
        add(s, at + k * .11, g, 0, .15)

# --- groove bed 100 BPM until the manual side is done ---
beat = .6
for k in range(int(14.0 / beat)):
    at = k * beat
    d = .3; t = T(d); f = 48 + 70 * np.exp(-t / .03)
    add(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .09), at, .42 if k % 2 == 0 else .3)
    h = hp(rng.standard_normal(int(.04 * SR)), 7000) * env(.04, .0005, .01); add(h, at + beat / 2, .1, .3)
for k in range(int(14.0 / (beat / 2))):
    at = k * beat / 2; d = .28; t = T(d)
    n = [55, 55, 65.4, 49][(k // 8) % 4]
    add(lp(np.sign(np.sin(2 * np.pi * n * t)) * .5, 400) * env(d, .005, .1), at, .09)

# --- manual side ---
for at in [.25, 1.9, 3.4, 4.6, 6.8, 12.4]: swish(at, .28)
for n in range(2, 31):
    at = 8.6 + ((n - 1) * 370) / (11220 - 480) * 3.8; swish(at, .07, .12)
typing(.35, .7); typing(2.05, 2.35); typing(2.45, 2.72); typing(3.75, 4.4)
for i in range(7): typing(4.7 + i * .27, 4.93 + i * .27)
typing(6.9, 7.3); typing(7.35, 7.6); typing(7.65, 7.87)
err(7.95)
t = 8.25
while t < 8.35: key(t, .6); t += .05
typing(8.35, 8.47)
typing(8.7, 12.3, rate=24, g=.3)            # frantic data entry during the montage
typing(12.5, 12.75); typing(12.8, 13.05); typing(13.15, 13.65)
cl = [.32, 1.6, 2.02, 2.42, 2.85, 3.25, 3.55, 3.6, 8.52, 13.85] + [8.7 + k * .13 + .06 for k in range(0, 28, 2)]
for at in cl: click(at, .55, -.15)
thud(14.0, .7); chime(14.02, [392.0, 261.6], .18, .16)

# --- automation side ---
chime(.25, [880, 1318.5], .16, .06)
for i in range(7): blip(.32 + i * .06, 1400 + i * 60, .06, .06)
swish(.8, .12, .2)
for k in range(30):                          # rows filling: accelerating, rising ticks
    at = .9 + 1.5 * (k / 30) ** (1 / 1.35)
    blip(at, 900 * 2 ** (k / 30), .09, .05)
for at in [.85, .97, 1.09]: swish(at + .2, .08, .2)
blip(2.6, 660, .15); blip(2.8, 784, .2)
click(3.9, .6, .15)
chime(3.95, [1046.5, 1318.5, 1568, 2093], .2, .06)
swish(4.6, .2, .35)

# --- stat cards + CTA ---
swish(14.8, .3, .3)
thud(15.1, .35); thud(15.85, .45)
impact(17.6, 1.0)
swish(19.8, .25, .3)
impact(20.22, .45); blip(20.23, 1318.5, .16, .25)
chime(21.15, [1046.5, 1568], .14, .05)
for f, a in [(130.8, 1), (196, .7), (261.6, .6), (329.6, .4)]:
    d = 8.8; tt = T(d); s = sum(np.sin(2 * np.pi * f * dt * tt) for dt in (1, 1.003, .997)) / 3
    s *= np.minimum(1, tt / .6) * np.clip((d - tt) / 1.2, 0, 1); add(s, 14.4, .05 * a, 0, .8)

import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else 'audio.wav'
def ir(seed):
    r = np.random.default_rng(seed); t = T(1.8); x = r.standard_normal(len(t)) * np.exp(-t / .35); x = lp(x, 6500); x[:int(.01 * SR)] = 0
    return x / np.sqrt(np.sum(x ** 2)) * .9
L += fftconvolve(WL, ir(1))[:N]; R += fftconvolve(WR, ir(2))[:N]
tt = np.arange(N) / SR; fade = np.clip((DUR - tt) / .3, 0, 1); L *= fade; R *= fade
pk = max(abs(L).max(), abs(R).max()); L, R = np.tanh(L / pk * 1.5), np.tanh(R / pk * 1.5)
pk = max(abs(L).max(), abs(R).max()); L, R = L / pk * .93, R / pk * .93
with wave.open(OUT, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
m = (L + R) / 2
print(' '.join(f'{20*np.log10(np.sqrt(np.mean(m[int(s*SR):int((s+1)*SR)]**2))+1e-9):.0f}' for s in range(23)))
