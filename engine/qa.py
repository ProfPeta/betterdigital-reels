"""Automatická kontrola obrazu bez renderu videa: text mimo bezpečnou zónu, překryv s titulkem, prázdné záběry, chyby stránky.
Uloží arch build/qa_sheet.jpg (3 snímky na scénu). usage: python3 engine/qa.py <díl>. Návratový kód 1 = našlo chyby."""
import glob, json, os, shutil, sys
from PIL import Image
from playwright.sync_api import sync_playwright

SPEC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec.json')))['safe']
CHECK = '''(S)=>{
 const vis=e=>{let o=1;for(let n=e;n&&n.nodeType===1;n=n.parentElement){const c=getComputedStyle(n);if(c.display==='none'||c.visibility==='hidden')return 0;o*=parseFloat(c.opacity)}return o};
 const textRects=root=>{const out=[];const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim()||!n.parentElement||n.parentElement.closest('svg'))continue;const op=vis(n.parentElement);if(op<.06)continue;const r=document.createRange();r.selectNodeContents(n);for(const q of [r.getBoundingClientRect()]){if(q.width>0)out.push({t:n.textContent.trim().slice(0,40),l:q.left,r:q.right,y0:q.top,y1:q.bottom,op})}}return out};
 const sc=[...document.querySelectorAll('#stage .sc')].filter(e=>e.style.display!=='none'&&e.style.zIndex==='2')[0];
 const tx=sc?textRects(sc):[];const cap=textRects(document.getElementById('cap'));
 const errs=[];
 for(const q of tx.concat(cap)){if(q.l<S.x0||q.r>S.x1||q.y0<S.y0||q.y1>S.y1)errs.push(`mimo zónu [${Math.round(q.l)}-${Math.round(q.r)}, ${Math.round(q.y0)}-${Math.round(q.y1)}]: ${q.t}`)}
 for(const c of cap)for(const q of tx){if(c.l<q.r&&q.l<c.r&&c.y0<q.y1&&q.y0<c.y1)errs.push(`překryv s titulkem: ${q.t}`)}
 let media=0;if(sc)for(const e of sc.querySelectorAll('img,svg,.big,.card,.ph,.chip')){if(vis(e)>.06)media++}
 return {errs,count:tx.length+media};
}'''


def run(ep):
    html = os.path.join(ep, 'reel.html'); b = os.path.join(ep, 'build'); q = os.path.join(b, 'qa')
    shutil.rmtree(q, ignore_errors=True); os.makedirs(q)
    errs, warns, pe = {}, [], []
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=1)
        pg.on('pageerror', lambda e: pe.append(str(e))); pg.goto('file://' + html); pg.wait_for_function('window.READY===true', timeout=60000)
        sc = pg.evaluate('window.SCN.map(s=>({id:s.id,t0:s.t0,t1:s.t1}))'); end = pg.evaluate('DURATION')
        pg.evaluate('document.getElementById("grain").style.display="none"')
        empty = 0.0; t = 0.0; last = None
        while t < end:
            pg.evaluate(f'render({t})'); r = pg.evaluate(CHECK, SPEC)
            for e in r['errs']: errs.setdefault(e, round(t, 1))
            if r['count'] == 0:
                empty += .25
                if empty >= .75 and last != round(t): warns.append(f'prázdný záběr kolem {t:.1f} s'); last = round(t)
            else: empty = 0
            t += .25
        for s in sc:
            d = s['t1'] - s['t0']
            for k, u in enumerate((.3, .6, .97)):
                tt = min(end - .05, s['t0'] + max(.25, d * u)); pg.evaluate(f'render({tt})'); pg.screenshot(path=os.path.join(q, f'{tt:07.2f}.png'))
        br.close()
    fs = sorted(glob.glob(q + '/*.png')); cols = 9; sz = (200, 356); rows = (len(fs) + cols - 1) // cols
    sh = Image.new('RGB', (cols * (sz[0] + 4), rows * (sz[1] + 4)), (120, 120, 120))
    for i, f in enumerate(fs): sh.paste(Image.open(f).convert('RGB').resize(sz), ((i % cols) * (sz[0] + 4), (i // cols) * (sz[1] + 4)))
    sh.save(os.path.join(b, 'qa_sheet.jpg'), quality=85); shutil.rmtree(q)
    for e, t in sorted(errs.items(), key=lambda x: x[1]): print(f'CHYBA {t:5.1f} s: {e}')
    for e in pe: print('CHYBA STRÁNKY:', e)
    for w in warns: print('POZOR:', w)
    print(f'QA: {len(errs) + len(pe)} chyb, {len(warns)} upozornění, {len(sc)} scén, arch build/qa_sheet.jpg')
    return 1 if errs or pe else 0


if __name__ == '__main__': sys.exit(run(os.path.abspath(sys.argv[1])))
