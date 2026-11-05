"""Retro (1bit Mac) varianty fotek pro Postavili to #01. Zdroje v photos/src/, výstup do photos/.
  j84_win.png     Jobs s Macem (1984), čtvercový ořez, 1bit Atkinson, 456×456 (1 tečka = 1 CSS px)
  j84_cut.png     totéž vyříznuté z pozadí (rembg), 1bit uvnitř, bílý „samolepkový“ okraj, průhledné okolí
  jobsgates_1b.png Jobs a Gates (2007), 1bit, 456×312
  jobs_mos_{20,10,5}.png  Jobs 2010 jako mozaika (velikost bloku v CSS px) pro „načítání“ fotky
  jobs_1b.png     Jobs 2010, 1bit (tečka 1 CSS px), 1080×1350 se zachovanou průhledností
  logo.png        duhové logo 1977 (obrázek od Petra), zmenšené, s průhledností
Atkinsonův dithering = ten, který používal původní Macintosh (6/8 chyby do 6 sousedů).
Zdroje jobs_1984.* a apple_logo_1977.* nejsou ve veřejném repu (licence) – bez nich se příslušné výstupy nepřepíšou.
usage: python3 -I retro.py   (spouštět s -I, zdroje jsou nahrané zvenku)"""
import glob, os
import numpy as np
from PIL import Image, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')


def src(pat):
    f = sorted(glob.glob(os.path.join(SRC, pat)))
    if not f: print(f'chybí zdroj {pat} – nechávám původní výstupy'); return None
    return ImageOps.exif_transpose(Image.open(f[0]))


def prep(gray, lo=2, hi=98, gamma=.9, sharpen=True):
    """kontrast pro 1bit: percentilové roztažení, gamma, doostření"""
    g = np.asarray(gray).astype(float)
    a, b = np.percentile(g, lo), np.percentile(g, hi)
    g = np.clip((g - a) / max(1, b - a), 0, 1) ** gamma
    im = Image.fromarray((g * 255).astype(np.uint8), 'L')
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=90, threshold=2)) if sharpen else im


def atkinson(gray):
    g = np.asarray(gray).astype(float) / 255; H, W = g.shape
    g = np.pad(g, ((0, 2), (1, 2)))
    for y in range(H):
        row = g[y]
        for x in range(1, W + 1):
            o = row[x]; n = 1. if o >= .5 else 0.; row[x] = n; e = (o - n) / 8
            if e:
                row[x + 1] += e; row[x + 2] += e
                g[y + 1, x - 1] += e; g[y + 1, x] += e; g[y + 1, x + 1] += e; g[y + 2, x] += e
    return g[:H, 1:W + 1] >= .5                                  # True = bílá


def onebit(mask_white, alpha=None, ink=(17, 17, 17), paper=(255, 255, 255)):
    H, W = mask_white.shape; out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = np.where(mask_white[..., None], paper, ink); out[..., 3] = 255 if alpha is None else alpha
    return Image.fromarray(out, 'RGBA')


def save(im, name):
    im.save(os.path.join(HERE, name), optimize=True); print(name, im.size)


def jobs1984():
    im = src('jobs_1984*')
    if im is None: return
    im = im.convert('RGB')                                      # 2000×1328
    sq = im.crop((340, 30, 1440, 1130)).resize((456, 456), Image.LANCZOS)
    save(onebit(atkinson(prep(sq.convert('L'), gamma=.85))), 'j84_win.png')
    # výřez: osoba + Mac
    from rembg import remove, new_session
    cut = remove(im.convert('RGBA'), session=new_session('isnet-general-use'))
    a = np.asarray(cut)[..., 3]
    a = np.where(a > 128, 255, 0).astype(np.uint8)              # tvrdá maska (1bit styl)
    m = Image.fromarray(a, 'L').filter(ImageFilter.MedianFilter(5))
    bb = m.getbbox(); W = 400
    s = W / (bb[2] - bb[0]); H = round((bb[3] - bb[1]) * s)
    rgb = im.crop(bb).resize((W, H), Image.LANCZOS); m = m.crop(bb).resize((W, H), Image.NEAREST)
    g = prep(rgb.convert('L'), gamma=.85)
    g = Image.composite(g, Image.new('L', g.size, 255), m)     # mimo osobu bílá (ať dithering nekreslí okraj)
    white = atkinson(g)
    PAD = 10; big = Image.new('L', (W + 2 * PAD, H + 2 * PAD), 0); big.paste(m, (PAD, PAD))
    outline = big.filter(ImageFilter.MaxFilter(13))             # bílý okraj ~6 px
    wb = np.ones((H + 2 * PAD, W + 2 * PAD), bool); wb[PAD:PAD + H, PAD:PAD + W] = white | (np.asarray(m) < 128)
    save(onebit(wb, np.asarray(outline)), 'j84_cut.png')


def jobsgates():
    im = src('jobs_gates*')
    if im is None: return
    im = im.convert('L').crop((330, 280, 1730, 1240)).resize((456, 312), Image.LANCZOS)
    save(onebit(atkinson(prep(im, gamma=.8))), 'jobsgates_1b.png')


def jobs2010():
    im = Image.open(os.path.join(HERE, 'jobs_bw.png')).convert('RGBA')   # 1080×1350, z process.py
    a = np.asarray(im).astype(float); al = a[..., 3:] / 255
    for blk in (20, 10, 5):                                     # CSS px (obrázek je 2× hustší)
        b = blk * 2; w, h = im.width // b, im.height // b
        pm = Image.fromarray((np.concatenate([a[..., :3] * al, al * 255], -1)).astype(np.uint8), 'RGBA')
        sm = np.asarray(pm.resize((w, h), Image.BOX)).astype(float)
        sa = np.maximum(sm[..., 3:], 1) / 255; sm[..., :3] = np.clip(sm[..., :3] / sa, 0, 255)
        up = Image.fromarray(sm.astype(np.uint8), 'RGBA').resize((w * b, h * b), Image.NEAREST)
        c = Image.new('RGBA', im.size, (0, 0, 0, 0)); c.paste(up, (0, 0)); save(c, f'jobs_mos_{blk}.png')
    half = im.resize((540, 675), Image.LANCZOS)
    g = Image.fromarray((np.asarray(half)[..., :3] @ [.299, .587, .114]).astype(np.uint8), 'L')
    w1 = atkinson(prep(g, gamma=.9)); al1 = np.asarray(half)[..., 3]
    save(onebit(w1, np.where(al1 > 100, 255, 0).astype(np.uint8), paper=(236, 231, 220)), 'jobs_1b.png')


def logo():
    im = src('apple_logo_1977*')
    if im is None: return
    im = im.convert('RGBA'); h = 480
    save(im.resize((round(im.width * h / im.height), h), Image.LANCZOS), 'logo.png')


if __name__ == '__main__':
    jobs1984(); jobsgates(); jobs2010(); logo()
