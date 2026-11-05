/* ------------------------------------------------------------ prvky */
const FLAG=w=>`<svg width="${w}" height="${w*2/3}" viewBox="0 0 24 16" style="display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.15)"><rect width="24" height="16" fill="#fff"/><rect y="8" width="24" height="8" fill="#D7141A"/><path d="M0 0 L12 8 L0 16Z" fill="#11457E"/></svg>`;
/* český rohlík (obecný pečivo, kreslený kódem) s čokoládou */
const ROLL=(w,choc=1)=>`<svg width="${w}" height="${w*.42}" viewBox="0 0 300 126" style="display:block;overflow:visible">
  <path d="M14 92 C 40 18, 260 18, 286 92 C 250 70, 50 70, 14 92 Z" fill="#E9A54A"/>
  <path d="M14 92 C 50 74, 250 74, 286 92 C 260 116, 40 116, 14 92 Z" fill="#C9822F"/>
  ${[0,1,2,3,4,5].map(i=>{const x=58+i*37;return `<path d="M${x} ${42-Math.sin(i/5*Math.PI)*8} C ${x+14} 60, ${x+10} 80, ${x-4} 92" stroke="#B9732A" stroke-width="5" fill="none" stroke-linecap="round"/>`}).join('')}
  <path d="M40 54 C 90 30, 210 30, 260 54" stroke="rgba(255,255,255,.35)" stroke-width="6" fill="none" stroke-linecap="round"/>
  ${choc?`<ellipse cx="286" cy="90" rx="13" ry="10" fill="#5a3420"/><path d="M290 96 C 296 106, 292 116, 286 118 C 282 112, 284 104, 290 96 Z" fill="#5a3420"/>`:''}</svg>`;
const COIN=(w=40)=>`<svg width="${w}" height="${w}" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#F2C94C" stroke="#c99a1c" stroke-width="3"/><text x="20" y="27" text-anchor="middle" font-family="IT" font-weight="900" font-size="18" fill="#9a7210">Kč</text></svg>`;
const PERSON=(c,w=24)=>`<svg width="${w}" height="${w*1.25}" viewBox="0 0 30 38"><circle cx="15" cy="9" r="8" fill="${c}"/><path d="M1 38 C 2 23, 8 19, 15 19 C 22 19, 28 23, 29 38 Z" fill="${c}"/></svg>`;
const CRT=`<svg width="330" height="250" viewBox="0 0 330 250"><rect x="5" y="5" width="320" height="210" rx="18" fill="#cfc8b8"/><rect x="25" y="22" width="280" height="172" rx="10" fill="#0b130b"/><rect x="125" y="215" width="80" height="18" fill="#b8b09e"/><rect x="85" y="232" width="160" height="12" rx="4" fill="#a59d8a"/></svg>`;
const TROPHY=`<svg width="110" height="130" viewBox="0 0 110 130"><path d="M25 8 L85 8 L80 60 C 76 78, 34 78, 30 60 Z" fill="#F2C94C"/><path d="M25 18 C 2 18, 4 52, 30 52" stroke="#F2C94C" stroke-width="7" fill="none"/><path d="M85 18 C 108 18, 106 52, 80 52" stroke="#F2C94C" stroke-width="7" fill="none"/><rect x="48" y="76" width="14" height="22" fill="#d9ad35"/><rect x="28" y="98" width="54" height="22" rx="4" fill="#8a6a1a"/><text x="55" y="48" text-anchor="middle" font-family="IT" font-weight="900" font-size="26" fill="#8a6a1a">ČR</text></svg>`;
const PLANE=`<svg width="34" height="34" viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="#fff"/></svg>`;
const LOGO=(f,w)=>`<img src="photos/${f}.png" style="width:${w}px;display:block">`;
const PIE=p=>{const a=p/100*2*Math.PI,x=60+56*Math.sin(a),y=60-56*Math.cos(a);return `<svg width="120" height="120" viewBox="0 0 120 120"><circle cx="60" cy="60" r="56" fill="#e7e1d2"/>${p>0?`<path d="M60 60 L60 4 A56 56 0 ${p>50?1:0} 1 ${x.toFixed(2)} ${y.toFixed(2)} Z" fill="#30A9E0"/>`:''}<circle cx="60" cy="60" r="26" fill="#fff"/></svg>`};

