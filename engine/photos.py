"""Fotky dílu podle photos/photos.json -> photos/<out>. Jednotně: sRGB, šířka ze spec.json, doostření při zvětšení, varování u malého zdroje.
Položka: {"src": "x.jpg", "out": "x.jpg", "box": [l, t, r, b] (volitelné), "source": "...", "license": "...", "label": "...", "min_width": 700 (volitelné)}
usage: python3 engine/photos.py <díl>"""
import json, os, sys
from PIL import Image, ImageFilter, ImageCms

SPEC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec.json')))['photo']


def run(ep):
    p = os.path.join(ep, 'photos'); mf = os.path.join(p, 'photos.json')
    if not os.path.exists(mf): print('fotky: žádný photos.json'); return 0
    bad = 0
    for it in json.load(open(mf)):
        s = os.path.join(p, 'src', it['src'])
        if not os.path.exists(s): print('CHYBÍ zdroj:', it['src'], '(fotky nejsou v repu, nahraj je znovu)'); bad += 1; continue
        if not it.get('license') or not it.get('source'): print('POZOR: chybí zdroj nebo licence:', it['src'])
        im = Image.open(s)
        try:
            if im.info.get('icc_profile'):
                im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(__import__('io').BytesIO(im.info['icc_profile'])), ImageCms.createProfile('sRGB'))
        except Exception: pass
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg
        im = im.convert('RGB')
        if it.get('box'): im = im.crop(it['box'])
        w = SPEC['output_width']; need = it.get('min_width', SPEC['min_width'])
        if im.width < need: print(f"POZOR: malá fotka {it['src']}: {im.width} px, chce to aspoň {need}")
        up = im.width < w
        if im.width != w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        if up: im = im.filter(ImageFilter.UnsharpMask(1.2, 70, 2))
        im.save(os.path.join(p, it['out']), quality=SPEC['output_jpeg_q'], optimize=True)
    print('fotky hotové' if not bad else f'fotky: {bad} chybí')
    return bad


if __name__ == '__main__': sys.exit(run(os.path.abspath(sys.argv[1])))
