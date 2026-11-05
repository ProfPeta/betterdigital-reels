import subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
DUR = 36.6
ONLY = [float(x) for x in sys.argv[2:]]
OUT = sys.argv[1]
WHITE = (255, 255, 255); BLACK = (12, 12, 12); YEL = (255, 212, 0); GREY = (236, 236, 236); MID = (150, 150, 150)
F = "/usr/share/fonts/opentype/inter/"
_fc = {}
def font(sz, w="Black"):
    k = (int(sz), w)
    if k not in _fc: _fc[k] = ImageFont.truetype(F + f"InterDisplay-{w}.otf", int(sz))
    return _fc[k]

A = "/mnt/user-data/attachments/b6479a3a-ba18-5735-9cdd-9f33a0fbd452/"
SITES = [
    dict(f=A + "525ceaed-image.jpg", url="seznam.cz", name="Seznam", year="1997", now=None,
         hide=[(300, 0, 910, 114), (695, 300, 850, 340), (425, 1078, 785, 1150), (430, 928, 506, 964)]),
    dict(f=A + "54ab8a6f-image.jpg", url="alzasoft.cz", name="Alzasoft", year="2001", now="dnes Alza",
         hide=[(0, 55, 180, 140), (875, 430, 1110, 472)]),
    dict(f=A + "615f9b38-image.jpg", url="skypicker.com", name="Skypicker", year="2014", now="dnes Kiwi.com",
         hide=[(350, 0, 860, 135)]),
]
CX, CW = 72, 936           # browser card
BAR = 84; VIEW_H = 840; CY = 400
for s in SITES:
    im = Image.open(s["f"]).convert("RGB")
    hid = im.copy()
    for (x0, y0, x1, y1) in s["hide"]:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, (x1 - x0) // 22), max(1, (y1 - y0) // 22)), Image.BILINEAR)
        reg2 = small.resize(reg.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(10))
        hid.paste(reg2, (x0, y0))
    sc = CW / im.width
    s["sharp"] = im.resize((CW, int(im.height * sc)), Image.LANCZOS)
    s["hid"] = hid.resize((CW, int(im.height * sc)), Image.LANCZOS)
    s["maxpan"] = max(0, s["sharp"].height - VIEW_H)

def ease(p): p = max(0.0, min(1.0, p)); return 1 - (1 - p) ** 3
def eio(p): p = max(0.0, min(1.0, p)); return p * p * (3 - 2 * p)
def lerp(a, b, p): return a + (b - a) * p

def rmask(size, r):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255); return m

SHADOW = {}
def shadow(size, r=30, blur=28, alpha=60):
    k = (size, r)
    if k not in SHADOW:
        pad = blur * 3
        s = Image.new("L", (size[0] + pad * 2, size[1] + pad * 2), 0)
        ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + size[0], pad + size[1] + 14), r, fill=alpha)
        SHADOW[k] = (s.filter(ImageFilter.GaussianBlur(blur)), pad)
    return SHADOW[k]

def paste_shadowed(fr, im, x, y, r=30, alpha=1.0):
    sh, pad = shadow(im.size, r)
    if alpha < 1: sh = sh.point(lambda v: int(v * alpha))
    fr.paste((0, 0, 0), (int(x) - pad, int(y) - pad), sh)
    m = rmask(im.size, r)
    if alpha < 1: m = m.point(lambda v: int(v * alpha))
    fr.paste(im, (int(x), int(y)), m)

