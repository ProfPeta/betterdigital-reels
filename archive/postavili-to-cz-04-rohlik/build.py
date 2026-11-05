"""Sestaví reel.html z kostry #03 (pomocníci a engine z ../postavili-to-03-nvidia/reel.html) + parts/style.css + parts/scenes.js.
usage: python3 build.py"""
import os
H = os.path.dirname(os.path.abspath(__file__)); N = os.path.join(H, '..', 'postavili-to-03-nvidia', 'reel.html')
src = open(N).read().split('\n')
start = [i for i, l in enumerate(src) if l.startswith('<script>') and 'timeline' not in l][0]
hud = [i for i, l in enumerate(src) if l.startswith('const HUD')][0]
eng = [i for i, l in enumerate(src) if l.startswith('/* ------------------------------------------------------------ sestavení')][0]
helpers = '\n'.join(src[start + 1:hud]); engine = '\n'.join(src[eng:])
for a, b in (("const YEARS=[1978,1993,1995,1997,2025],Y0=1978,Y1=2026", "const YEARS=[2005,2010,2012,2021,2025],Y0=2003,Y1=2026"),
             ("['#fff','#76B900','#000']", "['#fff','#F2A93B','#6BA53A']"), ("rgba(118,185,0,.8)) drop-shadow", "rgba(242,169,59,.8)) drop-shadow"),
             ("const tl=$('tl');", "const tl=$('tl');tl.className=s.cls==='cream'?'dk2':'';")):
    assert a in engine, a; engine = engine.replace(a, b)
css = open(os.path.join(H, 'parts', 'style.css')).read(); scn = open(os.path.join(H, 'parts', 'scenes.js')).read()
open(os.path.join(H, 'reel.html'), 'w').write(f'''<!doctype html>
<!-- POSTAVILI TO · Česká edice #4 – Rohlík / Tomáš Čupr. TikTok/Reels 540×960 CSS px (render 2×), 30 fps, délka podle hlasu (timeline.js).
     Styl: kostra Better Digital + barvy Rohlíku (zelená, oranžová, krémová). Generováno build.py z parts/. -->
<html lang="cs"><head><meta charset="utf-8"><title>POSTAVILI TO · Česká edice #4 – Rohlík</title>
<style>
{css}</style></head><body>
<div id="stage"></div>
<div id="tl"></div>
<div id="cap"></div>
<div id="gl"></div><div id="scanl"></div>
<canvas id="grain" width="180" height="320"></canvas>
<div id="flash"></div>
<script src="timeline.js"></script>
<script>
{helpers}
{scn}
{engine}''')
print('reel.html ok')
