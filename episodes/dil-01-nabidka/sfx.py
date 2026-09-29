import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; DUR = 23.2; N = int(DUR * SR)
rng = np.random.default_rng(11)
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

# --- groove bed 100 BPM until the manual side is done ---
beat = .6
for k in range(int(14.0 / beat)):
    at = k * beat
    d = .3; t = T(d); f = 48 + 70 * np.exp(-t / .03)
    add(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .002, .09), at, .42 if k % 2 == 0 else .3)
    h = hp(rng.standard_normal(int(.04 * SR)), 7000) * env(.04, .0005, .01); add(h, at + beat / 2, .1, .3)
# soft bass pulse following the beat
for k in range(int(14.0 / (beat / 2))):
    at = k * beat / 2; d = .28; t = T(d)
    n = [55, 55, 65.4, 49][(k // 8) % 4]
    add(lp(np.sign(np.sin(2 * np.pi * n * t)) * .5, 400) * env(d, .005, .1), at, .09)

# --- manual side ---
for at in [.25, 2.3, 4.3, 6.3, 8.1, 10.1, 11.9]: swish(at, .28)
scroll(.6, 1.1); scroll(1.25, 1.45)
for i in range(4): typing(2.45 + i * .45, 2.8 + i * .45)
typing(4.4, 4.75)
for i in range(3):
    t0 = 8.25 + i * .55; typing(t0, t0 + .25); typing(t0 + .28, t0 + .36); typing(t0 + .38, t0 + .5)
typing(9.85, 10.08)
t = 11.0
while t < 11.3: key(t, .6); t += .075      # backspaces
typing(11.3, 11.55)
typing(12.0, 12.4); typing(12.5, 12.9); typing(13.3, 13.65)
for at in [1.9, 4.35, 4.9, 5.2, 5.5, 5.8, 6.05, 6.45, 6.65, 6.85, 7.05, 7.25, 7.45, 7.7, 10.9, 10.97, 13.95]: click(at, .55, -.15)
# export progress hum
d = .35; tt = T(d); add(np.sin(2 * np.pi * (300 + 500 * tt / d) * tt) * .15 * np.sin(np.pi * tt / d), 12.95, 1)
# manual finished: thud + deflated two notes
thud(14.0, .7); chime(14.02, [392.0, 261.6], .18, .16)

# --- automation side ---
chime(.25, [880, 1318.5], .16, .06)                         # new inquiry
for k, at in enumerate([.95, 1.25, 1.5, 1.75]): blip(at, 1046.5 * 2 ** (k * 2 / 12), .16)
for at in [2.15, 2.4, 2.65]: swish(at + .15, .12, .25)
for k, at in enumerate([2.45, 2.7, 2.95]): blip(at, 784 * 2 ** (k * 4 / 12), .18)
t = 3.0
while t < 3.5: blip(t, 2400, .05, .03); t += .04              # total counting
blip(3.7, 660, .2)
click(4.4, .6, .15)
chime(4.45, [1046.5, 1318.5, 1568, 2093], .2, .06)          # sent!
swish(5.2, .2, .35)

# --- stat cards ---
swish(14.8, .3, .3)
thud(15.1, .35); thud(15.85, .45)
impact(17.6, 1.0)
swish(19.8, .25, .3)
impact(20.22, .45); blip(20.23, 1318.5, .16, .25)
chime(21.15, [1046.5, 1568], .14, .05)
# warm pad under the cards
for f, a in [(130.8, 1), (196, .7), (261.6, .6), (329.6, .4)]:
    d = 8.8; tt = T(d); s = sum(np.sin(2 * np.pi * f * dt * tt) for dt in (1, 1.003, .997)) / 3
    s *= np.minimum(1, tt / .6) * np.clip((d - tt) / 1.2, 0, 1); add(s, 14.4, .05 * a, 0, .8)

def ir(seed):
    r = np.random.default_rng(seed); t = T(1.8); x = r.standard_normal(len(t)) * np.exp(-t / .35); x = lp(x, 6500); x[:int(.01 * SR)] = 0
    return x / np.sqrt(np.sum(x ** 2)) * .9
L += fftconvolve(WL, ir(1))[:N]; R += fftconvolve(WR, ir(2))[:N]
tt = np.arange(N) / SR; fade = np.clip((DUR - tt) / .3, 0, 1); L *= fade; R *= fade
pk = max(abs(L).max(), abs(R).max()); L, R = np.tanh(L / pk * 1.5), np.tanh(R / pk * 1.5)
pk = max(abs(L).max(), abs(R).max()); L, R = L / pk * .93, R / pk * .93
import sys
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'audio.wav', 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
m = (L + R) / 2
print(' '.join(f'{20*np.log10(np.sqrt(np.mean(m[int(s*SR):int((s+1)*SR)]**2))+1e-9):.0f}' for s in range(23)))