/* ------------------------------------------------------------ scény */
const SCN=[
 /* 1 · háček: ve 12 prodával spolužákům rohlíky s čokoládou */
 {id:'hook',from:'s1',cls:'dk',cap:1,
  html:()=>`<div class="dots"></div>
   <div class="abs" style="left:74px;top:132px"><span class="badge">POSTAVILI TO <b>ČESKÁ EDICE #4</b>${FLAG(20)}</span></div>
   <div class="abs big" id="h12" style="left:74px;top:186px;font-size:120px;color:var(--ro);opacity:0;transform-origin:0 50%">12<span style="font-size:40px;color:#fff;letter-spacing:-.02em"> LET</span></div>
   <div class="abs" id="hkids" style="left:300px;top:206px;display:flex;gap:6px">${[0,1,2,3].map(i=>`<div class="hk" style="opacity:0">${PERSON(['#cfd8c4','#e8d9b8','#bcd0e0','#e0c4c4'][i],34)}</div>`).join('')}</div>
   <div class="abs" id="hroll" style="left:120px;top:340px;opacity:0">${ROLL(300)}</div>
   <div class="abs" id="hch" style="left:74px;top:500px;opacity:0"><span class="chip o">SVAČINA · PLNĚNÁ ČOKOLÁDOU</span></div>
   ${[0,1,2].map(i=>`<div class="abs hc" style="left:${150+i*90}px;top:440px;opacity:0">${COIN(42)}</div>`).join('')}`,
  anim:(t,s)=>{const A=s.t0+.05;const n=$('h12');n.style.opacity=t>=A?1:0;if(t>=A)n.style.transform=slamT(t-A,1.5,6);
    s.el.querySelectorAll('.hk').forEach((e,i)=>popIn(e,t,ck('s1',1)+i*.1,.2,.4));
    const R=ck('s1',2)-.05;const r=$('hroll');const p=e5((t-R)/.4);r.style.opacity=t>=R?1:0;r.style.transform=`translateY(${(40*(1-p)).toFixed(1)}px) rotate(${(lerp(-14,-4,p)+1.5*Math.sin(t*3)).toFixed(2)}deg)`;
    slideX($('hch'),t,ck('s1',3)+.05,-30,.3);s.el.querySelectorAll('.hc').forEach((e,i)=>{const a=ck('s1',3)+.2+i*.15;const q=e5((t-a)/.35);e.style.opacity=t>=a?1:0;e.style.transform=`translateY(${(-60*q).toFixed(1)}px) scale(${lerp(.4,1,q).toFixed(3)})`;if(t>a+.7)e.style.opacity=(1-clamp((t-a-.7)/.3)).toFixed(3)})},
  ev:s=>[[s.t0+.05,'slam',.35],...[0,1,2,3].map(i=>[ck('s1',1)+i*.1,'pop',i]),[ck('s1',2)-.05,'whoosh'],[ck('s1',3)+.05,'pop2'],...[0,1,2].map(i=>[ck('s1',3)+.2+i*.15,'coin'])]},

 /* 2 · dnes má firmu, která se jmenuje… Rohlík; stojí skoro 2 mld. $ */
 {id:'name',from:'s2',cls:'cream',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs mono" style="left:74px;top:186px;font-size:13px;color:#7a7465">DNES · JEHO FIRMA</div>
   <div class="abs big" id="nq" style="left:0;right:0;top:300px;text-align:center;font-size:150px;color:#1a1a1a">?</div>
   <div class="card" id="nlg" style="left:90px;top:262px;width:360px;height:190px;display:flex;align-items:center;justify-content:center;opacity:0">${LOGO('logo_rohlik',290)}</div>
   <div class="abs mono" id="nvl" style="left:74px;top:478px;font-size:12px;color:#7a7465;opacity:0">HODNOTA FIRMY · ODHAD 2024</div>
   <div class="abs big" id="nv" style="left:74px;top:500px;font-size:76px;color:var(--rgd);font-variant-numeric:tabular-nums;opacity:0">0 MLD. $</div>`,
  anim:(t,s)=>{const L=ck('s2',2)-.02;const q=$('nq');q.style.opacity=t<L?1:0;q.style.transform=`scale(${(1+.05*Math.sin(t*7)).toFixed(4)})`;
    const lg=$('nlg');lg.style.opacity=t>=L?1:0;if(t>=L)lg.style.transform=slamT(t-L,1.4,6);
    const V=ck('s3',1)-.15;fade($('nvl'),t,V-.1);const v=$('nv');v.style.opacity=t>=V?1:0;v.textContent=(1.9*eo((t-V)/1.2)).toFixed(1).replace('.',',')+' MLD. $';if(t>=V+1.2)v.style.transform=slamT(t-V-1.2,1.12,3)},
  ev:s=>[[ck('s2',1),'tick2'],[ck('s2',2)-.02,'slam',.45],[ck('s3',1)-.15,'count',1.2],[ck('s3',1)+1.05,'coin']]},

 /* 3 · Tomáš Čupr */
 {id:'who',from:'s4',cls:'dk',cap:1,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="wph" style="left:110px;top:190px;width:320px;height:320px"><img src="photos/cupr_portret.jpg"></div>
   <div class="card" id="wnc" style="left:74px;top:480px;padding:12px 18px;opacity:0;border-radius:12px"><div style="font-weight:900;font-size:34px;letter-spacing:-.03em">Tomáš Čupr</div><div class="mono" style="font-size:12px;color:#555;margin-top:4px">ZAKLADATEL ROHLÍKU</div></div>`,
  anim:(t,s)=>{const u=t-s.t0;const p=$('wph');p.style.opacity=clamp(u/.15);p.style.transform=`scale(${(1.08-.08*e5(u/.6)).toFixed(4)}) rotate(${lerp(-4,-1.5,e5(u/.6)).toFixed(2)}deg)`;slideIn($('wnc'),t,s.t0+.15,24,.3)},
  ev:s=>[[s.t0+.15,'pop2']]},

 /* 4 · první peníze z Counter-Striku, 2× mistr republiky */
 {id:'cs',from:'s5',cls:'retro',cap:1,tr:'glitch',
  html:()=>`<div class="abs mono" style="left:74px;top:186px;font-size:13px;color:#8fd18f">PRVNÍ VÝDĚLEK</div>
   <div class="abs" id="ccrt" style="left:105px;top:220px">${CRT}
    <div class="abs mono" style="left:40px;top:34px;font-size:11px;color:#6fdc6f">HP 100 · $ 800</div>
    <svg class="abs" id="cxh" width="60" height="60" viewBox="0 0 60 60" style="left:135px;top:78px"><circle cx="30" cy="30" r="18" fill="none" stroke="#6fdc6f" stroke-width="2.5"/><line x1="30" y1="2" x2="30" y2="20" stroke="#6fdc6f" stroke-width="2.5"/><line x1="30" y1="40" x2="30" y2="58" stroke="#6fdc6f" stroke-width="2.5"/><line x1="2" y1="30" x2="20" y2="30" stroke="#6fdc6f" stroke-width="2.5"/><line x1="40" y1="30" x2="58" y2="30" stroke="#6fdc6f" stroke-width="2.5"/></svg>
    <div class="abs mono" id="cmon" style="left:180px;top:160px;font-size:13px;color:#F2C94C;opacity:0">+ PRVNÍ PENÍZE</div></div>
   <div class="abs" id="ctr" style="left:74px;top:478px;opacity:0">${TROPHY}</div>
   <div class="abs big" id="c2x" style="left:200px;top:500px;font-size:84px;color:#F2C94C;opacity:0">2×</div>
   <div class="abs mono" id="c2l" style="left:204px;top:586px;font-size:13px;color:#fff;opacity:0">MISTR REPUBLIKY</div>`,
  anim:(t,s)=>{const u=t-s.t0;slideIn($('ccrt'),t,s.t0,24,.3);$('cxh').style.transform=`translate(${(40*Math.sin(u*1.7)).toFixed(1)}px,${(18*Math.sin(u*2.3+1)).toFixed(1)}px)`;
    popIn($('cmon'),t,ck('s5',2)+.1,.2,.5);popIn($('ctr'),t,st('s6')+.05,.3,.5);const X=ck('s6',1)+.05;const x=$('c2x');x.style.opacity=t>=X?1:0;if(t>=X)x.style.transform=slamT(t-X,1.5,6);fade($('c2l'),t,X+.2)},
  ev:s=>[[ck('s5',2)+.1,'shot'],[ck('s5',2)+.25,'coin'],[st('s6')+.05,'pop2'],[ck('s6',1)+.05,'slam',.35]]},

 /* 5 · 2005 Anglie: pomocník v tiskárně → spolumajitel agentury */
 {id:'uk',from:'s7',cls:'dk',cap:1,year:2005,tr:'flash',
  html:()=>`<div class="dots"></div>
   <svg class="abs" width="540" height="300" style="left:0;top:180px"><path id="uarc" d="M 400 230 Q 300 30 140 120" fill="none" stroke="rgba(242,169,59,.25)" stroke-width="2" stroke-dasharray="6 7"/><path id="uarc2" d="M 400 230 Q 300 30 140 120" fill="none" stroke="#F2A93B" stroke-width="3"/><circle cx="400" cy="230" r="7" fill="#fff"/><circle cx="140" cy="120" r="7" fill="#F2A93B"/></svg>
   <div class="abs" id="upl" style="left:0;top:0;opacity:0">${PLANE}</div>
   <div class="abs" style="left:356px;top:430px"><span class="chip w">ČESKO</span></div>
   <div class="abs" id="uen" style="left:84px;top:244px;opacity:0"><span class="chip o">ANGLIE</span></div>
   <div class="abs" id="ulad" style="left:0;top:0;width:540px;height:960px;opacity:0">
    ${[['POMOCNÍK V TISKÁRNĚ','#3a4a30',0],['…',null,1],['SPOLUMAJITEL AGENTURY','#6BA53A',2]].map(([n,c,i])=>c?`<div class="abs ul" data-i="${i}" style="left:74px;top:${520-i*130}px;width:392px;height:74px;border-radius:14px;background:${c};display:flex;align-items:center;padding:0 20px;gap:14px;opacity:0">${PERSON('#fff',28)}<span style="font-weight:900;font-size:24px;letter-spacing:-.02em">${n}</span></div>`:`<div class="abs ul mono" data-i="1" style="left:120px;top:${520-130}px;font-size:40px;color:#97A08E;opacity:0">↑</div>`).join('')}</div>`,
  anim:(t,s)=>{const P=$('uarc2');const L=P.getTotalLength();const A=s.t0+.1,B=ck('s7',1)+.6;const p=eio((t-A)/(B-A));P.style.strokeDasharray=L;P.style.strokeDashoffset=(L*(1-p)).toFixed(1);
    const pt=P.getPointAtLength(L*p),pt2=P.getPointAtLength(Math.min(L,L*p+2));const ang=Math.atan2(pt2.y-pt.y,pt2.x-pt.x)*180/Math.PI+90;
    const pl=$('upl');pl.style.opacity=t>=A&&p<1?1:0;pl.style.transform=`translate(${(pt.x-17).toFixed(1)}px,${(pt.y+180-17).toFixed(1)}px) rotate(${ang.toFixed(1)}deg)`;popIn($('uen'),t,B-.05,.25,.6);
    const D=st('s8')-.05;fade($('ulad'),t,D,.2);if(t>=D)s.el.querySelectorAll('svg,#uen,.chip').forEach(e=>{if(!e.closest('#ulad'))e.style.opacity=(1-clamp((t-D)/.2)).toFixed(3)});
    s.el.querySelectorAll('.ul').forEach(e=>{const i=+e.dataset.i;slideIn(e,t,[ck('s8',1),ck('s8',2)+.2,ck('s8',3)][i],24,.3)})},
  ev:s=>[[s.t0+.1,'jet',ck('s7',1)+.5-s.t0],[ck('s7',1)+.55,'pop2'],[ck('s8',1),'pop'],[ck('s8',3),'rise']]},

 /* 6 · 2010 Slevomat; 3 dny po spuštění investor koupí 49 % */
 {id:'slevomat',from:'s9',cls:'cream',cap:1,year:2010,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="abs mono" style="left:74px;top:186px;font-size:13px;color:#7a7465">ZPÁTKY DOMA</div>
   <div class="card" id="slg" style="left:140px;top:212px;width:260px;height:230px;display:flex;align-items:center;justify-content:center;opacity:0">${LOGO('logo_slevomat',200)}</div>
   <div class="abs" id="s3d" style="left:74px;top:470px;opacity:0"><div class="mono" style="font-size:12px;color:#7a7465">PO SPUŠTĚNÍ</div><div class="big" style="font-size:72px;color:#1a1a1a">3 DNY</div></div>
   <div class="abs" id="spie" style="left:330px;top:466px;opacity:0"><div id="spiev">${PIE(0)}</div><div class="abs big" id="spn" style="left:0;width:120px;top:44px;text-align:center;font-size:26px;color:#1a1a1a">0 %</div></div>
   <div class="abs mono" id="spl" style="left:318px;top:596px;font-size:11px;color:#7a7465;opacity:0">PRODÁNO INVESTOROVI</div>`,
  anim:(t,s)=>{const L=ck('s10',1)+.1;const lg=$('slg');lg.style.opacity=t>=L?1:0;if(t>=L)lg.style.transform=slamT(t-L,1.35,5);
    const D=st('s11')-.05;popIn($('s3d'),t,D,.25,.6);const P=ck('s11',2);fade($('spie'),t,P,.2);const v=Math.round(49*eo((t-P-.2)/1.4));$('spiev').innerHTML=PIE(v);$('spn').textContent=v+' %';fade($('spl'),t,ck('s11',3))},
  ev:s=>[[ck('s10',1)+.1,'slam',.35],[st('s11')-.05,'pop2'],[ck('s11',2)+.2,'count',1.4],[ck('s11',3)+.6,'coin']]},

 /* 7 · 2012 DámeJídlo; z obou firem odejde */
 {id:'dj',from:'s12',cls:'cream',cap:1,year:2012,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs mono" style="left:74px;top:186px;font-size:13px;color:#7a7465">O DVA ROKY POZDĚJI</div>
   <div class="card" id="dlg" style="left:74px;top:240px;width:392px;height:140px;display:flex;align-items:center;justify-content:center;opacity:0">${LOGO('logo_damejidlo',330)}</div>
   <div class="card" id="dsl" style="left:74px;top:400px;width:392px;height:120px;display:flex;align-items:center;justify-content:center;opacity:0">${LOGO('logo_slevomat',112)}</div>
   <div class="abs" id="dex" style="left:150px;top:350px;opacity:0"><span class="stamp" style="background:rgba(255,246,228,.9)">ODCHÁZÍ</span></div>`,
  anim:(t,s)=>{slideX($('dlg'),t,ck('s12',1)+.05,60,.35);const O=st('s13')-.05;slideX($('dsl'),t,O,-60,.3);const X=ck('s13',1)+.05;stampIn($('dex'),t,X,-8,1.8);
    if(t>=X+.25){const k=eo((t-X-.25)/.5);['dlg','dsl'].forEach((id,i)=>{const e=$(id);e.style.opacity=(1-.65*k).toFixed(3);e.style.transform=`translateX(${((i?-1:1)*40*k).toFixed(1)}px) scale(${(1-.08*k).toFixed(3)})`})}},
  ev:s=>[[ck('s12',1)+.05,'whoosh'],[st('s13')-.05,'whoosh'],[ck('s13',1)+.05,'stamp',.45]]},

 /* 8 · projekt na celý život: Rohlík */
 {id:'life',from:'s14',cls:'dk',cap:1,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="abs" id="lcupr" style="left:250px;top:250px;width:270px;opacity:0"><img src="photos/cupr_cut.png" style="width:270px;display:block;filter:drop-shadow(0 0 30px rgba(242,169,59,.25))"></div>
   <div class="abs" id="lq" style="left:74px;top:220px;width:210px;opacity:0;font-weight:900;font-size:40px;letter-spacing:-.04em;line-height:1.02">„Projekt na <span style="color:var(--ro)">celý život.</span>“</div>
   <div class="card" id="llg" style="left:74px;top:430px;width:220px;height:118px;display:flex;align-items:center;justify-content:center;opacity:0">${LOGO('logo_rohlik',176)}</div>`,
  anim:(t,s)=>{const u=t-s.t0;const c=$('lcupr');c.style.opacity=clamp(u/.25);c.style.transform=`translateX(${(30*(1-e5(u/.6))).toFixed(1)}px)`;
    slideIn($('lq'),t,ck('s14',3)-.1,20,.3);const L=st('s15')-.02;const lg=$('llg');lg.style.opacity=t>=L?1:0;if(t>=L)lg.style.transform=slamT(t-L,1.4,6)},
  ev:s=>[[s.t0,'whoosh'],[ck('s14',3)-.1,'pop'],[st('s15')-.02,'slam',.45]]},

 /* 9 · 2021 první český jednorožec, víc než miliarda dolarů */
 {id:'uni',from:'s16',cls:'gold',cap:1,year:2021,tr:'flash',
  html:()=>`<div class="dots"></div><div class="abs" style="inset:0;background:radial-gradient(50% 35% at 50% 40%,rgba(242,169,59,.25),transparent 70%)"></div>
   <div class="abs" id="uem" style="left:0;right:0;top:200px;text-align:center;font-size:150px;line-height:1;opacity:0">🦄</div>
   <div class="abs" id="ub" style="left:0;right:0;top:384px;text-align:center;opacity:0"><span class="badge" style="font-size:20px">PRVNÍ ČESKÝ JEDNOROŽEC ${FLAG(22)}</span></div>
   <div class="abs mono" id="uvl" style="left:0;right:0;top:446px;text-align:center;font-size:12px;color:#f5d9a6;opacity:0">HODNOTA FIRMY · 2021</div>
   <div class="abs big" id="uv" style="left:0;right:0;top:470px;text-align:center;font-size:56px;color:var(--ro);font-variant-numeric:tabular-nums;opacity:0">$ 0</div>`,
  anim:(t,s)=>{const E=ck('s16',1)+.1;const e=$('uem');e.style.opacity=t>=E?1:0;if(t>=E)e.style.transform=slamT(t-E,1.6,7)+` rotate(${(4*Math.sin((t-E)*3)).toFixed(2)}deg)`;popIn($('ub'),t,E+.35,.25,.6);
    const V=ck('s17',1)-.2;fade($('uvl'),t,V-.1);const v=$('uv');v.style.opacity=t>=V?1:0;v.textContent=(t>=V+1.1?'> ':'')+(eo((t-V)/1.1)).toFixed(1).replace('.',',')+' MLD. $';if(t>=V+1.1)v.style.transform=slamT(t-V-1.1,1.12,3)},
  ev:s=>[[ck('s16',1)+.1,'boom'],[ck('s16',1)+.45,'sparkle'],[ck('s17',1)-.2,'count',1.1],[ck('s17',1)+.9,'coin']]},

 /* 10 · dnes 5 zemí, v Německu Knuspr */
 {id:'today',from:'s18',cls:'dk',cap:1,year:2025,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="tph" style="left:74px;top:186px;width:392px;height:220px"><img src="photos/auta.jpg"><div class="lbl">ROZVOZ ROHLÍKU</div></div>
   <div class="abs" id="tcs" style="left:74px;top:426px;width:392px;display:flex;flex-direction:column;gap:7px">
    ${[['ČESKO','Rohlik'],['NĚMECKO','Knuspr'],['RAKOUSKO','Gurkerl'],['MAĎARSKO','Kifli'],['RUMUNSKO','Sezamo']].map(([c,b],i)=>`<div class="tc" data-i="${i}" style="height:36px;border-radius:10px;background:${i===1?'var(--ro)':'rgba(255,255,255,.08)'};color:${i===1?'#1a1a1a':'#fff'};display:flex;align-items:center;justify-content:space-between;padding:0 14px;opacity:0"><span class="mono" style="font-size:13px">${c}</span><span style="font-weight:900;font-size:19px;letter-spacing:-.02em">${b}</span></div>`).join('')}</div>`,
  anim:(t,s)=>{const u=t-s.t0;$('tph').style.transform=`scale(${(1.06-.06*e5(u/.8)).toFixed(4)})`;const C=ck('s18',1);
    s.el.querySelectorAll('.tc').forEach(e=>{const i=+e.dataset.i;slideX(e,t,C+i*.14,-40,.3)});const K=ck('s19',1)+.1;const k=s.el.querySelector('.tc[data-i="1"]');if(t>=K)k.style.transform=slamT(t-K,1.08,3)},
  ev:s=>[...[0,1,2,3,4].map(i=>[ck('s18',1)+i*.14,'pop',i]),[ck('s19',1)+.1,'pop2']]},

 /* 11 · a celé to začalo… rohlíkem s čokoládou */
 {id:'outro',from:'s20',cls:'dk',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs" id="oroll" style="left:95px;top:250px;opacity:0">${ROLL(350)}</div>
   <div class="abs" id="o1" style="left:74px;top:440px;width:392px;display:flex;justify-content:space-between;align-items:baseline;opacity:0"><span class="big" style="font-size:54px;color:var(--ro)">12 LET</span><span class="big" style="font-size:40px;color:#97A08E">→</span><span class="big" style="font-size:54px">2 MLD. $</span></div>`,
  anim:(t,s)=>{const R=ck('s20',1);const r=$('oroll');r.style.opacity=t>=R?1:0;if(t>=R)r.style.transform=slamT(t-R,1.6,6)+` rotate(${(-4+2*Math.sin((t-R)*3)).toFixed(2)}deg)`;slideIn($('o1'),t,R+.5,20,.3)},
  ev:s=>[[ck('s20',0)+.2,'tick2'],[ck('s20',1),'slam',.4],[ck('s20',1)+.5,'pop2']]},

 /* 12 · výzva */
 {id:'cta',from:'s21',cls:'white',cap:0,tr:'flash',
  html:()=>`<div class="abs" style="left:74px;top:150px"><span class="badge">POSTAVILI TO <b>ČESKÁ EDICE #4</b>${FLAG(20)}</span></div>
   <div class="abs" id="cq" style="left:74px;top:204px;width:400px;font-weight:900;font-size:50px;letter-spacing:-.04em;line-height:1.02;color:#111">Nakupuješ na Rohlíku?</div>
   ${[['ANO','#4f8a22'],['NE','#E5322D']].map(([a,c],i)=>`<div class="abs co" data-i="${i}" style="left:74px;top:${352+i*74}px;width:392px;height:62px;border:2.5px solid #111;border-radius:14px;display:flex;align-items:center;padding:0 20px;opacity:0"><span style="font-weight:900;font-size:30px;letter-spacing:-.03em;color:${c}">${a}</span></div>`).join('')}
   <div class="abs" id="cc" style="left:74px;top:518px;width:392px;height:56px;border-radius:999px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:800;font-size:21px;opacity:0">Napiš to do komentářů 👇</div>
   <div class="abs" id="csg" style="left:74px;top:604px;display:flex;align-items:center;gap:12px;opacity:0"><div style="background:#111;border-radius:8px;padding:8px 11px;display:flex">${uzel(18,'#fff')}</div><div style="font-weight:800;font-size:19px;color:#111;letter-spacing:-.03em">Better Digital</div></div>`,
  anim:(t,s)=>{slideIn($('cq'),t,s.t0+.05,16,.3);s.el.querySelectorAll('.co').forEach(e=>{const i=+e.dataset.i;slideX(e,t,ck('s22',i)+(i?.05:.1),-40,.3)});popIn($('cc'),t,ck('s22',1)+.5,.25,.7);slideIn($('csg'),t,ck('s22',1)+.9,10)},
  ev:s=>[[s.t0+.05,'whoosh'],[ck('s22',0)+.1,'pop',0],[ck('s22',1)+.05,'pop',1],[ck('s22',1)+.5,'notif']]},
];
