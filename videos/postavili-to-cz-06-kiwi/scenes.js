/* POSTAVILI TO · Česká edice #6: Kiwi.com / Oliver Dlouhý. Pomocníci: engine/story/lib.js. */
const AIR=(c,w=34,r=0)=>`<svg width="${w}" height="${w}" viewBox="0 0 24 24" style="display:block;transform:rotate(${r}deg)"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="${c}"/></svg>`;
const G0=()=>en('s3')+.08,G1=()=>st('s4')-.12;
const SCN=[
 /* 1 · háček: která firma je z Brna? */
 {id:'hook',from:'s1',cls:'blk',cap:1,
  html:()=>`<div class="abs" style="left:74px;top:132px">${BADGE()}</div>
   <div class="abs big" id="hq" style="left:74px;top:186px;font-size:60px;white-space:normal;width:392px;line-height:1;opacity:0">Která vznikla<br>v <span style="color:var(--y)">Brně?</span></div>
   <div class="opt ho" style="top:346px;opacity:0"><span class="l">A</span><span class="n">Skyscanner</span></div>
   <div class="opt ho" style="top:446px;opacity:0"><span class="l">B</span><span class="n">Kiwi.com</span></div>
   <div class="cd"><div class="tx">TIPNI SI · A, NEBO B?</div><div class="dg"></div><div class="bk"></div><div class="bar"></div></div>`,
  anim:(t,s)=>{const q=$('hq');q.style.opacity=1;q.style.transform=slamT(t-s.t0,1.04,2);const o=s.el.querySelectorAll('.ho');slideX(o[0],t,ck('s2',0)-.05,-40,.3);slideX(o[1],t,ck('s2',1)-.05,40,.3);
    const g0=G0(),g1=G1();const cd=s.el.querySelector('.cd');fade(cd,t,g0-.1,.15);const p=clamp((t-g0)/(g1-g0));cd.querySelector('.bar').style.width=(392*(1-p)).toFixed(1)+'px';cd.querySelector('.dg').textContent=t>=g0?String(Math.max(1,3-Math.floor(p*3))):'';
    o.forEach((e,i)=>{e.style.borderColor=t>=g0&&t<g1&&(Math.floor((t-g0)*2.6)%2===i)?'#FFD400':'#fff'})},
  ev:s=>[[s.t0+.02,'slam',.2],[ck('s2',0)-.05,'pop',0],[ck('s2',1)-.05,'pop',2],...[0,1,2].map(i=>[G0()+i*(G1()-G0())/3,'tick2']),[G1()-.05,'pop2']]},

 /* 2 · je to Kiwi.com */
 {id:'reveal',from:'s4',cls:'yel',cap:1,tr:'flash',
  html:()=>`<div class="card" id="rl" style="left:74px;top:210px;width:392px;height:210px;display:flex;align-items:center;justify-content:center;opacity:0"><img src="photos/logo_kiwi.jpg" style="width:330px;display:block"></div>
   <div class="abs" id="rc" style="left:74px;top:446px;display:flex;align-items:center;gap:10px;opacity:0"><span class="chip">BRNO · ČESKO</span>${FLAG(30)}</div>
   <div class="abs lb" id="rs" style="left:76px;top:500px;color:#333;opacity:0">SKYSCANNER JE ZE SKOTSKA</div>`,
  anim:(t,s)=>{const a=s.t0+.03;const l=$('rl');l.style.opacity=t>=a?1:0;if(t>=a)l.style.transform=slamT(t-a,1.3,5);slideIn($('rc'),t,s.t0+.35,14,.25);fade($('rs'),t,s.t0+.6)},
  ev:s=>[[s.t0+.03,'slam',.3],[s.t0+.1,'chime']]},

 /* 3 · student hledá letenku do Portugalska */
 {id:'who',from:'s5',cls:'dk',cap:1,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="wph" style="left:105px;top:140px;width:330px;height:380px"><img src="photos/dlouhy.jpg" style="object-position:50% 20%"></div>
   <div class="card" id="wnc" style="left:74px;top:470px;padding:11px 18px;opacity:0;border-radius:12px"><div style="font-weight:900;font-size:34px;letter-spacing:-.03em">Oliver Dlouhý</div><div class="mono" style="font-size:12px;color:#555;margin-top:3px">ZAKLADATEL KIWI.COM</div></div>
   <div class="abs" id="wch" style="left:74px;top:590px;opacity:0"><span class="chip o">${AIR('#0B0B0B',16,45)} LEVNÁ LETENKA · PORTUGALSKO</span></div>`,
  anim:(t,s)=>{const u=t-s.t0;const p=$('wph');p.style.opacity=clamp(u/.15);p.style.transform=`scale(${(1.08-.08*e5(u/.7)).toFixed(4)}) rotate(${lerp(-3,-1,e5(u/.7)).toFixed(2)}deg)`;slideIn($('wnc'),t,s.t0+.15,22,.3);slideX($('wch'),t,ck('s5',1),-30,.3)},
  ev:s=>[[s.t0+.15,'pop2'],[ck('s5',1),'whoosh']]},

 /* 4 · vyhledávače neumí spojit aerolinky, které nespolupracují */
 {id:'prob',from:'s6',cls:'white',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs lb" style="left:76px;top:150px;color:#666">VYHLEDÁVAČ LETENEK · ILUSTRACE</div>
   <div class="abs" id="ps" style="left:74px;top:176px;width:392px;height:62px;background:#0B0B0B;border-radius:12px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;opacity:0"><span class="mono" style="font-size:14px;color:#fff">ČESKO → PORTUGALSKO</span><span class="mono" id="p0" style="font-size:14px;color:#ff6b6b;opacity:0">0 SPOJENÍ</span></div>
   <svg class="abs" width="392" height="210" viewBox="0 0 392 210" style="left:74px;top:270px;overflow:visible">
    <line id="l1" x1="40" y1="80" x2="196" y2="80" stroke="#0B0B0B" stroke-width="5" stroke-linecap="round"/>
    <line id="l2" x1="196" y1="80" x2="352" y2="80" stroke="#E0B800" stroke-width="5" stroke-linecap="round"/>
    <circle cx="40" cy="80" r="11" fill="#0B0B0B"/><circle id="pm" cx="196" cy="80" r="13" fill="#fff" stroke="#0B0B0B" stroke-width="4"/><circle cx="352" cy="80" r="11" fill="#0B0B0B"/>
    <text x="40" y="120" text-anchor="middle" font-family="JB" font-size="12" letter-spacing="1">ČESKO</text><text x="196" y="120" text-anchor="middle" font-family="JB" font-size="12" letter-spacing="1">PŘESTUP</text><text x="352" y="120" text-anchor="middle" font-family="JB" font-size="12" letter-spacing="1">PORTUGALSKO</text>
    <text id="ta" x="118" y="56" text-anchor="middle" font-family="IT" font-weight="900" font-size="17">Aerolinka A</text><text id="tb" x="274" y="56" text-anchor="middle" font-family="IT" font-weight="900" font-size="17">Aerolinka B</text>
    <text id="px" x="196" y="95" text-anchor="middle" font-family="IT" font-weight="900" font-size="42" fill="#E5322D" opacity="0">✕</text>
   </svg>
   <div class="abs" id="pst" style="left:104px;top:450px;opacity:0"><span class="stamp" style="font-size:34px;background:#fff">NESPOLUPRACUJÍ</span></div>`,
  anim:(t,s)=>{slideIn($('ps'),t,s.t0+.05,14,.25);fade($('p0'),t,ck('s6',2)+.2,.15);const a=ck('s6',2),b=ck('s6',3);
    const L=(id,x)=>{const p=eo((t-x)/.5);$(id).setAttribute('stroke-dasharray','156');$(id).setAttribute('stroke-dashoffset',(156*(1-p)).toFixed(1))};L('l1',a);L('l2',b);
    $('ta').setAttribute('opacity',t>=a?1:0);$('tb').setAttribute('opacity',t>=b?1:0);const X=ck('s6',4);$('px').setAttribute('opacity',t>=X?1:0);stampIn($('pst'),t,X+.1,-5,1.15)},
  ev:s=>[[s.t0+.05,'pop2'],[ck('s6',2),'swish'],[ck('s6',2)+.2,'bonk'],[ck('s6',3),'swish'],[ck('s6',4)+.1,'stamp',.3]]},

 /* 5 · 2012: naprogramovali to sami, první investor 450 tisíc */
 {id:'build',from:'s7',cls:'dk',cap:1,year:2012,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="term" style="top:176px;height:108px"><div id="b1"></div><div id="b2" style="color:#FFD400"></div></div>
   <div class="abs big" id="bn" style="left:74px;top:304px;font-size:74px;color:var(--y);opacity:0">Skypicker</div>
   <div class="abs lb" id="bl" style="left:76px;top:384px;color:#bbb;opacity:0">PŮVODNÍ NÁZEV · BRNO, 2012</div>
   <div class="card" id="bc" style="left:74px;top:440px;width:392px;padding:14px 18px;border-radius:14px;opacity:0"><div class="big" style="font-size:56px" id="bcn">0 Kč</div><div class="lb" style="color:#555;margin-top:6px">PRVNÍ INVESTOR · JIŘÍ HLAVENKA</div></div>`,
  anim:(t,s)=>{typeTo($('b1'),'$ najdi --levne --spoj-aerolinky',t,s.t0+.1,26);typeTo($('b2'),'✓ hotovo: skypicker.com',t,ck('s7',2)-.2,30);
    const N=ck('s7',2)+.3;const n=$('bn');n.style.opacity=t>=N?1:0;if(t>=N)n.style.transform=slamT(t-N,1.15,2);fade($('bl'),t,N+.2);
    const C=st('s8')+.05;slideIn($('bc'),t,C,18,.3);const q=eo((t-ck('s8',2)+.1)/.8);$('bcn').textContent=fmt(450000*q)+' Kč'},
  ev:s=>[[s.t0+.1,'type',1.2],[ck('s7',2)+.3,'slam',.16],[st('s8')+.05,'pop2'],[ck('s8',2)-.1,'count',.8],[ck('s8',2)+.7,'coin']]},

 /* 6 · tržby: 140 milionů → přes 8 miliard */
 {id:'grow',from:'s9',cls:'white',cap:1,year:2016,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs lb" style="left:76px;top:170px;color:#666">TRŽBY · ZDROJ: FORBES</div>
   <div class="abs" id="g1" style="left:104px;top:574px;width:130px;height:8px;background:#0B0B0B;border-radius:4px 4px 0 0;opacity:0"></div>
   <div class="abs" id="g2" style="left:296px;top:582px;width:130px;height:0;background:#FFD400;border:3px solid #0B0B0B;border-bottom:0;border-radius:10px 10px 0 0;opacity:0"></div>
   <div class="abs big" id="g1v" style="left:74px;top:520px;width:190px;text-align:center;font-size:27px;opacity:0">140 mil. Kč</div>
   <div class="abs big" id="g2v" style="left:266px;top:214px;width:190px;text-align:center;font-size:36px;opacity:0">8+ mld. Kč</div>
   <div class="abs" style="left:74px;top:582px;width:392px;height:3px;background:#0B0B0B"></div>
   <div class="abs mono" style="left:104px;top:592px;width:130px;text-align:center;font-size:15px;color:#111">2014</div>
   <div class="abs mono" style="left:296px;top:592px;width:130px;text-align:center;font-size:15px;color:#111">2016</div>`,
  anim:(t,s)=>{const A=ck('s9',2)-.1;$('g1').style.opacity=t>=A?1:0;popIn($('g1v'),t,A,.2,.7);const B=ck('s10',1)-.5;const p=eo((t-B)/.9);const g=$('g2');g.style.opacity=t>=B?1:0;g.style.height=(310*p).toFixed(1)+'px';g.style.top=(582-310*p).toFixed(1)+'px';
    const v=$('g2v');v.style.opacity=t>=B+.9?1:0;if(t>=B+.9)v.style.transform=slamT(t-B-.9,1.3,3)},
  ev:s=>[[ck('s9',2)-.1,'pop',0],[ck('s10',1)-.5,'rise'],[ck('s10',1)+.4,'slam',.22],[ck('s10',1)+.45,'coin']]},

 /* 7 · 100 milionů hledání denně */
 {id:'srch',from:'s11',cls:'dk',cap:1,year:2016,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="abs" style="left:74px;top:176px;width:392px;display:flex;flex-wrap:wrap;gap:14px 20px">${Array.from({length:21},(_,i)=>`<div class="sp" style="opacity:0">${AIR(i%4===0?'#FFD400':'#8c8c8c',34,45)}</div>`).join('')}</div>
   <div class="abs big" id="sn" style="left:74px;top:372px;font-size:60px;color:var(--y);font-variant-numeric:tabular-nums">0</div>
   <div class="abs big" style="left:74px;top:440px;font-size:30px">hledání denně</div>
   <div class="abs lb" style="left:76px;top:486px;color:#bbb">ÚDAJ Z ROKU 2021 · FORBES</div>`,
  anim:(t,s)=>{const a=s.t0+.1;s.el.querySelectorAll('.sp').forEach((e,i)=>popIn(e,t,a+i*.07,.18,.4));const q=eo((t-a)/1.6);$('sn').textContent=fmt(1e8*q)},
  ev:s=>[[s.t0+.1,'count',1.6],[s.t0+.1,'blips',1.5],[s.t0+1.7,'pop2']]},

 /* 8 · aerolinkám se to nelíbilo: Ryanair, Southwest */
 {id:'air',from:'s12',cls:'dk',cap:1,tr:'glitch',
  html:()=>`<div class="dots"></div>
   <div class="abs big" id="at" style="left:74px;top:160px;font-size:58px;color:var(--red);opacity:0">Aerolinky ✕</div>
   <div class="acard ac" style="top:268px;opacity:0"><span class="n">Ryanair</span><span class="chip r">ROKY SPORŮ</span></div>
   <div class="acard ac" style="top:384px;opacity:0"><span class="n">Southwest</span><span class="chip w">ŽALOBA · USA 2021</span></div>
   <div class="abs" id="as" style="left:84px;top:500px;opacity:0"><span class="stamp" style="font-size:25px;background:rgba(255,255,255,.92)">SOUD: ZÁKAZ PRODEJE</span></div>
   <div class="abs lb" id="al" style="left:76px;top:580px;color:#bbb;opacity:0">TEXAS · PROSINEC 2021</div>`,
  anim:(t,s)=>{const a=s.t0+.05;const e=$('at');e.style.opacity=t>=a?1:0;if(t>=a)e.style.transform=slamT(t-a,1.2,4);const c=s.el.querySelectorAll('.ac');slideX(c[0],t,st('s13'),-40,.3);slideX(c[1],t,st('s14'),40,.3);stampIn($('as'),t,ck('s14',3)-.05,-4,1.15);fade($('al'),t,ck('s14',3)+.2)},
  ev:s=>[[s.t0+.05,'slam',.22],[st('s13'),'pop',0],[st('s14'),'pop',1],[ck('s14',3)-.05,'stamp',.35]]},

 /* 9 · 2019: většinu kupuje americký fond */
 {id:'fund',from:'s15',cls:'white',cap:1,year:2019,tr:'scan',
  html:()=>`<div class="dots"></div>
   <div class="ph" id="fph" style="left:74px;top:170px;width:392px;height:290px"><img src="photos/dlouhy2.jpg" style="object-position:60% 20%"><span class="lbl">OLIVER DLOUHÝ · ARCHIVNÍ FOTO</span></div>
   <div class="card" id="fc" style="left:74px;top:478px;width:392px;padding:14px 18px;background:#0B0B0B;color:#fff;border-radius:14px;opacity:0"><div style="font-weight:900;font-size:30px;letter-spacing:-.03em">General Atlantic</div><div class="lb" style="color:#FFD400;margin-top:5px">AMERICKÝ FOND · VĚTŠINOVÝ PODÍL</div></div>`,
  anim:(t,s)=>{const u=t-s.t0;$('fph').querySelector('img').style.transform=`scale(${(1.08-.05*Math.min(u,4)/4).toFixed(4)})`;slideIn($('fc'),t,ck('s15',1),18,.3)},
  ev:s=>[[ck('s15',1),'pop2'],[ck('s15',1)+.1,'coin']]},

 /* 10 · covid: letadla na zemi, miliardová ztráta */
 {id:'cov',from:'s16',cls:'dk',cap:1,year:2020,tr:'glitch',
  html:()=>`<div class="dots"></div>
   <div class="abs" style="left:74px;top:176px"><span class="chip r">COVID · 2020</span></div>
   <div class="abs" style="left:74px;top:236px;width:392px;display:flex;justify-content:space-between">${[0,1,2,3,4].map(i=>`<div class="cp">${AIR('#fff',56,45)}</div>`).join('')}</div>
   <div class="abs" style="left:74px;top:330px;width:392px;height:3px;background:#555"></div>
   <svg class="abs" width="392" height="150" viewBox="0 0 392 150" style="left:74px;top:360px;overflow:visible"><path id="cl" d="M0 20 L90 12 L170 26 L230 60 L300 118 L392 140" fill="none" stroke="#E5322D" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>
   <div class="abs big" id="cz" style="left:74px;top:540px;font-size:42px;color:var(--red);opacity:0">miliardová ztráta</div>`,
  anim:(t,s)=>{const D=ck('s16',1);s.el.querySelectorAll('.cp').forEach((e,i)=>{const p=eio((t-D-i*.08)/.5);e.style.transform=`translateY(${(34*p).toFixed(1)}px) rotate(${(-45*p).toFixed(1)}deg)`;e.style.opacity=(1-.6*p).toFixed(2)});
    const P=$('cl'),L=P.getTotalLength(),q=eio((t-ck('s16',3))/1.1);P.style.strokeDasharray=L;P.style.strokeDashoffset=(L*(1-q)).toFixed(1);const Z=ck('s16',4);const z=$('cz');z.style.opacity=t>=Z?1:0;if(t>=Z)z.style.transform=slamT(t-Z,1.2,4)},
  ev:s=>[[ck('s16',1),'drop',.8],[ck('s16',4),'slam',.3]]},

 /* 11 · přežila; Ryanair dnes spolupracuje */
 {id:'surv',from:'s17',cls:'yel',cap:1,year:2024,tr:'flash',
  html:()=>`<div class="abs big" id="vp" style="left:74px;top:170px;font-size:88px;opacity:0">Přežila.</div>
   <div class="card" id="v1" style="left:74px;top:320px;width:176px;height:110px;display:flex;align-items:center;justify-content:center;opacity:0"><img src="photos/logo_kiwi.jpg" style="width:150px;display:block"></div>
   <div class="abs big" id="vx" style="left:250px;top:346px;width:40px;text-align:center;font-size:44px;opacity:0">+</div>
   <div class="card" id="v2" style="left:290px;top:320px;width:176px;height:110px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:32px;letter-spacing:-.03em;opacity:0">Ryanair</div>
   <div class="abs" id="vc" style="left:74px;top:456px;opacity:0"><span class="chip">PARTNERSTVÍ · OD ROKU 2024</span></div>`,
  anim:(t,s)=>{const a=s.t0+.03;const p=$('vp');p.style.opacity=t>=a?1:0;if(t>=a)p.style.transform=slamT(t-a,1.3,5);popIn($('v2'),t,st('s18'),.22,.7);const B=st('s19');popIn($('v1'),t,B,.22,.7);fade($('vx'),t,B+.1,.15);slideIn($('vc'),t,ck('s19',1),14,.25)},
  ev:s=>[[s.t0+.03,'slam',.3],[st('s18'),'pop',0],[st('s19'),'pop',2],[ck('s19',1),'chime']]},

 /* 12 · výzva */
 {id:'cta',from:'s20',cls:'white',cap:0,tr:'flash',
  html:()=>`<div class="abs" style="left:74px;top:150px">${BADGE()}</div>
   <div class="abs" id="cq" style="left:74px;top:204px;width:392px;font-weight:900;font-size:48px;letter-spacing:-.04em;line-height:1.02;color:#111">Koupil bys letenku přes Kiwi?</div>
   ${[['ANO','#0B0B0B','#FFD400'],['NE','#fff','#E5322D']].map(([a,c,bg],i)=>`<div class="abs co" data-i="${i}" style="left:74px;top:${352+i*74}px;width:392px;height:62px;border:2.5px solid #111;border-radius:14px;background:${bg};display:flex;align-items:center;padding:0 20px;opacity:0"><span style="font-weight:900;font-size:30px;letter-spacing:-.03em;color:${c}">${a}</span></div>`).join('')}
   <div class="abs" id="ccc" style="left:74px;top:518px;width:392px;height:56px;border-radius:999px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:800;font-size:21px;opacity:0">Napiš to do komentářů 👇</div>
   <div class="abs" id="csg" style="left:74px;top:604px;display:flex;align-items:center;gap:12px;opacity:0"><div style="background:#111;border-radius:8px;padding:8px 11px;display:flex">${uzel(18,'#fff')}</div><div style="font-weight:800;font-size:19px;color:#111;letter-spacing:-.03em">Better Digital</div></div>`,
  anim:(t,s)=>{slideIn($('cq'),t,s.t0+.05,16,.3);s.el.querySelectorAll('.co').forEach(e=>{const i=+e.dataset.i;slideX(e,t,ck('s21',i)+(i?.05:.1),-40,.3)});popIn($('ccc'),t,ck('s21',1)+.5,.25,.7);slideIn($('csg'),t,ck('s21',1)+.9,10)},
  ev:s=>[[s.t0+.05,'whoosh'],[ck('s21',0)+.1,'pop',0],[ck('s21',1)+.05,'pop',1],[ck('s21',1)+.5,'notif']]},
];
