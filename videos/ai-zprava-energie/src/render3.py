import subprocess, sys
import render2 as V
V.DUR = 29.4
V.MAP = [((0,3.0),(0,4.2)),((3.0,6.3),(4.2,9.6)),((6.3,11.5),(9.6,15.4)),((11.5,15.35),(15.4,20.4)),((20.5,24.8),(20.4,25.2)),((24.8,29.4),(25.2,28.0))]
V.G0, V.G1 = 15.35, 20.5
_g = V.google
def google(t):
    # delay "Skoro stejně" to match VO
    return _g(t)
import render2
src = open('render2.py').read()
W,H,FPS = V.W,V.H,V.FPS
out='tmp3.mp4'
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
for i in range(int(V.DUR*FPS)):
    p.stdin.write(V.frame(i/FPS).tobytes())
p.stdin.close(); sys.exit(p.wait())
