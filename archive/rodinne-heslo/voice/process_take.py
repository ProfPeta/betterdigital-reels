"""Hlasovka „Kubíčka“ z ElevenLabs -> hlasová zpráva z telefonu (voice.wav + words.json pro reel.html).

Zdroj: take_elevenlabs.mp3 – navržený hlas „Kubíček – mladý kluk (rodinné heslo)“ (ElevenLabs Voice Design,
mladý Čech ~19 let), vygenerováno v aplikaci ElevenLabs tímto promptem:
  [scared] [breathless] Mami… to jsem já. [trembling voice] Měl jsem nehodu. [on the verge of tears] Potřebuju hned peníze. [softly] Nemůžu volat.

Úprava je záměrně jemná, hlas samotný se nemění: ořez ticha na začátku, šustnutí telefonu, EQ mikrofonu,
lehká komprese, tichá noční ulice místo digitálního ticha v pauzách, krátký prostor a kodek Opus 24 kb/s
jako u hlasových zpráv v messengerech.

Časy slov (WORDS) jsou ručně zarovnané na nahrávku: konce vět podle ticha, hranice uvnitř vět podle
akustických orientačních bodů (sykavka „s“ v „jsem“, „ř“ v „Potřebuju“, „ž“ v „Nemůžu“, závěry a výbuchy
souhlásek), ověřené přepisem Whisperu na postupně prodlužovaných úsecích. Vzlyky a nádechy mezi slovy
nejsou slova, „Mami,“ zůstává zvýrazněné i přes vzlyk po něm.
usage: python3 process_take.py
"""
import json, os, subprocess, tempfile
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TRIM = .12                                   # ticho na začátku nahrávky (s)
# slovo, začátek, konec v sekundách v původní nahrávce take_elevenlabs.mp3
WORDS = [['Mami,', .17, 1.22], ['to', 1.38, 1.48], ['jsem', 1.48, 1.69], ['já.', 1.69, 2.13],
         ['Měl', 2.66, 2.94], ['jsem', 2.94, 3.16], ['nehodu.', 3.16, 3.78],
         ['Potřebuju', 4.32, 4.82], ['hned', 4.82, 5.08], ['peníze.', 5.10, 5.75],
         ['Nemůžu', 6.34, 6.88], ['volat.', 6.88, 7.46]]
rng = np.random.default_rng(11)


def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def smooth(x, n): return np.convolve(x, np.ones(n) / n, 'same')


def load(path):
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, 'a.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ac', '1', '-ar', str(SR), w], check=True)
        x, _ = sf.read(w)
    return x


def rustle(d, g):
    """Šustnutí a ťuknutí prstem o telefon (začátek a konec nahrávání)."""
    n = int(d * SR); x = np.zeros(n)
    for _ in range(int(rng.integers(6, 11))):
        L = int(rng.integers(80, 700)); i = int(rng.integers(0, max(1, n - L)))
        x[i:i + L] += rng.standard_normal(L) * np.hanning(L) * rng.uniform(.25, 1)
    x = bp(x, 900, 6000) + .7 * lp(x, 220); return x / (np.abs(x).max() + 1e-9) * g


def opus(x):
    """Kodek hlasových zpráv: Opus 24 kb/s, 16 kHz (voip), zarovnaný zpět na původní časy."""
    with tempfile.TemporaryDirectory() as d:
        a, b, c = (os.path.join(d, f) for f in ('in.wav', 'v.ogg', 'out.wav'))
        sf.write(a, (x / (np.abs(x).max() + 1e-9) * .9).astype(np.float32), SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-ar', '16000', '-c:a', 'libopus', '-b:a', '24k', '-application', 'voip', b], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', b, '-ar', str(SR), c], check=True)
        y, _ = sf.read(c)
    y = np.pad(y, (0, max(0, len(x) + 2000 - len(y))))
    ex = smooth(np.abs(x), 96); ey = smooth(np.abs(y[:len(x) + 2000]), 96)
    lags = np.arange(-2000, 2001); m = len(x) - 4000
    k = int(lags[np.argmax([np.dot(ex[2000:2000 + m], ey[2000 + l:2000 + l + m]) for l in lags])])
    y = y[k:] if k >= 0 else np.concatenate([np.zeros(-k), y])
    y = y[:len(x)]; return np.pad(y, (0, len(x) - len(y)))


v = load(os.path.join(HERE, 'take_elevenlabs.mp3'))[int(TRIM * SR):]
v = v / np.abs(v).max() * .8
pre = rustle(.10, .05)                                # šustnutí těsně před prvním nádechem (překryv)
v[:len(pre)] += pre
end = int(min(len(v), (WORDS[-1][2] - TRIM + .12) * SR))
tail = rustle(.09, .04); v = np.concatenate([v[:end], np.zeros(int(.03 * SR))])
v[-len(tail):] += tail                                  # konec nahrávání: puštění tlačítka
# telefon: EQ mikrofonu, presence, jemná komprese (AGC), lehké zaoblení špiček
v = hp(v, 120); v = lp(v, 7800, 4); v = v + .18 * bp(v, 2000, 4500)
env = np.sqrt(smooth(v ** 2, int(.03 * SR))) + 1e-6
thr = .3 * env.max(); v = v * np.minimum(1, (thr / env) ** .35)
v = np.tanh(v / np.abs(v).max() * 1.05)
# noční ulice pod celou zprávou (zaplní digitální ticho v pauzách), krátký prostor
L = len(v); tt = np.arange(L) / SR
rumble = lp(np.cumsum(rng.standard_normal(L)) / 300, 120); rumble -= rumble.mean()
car = bp(rng.standard_normal(L), 300, 2500) * np.exp(-((tt - L / SR * .7) / 1.1) ** 2) * .5
wind = lp(rng.standard_normal(L), 300) * (.5 + .5 * np.sin(2 * np.pi * .6 * tt) ** 2)
amb = rumble / (np.abs(rumble).max() + 1e-9) * .04 + car * .022 + wind * .022 + hp(rng.standard_normal(L), 3000) * .003
ir_n = int(.2 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / (.04 * SR)); ir = lp(ir, 5000)
ir[:int(.004 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
v = v + fftconvolve(v, ir)[:L] * .06 + amb
v = opus(v); v = v / np.abs(v).max() * .9
sf.write(os.path.join(HERE, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
words = [[w, round(a - TRIM, 3), round(b - TRIM, 3)] for w, a, b in WORDS]
json.dump({'source': 'ElevenLabs (navržený hlas „Kubíček – mladý kluk“), take_elevenlabs.mp3', 'duration': round(L / SR, 3),
           'firstWord': words[0][1], 'lastWordEnd': words[-1][2], 'words': words},
          open(os.path.join(HERE, 'words.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({'duration': L / SR, 'speech': [words[0][1], words[-1][2]]}, ensure_ascii=False))
