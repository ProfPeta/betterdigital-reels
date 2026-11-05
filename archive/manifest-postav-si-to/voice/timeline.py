"""Časy scén podle hlasu (voice.wav + segments.json) -> timeline.json pro reel.html a sfx.py.
Hranice uvnitř vět: odhad podle počtu slabik, zpřesněný na nejtišší místo (mezeru mezi slovy) v okolí ±0,18 s.
Střih je 0,04 s před začátkem slova. usage: python3 timeline.py"""
import json, os
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000; LEAD = .04
x, _ = sf.read(os.path.join(HERE, 'voice.wav')); seg = json.load(open(os.path.join(HERE, 'segments.json')))['segments']
w = int(.025 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same'))
st = lambda k: seg[k - 1][0]                                   # začátek segmentu (číslováno od 1)
def cut(k, p):
    a, b = seg[k - 1]; c = a + p * (b - a); lo, hi = max(a + .1, c - .18), min(b - .1, c + .18)
    i0, i1 = int(lo * SR), int(hi * SR); return (i0 + int(np.argmin(e[i0:i1]))) / SR
c = dict(maji=cut(1, .588), sakra=cut(2, .286), nastvani=cut(2, .571), ucila=cut(3, .316), chtel=cut(7, .308),
         ve=cut(11, .167), rucne=cut(11, .667), kdyz=cut(17, .615), tosam=cut(21, .667), weby=cut(22, .333),
         pro=cut(22, .857), kaderni=cut(25, .353), ucetni=cut(25, .588), nebo=cut(25, .765), avers=cut(27, .5),
         tojde=cut(27, .786), postavit=cut(28, .571), nejvic=cut(30, .625))
starts = [('H1', 0), ('H2', c['maji']), ('H3', st(2)), ('H4', c['nastvani']), ('A1', st(3)), ('A2', st(4)), ('A3', st(5)),
          ('B1', st(7)), ('B2', st(8)), ('B3', st(9)), ('C1', st(11)), ('C2', c['rucne']), ('C3', st(15)),
          ('P1', st(17)), ('P2', c['kdyz']), ('P3', st(18)), ('P4', st(19)), ('P5', st(20)), ('P6', st(21)),
          ('V1', st(22)), ('V2', st(23)), ('V3', st(24)), ('Y1', st(25)), ('Y2', c['kaderni']), ('Y3', c['ucetni']),
          ('Y4', c['nebo']), ('Y5', st(26)), ('Y6', st(27)), ('Y7', c['avers']), ('Y8', st(28)), ('Y9', st(29)),
          ('E1', st(30)), ('E2', st(31))]
T = {k: round(max(0, v - LEAD), 3) if k != 'H1' else 0 for k, v in starts}
END = round(seg[30][1] + 2.25, 2)
rel = lambda k, t: round(t - LEAD - T[k], 3)                    # čas uvnitř scény (od jejího začátku)
VT = dict(sakra=rel('H3', c['sakra']), a1l=rel('A1', c['ucila']), a3s=rel('A3', st(6)), b1l=rel('B1', c['chtel']),
          b3s=rel('B3', st(10)), c1l=rel('C1', c['ve']), c2=[0, rel('C2', st(12)), rel('C2', st(13)), rel('C2', st(14))],
          c3s=rel('C3', st(16)), p6=rel('P6', c['tosam']), v1=[0, rel('V1', c['weby']), rel('V1', c['pro'])],
          y7=rel('Y7', c['tojde']), y8=rel('Y8', c['postavit']), e1=rel('E1', c['nejvic']), vo_end=round(seg[30][1], 3))
json.dump({'S': T, 'END': END, 'VT': VT}, open(os.path.join(os.path.dirname(HERE), 'timeline.json'), 'w'), indent=1)
print(json.dumps({'S': T, 'END': END, 'VT': VT}))
