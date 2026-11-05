/* ------------------------------------------------------------ prvky */
const FLAG=w=>`<svg width="${w}" height="${w*2/3}" viewBox="0 0 24 16" style="display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.15)"><rect width="24" height="16" fill="#fff"/><rect y="8" width="24" height="8" fill="#D7141A"/><path d="M0 0 L12 8 L0 16Z" fill="#11457E"/></svg>`;
const BADGE=`<span class="badge">POSTAVILI TO <b>ČESKÁ EDICE #5</b>${FLAG(20)}</span>`;
const PERSON=(c,w=24,dash=0)=>dash?`<svg width="${w}" height="${w*1.25}" viewBox="0 0 30 38"><circle cx="15" cy="9" r="7.5" fill="none" stroke="${c}" stroke-width="1.6" stroke-dasharray="3 3"/><path d="M2 37 C 3 24, 8 20, 15 20 C 22 20, 27 24, 28 37 Z" fill="none" stroke="${c}" stroke-width="1.6" stroke-dasharray="3 3"/></svg>`:`<svg width="${w}" height="${w*1.25}" viewBox="0 0 30 38"><circle cx="15" cy="9" r="8" fill="${c}"/><path d="M1 38 C 2 23, 8 19, 15 19 C 22 19, 28 23, 29 38 Z" fill="${c}"/></svg>`;
const PLANE=`<svg width="34" height="34" viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="#fff"/></svg>`;
const CODE=`void *TrainModelThread(void *id) {
  ...
  // 'g' is the gradient multiplied by the
  // learning rate
  g = (1 - vocab[word].code[d] - f) * alpha;
  // Propagate errors output -> hidden
  for (c = 0; c &lt; layer1_size; c++)
    neu1e[c] += g * syn1[c + l2];
  // Learn weights hidden -> output
  for (c = 0; c &lt; layer1_size; c++)
    syn1[c + l2] += g * neu1[c];`;
const VEC={Kr:'0.62  −0.31  0.88  0.14 …',Mu:'0.51  −0.74  0.12  0.33 …',Ze:'0.47   0.68  0.09  0.29 …'};

