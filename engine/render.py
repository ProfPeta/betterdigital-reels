#!/usr/bin/env python3
"""Deterministic frame renderer for the reel pages.

Every reel page (episodes/*/reel.html) exposes:
  window.READY     -> true once fonts are loaded and scenes are built
  window.DURATION  -> length in seconds
  window.render(t) -> draws the frame for time t (pure function of t)

Usage:
  python3 engine/render.py stills episodes/dil-02-faktury/reel.html qa/ 1.3,4.2,9.6,14.3,16.5,18.6,22.9
  python3 engine/render.py video  episodes/dil-02-faktury/reel.html raw.mp4

Output is 1080x1920 (540x960 CSS px at device scale 2), 30 fps, H.264.
Chromium comes preinstalled for Playwright (do NOT run `playwright install`).
"""
import os, subprocess, sys
from playwright.sync_api import sync_playwright

FPS = 30
mode, html, out = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.on('pageerror', lambda e: print('PAGE ERROR:', e, file=sys.stderr))
    pg.goto('file://' + html)
    pg.wait_for_function('window.READY===true', timeout=60000)
    if mode == 'stills':
        os.makedirs(out, exist_ok=True)
        for t in [float(x) for x in sys.argv[4].split(',')]:
            pg.evaluate(f'render({t})')
            pg.screenshot(path=os.path.join(out, f'{t:05.2f}.png'))
    elif mode == 'video':
        dur = pg.evaluate('DURATION')
        # -bf 0: no B-frames, so the first video frame has pts 0. finalize.sh drops edit lists (Instagram API),
        # and with B-frames the video would then start 2 frames late (sound 67 ms ahead of the picture).
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-bf', '0', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            pg.evaluate(f'render({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=95))
        ff.stdin.close(); ff.wait()
    else:
        sys.exit('mode must be stills or video')
    b.close()
