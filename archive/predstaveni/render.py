import os, subprocess, sys
from playwright.sync_api import sync_playwright
# usage: python3 rend.py <v|h> <stills|video> <html> <out> [times]
mode, what, html, out = sys.argv[1:5]
FPS = 30
vw, vh = (540, 960) if mode == 'v' else (960, 540)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': vw, 'height': vh}, device_scale_factor=2)
    pg.on('pageerror', lambda e: print('PAGEERR', e, file=sys.stderr))
    pg.goto('file://' + os.path.abspath(html))
    pg.wait_for_function('window.READY===true', timeout=60000)
    if what == 'stills':
        os.makedirs(out, exist_ok=True)
        for t in [float(x) for x in sys.argv[5].split(',')]:
            pg.evaluate(f'render({t})')
            pg.screenshot(path=f'{out}/{mode}_{t:05.2f}.png')
    else:
        dur = pg.evaluate('DURATION')
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'medium', '-crf', os.environ.get('CRF', '18'), '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            pg.evaluate(f'render({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=95))
        ff.stdin.close(); ff.wait()
    b.close()
