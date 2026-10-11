"""Fotky a loga pro POSTAVILI TO · Česká edice #1 (Avast). Zdroje v photos/src/ nahrál Petr, licence neověřené –
zdroje ani zpracované verze nejsou ve veřejném repu (.gitignore).
  baudis_cut.png / kucera_cut.png   portréty zakladatelů, vyříznuté (rembg) – Baudiš je ten s pleší, Kučera s brýlemi
  baudis_young.jpg                  mladý Pavel Baudiš u stolu s počítači (archivní fotka), mírně dorovnané barvy
  duo.jpg                           oba zakladatelé na vyhlídce nad Prahou, barevná úprava
  olivetti_cut.png                  Olivetti M24 bez růžového pozadí (rembg)
  logo_*.png                        loga Avast, AVG, McAfee, Norton na průhledném pozadí, oříznutá
usage: python3 -I photos/process.py [funkce…]   (spouštět s -I, zdroje jsou nahrané zvenku)"""
import glob, os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')


def src(pat, mode='RGB'):
    f = sorted(glob.glob(os.path.join(SRC, pat)))
    if not f: print('chybí zdroj', pat); return None
    return ImageOps.exif_transpose(Image.open(f[0])).convert(mode)


def save(im, name, **kw):
    im.save(os.path.join(HERE, name), **kw); print(name, im.size)


def cutout(im, width, sharpen=1.2, contrast=1.06, color=1.0):
    from rembg import remove, new_session
    cut = remove(im.convert('RGBA'), session=new_session('isnet-general-use'))
    a = cut.getchannel('A'); bb = a.getbbox(); cut = cut.crop(bb)
    rgb = ImageEnhance.Sharpness(cut.convert('RGB')).enhance(sharpen)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast); rgb = ImageEnhance.Color(rgb).enhance(color)
    out = rgb.convert('RGBA'); out.putalpha(cut.getchannel('A'))
    h = round(out.height * width / out.width)
    return out.resize((width, h), Image.LANCZOS)


def white_to_alpha(im, thr=.035):
    """logo na bílém pozadí -> průhledné pozadí (odečtení bílé, zachová vyhlazené hrany)"""
    a = np.asarray(im.convert('RGB')).astype(float) / 255
    alpha = np.clip((1 - a).max(2), 0, 1)
    alpha = np.clip((alpha - thr) / (1 - thr), 0, 1)
    col = np.where(alpha[..., None] > 1e-3, (a - (1 - alpha[..., None])) / np.maximum(alpha[..., None], 1e-3), 0)
    out = np.dstack([np.clip(col, 0, 1), alpha])
    img = Image.fromarray((out * 255).astype(np.uint8), 'RGBA')
    return img.crop(img.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())


def founders():
    for name, f, w in (('baudis_cut.png', 'baudis*', 620), ('kucera_cut.png', 'kucera*', 620)):
        im = src(f)
        if im is None: continue
        save(cutout(im, w, 1.15, 1.05, .95), name, optimize=True)


def young():
    im = src('baudis_young*')
    if im is None: return
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(.95)).enhance(1.06)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    save(im.resize((round(im.width * 900 / im.height), 900) if im.height < 900 else im.size, Image.LANCZOS), 'baudis_young.jpg', quality=92)


def duo():
    im = src('duo*')
    if im is None: return
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(.92)).enhance(1.05)
    save(im.resize((1110, 624), Image.LANCZOS), 'duo.jpg', quality=92)


def olivetti():
    im = src('olivetti*')
    if im is None: return
    save(cutout(im, 700, 1.2, 1.04, .55), 'olivetti_cut.png', optimize=True)


def logos():
    for name, f in (('logo_avast.png', 'logo_avast*'), ('logo_avg.png', 'logo_avg*'), ('logo_norton.png', 'logo_norton*')):
        im = src(f)
        if im is None: continue
        lg = white_to_alpha(im); h = 300; save(lg.resize((round(lg.width * h / lg.height), h), Image.LANCZOS), name, optimize=True)
    im = src('logo_mcafee*', 'RGBA')
    if im is not None:
        a = np.asarray(im).astype(float)
        if a[..., 3].min() > 250: im = white_to_alpha(im)          # bílé pozadí bez průhlednosti
        else: im = im.crop(im.getchannel('A').getbbox())
        h = 300; save(im.resize((round(im.width * h / im.height), h), Image.LANCZOS), 'logo_mcafee.png', optimize=True)


if __name__ == '__main__':
    import sys
    for f in (sys.argv[1:] or ['founders', 'young', 'duo', 'olivetti', 'logos']): globals()[f]()
