#!/usr/bin/env python3
"""Vykreslení stránky reel.html po snímcích (render(t) je čistá funkce času). Výstup 1080×1920, 30 fps.
  python3 engine/render.py stills <reel.html> <složka> 1.3,4.2,9.6
  python3 engine/render.py video  <reel.html> <raw.mp4> [--from F --to F] [--workers N]
Video běží v několika prohlížečích najednou a úseky se spojí bez překódování."""
import os, subprocess, sys, tempfile, multiprocessing as mp
from playwright.sync_api import sync_playwright

FPS = 30


def page(p, html):
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.on('pageerror', lambda e: print('CHYBA STRÁNKY:', e, file=sys.stderr))
    pg.goto('file://' + html); pg.wait_for_function('window.READY===true', timeout=60000)
    return b, pg


def chunk(a):
    """Téměř bezztrátový mezistupeň bez B-snímků; finální kódování dělá make.py."""
    html, out, f0, f1 = a
    with sync_playwright() as p:
        b, pg = page(p, html)
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-bf', '0', '-g', '30', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for i in range(f0, f1):
            pg.evaluate(f'render({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=100))
        ff.stdin.close(); ff.wait(); b.close()
    return out


def opt(args, name, default):
    return int(args[args.index(name) + 1]) if name in args else default


def video(html, out, args):
    with sync_playwright() as p:
        b, pg = page(p, html); total = int(pg.evaluate('DURATION') * FPS); b.close()
    f0, f1 = opt(args, '--from', 0), opt(args, '--to', total)
    w = opt(args, '--workers', os.cpu_count() or 2)
    cuts = [f0 + (f1 - f0) * i // w for i in range(w + 1)]
    with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(out))) as d:
        jobs = [(html, os.path.join(d, f'{i:02}.mp4'), cuts[i], cuts[i + 1]) for i in range(w)]
        with mp.get_context('spawn').Pool(w) as pool: parts = pool.map(chunk, jobs)
        lst = os.path.join(d, 'list.txt'); open(lst, 'w').write(''.join(f"file '{q}'\n" for q in parts))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True)
    print(f'render {f1 - f0} snímků, {w} procesy -> {out}')


def stills(html, out, ts):
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b, pg = page(p, html)
        for t in ts:
            pg.evaluate(f'render({t})'); pg.screenshot(path=os.path.join(out, f'{t:06.2f}.png'))
        b.close()


if __name__ == '__main__':
    mode, html, out = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
    if mode == 'stills': stills(html, out, [float(x) for x in sys.argv[4].split(',')])
    elif mode == 'video': video(html, out, sys.argv[4:])
    else: sys.exit('mode: stills nebo video')
