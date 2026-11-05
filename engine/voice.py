"""Hlas -> build/voice.wav, build/segments.json, build/timeline.{js,json}.
Mapu vět na úseky řeči najde sám podle délky a pauz, přepis k tomu není potřeba. Ruční oprava: "map" v episode.json.
Bez nahrávky jsou časy jen odhad ze slabik, aby šel díl kontrolovat ještě před hlasem. usage: python3 engine/voice.py <díl>"""
import importlib.util, json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000


def load_script(ep):
    sp = importlib.util.spec_from_file_location('script', os.path.join(ep, 'script.py'))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


def segments(x):
    win = int(.02 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, 'same')); db = 20 * np.log10(e + 1e-9)
    on = db > db.max() - 38; segs = []; i = 0; n = len(on); hold = int(.12 * SR)
    while i < n:
        if on[i]:
            j = i
            while j < n and (on[j] or on[j:j + hold].any()): j += 1
            segs.append([i, j]); i = j
        else: i += 1
    return segs


def prep(ep, cfg):
    """Tempo (auto = zkrátit nad 66 s, nejvýš o 8 %), zkrácení pauz, filtr, komprese, normalizace."""
    take = os.path.join(ep, 'voice', 'take_elevenlabs.mp3'); b = os.path.join(ep, 'build')
    raw = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', take], capture_output=True, text=True).stdout)
    tempo = cfg.get('tempo', 'auto'); tempo = min(1.08, max(1.0, raw * .97 / 66)) if tempo == 'auto' else float(tempo)
    cap = float(cfg.get('pause_cap', .30))
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, 'v.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', take, '-af', f'atempo={tempo}', '-ac', '1', '-ar', str(SR), w], check=True)
        x, _ = sf.read(w)
    seg = segments(x)
    out = [x[:seg[0][1]]]; new = [[seg[0][0] / SR, seg[0][1] / SR]]; fade = int(.015 * SR)
    for k in range(1, len(seg)):
        a, e = seg[k]; gap = (a - seg[k - 1][1]) / SR; want = .5 if gap > .8 else cap
        g = x[seg[k - 1][1]:a]
        if gap > want:
            keep = int(want * SR); h = keep // 2; left, right = g[:h], g[len(g) - (keep - h):]
            if len(left) > fade and len(right) > fade:
                r = np.linspace(0, 1, fade); g = np.concatenate([left[:-fade], left[-fade:] * (1 - r) + right[:fade] * r, right[fade:]])
            else: g = np.concatenate([left, right])
        out.append(g); cur = sum(len(o) for o in out); out.append(x[a:e]); new.append([cur / SR, (cur + e - a) / SR])
    out.append(x[seg[-1][1]:seg[-1][1] + int(.3 * SR)])
    v = sosfilt(butter(2, 70, 'high', fs=SR, output='sos'), np.concatenate(out))
    env = np.sqrt(np.convolve(v ** 2, np.ones(int(.03 * SR)) / int(.03 * SR), 'same')) + 1e-6
    v = v * np.minimum(1, (.25 * env.max() / env) ** .3); v = v / np.abs(v).max() * .89
    sf.write(os.path.join(b, 'voice.wav'), v.astype(np.float32), SR, subtype='PCM_16')
    json.dump({'tempo': tempo, 'cap': cap, 'duration': round(len(v) / SR, 3), 'segments': [[round(a, 3), round(e, 3)] for a, e in new]},
              open(os.path.join(b, 'segments.json'), 'w'), indent=1)
    print(f'hlas {raw:.1f} s -> {len(v) / SR:.1f} s (tempo {tempo:.3f}), {len(new)} úseků')


