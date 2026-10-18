"""Přerenderuje jen úsek snímků [f0, f1) stránky reel.html (stejné nastavení jako engine/render.py) -> seg.mp4"""
import os, subprocess, sys
from playwright.sync_api import sync_playwright
html, out, f0, f1 = os.path.abspath(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.on('pageerror', lambda e: print('PAGE ERROR:', e, file=sys.stderr))
    pg.goto('file://' + html); pg.wait_for_function('window.READY===true', timeout=60000)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-bf', '0', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(f0, f1):
        pg.evaluate(f'render({i / FPS})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=95))
    ff.stdin.close(); ff.wait(); b.close()
print('ok', f1 - f0, 'snímků')
