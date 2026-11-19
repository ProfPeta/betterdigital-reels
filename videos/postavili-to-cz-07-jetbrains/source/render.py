import sys, base64, subprocess, pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).parent.resolve()
mode = sys.argv[1]  # "stills" or "video"
FPS, DUR = 30, 56.4

with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto((here / "index.html").as_uri())
    pg.evaluate("window.ready")
    grab = "(t)=>{renderFrame(t);return document.getElementById('c').toDataURL('image/png')}"
    if mode == "stills":
        ts = [float(x) for x in sys.argv[2:]]
        for t in ts:
            d = pg.evaluate(grab, t)
            (here / f"still_{t:05.2f}.png").write_bytes(base64.b64decode(d.split(",")[1]))
    else:
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                               "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                               str(here / "video_noaudio.mp4")], stdin=subprocess.PIPE)
        n = int(DUR * FPS)
        for i in range(n):
            d = pg.evaluate(grab, i / FPS)
            ff.stdin.write(base64.b64decode(d.split(",")[1]))
            if i % 300 == 0:
                print(i, "/", n, flush=True)
        ff.stdin.close(); ff.wait()
    b.close()
