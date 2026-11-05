"""Fotky pro POSTAVILI TO #03 · Jensen Huang / Nvidia. Zdroje v photos/src/ nahrál Petr (vypadají jako Wikimedia Commons,
licence neověřené) – zdroje ani zpracované verze nejsou ve veřejném repu (.gitignore).
  huang.png        Jensen Huang v kožené bundě, vyříznutý (rembg)
  huang_bw.jpg     portrét, černobílý výřez obličeje (hook)
  oneida.jpg       vstup Oneida Baptist Institute
  dennys.jpg       cedule Denny's
  sega.png         Sega Saturn na průhledném pozadí
  riva.jpg         čip RIVA 128 (čtverec)
  hq.jpg           sídlo Nvidie Endeavor
usage: python3 -I photos/process.py"""
import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')
def src(name, mode='RGB'):
    return ImageOps.exif_transpose(Image.open(os.path.join(SRC, name))).convert(mode)
def save(im, name, **kw):
    im.save(os.path.join(HERE, name), **kw); print(name, im.size)
def fit_h(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
def sharp(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2))

# Huang – výřez postavy
from rembg import remove, new_session
hu = src('huang.jpg')
cut = remove(hu.convert('RGBA'), session=new_session('isnet-general-use'))
cut = cut.crop(cut.getchannel('A').getbbox())
save(sharp(fit_h(cut, 1100)), 'huang.png', optimize=True)
# portrét pro hook: obličej + ramena, černobíle se zvýšeným kontrastem
w, h = hu.size
face = hu.crop((int(w * .16), int(h * .17), int(w * .80), int(h * .62)))
bw = ImageEnhance.Contrast(ImageOps.grayscale(face)).enhance(1.25)
save(sharp(fit_h(bw.convert('RGB'), 900)), 'huang_bw.jpg', quality=92)

on = src('oneida.jpg'); save(sharp(fit_h(on, 760)), 'oneida.jpg', quality=90)
dn = src('dennys.jpg'); w, h = dn.size
dn = dn.crop((int(w * .26), 0, int(w * .74), int(h * .72)))
save(sharp(fit_h(dn, 900)), 'dennys.jpg', quality=90)

# Sega Saturn: bílé pozadí souvislé s okrajem -> průhledné
sg = src('sega_saturn.jpg'); a = np.asarray(sg).astype(int); white = (255 - a).max(2) < 18
lab, _ = ndimage.label(white); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
alpha = np.where(np.isin(lab, list(edge)), 0, 255).astype(np.uint8)
alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2)))
sg = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), 'RGBA'); sg = sg.crop(sg.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
save(sg.resize((760, round(sg.height * 760 / sg.width)), Image.LANCZOS), 'sega.png', optimize=True)

rv = src('riva128.jpg'); save(sharp(rv.resize((820, 820), Image.LANCZOS)), 'riva.jpg', quality=90)
hq = src('hq_endeavor.jpg'); hq = ImageEnhance.Color(hq).enhance(.9); save(sharp(fit_h(hq, 900)), 'hq.jpg', quality=90)
