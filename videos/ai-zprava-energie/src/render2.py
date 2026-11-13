import subprocess, sys
from PIL import ImageDraw
import render as R
from render import W, H, FPS, BLACK, GREY, YEL, WHITE, HUGE, MID, BIG, SMALL, TINY, anim, text_c, mix, ease

DUR = 29.0
# new segment -> old segment (linear remap)
MAP = [((0, 3.8), (0, 4.2)), ((3.8, 8.4), (4.2, 9.6)), ((8.4, 13.4), (9.6, 15.4)),
       ((13.4, 17.4), (15.4, 20.4)), ((21.6, 25.8), (20.4, 25.2)), ((25.8, 29.0), (25.2, 28.0))]
G0, G1 = 17.4, 21.6

def google(t):
    from PIL import Image
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)
    text_c(dr, 120, "POKUS  ·  1 ZPRÁVA", TINY, GREY, 1.0)
    a, dy = anim(t, G0, G1)
    text_c(dr, 420 + dy, "Pro srovnání:\njedno hledání\nna Googlu (2011)", MID, BLACK, a, spacing=14)
    # two bars
    p = ease((t - (G0 + 0.6)) / 0.9)
    rows = [("Google", 0.30, 820), ("AI zpráva", 0.34, 1010)]
    for label, v, y in rows:
        dr.text((140, y), label, font=SMALL, fill=mix(BLACK, a), anchor="lm")
        x0 = 140; maxw = 800
        w = int(maxw * (v / 0.34) * p)
        dr.rounded_rectangle((x0, y + 40, x0 + max(w, 1), y + 110), 14,
                             fill=mix(YEL if label == "AI zpráva" else BLACK, a))
        dr.text((x0 + max(w, 1) - 20, y + 75), f"{v:.2f} Wh".replace(".", ","), font=SMALL,
                fill=mix(BLACK if label == "AI zpráva" else WHITE, a * ease((t - (G0 + 1.4)) / 0.3),
                         YEL if label == "AI zpráva" else BLACK), anchor="rm")
    a2, dy2 = anim(t, G0 + 3.6, G1)
    text_c(dr, 1260 + dy2, "Skoro stejně.", BIG, BLACK, a2)
    text_c(dr, 1780, "Zdroje: S. Altman (6/2025), Google (2011)", TINY, GREY, 0.8)
    return im

def frame(t):
    if G0 <= t < G1:
        im = google(t)
    else:
        for (n0, n1), (o0, o1) in MAP:
            if n0 <= t < n1 or (t >= n1 and n1 == DUR):
                im = R.frame(o0 + (t - n0) / (n1 - n0) * (o1 - o0))
                break
    dr = ImageDraw.Draw(im)
    dr.rectangle((0, 0, W, 14), fill=(235, 235, 235))
    dr.rectangle((0, 0, int(W * t / DUR), 14), fill=YEL)
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f"/home/claude/video/s2_{ts}.png")
        sys.exit()
    out = "/home/claude/video/tmp2.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    sys.exit(p.wait())
