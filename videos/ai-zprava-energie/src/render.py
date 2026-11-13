import subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
DUR = 28.0
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
GREY = (120, 120, 120)
YEL = (255, 210, 0)

F = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(F + name, size)
BIG = font("InterDisplay-Bold.otf", 112)
HUGE = font("InterDisplay-Bold.otf", 250)
MID = font("InterDisplay-Bold.otf", 76)
SMALL = font("Inter-Medium.otf", 40)
TINY = font("Inter-Medium.otf", 32)
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 46)

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

def mix(c, a, bg=WHITE):
    return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))

def anim(t, t0, t1=None, d=0.35):
    """alpha + y-offset for element visible from t0 to t1"""
    a = ease((t - t0) / d)
    if t1 is not None:
        a = min(a, ease((t1 - t) / 0.25))
    return a, int((1 - ease((t - t0) / d)) * 40)

def text_c(dr, y, s, f, col, a=1.0, x=None, anchor="mt", spacing=10):
    if a <= 0: return
    x = W // 2 if x is None else x
    dr.multiline_text((x, y), s, font=f, fill=mix(col, a), anchor=anchor if "\n" not in s else ("ma" if anchor == "mt" else anchor), align="center", spacing=spacing)

def logo(dr, cx, cy, a):
    if a <= 0: return
    w, h = 260, 90
    dr.rounded_rectangle((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), 18, fill=mix(BLACK, a))
    r = 22
    lx, rx = cx - 70, cx + 70
    dr.ellipse((lx - r, cy - r, lx + r, cy + r), outline=mix(WHITE, a, mix(BLACK, a)), width=6)
    dr.line((lx + r, cy, rx - r, cy), fill=mix(WHITE, a, mix(BLACK, a)), width=6)
    dr.ellipse((rx - r, cy - r, rx + r, cy + r), fill=mix(YEL, a, mix(BLACK, a)))

