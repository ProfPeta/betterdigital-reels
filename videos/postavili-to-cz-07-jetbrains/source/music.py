import numpy as np, wave
SR=44100; BPM=124; B=60/BPM; DUR=56.4; N=int(SR*DUR)
out=np.zeros(N); rng=np.random.default_rng(7)
def add(sig,t,g=1.0):
    i=int(t*SR); 
    if i>=N: return
    e=min(N,i+len(sig)); out[i:e]+=sig[:e-i]*g
def env(n,a=0.005,d=0.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def kick():
    n=int(.45*SR); t=np.arange(n)/SR; f=45+110*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7)*1.0
def hat(o=False):
    n=int((.18 if o else .05)*SR); x=rng.standard_normal(n); x=np.diff(np.concatenate([[0],x]))
    return x*env(n,.001,.06 if o else .015)*.25
def clap():
    n=int(.25*SR); x=rng.standard_normal(n)
    e=sum(np.roll(env(n,.001,.012),int(k*SR)) for k in (0,.01,.02))+env(n,.001,.08)
    return np.convolve(x,[1,-.9],'same')*e*.22
def saw(f,n):
    t=np.arange(n)/SR; return 2*((t*f)%1)-1
def lp(x,a): 
    y=np.zeros_like(x); s=0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def note(m): return 440*2**((m-69)/12)
chords=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]  # Am F C G
bar=4*B; nbars=int(DUR/bar)+1
# pad (whole song)
for b in range(nbars):
    root,ch=chords[b%4]; n=int(bar*SR)
    sig=sum(saw(note(m+12),n)+saw(note(m+12)*1.006,n) for m in ch)/6
    t=np.arange(n)/SR; sig*=np.minimum(1,t/.3)*np.minimum(1,(bar-t)/.3)
    add(lp(sig,.04),b*bar,.16)
start=1.45  # drums enter after first line opener
breakdown=(39.0,44.3)  # calmer during 2022 part
for b in range(nbars):
    root,ch=chords[b%4]
    for k in range(4):
        t0=b*bar+k*B
        if t0>=DUR-0.3: continue
        calm = breakdown[0]<=t0<breakdown[1]
        if t0>=start and not calm: add(kick(),t0,.9)
        if t0>=start and not calm and k in (1,3): add(clap(),t0,1)
        if t0>=start: add(hat(),t0+B/2,.9 if not calm else .4)
        for s16 in range(4):
            tt=t0+s16*B/4
            if t0>=start and not calm: add(hat(),tt,.35)
            # pluck arp
            m=ch[(k*4+s16)%3]+24+(12 if s16==3 else 0)
            n=int(.18*SR); pl=lp(saw(note(m),n),.18)*env(n,.002,.06)
            add(pl,tt,.10 if not calm else .06)
        # sub bass 8ths
        if t0>=start:
            for h in (0,.5):
                n=int(B/2*SR*.9); tb=np.arange(n)/SR
                bs=np.sin(2*np.pi*note(root-12)*tb)*env(n,.005,.18)
                add(bs,t0+h*B,.35 if not calm else .2)
# impacts at scene cuts
cuts=[5.4,8.6,12.3,15.2,16.4,22.95,25.75,30.25,31.2,33.7,39.0,44.35,49.3]
for c in cuts:
    n=int(.6*SR); t=np.arange(n)/SR
    boom=np.sin(2*np.pi*(40+60*np.exp(-t*20))*t)*np.exp(-t*5)
    add(boom,c,.45)
    # riser whoosh before cut
    n=int(.45*SR); x=lp(rng.standard_normal(n),.25)*np.linspace(0,1,n)**2
    add(x,c-.45,.18)
out=out/np.max(np.abs(out))*.85
with wave.open('music.wav','w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes())
print('ok')
