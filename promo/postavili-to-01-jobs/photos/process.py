"""Fotky pro Postavili to #01: zdroje v photos/src/ (nahrané z Wikimedia Commons) -> zpracované PNG pro reel.html.
  <name>_ht.png  novinový rastr (tečky inkoustu, průhledné pozadí)
  <name>_bw.png  černobílá verze s vyšším kontrastem (u osob a předmětů vyříznutá z pozadí)
Když zdroj chybí, vznikne zástupný obrázek (šedá silueta + popisek), aby šlo animaci ladit předem.
Vyřezávání: rembg (u2net_human_seg pro lidi, isnet-general-use pro předměty).
usage: python3 -I process.py   (spouštět s -I, zdrojové soubory jsou nahrané zvenku)"""
import glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = {   # jméno: (vzor zdroje, režim, šířka, výška, ohnisko x/y pro ořez 0..1)
    'jobs':      ('jobs_2010*', 'person', 1080, 1350, (.5, .35)),
    'jobsgates': ('jobs_gates*', 'full', 1080, 660, (.5, .3)),
    'apple1':    ('apple1*', 'object', 1080, 820, (.5, .5)),
    'next':      ('nextcube*', 'object', 900, 900, (.5, .5)),
}


PRECROP = {'jobsgates': (330, 280, 1730, 1240)}          # ořez zdroje před zpracováním (px)


def cover(img, W, H, focus):
    w, h = img.size; s = max(W / w, H / h); img = img.resize((max(W, round(w * s)), max(H, round(h * s))), Image.LANCZOS)
    w, h = img.size; fx, fy = focus
    x = int(np.clip(fx * w - W / 2, 0, w - W)); y = int(np.clip(fy * h - H / 2, 0, h - H))
    return img.crop((x, y, x + W, y + H))


def contain(img, W, H):
    img = img.copy(); img.thumbnail((W, H), Image.LANCZOS)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); c.paste(img, ((W - img.width) // 2, (H - img.height) // 2), img); return c


def halftone(rgba, cell=10, ss=4, ink=(14, 14, 14)):
    a = np.asarray(rgba).astype(float) / 255; g = (a[..., :3] @ [.299, .587, .114]); al = a[..., 3]
    g = np.clip((g - .5) * 1.25 + .5, 0, 1)                      # víc kontrastu
    H, W = g.shape; big = Image.new('L', (W * ss, H * ss), 0); d = ImageDraw.Draw(big)
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            dark = (1 - g[y:y + cell, x:x + cell].mean()) * al[y:y + cell, x:x + cell].mean()
            r = cell / 2 * 1.42 * np.sqrt(dark)
            if r > .35:
                cx, cy = (x + cell / 2) * ss, (y + cell / 2) * ss
                d.ellipse([cx - r * ss, cy - r * ss, cx + r * ss, cy + r * ss], fill=255)
    cov = np.asarray(big.resize((W, H), Image.LANCZOS))
    out = np.zeros((H, W, 4), np.uint8); out[..., :3] = ink; out[..., 3] = cov
    return Image.fromarray(out, 'RGBA')


def bw(rgba):
    a = np.asarray(rgba).astype(float); g = a[..., :3] @ [.299, .587, .114]
    g = np.clip((g / 255 - .5) * 1.3 + .52, 0, 1) * 255
    out = np.zeros_like(a); out[..., 0] = out[..., 1] = out[..., 2] = g; out[..., 3] = a[..., 3]
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


def placeholder(name, mode, W, H):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if mode == 'person':
        d.ellipse([W * .3, H * .12, W * .7, H * .52], fill=(120, 120, 120, 255))
        d.rounded_rectangle([W * .1, H * .5, W * .9, H * 1.1], radius=int(W * .25), fill=(100, 100, 100, 255))
    elif mode == 'full':
        d.rectangle([0, 0, W, H], fill=(150, 150, 150, 255))
        for cx in (.33, .67):
            d.ellipse([W * (cx - .13), H * .2, W * (cx + .13), H * .5], fill=(95, 95, 95, 255))
            d.rounded_rectangle([W * (cx - .22), H * .5, W * (cx + .22), H * 1.05], radius=int(W * .1), fill=(80, 80, 80, 255))
    else:
        d.rounded_rectangle([W * .12, H * .25, W * .88, H * .8], radius=12, fill=(110, 110, 110, 255))
    d.text((20, 20), f'FOTO: {name}', fill=(255, 40, 40, 255))
    return im


def process(name):
    pat, mode, W, H, focus = SPECS[name]
    src = sorted(glob.glob(os.path.join(HERE, 'src', pat)))
    if not src:
        im = placeholder(name, mode, W, H); tag = 'zástupný'
    else:
        im = ImageOps.exif_transpose(Image.open(src[0])).convert('RGBA')
        if name in PRECROP: im = im.crop(PRECROP[name])
        if mode in ('person', 'object'):
            from rembg import remove, new_session
            sess = new_session('isnet-general-use')          # obecný model: u lidí nechá i to, co drží v ruce
            im = remove(im, session=sess)
            bbox = im.getbbox(); im = im.crop(bbox) if bbox else im
            im = cover(im, W, H, focus) if mode == 'person' else contain(im, W, H)
        else:
            im = cover(im, W, H, focus)
        tag = os.path.basename(src[0])
    halftone(im).save(os.path.join(HERE, f'{name}_ht.png'))
    bw(im).save(os.path.join(HERE, f'{name}_bw.png'))
    print(name, '<-', tag, im.size)


if __name__ == '__main__':
    for n in SPECS: process(n)
