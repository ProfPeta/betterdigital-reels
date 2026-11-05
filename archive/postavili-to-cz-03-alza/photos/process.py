"""Fotky a loga pro POSTAVILI TO · Česká edice #3 (Alza). Zdroje v photos/src/ nahrál Petr, licence neověřené –
zdroje ani zpracované verze nejsou ve veřejném repu (.gitignore).
  zavoral_kresba.png   kresba Aleše Zavorala (ilustrace z médií), vyříznutá (rembg)
  zavoral_foto.jpg     mladý Aleš Zavoral v prodejně (archivní foto), dorovnané barvy; zavoral_crop.jpg = výřez na něj
  alzak.png            maskot Alzák na průhledném pozadí
  logo_alza.png        logo Alza.cz, pozadí spojené s okrajem průhledné (bílé „a“ uvnitř zůstává)
  logo_a.png           jen čtvercová ikona „a“
usage: python3 -I photos/process.py   (spouštět s -I, zdroje jsou nahrané zvenku)"""
import glob, os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')
def src(pat, mode='RGB'):
    f = sorted(glob.glob(os.path.join(SRC, pat)))
    return ImageOps.exif_transpose(Image.open(f[0])).convert(mode)
def save(im, name, **kw):
    im.save(os.path.join(HERE, name), **kw); print(name, im.size)
def cutout(im, width):
    from rembg import remove, new_session
    cut = remove(im.convert('RGBA'), session=new_session('isnet-general-use'))
    cut = cut.crop(cut.getchannel('A').getbbox())
    return cut.resize((width, round(cut.height * width / cut.width)), Image.LANCZOS)
def bg_alpha(im, thr=40):
    """průhledné jen to bílé pozadí, které souvisí s okrajem obrázku"""
    a = np.asarray(im.convert('RGB')).astype(int); white = (255 - a).max(2) < thr
    lab, _ = ndimage.label(white); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge)); alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.2)))
    out = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), 'RGBA')
    return out.crop(out.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())

kr = src('zavoral_kresba*'); save(cutout(kr, 640), 'zavoral_kresba.png', optimize=True)
fo = src('zavoral_foto*'); fo = ImageEnhance.Contrast(ImageEnhance.Color(fo).enhance(.95)).enhance(1.05)
fo = fo.resize((round(fo.width * 900 / fo.height), 900), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
save(fo, 'zavoral_foto.jpg', quality=92)
save(fo.crop((30, 0, 450, 450)), 'zavoral_crop.jpg', quality=92)
az = src('alzak*', 'RGBA')
if az.getchannel('A').getextrema()[0] < 250: az = az.crop(az.getchannel('A').getbbox())
else: az = cutout(az, az.width)
save(az.resize((600, round(az.height * 600 / az.width)), Image.LANCZOS), 'alzak.png', optimize=True)
lg = bg_alpha(src('logo_alza.webp')); lg = lg.resize((round(lg.width * 260 / lg.height), 260), Image.LANCZOS); save(lg, 'logo_alza.png', optimize=True)
ic = lg.crop((0, 0, round(lg.height * 1.08), lg.height)); ic = ic.crop(ic.getchannel('A').getbbox()); save(ic, 'logo_a.png', optimize=True)
