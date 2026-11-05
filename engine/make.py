#!/usr/bin/env python3
"""Jeden příkaz na výrobu videa. Díl = složka ve videos/. Vše se dělá lokálně do <díl>/build/, nic se samo neposílá.

  python3 engine/make.py new <slug>        nový díl ze šablony
  python3 engine/make.py draft <díl>       fotky, hlas, časy, scény, QA (bez renderu, asi 30 s)
  python3 engine/make.py all <díl>         draft + zvuk, render, finální kódování, obálka, náhled, kontrola
  python3 engine/make.py <krok> <díl>      photos | voice | page | events | qa | audio | video | encode | preview | check | transcript
  python3 engine/make.py push <díl>        nahraje jen video a obálku do větve media a vypíše odkaz pro Metricool
  python3 engine/make.py payload <díl>     vypíše data pro plánování v Metricoolu z post.json
"""
import difflib, json, os, re, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ENG = os.path.join(ROOT, 'engine')
sys.path.insert(0, ENG)
SPEC = json.load(open(os.path.join(ENG, 'spec.json')))
REPO = 'ProfPeta/betterdigital-reels'; BLOG = '7151077'; TZ = 'Europe/Prague'


def sh(*a, **k): return subprocess.run(a, check=True, **k)
def B(ep, *p): return os.path.join(ep, 'build', *p)
def cfg(ep): return json.load(open(os.path.join(ep, 'episode.json')))
def die(m): sys.exit('CHYBA: ' + m)


def page(ep):
    """Vygeneruje reel.html: sdílené styly a engine, data dílu, scény dílu."""
    c = cfg(ep); os.makedirs(B(ep), exist_ok=True)
    extra = '<link rel="stylesheet" href="style.css">' if os.path.exists(os.path.join(ep, 'style.css')) else ''
    pub = {k: c[k] for k in ('years', 'y0', 'y1', 'badge', 'grain', 'accent') if k in c}
    open(os.path.join(ep, 'reel.html'), 'w').write(f'''<!doctype html><!-- generuje engine/make.py, needitovat -->
<html lang="cs"><head><meta charset="utf-8"><title>{c.get('title', '')}</title>
<link rel="stylesheet" href="../../engine/story/base.css">{extra}</head><body>
<div id="stage"></div><div id="tl"></div><div id="cap"></div><div id="gl"></div><div id="scanl"></div>
<canvas id="grain" width="180" height="320"></canvas><div id="flash"></div>
<script>window.CFG={json.dumps(pub, ensure_ascii=False)};</script>
<script src="build/timeline.js"></script>
<script src="../../engine/story/lib.js"></script>
<script src="scenes.js"></script>
<script src="../../engine/story/engine.js"></script>
</body></html>
''')
    print('reel.html hotové')


def events(ep):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 540, 'height': 960})
        pg.goto('file://' + os.path.join(ep, 'reel.html')); pg.wait_for_function('window.READY===true', timeout=60000)
        ev = pg.evaluate('window.EV'); b.close()
    json.dump({'events': [[round(e[0], 3)] + e[1:] for e in ev]}, open(B(ep, 'fx.json'), 'w'), ensure_ascii=False)
    print(len(ev), 'zvukových událostí')


def audio(ep):
    sh(sys.executable, os.path.join(ENG, 'sfxlib.py'), B(ep, 'audio.wav'), env={**os.environ, 'EP_DIR': ep})


def video(ep): sh(sys.executable, os.path.join(ENG, 'render.py'), 'video', os.path.join(ep, 'reel.html'), B(ep, 'raw.mp4'))


