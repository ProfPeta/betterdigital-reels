"""Záznam kalkulačky (app/index.html) po snímcích pro reel.html – skutečná aplikace v Chromiu, nic se v ní nemění.
Čas aplikace řídí falešné hodiny Playwrightu (page.clock), takže záznam je přesně 30 fps a „zrychlená hodina“ je
skutečný výpočet aplikace, jen se hodiny posouvají rychleji. CSS animace se krokují stejným časem (Web Animations API).
Ťuknutí (+, +, 50 tis., Spustit) jsou kliknutí na prvky aplikace ve chvílích podle hlasu (timeline.json).
Systémové písmo „telefonu“ = Inter Tight (fontconfig), aplikace sama žádné písmo nenačítá.
Výstup: app_frames/f0000.jpg… (v .gitignore, dá se kdykoli znovu vyrobit) a app_data.js (kód, rozměry prvků, plán).
usage: python3 app_capture.py"""
import datetime, json, os, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
APP = os.path.join(HERE, 'app', 'index.html'); OUT = os.path.join(HERE, 'app_frames')
TL = json.load(open(os.path.join(HERE, 'timeline.json'))); S = TL['S']
CK = {}
for sid, i, txt, a, b in TL['chunks']: CK.setdefault(sid, {})[i] = a
st = lambda s: S[s][0]; ck = lambda s, i: CK[s][i]
FPS = 30; W, H = 390, 844

# plán ve videočase (s): kdy se aplikace spustí, kdy se ťuká, kdy se zrychlí hodina porady
V0 = round(ck('s5', 2) + .92, 3)                     # „…a aplikaci spustila“
TAPS = [['plus', round(ck('s7', 0) + .55, 3)], ['plus', round(ck('s7', 0) + .97, 3)],
        ['chip50', round(ck('s7', 2) + .62, 3)], ['go', round(ck('s8', 0) + .52, 3)]]
GO = TAPS[-1][1]
FF0 = round(st('s9') + .45, 3); FF1 = round(FF0 + 3.0, 3)   # 1 hodina porady za 3 s videa
V1 = round(st('s11') + .1, 3)
SEL = {'plus': '#plus', 'minus': '#minus', 'chip50': '#chips button[data-v="50000"]', 'go': '#go'}


def meeting(v):
    """uplynulý čas porady (s) ve videočase v; mezi FF0 a FF1 hladké zrychlení na 1 hodinu (na krajích reálný čas)"""
    if v <= GO: return 0.0
    if v <= FF0: return v - GO
    e0 = FF0 - GO
    if v <= FF1:
        x = (v - FF0) / (FF1 - FF0); s = x * x * x * (x * (6 * x - 15) + 10)
        return e0 + (v - FF0) + (3600 - e0 - (FF1 - FF0)) * s
    return 3600 + (v - FF1)


def app_ms(v):
    """čas aplikace (ms od načtení) ve videočase v"""
    return 1000 * ((min(v, GO) - V0) + meeting(v))


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.jpg'): os.remove(os.path.join(OUT, f))
    conf_dir = tempfile.mkdtemp()
    conf = os.path.join(conf_dir, 'fonts.conf')
    open(conf, 'w').write(f'''<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>
<include ignore_missing="yes">/etc/fonts/fonts.conf</include><dir>{REPO}/engine/fonts</dir><cachedir>{conf_dir}/cache</cachedir>
<match target="pattern"><test qual="any" name="family"><string>system-ui</string></test>
<edit name="family" mode="assign" binding="strong"><string>Inter Tight</string></edit></match>
<alias binding="strong"><family>sans-serif</family><prefer><family>Inter Tight</family></prefer></alias></fontconfig>''')
    errs = []
    t0 = datetime.datetime(2026, 10, 12, 10, 0, 0)
    with sync_playwright() as p:
        b = p.chromium.launch(env={**os.environ, 'FONTCONFIG_FILE': conf})
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.clock.install(time=t0)
        pg.goto('file://' + APP)
        pg.clock.pause_at(t0 + datetime.timedelta(seconds=1))
        base = 1000.0; cur = 0.0                          # app čas (ms od pause_at)

        def advance(to):
            nonlocal cur
            d = to - cur
            if d <= 0: return
            if d > 250: pg.clock.fast_forward(int(d - 20)); pg.clock.run_for(20)
            else: pg.clock.run_for(max(1, int(round(d))))
            pg.evaluate('dt => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = (a.currentTime || 0) + dt; } }', d)
            cur = to

        layout = pg.evaluate('''sel => Object.fromEntries(Object.entries(sel).map(([k, s]) => {
            const r = document.querySelector(s).getBoundingClientRect(); return [k, [r.x, r.y, r.width, r.height]]; }))''',
                             {**SEL, 'cost': '#cost', 'time': '#time', 'meter': '.meter', 'stats': '.stats'})
        n = int(round((V1 - V0) * FPS)) + 1; prev = V0 - 1e-6; done = set()
        for i in range(n):
            v = V0 + i / FPS
            for k, (name, at) in enumerate(TAPS):
                if k not in done and prev < at <= v:
                    advance(app_ms(at)); pg.evaluate('s => document.querySelector(s).click()', SEL[name]); done.add(k)
            advance(app_ms(v))
            pg.screenshot(path=os.path.join(OUT, f'f{i:04d}.jpg'), type='jpeg', quality=90)
            prev = v
            if i % 60 == 0: print(f'{i}/{n}  v={v:.2f}  {pg.inner_text("#cost")}  {pg.inner_text("#time")}', flush=True)
        final = {'cost': pg.inner_text('#cost'), 'time': pg.inner_text('#time'), 'perHour': pg.inner_text('#perHour'),
                 'people': pg.inner_text('#people'), 'compare': pg.inner_text('#compare')}
        b.close()
    code = open(APP, encoding='utf-8').read()
    bs = os.path.join(HERE, 'app', 'build_start'); be = os.path.join(HERE, 'app', 'build_end')
    build_s = round(float(open(be).read()) - float(open(bs).read()), 1)
    data = {'code': code, 'lines': code.count('\n'), 'build_s': build_s, 'size': [W, H], 'layout': layout, 'fps': FPS,
            'v0': V0, 'v1': V1, 'frames': n, 'taps': TAPS, 'go': GO, 'ff0': FF0, 'ff1': FF1, 'final': final,
            'prompt': open(os.path.join(HERE, 'app', 'zadani.txt'), encoding='utf-8').read().strip()}
    open(os.path.join(HERE, 'app_data.js'), 'w', encoding='utf-8').write('window.APP=' + json.dumps(data, ensure_ascii=False) + ';\n')
    print('hotovo', n, 'snímků; konec:', final, '; chyby:', errs or 'žádné')


if __name__ == '__main__':
    main()