def frame(t):
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)
    # top label, always
    text_c(dr, 120, "POKUS  ·  1 ZPRÁVA", TINY, GREY, 1.0)

    # S1 0–4.2: hook + chat box typing
    if t < 4.4:
        a, dy = anim(t, 0, 4.2, d=0.01)
        text_c(dr, 420 + dy, "Kolik energie\nstojí jedna\nzpráva do AI?", BIG, BLACK, a, spacing=14)
        msg = "Ahoj, jak se máš?"
        n = int(max(0, min(len(msg), (t - 0.6) / 1.4 * len(msg))))
        bx0, by0, bx1, by1 = 110, 1150, 970, 1290
        sent = t >= 2.9
        flash = ease((t - 2.9) / 0.15) * ease((3.6 - t) / 0.4) if sent else 0
        fill = mix(YEL, flash) if flash > 0 else WHITE
        dr.rounded_rectangle((bx0, by0, bx1, by1), 70, fill=mix(fill, a), outline=mix(BLACK, a), width=5)
        cur = "▍" if (int(t * 2) % 2 == 0 and not sent) else ""
        dr.text((bx0 + 60, (by0 + by1) // 2), msg[:n] + cur, font=MONO, fill=mix(BLACK, a), anchor="lm")
        # send button
        cx, cy = bx1 - 70, (by0 + by1) // 2
        dr.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=mix(BLACK, a))
        dr.polygon([(cx - 14, cy + 16), (cx, cy - 18), (cx + 14, cy + 16)], fill=mix(WHITE, a, mix(BLACK, a)))
        a2, dy2 = anim(t, 3.1, 4.2)
        text_c(dr, 1400 + dy2, "Odesláno.", SMALL, GREY, a2)

    # S2 4.2–9.6: 0,34 Wh counter
    if 4.2 <= t < 9.8:
        a, dy = anim(t, 4.2, 9.6)
        text_c(dr, 520 + dy, "Jedna zpráva =", MID, BLACK, a)
        v = 0.34 * ease((t - 4.5) / 1.6)
        s = f"{v:.2f}".replace(".", ",")
        text_c(dr, 760 + dy, s, HUGE, BLACK, a)
        text_c(dr, 1030 + dy, "Wh", MID, BLACK, a)
        ul = ease((t - 6.1) / 0.5)
        if ul > 0:
            dr.rectangle((W // 2 - 300, 1140, W // 2 - 300 + int(600 * ul), 1160), fill=mix(YEL, a))
        a3, dy3 = anim(t, 6.6, 9.6)
        text_c(dr, 1260 + dy3, "podle Sama Altmana,\nšéfa OpenAI (2025)", SMALL, GREY, a3, spacing=12)

    # S3 9.6–15.4: oven + bulb
    if 9.6 <= t < 15.6:
        a, dy = anim(t, 9.6, 15.4)
        text_c(dr, 440 + dy, "To je jako trouba\nzapnutá na…", MID, BLACK, a, spacing=12)
        # 1-second bar filling 10.6 -> 11.8
        p = ease((t - 10.6) / 1.2) if t < 11.8 else 1.0
        x0, x1, y = 140, 940, 760
        dr.rounded_rectangle((x0, y, x1, y + 70), 35, outline=mix(BLACK, a), width=5)
        if p > 0.02:
            dr.rounded_rectangle((x0 + 8, y + 8, x0 + 8 + int((x1 - x0 - 16) * p), y + 62), 28, fill=mix(YEL, a))
        sec = min(1.0, max(0.0, (t - 10.6) / 1.2) * 1.0)
        text_c(dr, 870, f"{sec:.1f} s".replace(".", ","), BIG, BLACK, a)
        a4, dy4 = anim(t, 12.4, 15.4)
        text_c(dr, 1150 + dy4, "nebo úsporná žárovka\nna pár minut.", MID, BLACK, a4, spacing=12)

    # S4 15.4–20.4: water
    if 15.4 <= t < 20.6:
        a, dy = anim(t, 15.4, 20.4)
        text_c(dr, 460 + dy, "A voda na chlazení?", MID, BLACK, a)
        a5, dy5 = anim(t, 16.2, 20.4)
        text_c(dr, 640 + dy5, "1/15", HUGE, BLACK, a5)
        text_c(dr, 920 + dy5, "čajové lžičky", MID, BLACK, a5)
        # spoon
        a6, _ = anim(t, 16.8, 20.4)
        if a6 > 0:
            cx, cy = W // 2 - 120, 1220
            dr.ellipse((cx - 90, cy - 55, cx + 90, cy + 55), outline=mix(BLACK, a6), width=6)
            dr.rounded_rectangle((cx + 85, cy - 9, cx + 400, cy + 9), 9, fill=mix(BLACK, a6))
            drop = ease((t - 17.4) / 0.6)
            if drop > 0:
                r = int(14 * drop)
                dr.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(YEL, a6))
        a7, dy7 = anim(t, 17.6, 20.4)
        text_c(dr, 1360 + dy7, "(asi 0,3 ml)", SMALL, GREY, a7)

    # S5 20.4–25.2: multiply
    if 20.4 <= t < 25.4:
        a, dy = anim(t, 20.4, 25.2)
        text_c(dr, 480 + dy, "Málo?", BIG, BLACK, a)
        a8, dy8 = anim(t, 21.2, 25.2)
        text_c(dr, 700 + dy8, "Teď to vynásob\nkaždou zprávou\nod každého člověka.", MID, BLACK, a8, spacing=14)
        a9, dy9 = anim(t, 23.0, 25.2)
        text_c(dr, 1180 + dy9, "Nezávislé odhady pro novější\nmodely vychází i výrazně víc.", SMALL, GREY, a9, spacing=12)

    # S6 25.2–28: CTA
    if t >= 25.2:
        a, dy = anim(t, 25.2)
        text_c(dr, 560 + dy, "Kolik zpráv\ndo AI pošleš\ndenně ty?", BIG, BLACK, a, spacing=14)
        a10, dy10 = anim(t, 25.8)
        if a10 > 0:
            cx, cy = W // 2, 1110 + dy10
            dr.rectangle((cx - 6, cy - 50, cx + 6, cy + 30), fill=mix(YEL, a10))
            dr.polygon([(cx - 36, cy + 20), (cx + 36, cy + 20), (cx, cy + 66)], fill=mix(YEL, a10))
        a11, _ = anim(t, 26.2)
        logo(dr, W // 2, 1560, a11)
        text_c(dr, 1640, "betterdigital.cz", TINY, GREY, a11)

    # bottom source line (constant small)
    if 4.2 <= t < 25.2:
        text_c(dr, 1780, "Zdroj: Sam Altman, blog (6/2025)", TINY, GREY, 0.8)
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f"/home/claude/video/still_{ts}.png")
        sys.exit()
    out = "/home/claude/video/tmp_render.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    sys.exit(p.wait())
