"""Vytáhne zvukové události z reel.html (window.EV) do fx.json, aby zvuk (sfx.py) seděl přesně na animace.
usage: python3 export_ev.py"""
import json, os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 540, 'height': 960})
    pg.goto('file://' + os.path.join(HERE, 'reel.html')); pg.wait_for_function('window.READY===true', timeout=60000)
    ev = pg.evaluate('window.EV'); b.close()
json.dump({'events': [[round(e[0], 3)] + e[1:] for e in ev]}, open(os.path.join(HERE, 'fx.json'), 'w'), ensure_ascii=False, indent=0)
print(len(ev), 'událostí ->', os.path.join(HERE, 'fx.json'))
