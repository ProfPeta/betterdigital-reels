"""Fotky a loga pro POSTAVILI TO · Česká edice #2 (Seznam). Zdroje v photos/src/ nahrál Petr, licence neověřené –
zdroje ani zpracované verze nejsou ve veřejném repu (.gitignore).
  ivo_mlady.jpg     mladý Ivo Lukačovič před logem Seznamu (archivní fotka)
  ivo_hory_cut.png  Ivo Lukačovič dnes (hory), vyříznutý (rembg)
  pes_cut.png       pes (maskot), vyříznutý
  logo_s.png / logo_mapy.png / logo_zpravy.png   loga
usage: python3 -I photos/process.py"""
import glob, os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')
def src(p, mode='RGB'):
    f = sorted(glob.glob(os.path.join(SRC, p))); return ImageOps.exif_transpose(Image.open(f[0])).convert(mode)
def save(im, name, **kw): im.save(os.path.join(HERE, name), **kw); print(name, im.size)
def cutout(im, w):
    from rembg import remove, new_session
    c = remove(im.convert('RGBA'), session=new_session('isnet-general-use')); c = c.crop(c.getchannel('A').getbbox())
    return c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
im = src('ivo_mlady*'); im = ImageEnhance.Contrast(im).enhance(1.06).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
save(im.resize((round(im.width * 900 / im.height), 900), Image.LANCZOS), 'ivo_mlady.jpg', quality=92)
save(cutout(src('ivo_hory*'), 620), 'ivo_hory_cut.png', optimize=True)
save(cutout(src('pes*'), 700), 'pes_cut.png', optimize=True)
save(src('logo_s*', 'RGBA').resize((300, 300), Image.LANCZOS), 'logo_s.png', optimize=True)
m = src('logo_mapy*'); save(m.resize((round(m.width * 220 / m.height), 220), Image.LANCZOS), 'logo_mapy.png', optimize=True)
z = src('logo_zpravy*'); z = z.crop((180, 300, 1480, 560)); save(z.resize((round(z.width * 160 / z.height), 160), Image.LANCZOS), 'logo_zpravy.png', optimize=True)
