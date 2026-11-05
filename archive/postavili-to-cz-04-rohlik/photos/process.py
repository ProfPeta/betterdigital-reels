"""Fotky a loga pro POSTAVILI TO · Česká edice #4 (Rohlík / Tomáš Čupr). Zdroje v photos/src/ nahrál Petr, licence neověřené –
zdroje ani zpracované verze nejsou ve veřejném repu (.gitignore).
usage: python3 -I photos/process.py"""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')
def src(name, mode='RGB'): return ImageOps.exif_transpose(Image.open(os.path.join(SRC, name))).convert(mode)
def save(im, name, **kw): im.save(os.path.join(HERE, name), **kw); print(name, im.size)
def fit_h(im, h): return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
def sharp(im): return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2))
def bg_alpha(im, thr=30):
    if im.mode == 'RGBA' and im.getchannel('A').getextrema()[0] < 250:
        return im.crop(im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    a = np.asarray(im.convert('RGB')).astype(int); white = (255 - a).max(2) < thr
    lab, _ = ndimage.label(white); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    alpha = np.where(np.isin(lab, list(edge)), 0, 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.0)))
    out = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), 'RGBA')
    return out.crop(out.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())

from rembg import remove, new_session
ses = new_session('isnet-general-use')
cs = src('cupr_smich.png'); save(sharp(fit_h(cs, 900)), 'cupr_portret.jpg', quality=92)
co = src('cupr_okno.webp'); cut = remove(co.convert('RGBA'), session=ses); cut = cut.crop(cut.getchannel('A').getbbox())
save(sharp(fit_h(cut, 1000)), 'cupr_cut.png', optimize=True)
for n, f, h in (('logo_rohlik', 'logo_rohlik.png', 240), ('logo_slevomat', 'logo_slevomat.png', 300), ('logo_damejidlo', 'logo_damejidlo.webp', 160)):
    save(fit_h(bg_alpha(src(f, 'RGBA')), h), n + '.png', optimize=True)
au = src('auta.jpg'); save(sharp(fit_h(au, 760)), 'auta.jpg', quality=90)