def encode(ep):
    """Finální kódování podle spec.json. Bez B-snímků a edit listů (požadavek Instagram API, jinak se rozjede zvuk)."""
    v, a = SPEC['video'], SPEC['audio']
    sh('ffmpeg', '-v', 'error', '-y', '-i', B(ep, 'raw.mp4'), '-i', B(ep, 'audio.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', v['preset'], '-crf', str(v['crf']),
       '-profile:v', 'high', '-bf', '0', '-pix_fmt', v['pix_fmt'], '-c:a', 'aac', '-b:a', a['bitrate'], '-ar', str(a['rate']), '-shortest', '-movflags', '+faststart', '-use_editlist', '0', B(ep, 'video.mp4'))
    ms = json.load(open(os.path.join(ep, 'post.json'))).get('coverMs', 2000)
    sh('ffmpeg', '-v', 'error', '-y', '-ss', str(ms / 1000), '-i', B(ep, 'raw.mp4'), '-frames:v', '1', '-q:v', '2', B(ep, 'cover.jpg'))
    print(f"video.mp4 {os.path.getsize(B(ep, 'video.mp4')) / 1e6:.1f} MB")


def preview(ep):
    sh('ffmpeg', '-v', 'error', '-y', '-i', B(ep, 'video.mp4'), '-vf', 'scale=720:1280', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-c:a', 'copy', '-movflags', '+faststart', B(ep, 'preview_720p.mp4'))
    print(f"náhled {os.path.getsize(B(ep, 'preview_720p.mp4')) / 1e6:.1f} MB")


def check(ep):
    """Kontrola hotového souboru proti spec.json."""
    f = B(ep, 'video.mp4'); v, a = SPEC['video'], SPEC['audio']; errs = []
    p = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,start_time,sample_rate:format=duration,size', '-of', 'json', f], capture_output=True, text=True).stdout)
    vs = [s for s in p['streams'] if s['codec_type'] == 'video'][0]; au = [s for s in p['streams'] if s['codec_type'] == 'audio'][0]
    for k, want, got in (('šířka', v['width'], vs['width']), ('výška', v['height'], vs['height']), ('fps', f"{v['fps']}/1", vs['r_frame_rate']), ('kodek', v['codec'], vs['codec_name']), ('pixely', v['pix_fmt'], vs['pix_fmt']), ('zvuk', a['codec'], au['codec_name']), ('vzorkování', str(a['rate']), au['sample_rate'])):
        if want != got: errs.append(f'{k}: {got}, má být {want}')
    if abs(float(vs.get('start_time', 0))) > 1e-3: errs.append('video nezačíná v čase 0, rozjede se zvuk')
    d = open(f, 'rb').read(); m = d.find(b'mdat')
    if not 0 <= d.find(b'moov') < m: errs.append('moov není na začátku')
    if d[:m].count(b'elst'): errs.append('soubor má edit list')
    mb = int(p['format']['size']) / 1e6; dur = float(p['format']['duration'])
    if mb > v['max_mb']: errs.append(f'velikost {mb:.0f} MB nad limitem {v["max_mb"]} MB')
    from sfxlib_lufs import lufs
    I, pk = lufs(f)
    if abs(I - a['lufs']) > a['lufs_tol']: errs.append(f'hlasitost {I:.1f} LUFS, má být {a["lufs"]}')
    if pk > a['peak_max']: errs.append(f'špička {pk:.1f} dBFS nad {a["peak_max"]}')
    print(f"kontrola: {vs['width']}×{vs['height']} {vs['r_frame_rate']} fps, {dur:.1f} s, {mb:.1f} MB, {I:.1f} LUFS, špička {pk:.1f} dBFS")
    if dur > SPEC['story']['max_seconds']: print(f'POZOR: délka {dur:.0f} s nad doporučených {SPEC["story"]["max_seconds"]} s')
    for e in errs: print('CHYBA:', e)
    return 1 if errs else 0


def transcript(ep):
    """Volitelné: přepis hlasu proti scénáři. Model se stahuje jen jednou za session (asi 2 min)."""
    from voice import load_script
    d = os.path.join(ENG, 'tools', 'sherpa-onnx-whisper-turbo')
    if not os.path.isdir(d): sh('bash', os.path.join(ENG, 'tools', 'get_whisper.sh'))
    import numpy as np, soundfile as sf, sherpa_onnx
    from scipy.signal import resample_poly
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + '/turbo-encoder.int8.onnx', decoder=d + '/turbo-decoder.int8.onnx', tokens=d + '/turbo-tokens.txt', language='cs', task='transcribe', num_threads=os.cpu_count() or 2)
    src = B(ep, 'audio.wav') if os.path.exists(B(ep, 'audio.wav')) else B(ep, 'voice.wav')
    x, sr = sf.read(src, dtype='float32', always_2d=True); x = x.mean(1); seg = json.load(open(B(ep, 'segments.json')))['segments']
    bl = []; a = seg[0][0]; e = a
    for s, q in seg:
        if q - a > 25: bl.append((a, e)); a = s
        e = q
    bl.append((a, e)); tx = []
    for a, e in bl:
        y = resample_poly(x[int(max(0, a - .05) * sr):int((e + .1) * sr)], 1, 3).astype(np.float32)
        s = rec.create_stream(); s.accept_waveform(16000, y); rec.decode_stream(s); tx.append(s.result.text.strip())
    t = ' '.join(tx); ref = ' '.join(' '.join(c) for _, c in load_script(ep).SENT).replace('*', '')
    n = lambda z: re.sub(r'[^\w ]', '', z.lower()).split(); A, Z = n(ref), n(t)
    print(t); print(f'shoda se scénářem {difflib.SequenceMatcher(None, A, Z).ratio():.0%}')
    sm = difflib.SequenceMatcher(None, A, Z)
    for op, i, j, k, l in sm.get_opcodes():
        if op != 'equal': print(f"  rozdíl: {' '.join(A[i:j])!r} -> {' '.join(Z[k:l])!r}")


def push(ep):
    """Jen hotový soubor do větve media. Hlavní větev zůstává bez videí, media drží vždy jen poslední nahrané."""
    slug = os.path.basename(ep); url0 = subprocess.run(['git', '-C', ROOT, 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()
    tmp = B(ep, '_media'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(os.path.join(tmp, slug))
    for f in ('video.mp4', 'cover.jpg'): shutil.copy(B(ep, f), os.path.join(tmp, slug, f))
    g = lambda *a: sh('git', '-C', tmp, *a)
    g('init', '-q', '-b', 'media'); g('add', '-A'); g('-c', 'user.name=Claude', '-c', 'user.email=noreply@anthropic.com', 'commit', '-q', '-m', f'Media pro Metricool: {slug}'); g('push', '-q', '-f', url0, 'media:media')
    shutil.rmtree(tmp); url = f'https://raw.githubusercontent.com/{REPO}/media/{slug}/video.mp4'
    print(url); return url


def payload(ep):
    """Data pro createScheduledPost, jedna položka na síť. Video musí být nahrané přes push."""
    p = json.load(open(os.path.join(ep, 'post.json'))); slug = os.path.basename(ep); out = []
    media = [f'https://raw.githubusercontent.com/{REPO}/media/{slug}/video.mp4']
    for net, n in p['networks'].items():
        i = {'autoPublish': True, 'descendants': [], 'draft': False, 'firstCommentText': p.get('firstComment', ''), 'hasNotReadNotes': False, 'media': media, 'videoCoverMilliseconds': p.get('coverMs', 2000), 'mediaAltText': [],
             'providers': [{'network': net}], 'publicationDate': {'dateTime': n['publishAt'][:19], 'timezone': TZ}, 'shortener': False, 'smartLinkData': {'ids': []}, 'text': n['text']}
        if net == 'instagram': i['instagramData'] = {'type': 'REEL', 'showReelOnFeed': True, 'collaborators': [], 'isAiGenerated': p.get('aiVoice', True)}
        if net == 'tiktok': i['tiktokData'] = {'disableComment': False, 'disableDuet': False, 'disableStitch': False, 'privacyOption': 'PUBLIC_TO_EVERYONE', 'commercialContentThirdParty': False, 'commercialContentOwnBrand': p.get('ownBrand', False), 'title': n['text'], 'autoAddMusic': False, 'photoCoverIndex': 0, 'isAigc': p.get('aiVoice', True)}
        if net == 'facebook': i['facebookData'] = {'type': 'REEL', 'title': n.get('title', '')}
        out.append({'network': net, 'blogId': BLOG, 'date': n['publishAt'], 'info': i})
    print(json.dumps(out, ensure_ascii=False, indent=1))


def new(slug):
    d = os.path.join(ROOT, 'videos', slug)
    if os.path.exists(d): die('díl už existuje')
    shutil.copytree(os.path.join(ROOT, 'videos', '_template'), d); print(d)


def timed(name, fn, ep):
    t = time.time(); r = fn(ep); print(f'  [{name}: {time.time() - t:.0f} s]', flush=True); return r


def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == 'new': return new(arg)
    ep = os.path.abspath(arg if os.path.isdir(arg) else os.path.join(ROOT, 'videos', arg))
    if not os.path.exists(os.path.join(ep, 'episode.json')): die(f'{ep} není díl')
    import photos, voice, qa
    steps = dict(photos=photos.run, voice=voice.run, page=page, events=events, qa=qa.run, audio=audio, video=video, encode=encode, preview=preview, check=check, transcript=transcript, push=push, payload=payload)
    draft = ['photos', 'voice', 'page', 'qa', 'events']
    seq = {'draft': draft, 'all': draft + ['audio', 'video', 'encode', 'preview', 'check']}.get(cmd, [cmd])
    t0 = time.time()
    for s in seq:
        if s not in steps: sys.exit(__doc__)
        r = timed(s, steps[s], ep)
        if s in ('photos', 'qa') and r and cmd == 'all': die(f'krok {s} našel chyby, oprav je a spusť znovu')
        if s == 'check' and r: sys.exit(1)
    if len(seq) > 1: print(f'hotovo za {time.time() - t0:.0f} s')


if __name__ == '__main__': main()