def automap(seg, syl, lam=1.0, gap=.22):
    """Přiřadí věty po sobě jdoucím úsekům řeči. Trestá odchylku od průměrného tempa a začátek věty po krátké pauze (čárka)."""
    d = [e - a for a, e in seg]; n, k = len(d), len(syl)
    if k > n: raise SystemExit(f'CHYBA: {k} vět, ale jen {n} úseků řeči. Nastav "map" v episode.json.')
    r = sum(d) / sum(syl); P = np.cumsum([0] + d); INF = 1e18
    C = np.full((k + 1, n + 1), INF); B = np.zeros((k + 1, n + 1), int); C[0, 0] = 0
    for i in range(1, k + 1):
        for j in range(i, n - (k - i) + 1):
            for h in range(i - 1, j):
                if C[i - 1, h] >= INF: continue
                c = C[i - 1, h] + ((P[j] - P[h]) - r * syl[i - 1]) ** 2 + (lam if h > 0 and seg[h][0] - seg[h - 1][1] < gap else 0)
                if c < C[i, j]: C[i, j] = c; B[i, j] = h
    mp = []; j = n
    for i in range(k, 0, -1): j = int(B[i, j]); mp.append(j + 1)
    return mp[::-1]


def timeline(ep, cfg):
    m = load_script(ep); SENT, syllables = m.SENT, m.syllables; b = os.path.join(ep, 'build')
    syl = [sum(syllables(c) for c in cs) for _, cs in SENT]
    have = os.path.exists(os.path.join(b, 'voice.wav'))
    if have:
        x, _ = sf.read(os.path.join(b, 'voice.wav')); seg = json.load(open(os.path.join(b, 'segments.json')))['segments']
        w = int(.025 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same'))
        mp = cfg.get('map') or automap(seg, syl)
        bounds = [seg[i - 1][0] for i in mp]
    else:
        seg, t = [], .1
        for s in syl: seg.append([t, t + .17 * s]); t += .17 * s + .32
        e = None; mp = list(range(1, len(syl) + 1)); bounds = [s[0] for s in seg]

    def dip(c, lo, hi):
        if e is None: return c
        i0, i1 = int(max(lo, c - .2) * SR), int(min(hi, c + .2) * SR)
        return (i0 + int(np.argmin(e[i0:i1]))) / SR if i1 > i0 + 10 else c
    ends = []
    for k in range(len(SENT)):
        nb = bounds[k + 1] if k + 1 < len(SENT) else seg[-1][1]
        inside = [q for a, q in seg if bounds[k] < q <= nb + 1e-6]
        ends.append(max(inside) if inside else nb)
    S = {sid: [round(bounds[k], 3), round(ends[k], 3)] for k, (sid, _) in enumerate(SENT)}
    chunks = []; LEAD = .05
    for k, (sid, cs) in enumerate(SENT):
        a, z = S[sid]; ws = [syllables(c) for c in cs]; cc = np.cumsum([0] + ws) / sum(ws)
        ts = [a] + [dip(a + cc[i] * (z - a), a + .1, z - .1) for i in range(1, len(cs))] + [z]
        for i, c in enumerate(cs): chunks.append([sid, i, c, round(ts[i] - LEAD, 3), round(ts[i + 1] - LEAD, 3)])
    END = round(S[SENT[-1][0]][1] + float(cfg.get('hold', 2.4)), 2)
    out = {'voice': have, 'S': S, 'chunks': chunks, 'END': END, 'map': mp}
    json.dump(out, open(os.path.join(b, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(b, 'timeline.js'), 'w').write('window.TL=' + json.dumps(out, ensure_ascii=False) + ';\n')
    print(('časy z hlasu' if have else 'POZOR: bez hlasu, časy jen odhad') + f', konec {END} s, mapa {mp}')


def run(ep):
    cfg = json.load(open(os.path.join(ep, 'episode.json'))); os.makedirs(os.path.join(ep, 'build'), exist_ok=True)
    if os.path.exists(os.path.join(ep, 'voice', 'take_elevenlabs.mp3')): prep(ep, cfg)
    timeline(ep, cfg)


if __name__ == '__main__': run(os.path.abspath(sys.argv[1]))
