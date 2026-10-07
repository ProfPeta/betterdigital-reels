"""Fotky pro Postavili to #02 (Musk): photos/src/ (nahrál Petr, licence neověřené – v gitu nejsou) -> PNG/JPG pro reel.html.
  musk_cut.png      portrét se Starshipem v ruce, vyříznutý (rembg), studená černobílá
  young.jpg         mladý Musk u počítače (90. léta), teplé vybledlé barvy
  oval.jpg          Oválná pracovna 2025, ořez jen na Muska (dítě v záběru není), černobílá
  starship.jpg      start Starshipu, výřez na výšku 1080×1920
  tesla.jpg         Musk na pódiu Tesly, ořez na Muska a auto, chladné barvy
usage: python3 -I photos/process.py [funkce…]   (spouštět s -I, zdroje jsou nahrané zvenku)"""
import glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')


def src(pat):
    f = sorted(glob.glob(os.path.join(SRC, pat)))
    if not f: print('chybí zdroj', pat); return None
    return ImageOps.exif_transpose(Image.open(f[0])).convert('RGB')


def cover(im, W, H, fx=.5, fy=.5):
    s = max(W / im.width, H / im.height); im = im.resize((max(W, round(im.width * s)), max(H, round(im.height * s))), Image.LANCZOS)
    x = int(np.clip(fx * im.width - W / 2, 0, im.width - W)); y = int(np.clip(fy * im.height - H / 2, 0, im.height - H))
    return im.crop((x, y, x + W, y + H))


def cool_bw(rgb, contrast=1.25, tint=(0.93, 0.97, 1.04)):
    g = np.asarray(rgb.convert('L')).astype(float) / 255
    g = np.clip((g - .5) * contrast + .5, 0, 1)
    out = np.stack([g * tint[0], g * tint[1], g * tint[2]], -1)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGB')


def halftone(gray, cell=6, ss=4):
    g = np.asarray(gray).astype(float) / 255; H, W = g.shape
    big = Image.new('L', (W * ss, H * ss), 0); d = ImageDraw.Draw(big)
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            r = cell / 2 * 1.45 * np.sqrt(g[y:y + cell, x:x + cell].mean())   # světlé tečky na černé
            if r > .3:
                cx, cy = (x + cell / 2) * ss, (y + cell / 2) * ss; d.ellipse([cx - r * ss, cy - r * ss, cx + r * ss, cy + r * ss], fill=255)
    return big.resize((W, H), Image.LANCZOS)


def save(im, name, **kw):
    im.save(os.path.join(HERE, name), **kw); print(name, im.size)


def portrait():
    im = src('musk_starship_model*')
    if im is None: return
    from rembg import remove, new_session
    cut = remove(im.convert('RGBA'), session=new_session('isnet-general-use'))
    a = cut.getchannel('A'); bb = a.getbbox(); cut = cut.crop(bb); a = a.crop(bb)
    rgb = cool_bw(ImageEnhance.Sharpness(cut.convert('RGB')).enhance(1.3), 1.3)
    out = rgb.convert('RGBA'); out.putalpha(a)
    W = 760; out = out.resize((W, round(out.height * W / out.width)), Image.LANCZOS)
    save(out, 'musk_cut.png', optimize=True)


def young():
    im = src('musk_young_pc*')
    if im is None: return
    im = cover(im, 1000, 750, .55, .45)
    a = np.asarray(im).astype(float) / 255
    a = a * .86 + .07; a[..., 0] *= 1.05; a[..., 2] *= .9                       # vybledlé, teplejší
    save(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)), 'young.jpg', quality=92)


def oval():
    im = src('musk_oval_office*')                                                # 399×501, dítě je vlevo dole
    if im is None: return
    im = im.crop((140, 0, 399, 259))                                             # jen Musk (hlava, ramena) + vlajka a okno
    g = ImageOps.autocontrast(im.convert('L'), cutoff=1).resize((518, 518), Image.LANCZOS)
    g = g.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    save(cool_bw(g.convert('RGB'), 1.15), 'oval.jpg', quality=92)


def starship():
    im = src('starship_launch*')
    if im is None: return
    im = cover(im, 1080, 1920, .5, .5)
    save(ImageEnhance.Contrast(im).enhance(1.08), 'starship.jpg', quality=90)


def tesla():
    im = src('musk_tesla_stage*')                                                # 1110×624, vpravo Musk a auto
    if im is None: return
    im = im.crop((470, 0, 1110, 624))
    im = cover(im, 760, 740, .55, .4)
    a = np.asarray(ImageEnhance.Color(im).enhance(.75)).astype(float) / 255
    a[..., 2] = np.clip(a[..., 2] * 1.04, 0, 1)
    save(Image.fromarray((a * 255).astype(np.uint8)), 'tesla.jpg', quality=92)


if __name__ == '__main__':
    import sys
    for f in (sys.argv[1:] or ['portrait', 'young', 'oval', 'starship', 'tesla']): globals()[f]()