/* ------------------------------------------------------------ scény */
const SCN=[
 /* 1 · háček: Zuckerberg, miliony */
 {id:'hook',from:'s1',cls:'blk',cap:1,
  html:()=>`<div class="ph" id="hph" style="left:80px;top:176px;width:380px;height:470px;border-radius:14px;box-shadow:none"><img src="photos/zuck.jpg" style="object-position:50% 12%"></div>
   <div class="abs" style="left:74px;top:132px">${BADGE}</div>
   <div class="abs" id="hch" style="left:96px;top:192px;opacity:0"><span class="chip o">PŘETAHOVAL HO OSOBNĚ</span></div>
   <div class="abs big" id="hm" style="left:96px;top:520px;font-size:62px;color:var(--y);opacity:0;text-shadow:0 4px 30px #000">MILIONY $</div>
   <div class="abs lb" id="hl" style="left:98px;top:586px;color:#fff;opacity:0;text-shadow:0 1px 8px #000">ROČNĚ · SLOVY MIKOLOVA, 2025</div>`,
  anim:(t,s)=>{const u=t-s.t0;$('hph').style.transform=`scale(${(1.08-.08*e5(u/1.2)).toFixed(4)})`;slideX($('hch'),t,ck('s1',0)+.3,-24,.3);
    const M=st('s2')+.05;const m=$('hm');m.style.opacity=t>=M?1:0;if(t>=M)m.style.transform=slamT(t-M,1.25,3);fade($('hl'),t,M+.25)},
  ev:s=>[[ck('s1',0)+.3,'pop2'],[st('s2')+.05,'slam',.22],[st('s2')+.1,'coin']]},

 /* 2 · v Česku 5 let, žádný normální grant */
 {id:'grant',from:'s3',cls:'white',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs" style="left:74px;top:150px;display:flex;align-items:center;gap:10px">${FLAG(30)}<span class="mono" style="font-size:15px;color:#111">V ČESKU</span></div>
   <div class="abs big" id="g5" style="left:74px;top:188px;font-size:124px;color:#0B0B0B;opacity:0">5 LET</div>
   <div class="abs" style="left:74px;top:322px;width:392px;display:flex;gap:10px">${[1,2,3,4,5].map(i=>`<div class="gb" style="width:70px;height:88px;border:2.5px solid #0B0B0B;border-radius:10px;position:relative;opacity:0"><span class="mono" style="position:absolute;left:8px;top:6px;font-size:11px;color:#555">ROK ${i}</span><span class="gx" style="position:absolute;left:0;right:0;top:24px;text-align:center;font-weight:900;font-size:48px;color:var(--red);opacity:0">✕</span></div>`).join('')}</div>
   <div class="card" id="gq" style="left:74px;top:440px;width:392px;padding:16px 18px;background:#0B0B0B;color:#fff;opacity:0;border-radius:14px"><div class="q">„…nemám jediný <span style="color:var(--y)">normální grant.</span>“</div><div class="lb" style="margin-top:8px;color:#bbb">TOMÁŠ MIKOLOV · 2025</div></div>`,
  anim:(t,s)=>{const F=ck('s3',1);const g=$('g5');g.style.opacity=t>=F?1:0;if(t>=F)g.style.transform=slamT(t-F,1.2,3);
    s.el.querySelectorAll('.gb').forEach((e,i)=>{popIn(e,t,F+.08+i*.1,.2,.7);const x=e.querySelector('.gx');popIn(x,t,F+.55+i*.1,.16,1.4)});
    slideIn($('gq'),t,ck('s3',2)+.05,18,.3)},
  ev:s=>[[ck('s3',1),'slam',.2],...[0,1,2,3,4].map(i=>[ck('s3',1)+.55+i*.1,'tick2']),[ck('s3',2)+.05,'pop2']]},

 /* 3 · Tomáš Mikolov */
 {id:'who',from:'s4',cls:'dk',cap:1,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="wph" style="left:100px;top:156px;width:340px;height:410px"><img src="photos/mikolov.jpg" style="object-position:50% 20%"></div>
   <div class="card" id="wnc" style="left:74px;top:510px;padding:12px 18px;opacity:0;border-radius:12px"><div style="font-weight:900;font-size:36px;letter-spacing:-.03em">Tomáš Mikolov</div><div class="mono" style="font-size:12px;color:#555;margin-top:4px">VĚDEC · ROZENÝ V ŠUMPERKU</div></div>`,
  anim:(t,s)=>{const u=t-s.t0;const p=$('wph');p.style.opacity=clamp(u/.15);p.style.transform=`scale(${(1.08-.08*e5(u/.7)).toFixed(4)}) rotate(${lerp(-3,-1,e5(u/.7)).toFixed(2)}deg)`;slideIn($('wnc'),t,s.t0+.12,22,.3)},
  ev:s=>[[s.t0+.12,'pop2']]},

 /* 4 · 2012 Google, Vánoce, slova na čísla */
 {id:'google',from:'s5',cls:'dk',cap:1,year:2012,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="abs big" id="gy" style="left:74px;top:210px;font-size:150px;color:var(--y)">2012</div>
   <div class="abs big" id="gg" style="left:74px;top:178px;font-size:82px;opacity:0">Google</div>
   <div class="abs" id="gx" style="left:76px;top:272px;opacity:0"><span class="chip o">VÁNOCE 2012 · PÍŠE ČLÁNEK</span></div>
   <div class="abs lb" id="gi" style="left:76px;top:322px;color:#9a9a9a;opacity:0">SLOVO → ČÍSLA · ILUSTRACE</div>
   ${[['král',VEC.Kr],['muž',VEC.Mu],['žena',VEC.Ze]].map(([w,v],i)=>`<div class="abs gr" style="left:74px;top:${350+i*86}px;width:392px;height:74px;background:#1d1d1d;border-radius:12px;padding:9px 16px;opacity:0"><div style="font-weight:900;font-size:26px;letter-spacing:-.02em">${w}</div><div class="wd gv" data-v="${v}" style="color:var(--y);margin-top:2px"></div></div>`).join('')}`,
  anim:(t,s)=>{const G=ck('s5',1);$('gy').style.opacity=t<G?1:0;$('gy').style.transform=`scale(${(1.1-.1*e5((t-s.t0)/.4)).toFixed(4)})`;const g=$('gg');g.style.opacity=t>=G?1:0;if(t>=G)g.style.transform=slamT(t-G,1.18,2);slideX($('gx'),t,ck('s5',2),-30,.3);
    const W=ck('s5',4);fade($('gi'),t,W-.1);s.el.querySelectorAll('.gr').forEach((e,i)=>{slideIn(e,t,W-.1+i*.17,14,.25);const v=e.querySelector('.gv');typeTo(v,v.dataset.v,t,W+.05+i*.17,44)})},
  ev:s=>[[ck('s5',1),'slam',.14],[ck('s5',2),'pop2'],[ck('s5',3),'type',1.1],...[0,1,2].map(i=>[ck('s5',4)-.1+i*.17,'pop',i])]},

 /* 5 · král − muž + žena = královna */
 {id:'eq',from:'s6',cls:'white',cap:1,year:2012,tr:'flash',
  html:()=>`<div class="dots"></div>
   <svg class="abs" width="392" height="300" viewBox="0 0 392 300" style="left:74px;top:170px;overflow:visible">
    <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#0B0B0B"/></marker><marker id="ay" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#E0B800"/></marker></defs>
    <line id="e1" x1="298" y1="230" x2="104" y2="230" stroke="#0B0B0B" stroke-width="3.5" marker-end="url(#ah)" opacity="0"/>
    <line id="e2" x1="86" y1="216" x2="86" y2="78" stroke="#0B0B0B" stroke-width="3.5" marker-end="url(#ah)" opacity="0"/>
    <line id="e3" x1="100" y1="60" x2="288" y2="60" stroke="#E0B800" stroke-width="3.5" stroke-dasharray="7 6" marker-end="url(#ay)" opacity="0"/>
    <circle id="dk" cx="310" cy="230" r="11" fill="#0B0B0B" opacity="0"/>
    <circle id="dm" cx="86" cy="230" r="11" fill="#0B0B0B" opacity="0"/>
    <circle id="dz" cx="86" cy="60" r="11" fill="#0B0B0B" opacity="0"/>
    <circle id="dq" cx="310" cy="60" r="17" fill="#FFD400" stroke="#0B0B0B" stroke-width="3" opacity="0"/>
   </svg>
   <div class="abs big tk" data-k="dk" style="left:352px;top:416px;font-size:30px;opacity:0">král</div>
   <div class="abs big tk" data-k="dm" style="left:112px;top:416px;font-size:30px;opacity:0">muž</div>
   <div class="abs big tk" data-k="dz" style="left:96px;top:186px;font-size:30px;opacity:0">žena</div>
   <div class="abs big" id="tq" style="left:310px;top:176px;font-size:32px;padding:3px 9px;background:#FFD400;border-radius:7px;opacity:0">královna</div>
   <div class="abs" id="eqn" style="left:74px;top:476px;width:392px;display:flex;justify-content:space-between;font-weight:900;font-size:27px;letter-spacing:-.03em;opacity:0"><span class="en" data-i="0">král</span><span class="en" data-i="1">−</span><span class="en" data-i="1">muž</span><span class="en" data-i="2">+</span><span class="en" data-i="2">žena</span><span class="en" data-i="3">=</span><span class="en" data-i="3" style="background:#FFD400;padding:0 6px;border-radius:5px">královna</span></div>
   <div class="abs lb" style="left:76px;top:524px;color:#777">ILUSTRACE · ZJEDNODUŠENO</div>`,
  anim:(t,s)=>{const a=ck('s6',0),b=ck('s6',1),c=ck('s6',2),d=st('s7');const on=(id,x)=>{$(id).setAttribute('opacity',t>=x?1:0)};
    on('dk',a);on('dm',b);on('dz',c);on('e1',b);on('e2',c);const Q=d+.3;on('e3',Q-.15);on('dq',Q);
    const q=$('tq');q.style.opacity=t>=Q?1:0;if(t>=Q)q.style.transform=slamT(t-Q,1.3,2);
    s.el.querySelectorAll('.tk').forEach(e=>{const k=e.dataset.k;popIn(e,t,k==='dk'?a:k==='dm'?b:c,.2,.7)});
    $('eqn').style.opacity=t>=a?1:0;s.el.querySelectorAll('.en').forEach(e=>{e.style.opacity=t>=[a,b,c,Q][+e.dataset.i]?1:.14})},
  ev:s=>[[ck('s6',0),'pop',0],[ck('s6',1),'pop',1],[ck('s6',2),'pop',2],[st('s7')+.3,'chime']]},

 /* 6 · konference článek zamítne */
 {id:'reject',from:'s8',cls:'dk',cap:1,year:2013,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="rph" style="left:84px;top:178px;width:372px;height:352px;border-radius:8px"><img src="photos/arxiv.jpg" style="object-position:50% 0"></div>
   <div class="abs" id="rst" style="left:96px;top:320px;opacity:0"><span class="stamp" style="background:rgba(255,255,255,.88);font-size:52px">ZAMÍTNUTO</span></div>
   <div class="abs lb" id="rl" style="left:84px;top:544px;color:#cfcfcf;opacity:0">KONFERENCE ICLR 2013 · ARXIV 1301.3781</div>`,
  anim:(t,s)=>{const u=t-s.t0;const p=$('rph');p.style.opacity=clamp(u/.15);p.style.transform=`translateY(${(20*(1-e5(u/.4))).toFixed(1)}px) rotate(${lerp(2.5,-1,e5(u/.5)).toFixed(2)}deg)`;
    stampIn($('rst'),t,ck('s8',1)-.05,-9,1.7);fade($('rl'),t,s.t0+.2)},
  ev:s=>[[s.t0+.02,'paper'],[ck('s8',1)-.05,'stamp',.3]]},

 /* 7 · word2vec */
 {id:'w2v',from:'s9',cls:'dk',cap:1,year:2013,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="abs" id="wcode" style="left:74px;top:176px;width:392px;height:230px;background:#141414;border:1px solid #333;border-radius:12px;overflow:hidden;padding:12px 14px"><div class="lb" style="color:#8a8a8a;margin-bottom:8px;font-size:10px">word2vec.c · © 2013 GOOGLE · APACHE 2.0</div><div style="height:178px;overflow:hidden"><pre id="wpre" style="font-size:12px">${CODE}</pre></div></div>
   <div class="abs big" id="wn" style="left:74px;top:422px;font-size:76px;color:var(--y);opacity:0">word2vec</div>
   <div class="abs" id="wc" style="left:76px;top:504px;opacity:0"><span class="big" id="wcn" style="font-size:40px;font-variant-numeric:tabular-nums">0</span><span class="big" style="font-size:24px"> citací</span></div>
   <div class="abs lb" id="wcl" style="left:76px;top:552px;color:#bbb;font-size:11px;opacity:0">NAVAZUJÍCÍ ČLÁNEK · STAV 2023</div>`,
  anim:(t,s)=>{const u=t-s.t0;slideIn($('wcode'),t,s.t0,18,.3);$('wpre').style.transform=`translateY(${(-5*Math.min(u,5)).toFixed(1)}px)`;
    const N=ck('s9',1);const n=$('wn');n.style.opacity=t>=N?1:0;if(t>=N)n.style.transform=slamT(t-N,1.2,2);
    const C=ck('s9',2);fade($('wc'),t,C-.05,.12);fade($('wcl'),t,C+.1);const q=eo((t-C)/1.2);$('wcn').textContent=(q>=1?'40 000+':fmt(40000*q));},
  ev:s=>[[ck('s9',1),'slam',.16],[ck('s9',2),'count',1.2]]},

 /* 8 · ChatGPT nevymyslel, ale stojí na těchto principech */
 {id:'gpt',from:'s10',cls:'white',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   ${[['ChatGPT','#fff','#0B0B0B',0],['JAZYKOVÉ MODELY','#fff','#0B0B0B',1],['SLOVA JAKO ČÍSLA','#FFD400','#0B0B0B',2]].map(([l,bg,c,i])=>`<div class="abs ll" data-i="${i}" style="left:74px;top:${[176,292,408][i]}px;width:392px;height:${i?96:104}px;background:${bg};border:3px solid #0B0B0B;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:${i?30:56}px;letter-spacing:-.03em;color:${c};opacity:0">${l}</div>`).join('')}
   <div class="abs" id="gnv" style="left:240px;top:150px;opacity:0"><span class="chip" style="background:var(--red);font-size:14px">TOHLE NEVYMYSLEL</span></div>
   <div class="abs lb" id="gba" style="left:76px;top:516px;color:#555;opacity:0">ZÁKLAD · WORD2VEC, 2013</div>`,
  anim:(t,s)=>{const L=s.el.querySelectorAll('.ll');const A=s.t0+.02;L[0].style.opacity=t>=A?1:0;if(t>=A)L[0].style.transform=slamT(t-A,1.12,2);
    popIn($('gnv'),t,ck('s10',0)+.75,.2,.7);const P=st('s11')+.08;slideIn(L[2],t,P+.2,20,.28);slideIn(L[1],t,P+.55,20,.28);fade($('gba'),t,P+.4)},
  ev:s=>[[ck('s10',0)+.75,'pop2'],[st('s11')+.28,'thunk'],[st('s11')+.63,'pop',0]]},

 /* 9 · 2020 návrat na ČVUT, vlastní tým */
 {id:'back',from:'s12',cls:'dk',cap:1,year:2020,tr:'scan',
  html:()=>`<div class="dots"></div>
   <svg class="abs" width="540" height="240" style="left:0;top:170px"><path d="M 90 190 Q 260 -30 440 170" fill="none" stroke="rgba(255,212,0,.25)" stroke-width="2" stroke-dasharray="6 7"/><path id="barc" d="M 90 190 Q 260 -30 440 170" fill="none" stroke="#FFD400" stroke-width="3"/><circle cx="90" cy="190" r="7" fill="#fff"/><circle cx="440" cy="170" r="7" fill="#FFD400"/></svg>
   <div class="abs" id="bpl" style="left:0;top:0;opacity:0">${PLANE}</div>
   <div class="abs" style="left:74px;top:374px"><span class="chip w">USA</span></div>
   <div class="abs" id="bcz" style="left:360px;top:354px;opacity:0"><span class="chip o">PRAHA · ČVUT</span></div>
   <div class="abs lb" id="btl" style="left:76px;top:446px;color:#bbb;opacity:0">VLASTNÍ VÝZKUMNÝ TÝM</div>
   <div class="abs" style="left:74px;top:470px;display:flex;gap:18px">${[0,1,2,3,4].map(i=>`<div class="bp" style="opacity:0">${i?PERSON('#8c8c8c',52,1):PERSON('#FFD400',52)}</div>`).join('')}</div>`,
  anim:(t,s)=>{const P=$('barc');const L=P.getTotalLength();const A=s.t0+.05,B=en('s12')-.1;const p=eio((t-A)/(B-A));P.style.strokeDasharray=L;P.style.strokeDashoffset=(L*(1-p)).toFixed(1);
    const a=P.getPointAtLength(L*p),b=P.getPointAtLength(Math.min(L,L*p+2));const ang=Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI+90;const pl=$('bpl');pl.style.opacity=t>=A&&p<1?1:0;pl.style.transform=`translate(${(a.x-17).toFixed(1)}px,${(a.y+170-17).toFixed(1)}px) rotate(${ang.toFixed(1)}deg)`;
    popIn($('bcz'),t,B-.05,.25,.6);fade($('btl'),t,st('s13'));s.el.querySelectorAll('.bp').forEach((e,i)=>popIn(e,t,st('s13')+.05+i*.12,.2,.5))},
  ev:s=>[[s.t0+.05,'jet',en('s12')-s.t0-.15],[en('s12')-.15,'pop2'],...[0,1,2,3,4].map(i=>[st('s13')+.05+i*.12,'pop',i])]},

 /* 10 · jedna velká nula */
 {id:'zero',from:'s14',cls:'dk',cap:1,year:2020,tr:'glitch',
  html:()=>`<div class="dots"></div>
   <div class="abs" id="zch" style="left:74px;top:174px;opacity:0"><span class="chip w">Z VEŘEJNÝCH PENĚZ · PO 5 LETECH</span></div>
   <div class="abs" id="zp" style="left:74px;top:300px;display:flex;gap:18px;opacity:0">${[0,1,2,3,4].map(i=>i?PERSON('#8c8c8c',64,1):PERSON('#FFD400',64)).join('')}</div>
   <div class="abs big" id="z0" style="left:0;right:0;top:206px;text-align:center;font-size:330px;color:var(--y);opacity:0">0</div>
   <div class="abs" id="zq" style="left:74px;top:540px;width:392px;opacity:0"><span class="q">„jedna velká nula“</span><span class="lb" style="display:block;margin-top:4px;color:#bbb">TOMÁŠ MIKOLOV · 2025</span></div>`,
  anim:(t,s)=>{slideX($('zch'),t,s.t0+.05,-24,.3);const Z=ck('s14',3)+.2;$('zp').style.opacity=t<Z?clamp((t-s.t0-.1)/.25).toFixed(3):0;const z=$('z0');z.style.opacity=t>=Z?1:0;if(t>=Z)z.style.transform=slamT(t-Z,1.3,3);fade($('zq'),t,Z+.3)},
  ev:s=>[[s.t0+.05,'pop2'],[ck('s14',3)+.2,'slam',.3]]},

 /* 11 · Singapur */
 {id:'sg',from:'s15',cls:'yel',cap:1,tr:'flash',
  html:()=>`<div class="abs big" style="left:74px;top:156px;font-size:64px" id="sn">Singapur</div>
   <div class="abs lb" id="sd" style="left:76px;top:224px;color:#333;opacity:0">ŽÁDOST · LISTOPAD 2024 · SLOVY MIKOLOVA</div>
   <svg class="abs" id="sc" width="130" height="130" viewBox="0 0 130 130" style="left:74px;top:266px;opacity:0"><circle cx="65" cy="65" r="58" fill="#fff" stroke="#0B0B0B" stroke-width="6"/><line id="shh" x1="65" y1="65" x2="65" y2="35" stroke="#0B0B0B" stroke-width="7" stroke-linecap="round"/><line id="shm" x1="65" y1="65" x2="65" y2="20" stroke="#0B0B0B" stroke-width="4" stroke-linecap="round"/></svg>
   <div class="abs big" id="sh" style="left:224px;top:296px;font-size:44px;line-height:1;white-space:normal;width:240px;opacity:0">pár hodin práce</div>
   <div class="abs lb" id="sl" style="left:76px;top:424px;color:#333;opacity:0">ZHRUBA</div>
   <div class="abs big" id="sm" style="left:74px;top:442px;font-size:92px;font-variant-numeric:tabular-nums;opacity:0">0 MIL. $</div>
   <div class="abs lb" id="sp" style="left:76px;top:540px;color:#333;opacity:0">GRANT NA PRVNÍ POKUS</div>`,
  anim:(t,s)=>{popIn($('sn'),t,ck('s15',1),.22,.8);fade($('sd'),t,ck('s15',1)+.15);const H=st('s16');popIn($('sc'),t,H,.22,.7);fade($('sh'),t,H+.05,.15);
    const r=clamp((t-H)/1.6)*720;$('shm').setAttribute('transform',`rotate(${r.toFixed(1)} 65 65)`);$('shh').setAttribute('transform',`rotate(${(r/12).toFixed(1)} 65 65)`);
    const M=ck('s16',2)-.05;fade($('sl'),t,ck('s16',1)-.05);const m=$('sm');m.style.opacity=t>=M?1:0;m.textContent=Math.round(3*eo((t-M)/.7))+' MIL. $';if(t>=M+.7)m.style.transform=slamT(t-M-.7,1.1,2);fade($('sp'),t,M+.8)},
  ev:s=>[[ck('s15',1),'pop2'],[st('s16'),'tickdown',1.3],[ck('s16',2)-.05,'count',.7],[ck('s16',2)+.65,'coin']]},

 /* 12 · 2025 BottleCap, investuje zakladatel Seznamu */
 {id:'bc',from:'s17',cls:'dk',cap:1,year:2025,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="cph" style="left:74px;top:172px;width:392px;height:268px"><img src="photos/tym.jpg" style="object-position:40% 50%"><span class="lbl">TÝM BOTTLECAP AI · ARCHIVNÍ FOTO</span></div>
   <div class="abs big" id="cn" style="left:74px;top:452px;font-size:60px;color:var(--y);opacity:0">BottleCap AI</div>
   <div class="card" id="cl" style="left:74px;top:526px;width:392px;padding:10px 16px;border-radius:12px;opacity:0"><div style="font-weight:900;font-size:24px;letter-spacing:-.025em">+ Ivo Lukačovič</div><div class="lb" style="color:#555;margin-top:2px">ZAKLADATEL SEZNAMU · INVESTICE 2026</div></div>`,
  anim:(t,s)=>{const u=t-s.t0;const p=$('cph');p.style.opacity=clamp(u/.15);$('cph').querySelector('img').style.transform=`scale(${(1.1-.05*Math.min(u,4)/4).toFixed(4)})`;
    const N=ck('s17',2)-.03;const n=$('cn');n.style.opacity=t>=N?1:0;if(t>=N)n.style.transform=slamT(t-N,1.15,2);slideIn($('cl'),t,ck('s18',1)-.05,18,.3)},
  ev:s=>[[ck('s17',2)-.03,'slam',.14],[ck('s18',1)-.05,'pop2']]},

 /* 13 · medaile */
 {id:'medal',from:'s19',cls:'dk',cap:1,year:2026,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="mph" style="left:74px;top:172px;width:392px;height:286px"><img src="photos/medaile.jpg" style="object-position:50% 30%"><span class="lbl">PRAŽSKÝ HRAD · 28. 10. 2026</span></div>
   <div class="card" id="mc" style="left:74px;top:476px;width:392px;padding:13px 16px;background:#FFD400;border-radius:12px;opacity:0"><div style="font-weight:900;font-size:33px;letter-spacing:-.03em">Medaile Za zásluhy</div><div class="lb" style="color:#333;margin-top:3px">OBLAST VĚDY A TECHNIKY</div></div>`,
  anim:(t,s)=>{const u=t-s.t0;const p=$('mph');p.style.opacity=clamp(u/.15);p.querySelector('img').style.transform=`scale(${(1.03+.05*Math.min(u,5)/5).toFixed(4)})`;slideIn($('mc'),t,ck('s19',2)-.05,18,.3)},
  ev:s=>[[ck('s19',2)-.05,'chime']]},

 /* 14 · peníze ne, medaile ano */
 {id:'punch',from:'s20',cls:'white',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs" id="p1" style="left:74px;top:210px;width:392px;height:128px;border:3px solid #0B0B0B;border-radius:16px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;opacity:0"><span class="big" style="font-size:46px;white-space:normal;line-height:1">Peníze<br>na tým</span><span class="big" style="font-size:86px;color:var(--red)">✕</span></div>
   <div class="abs" id="p2" style="left:74px;top:366px;width:392px;height:128px;background:#FFD400;border:3px solid #0B0B0B;border-radius:16px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;opacity:0"><span class="big" style="font-size:46px">Medaile</span><span class="big" style="font-size:86px">✓</span></div>`,
  anim:(t,s)=>{const a=s.t0+.04;const p=$('p1');p.style.opacity=t>=a?1:0;if(t>=a)p.style.transform=slamT(t-a,1.1,2);const b=st('s21')+.02;const q=$('p2');q.style.opacity=t>=b?1:0;if(t>=b)q.style.transform=slamT(t-b,1.12,2)},
  ev:s=>[[s.t0+.04,'bonk'],[st('s21')+.02,'coin']]},

 /* 15 · výzva */
 {id:'cta',from:'s22',cls:'white',cap:0,tr:'flash',
  html:()=>`<div class="abs" style="left:74px;top:150px">${BADGE}</div>
   <div class="abs" id="cq" style="left:74px;top:204px;width:400px;font-weight:900;font-size:50px;letter-spacing:-.04em;line-height:1.02;color:#111">Měl se vracet do Česka?</div>
   ${[['ANO','#0B0B0B','#FFD400'],['NE','#fff','#E5322D']].map(([a,c,bg],i)=>`<div class="abs co" data-i="${i}" style="left:74px;top:${352+i*74}px;width:392px;height:62px;border:2.5px solid #111;border-radius:14px;background:${bg};display:flex;align-items:center;padding:0 20px;opacity:0"><span style="font-weight:900;font-size:30px;letter-spacing:-.03em;color:${c}">${a}</span></div>`).join('')}
   <div class="abs" id="ccc" style="left:74px;top:518px;width:392px;height:56px;border-radius:999px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:800;font-size:21px;opacity:0">Napiš to do komentářů 👇</div>
   <div class="abs" id="csg" style="left:74px;top:604px;display:flex;align-items:center;gap:12px;opacity:0"><div style="background:#111;border-radius:8px;padding:8px 11px;display:flex">${uzel(18,'#fff')}</div><div style="font-weight:800;font-size:19px;color:#111;letter-spacing:-.03em">Better Digital</div></div>`,
  anim:(t,s)=>{slideIn($('cq'),t,s.t0+.05,16,.3);s.el.querySelectorAll('.co').forEach(e=>{const i=+e.dataset.i;slideX(e,t,ck('s23',i)+(i?.05:.1),-40,.3)});popIn($('ccc'),t,ck('s23',1)+.5,.25,.7);slideIn($('csg'),t,ck('s23',1)+.9,10)},
  ev:s=>[[s.t0+.05,'whoosh'],[ck('s23',0)+.1,'pop',0],[ck('s23',1)+.05,'pop',1],[ck('s23',1)+.5,'notif']]},
];
