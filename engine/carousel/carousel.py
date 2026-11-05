#!/usr/bin/env python3
"""Carousel z jednoho souboru slides.json do obou formátů: build/feed/ 1080×1350 (Instagram, Facebook), build/vertical/ 1080×1920 (TikTok).
Slide: {"bg": "white|black|yellow", "kicker": "...", "title": "text *zvýraznění*", "body": "...", "image": "photos/x.jpg", "label": "ILUSTRACE"}
usage: python3 engine/carousel/carousel.py <složka>"""
import json, os, sys
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); d = os.path.abspath(sys.argv[1]); slides = json.load(open(os.path.join(d, 'slides.json'))); bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920}); pg.goto('file://' + os.path.join(H, 'template.html'))
    for fmt, h in (('feed', 1350), ('vertical', 1920)):
        o = os.path.join(d, 'build', fmt); os.makedirs(o, exist_ok=True); pg.set_viewport_size({'width': 1080, 'height': h})
        for i, s in enumerate(slides):
            pg.evaluate('([s,i,n,f,d])=>show(s,i,n,f,d)', [s, i, len(slides), fmt, d])
            if pg.evaluate('(()=>{const r=document.querySelector(".s"),f=document.querySelector(".foot").getBoundingClientRect();return [...r.children].some(e=>!e.classList.contains("foot")&&e.getBoundingClientRect().bottom>f.top-4)})()'): print(f'CHYBA: text přetéká, {fmt} slide {i + 1}'); bad += 1
            pg.screenshot(path=os.path.join(o, f'{i + 1:02}.png'))
    b.close()
print(len(slides), 'slidů v obou formátech' if not bad else f'{bad} přetečení'); sys.exit(1 if bad else 0)
