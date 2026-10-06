"""Časy vět a titulků podle hlasu -> timeline.js (pro reel.html) a timeline.json (pro sfx.py).
S hlasem (voice.wav + segments.json z prep.py): hranice vět se přichytí na pauzy mezi segmenty, uvnitř segmentu
na nejtišší místo v okolí odhadu podle slabik. Bez hlasu: prozatímní časy z počtu slabik (0,17 s/slabika).
usage: python3 timeline.py"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EP = os.path.dirname(HERE)
sys.path.insert(0, EP)
from script import SENT, syllables  # noqa: E402

SR = 48000; LEAD = .05; HOLD = 2.4
syl = [sum(syllables(c) for c in chunks) for _, chunks in SENT]
have_voice = os.path.exists(os.path.join(HERE, 'voice.wav')) and os.path.exists(os.path.join(HERE, 'segments.json'))
if have_voice:
    import soundfile as sf
    x, _ = sf.read(os.path.join(HERE, 'voice.wav'))
    seg = json.load(open(os.path.join(HERE, 'segments.json')))['segments']
    w = int(.025 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same'))
else:
    seg, t = [], .1
    for s in syl: seg.append([t, t + .17 * s]); t += .17 * s + .32
    e = None

# „řečový čas“ (bez pauz) -> skutečný čas
sp = np.cumsum([0] + [b - a for a, b in seg]); Tsp = sp[-1]
def real(u):
    k = int(np.clip(np.searchsorted(sp, u, 'right') - 1, 0, len(seg) - 1)); return seg[k][0] + (u - sp[k])
def dip(c, lo, hi):
    if e is None: return c
    i0, i1 = int(max(lo, c - .2) * SR), int(min(hi, c + .2) * SR)
    return (i0 + int(np.argmin(e[i0:i1]))) / SR if i1 > i0 + 10 else c

# hranice vět: ruční mapa (voice/map.json = segment, kterým začíná každá věta, číslováno od 1), jinak odhad
MAPF = os.path.join(HERE, 'map.json')
cum = np.cumsum([0] + syl) / sum(syl)
bounds = [seg[0][0]]
if have_voice and os.path.exists(MAPF):
    mp = json.load(open(MAPF)); assert len(mp) == len(SENT), 'map.json musí mít položku pro každou větu'
    bounds = [seg[i - 1][0] for i in mp]
for k in range(len(bounds), len(SENT)):
    c = real(cum[k] * Tsp)
    starts = [a for a, _ in seg[1:]]
    near = min(starts, key=lambda s: abs(s - c)) if starts else c
    b = near if abs(near - c) < .7 else dip(c, bounds[-1] + .2, seg[-1][1])
    bounds.append(max(b, bounds[-1] + .25))
ends = []
for k in range(len(SENT)):
    nb = bounds[k + 1] if k + 1 < len(SENT) else seg[-1][1]
    inside = [b for a, b in seg if bounds[k] < b <= nb + 1e-6]
    ends.append(max(inside) if inside else nb)
S = {sid: [round(bounds[k], 3), round(ends[k], 3)] for k, (sid, _) in enumerate(SENT)}

# titulky: kousky věty úměrně slabikám, hranice na nejtišší místo
chunks = []
for k, (sid, cs) in enumerate(SENT):
    a, b = S[sid]; ws = [syllables(c) for c in cs]; cc = np.cumsum([0] + ws) / sum(ws)
    ts = [a] + [dip(a + cc[i] * (b - a), a + .1, b - .1) for i in range(1, len(cs))] + [b]
    for i, c in enumerate(cs):
        chunks.append([sid, i, c, round(ts[i] - LEAD, 3), round(ts[i + 1] - LEAD, 3)])
END = round(S[SENT[-1][0]][1] + HOLD, 2)
out = {'voice': have_voice, 'S': S, 'chunks': chunks, 'END': END}
json.dump(out, open(os.path.join(EP, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(EP, 'timeline.js'), 'w').write('window.TL=' + json.dumps(out, ensure_ascii=False) + ';\n')
print(('HLAS' if have_voice else 'PROZATÍMNÍ'), 'END', END, ' '.join(f'{k}:{v[0]:.1f}' for k, v in S.items()))