def tw(d, s, f): bb = d.textbbox((0, 0), s, font=f); return bb[2] - bb[0], bb
def text_c(d, y, s, sz, fill=BLACK, w="Black", alpha=1.0, cx=W // 2):
    f = font(sz, w); wdt, bb = tw(d, s, f)
    if alpha < 1: fill = tuple(int(lerp(255, c, alpha)) for c in fill)
    d.text((cx - wdt / 2 - bb[0], y - bb[1]), s, font=f, fill=fill)

def pill(d, y, s, sz, bg=YEL, fg=BLACK, cx=W // 2, padx=30, pady=18, w="Black"):
    f = font(sz, w); wdt, bb = tw(d, s, f); th = bb[3] - bb[1]
    x0 = cx - wdt / 2 - padx
    d.rounded_rectangle((x0, y, x0 + wdt + 2 * padx, y + th + 2 * pady), (th + 2 * pady) // 2, fill=bg)
    d.text((x0 + padx - bb[0], y + pady - bb[1]), s, font=f, fill=fg)

def browser(s, pan, reveal, typed, dim=0.0):
    """Return browser-window image (CW x BAR+VIEW_H)."""
    card = Image.new("RGB", (CW, BAR + VIEW_H), WHITE)
    d = ImageDraw.Draw(card)
    d.rectangle((0, 0, CW, BAR), fill=GREY)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse((28 + i * 34, 30, 50 + i * 34, 52), fill=c)
    d.rounded_rectangle((150, 18, CW - 28, BAR - 18), 24, fill=WHITE)
    f = font(32, "SemiBold")
    if typed <= 0:
        for i in range(3): d.rounded_rectangle((180 + i * 70, 34, 236 + i * 70, 50), 8, fill=(205, 205, 205))
        d.text((420, 26), ".cz" if s["url"].endswith(".cz") else ".com", font=f, fill=MID)
    else:
        n = int(round(len(s["url"]) * min(1, typed)))
        d.text((182, 25), s["url"][:n], font=f, fill=BLACK)
        if typed < 1.3 and int(typed * 8) % 2 == 0:
            x = 182 + d.textlength(s["url"][:n], font=f) + 4; d.line((x, 28, x, 58), fill=BLACK, width=3)
    view = s["sharp"].crop((0, int(pan), CW, int(pan) + VIEW_H)) if reveal >= 1 else (
        s["hid"].crop((0, int(pan), CW, int(pan) + VIEW_H)) if reveal <= 0 else
        Image.blend(s["hid"].crop((0, int(pan), CW, int(pan) + VIEW_H)), s["sharp"].crop((0, int(pan), CW, int(pan) + VIEW_H)), reveal))
    if dim > 0: view = Image.blend(view, Image.new("RGB", view.size, BLACK), dim)
    card.paste(view, (0, BAR))
    d.line((0, BAR, CW, BAR), fill=(215, 215, 215), width=2)
    return card

# ----- timeline (seconds, from voiceover pauses) -----
R = [  # start, ticks(3), reveal, now_line, end
    dict(st=5.96, ticks=(7.06, 7.92, 8.90), rv=10.06, sub=10.97, end=12.92, label="KOLO 1 / 3"),
    dict(st=12.92, ticks=(13.99, 14.79, 15.73), rv=16.85, sub=17.93, end=19.54, label="KOLO 2 / 3"),
    dict(st=19.54, ticks=(20.88, 21.73, 22.68), rv=23.77, sub=24.90, end=29.49, label="KOLO 3 / 3 · TĚŽŠÍ"),
]
T_OUT = 29.49

THUMBS = None
def thumbs():
    global THUMBS
    if THUMBS is None:
        THUMBS = []
        for i, s in enumerate(SITES):
            th = s["hid"].crop((0, 0, CW, min(s["hid"].height, int(CW * 0.95)))).resize((390, int(390 * min(s["hid"].height, int(CW * 0.95)) / CW)), Image.LANCZOS)
            hh = min(s["sharp"].height, int(CW * 0.98)); sharp = s["sharp"].crop((0, 0, CW, hh)).resize((280, int(280 * hh / CW)), Image.LANCZOS)
            THUMBS.append((th, sharp))
    return THUMBS

def intro(fr, t):
    d = ImageDraw.Draw(fr)
    a1 = ease(t / 0.35)
    text_c(d, 330 + (1 - a1) * 24, "Tyhle weby dnes", 84, alpha=a1)
    text_c(d, 430 + (1 - a1) * 24, "vydělávají miliardy.", 84, alpha=a1)
    ths = thumbs()
    angles = [-9, 0, 9]; xs = [W / 2 - 245, W / 2, W / 2 + 245]
    order = [0, 2, 1]
    for i in order:
        th, _ = ths[i]
        p = ease((t - 0.15 - i * 0.12) / 0.5)
        if p <= 0: continue
        fl = math.sin(t * 1.6 + i * 2.1) * 10
        rot = th.convert("RGBA").rotate(angles[i] * p, resample=Image.BICUBIC, expand=True)
        m = rmask(th.size, 24).rotate(angles[i] * p, resample=Image.BICUBIC, expand=True)
        x = xs[i] - rot.width / 2; y = 620 + (1 - p) * 220 + fl + (50 if i != 1 else 0)
        sh = m.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.22 * p))
        fr.paste((0, 0, 0), (int(x), int(y + 18)), sh)
        fr.paste(rot.convert("RGB"), (int(x), int(y)), m.point(lambda v: int(v * p)))
    if t > 2.9:
        a = ease((t - 2.9) / 0.35)
        d = ImageDraw.Draw(fr)
        pill(d, 1300 + (1 - a) * 20, "Poznáš je?", 64)
        text_c(d, 1430, "podle toho, jak vypadaly na začátku", 40, w="SemiBold", fill=(70, 70, 70), alpha=a)

def round_scene(fr, t, k):
    r = R[k]; s = SITES[k]; d = ImageDraw.Draw(fr)
    tl = t - r["st"]
    # enter / exit motion
    enter = ease(tl / 0.5)
    exit_ = eio((t - (r["end"] - 0.4)) / 0.4) if k < 2 else eio((t - (T_OUT - 0.4)) / 0.4)
    dx = (1 - enter) * 1100 - exit_ * 1100
    # chip
    a = ease(tl / 0.35)
    f = font(36); wdt, bb = tw(d, r["label"], f)
    x0 = W / 2 - wdt / 2 - 26 + dx * 0.4
    d.rounded_rectangle((x0, 300, x0 + wdt + 52, 300 + 66), 33, fill=BLACK)
    d.text((x0 + 26 - bb[0], 300 + 33 - (bb[1] + bb[3]) / 2), r["label"], font=f, fill=WHITE)
    # pan: slow scroll down while guessing, back to top on reveal
    guess_p = eio((t - r["st"]) / (r["rv"] - r["st"]))
    pan_down = s["maxpan"] * 0.55 * guess_p
    back = eio((t - r["rv"]) / 0.6)
    pan = lerp(pan_down, 0, back)
    reveal = eio((t - r["rv"]) / 0.45)
    typed = (t - r["rv"] - 0.15) / 0.5 if t > r["rv"] + 0.15 else 0
    # dim during countdown
    cd = 0.0
    if r["ticks"][0] - 0.1 < t < r["rv"]: cd = 0.35 * ease((t - r["ticks"][0] + 0.1) / 0.25)
    if r["rv"] <= t < r["rv"] + 0.3: cd = 0.35 * (1 - (t - r["rv"]) / 0.3)
    card = browser(s, pan, reveal, typed, dim=cd)
    pop = 1 + 0.03 * math.sin(math.pi * max(0, min(1, (t - r["rv"]) / 0.4)))
    if pop != 1:
        card = card.resize((int(card.width * pop), int(card.height * pop)), Image.BICUBIC)
    paste_shadowed(fr, card, CX + dx - (card.width - CW) / 2, CY - (card.height - (BAR + VIEW_H)) / 2, 30)
    d = ImageDraw.Draw(fr)
    # countdown
    for i, tk in enumerate(r["ticks"]):
        nxt = r["ticks"][i + 1] if i < 2 else r["rv"]
        if tk <= t < nxt:
            p = (t - tk)
            sc = 1 + 0.35 * (1 - ease(p / 0.22))
            rad = int(140 * sc); cx, cy = W / 2, CY + BAR + VIEW_H / 2
            d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=YEL)
            n = str(3 - i); f = font(int(190 * sc)); wdt, bb = tw(d, n, f)
            d.text((cx - (bb[0] + bb[2]) / 2, cy - (bb[1] + bb[3]) / 2), n, font=f, fill=BLACK)
    # guess prompt
    if t < r["rv"] and tl > 0.3:
        al = ease((tl - 0.3) / 0.3)
        text_c(d, 1385, "Která firma to je?", 50, alpha=al)
    # reveal labels
    if t >= r["rv"]:
        p = ease((t - r["rv"]) / 0.35)
        txt = f"{s['name']} · {s['year']}"
        f = font(66); wdt, bb = tw(d, txt, f); th_ = bb[3] - bb[1]
        y = 1350 + (1 - p) * 30
        x0 = W / 2 - wdt / 2 - 34 + dx
        d.rounded_rectangle((x0, y, x0 + wdt + 68, y + th_ + 40), (th_ + 40) // 2, fill=YEL)
        d.text((x0 + 34 - bb[0], y + 20 - bb[1]), txt, font=f, fill=BLACK)
        if s["now"] and t >= r["sub"]:
            q = ease((t - r["sub"]) / 0.35)
            text_c(d, 1480 + (1 - q) * 20, "→ " + s["now"], 48, w="Bold", alpha=q, cx=W // 2 + dx)

def outro(fr, t):
    d = ImageDraw.Draw(fr); tl = t - T_OUT
    a = ease(tl / 0.4)
    text_c(d, 330 + (1 - a) * 24, "Kolik jsi dal?", 104, alpha=a)
    ths = thumbs(); names = ["Seznam", "Alza", "Kiwi.com"]
    for i in range(3):
        _, sh = ths[i]
        p = ease((tl - 0.1 - i * 0.12) / 0.45)
        if p <= 0: continue
        x = 72 + i * (280 + 48); y = 530 + (1 - p) * 60
        paste_shadowed(fr, sh, x, y, 22, alpha=p)
        d = ImageDraw.Draw(fr)
        text_c(d, y + sh.height + 30, names[i], 40, cx=int(x + 140), alpha=p)
    if t > 30.5:
        q = ease((t - 30.5) / 0.35)
        d = ImageDraw.Draw(fr)
        f = font(150); s_ = "0 – 3"
        text_c(d, 1030 + (1 - q) * 20, s_, 150, alpha=q)
        pill(d, 1230, "Napiš skóre do komentářů", 48)
    if t > 33.0:
        q = ease((t - 33.0) / 0.35)
        text_c(ImageDraw.Draw(fr), 1370 + (1 - q) * 16, "Příště: weby, které zkrachovaly", 42, w="Bold", alpha=q)
        text_c(ImageDraw.Draw(fr), 1440 + (1 - q) * 16, "Sleduj @betterdigital.cz", 38, w="SemiBold", fill=(90, 90, 90), alpha=q)

def render(t):
    fr = Image.new("RGB", (W, H), WHITE)
    if t < R[0]["st"] + 0.3:
        if t < R[0]["st"]: intro(fr, t)
        else:
            # crossfade intro out while card enters
            tmp = Image.new("RGB", (W, H), WHITE); intro(tmp, t)
            fr = Image.blend(tmp, fr, ease((t - R[0]["st"]) / 0.3))
    if t >= R[0]["st"] and t < T_OUT:
        k = 0 if t < R[1]["st"] else (1 if t < R[2]["st"] else 2)
        # previous card exiting during first 0.0s handled by its own exit window
        if k > 0 and t < R[k]["st"] + 0.01: pass
        round_scene(fr, t, k)
        if k < 2 and t > R[k]["end"] - 0.4:  # next card entering overlaps
            pass
    if T_OUT - 0.4 <= t < T_OUT:
        pass
    if t >= T_OUT: outro(fr, t)
    return fr

if ONLY:
    for t in ONLY: render(t).save(f"p_{t:05.2f}.png")
    sys.exit()
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)):
    p.stdin.write(render(i / FPS).tobytes())
p.stdin.close(); p.wait()
