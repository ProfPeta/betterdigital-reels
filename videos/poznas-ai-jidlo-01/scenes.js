/* POZNÁŠ AI? Jídlo #1. Kolo 1 svíčková (A pravá), kolo 2 smažák (B pravá), kolo 3 vepřo knedlo zelo (obě AI). */
const R=[null,{d:'Svíčková',a:'svickova_real',b:'svickova_ai',ra:1,rb:0},{d:'Smažák',a:'smazak_ai',b:'smazak_real',ra:0,rb:1},{d:'Vepřo knedlo zelo',a:'vepro_ai1',b:'vepro_ai2',ra:0,rb:0}];
const GAP=s=>[en(s)+.08,en(s)+2.38];
const PAIR=(k,ans)=>{const r=R[k];return ['a','b'].map((x,i)=>`<div class="pr" data-i="${i}" style="top:${i?448:176}px;opacity:0"><img src="photos/${r[x]}.jpg"><div class="dim"></div><span class="abl" style="opacity:0">${x.toUpperCase()}</span>${ans&&!r['r'+x]?'<span class="lbl" style="opacity:0">VYGENEROVÁNO V CHATGPT</span>':''}${ans?`<div class="st2"><span class="stamp bg ${r['r'+x]?'ok':''}">${r['r'+x]?'PRAVÁ':'AI'}</span></div>`:''}</div>`).join('')};
const HEAD=(k,tag)=>`<div class="hd" id="hd${tag}${k}" style="opacity:0"><span class="n">${tag==='a'?'ODPOVĚĎ':'KOLO'} ${k} / 3</span><span class="t" style="font-size:${R[k].d.length>12?30:40}px">${R[k].d}</span></div>`;
const showPair=(s,t,a,dx=40)=>s.el.querySelectorAll('.pr').forEach((e,i)=>{slideX(e,t,a+i*.12,i?dx:-dx,.32)});
function round(k,sid,tr){return {id:'r'+k,from:sid,cls:'dk',cap:0,tr,
  html:()=>`<div class="dots"></div>${HEAD(k,'r')}${PAIR(k,0)}<div class="cd"><div class="tx">TIPNI SI · A, NEBO B?</div><div class="dg"></div><div class="bk"></div><div class="bar"></div></div>`,
  anim:(t,s)=>{slideIn($('hdr'+k),t,s.t0+.02,14,.25);showPair(s,t,s.t0+.05);
    const A=ck(sid,2),Bt=A+.42;const ls=s.el.querySelectorAll('.abl');popIn(ls[0],t,A,.2,1.6);popIn(ls[1],t,Bt,.2,1.6);
    const [g0,g1]=GAP(sid);const cd=s.el.querySelector('.cd');fade(cd,t,g0-.1,.15);const p=clamp((t-g0)/(g1-g0));
    cd.querySelector('.bar').style.width=(400*(1-p)).toFixed(1)+'px';cd.querySelector('.dg').textContent=t>=g0?String(Math.max(1,3-Math.floor(p*3))):'';
    s.el.querySelectorAll('.pr').forEach((e,i)=>{e.style.outlineColor=t>=g0&&t<g1&&(Math.floor((t-g0)*2.6)%2===i)?'#FFD400':'rgba(255,255,255,.9)'})},
  ev:s=>{const [g0,g1]=GAP(sid);return [[s.t0+.05,'whoosh'],[ck(sid,2),'pop',0],[ck(sid,2)+.42,'pop',2],...[0,1,2].map(i=>[g0+i*(g1-g0)/3,'tick2']),[g1-.05,'pop2']]}}}
function answer(k,sid,tr,st){return {id:'a'+k,from:sid,cls:'dk',cap:1,capY:712,capS:k===3?['s12','s13']:[sid],tr,
  html:()=>`<div class="dots"></div>${HEAD(k,'a')}${PAIR(k,1)}`,
  anim:(t,s)=>{slideIn($('hda'+k),t,s.t0+.02,14,.25);showPair(s,t,s.t0+.04,24);s.el.querySelectorAll('.abl').forEach(e=>e.style.opacity=t>=s.t0+.2?1:0);
    const T0=st(s),r=R[k];s.el.querySelectorAll('.pr').forEach((e,i)=>{const a=T0+(k===3?i*.35:0),real=r[i?'rb':'ra'];
      const sp=e.querySelector('.st2');sp.style.opacity=t>=a?1:0;if(t>=a)sp.firstChild.style.transform=`rotate(${i?6:-7}deg) `+slamT(t-a,1.9,5);
      const lb=e.querySelector('.lbl');if(lb)fade(lb,t,a+.25);e.querySelector('.dim').style.opacity=t>=a&&!real&&k<3?.35:0;
      e.style.outlineColor=k<3&&t>=a&&real?'#18a34a':'rgba(255,255,255,.9)'});},
  ev:s=>{const T0=st(s);return k===3?[[T0,'stamp',.3],[T0+.35,'stamp',.35],[T0+.4,'shk',4],[T0+.75,'glitch',.25]]:[[T0,'stamp',.3],[T0+.12,'chime']]}}}
const SCN=[
 /* 1 · háček: tři talíře, otázka */
 {id:'hook',from:'s1',cls:'blk',cap:1,
  html:()=>`<div class="abs" style="left:70px;top:118px">${BADGE()}</div>
   ${[['vepro_ai2',-8,40,186],['svickova_real',7,150,300],['smazak_ai',-4,60,420]].map(([f,r,x,y],i)=>`<div class="pr hc" data-i="${i}" style="left:${x}px;top:${y}px;width:360px;height:236px;opacity:0" data-r="${r}"><img src="photos/${f}.jpg"></div>`).join('')}
   <div class="abs" id="hai" style="left:262px;top:196px;opacity:0"><span class="stamp bg" style="font-size:44px">AI?</span></div>
   <div class="abs big" id="hq" style="left:0;right:0;top:560px;text-align:center;opacity:0"><span style="background:#FFD400;color:#0B0B0B;font-size:56px;padding:4px 16px;border-radius:12px">POZNÁŠ TO?</span></div>`,
  anim:(t,s)=>{s.el.querySelectorAll('.hc').forEach((e,i)=>{const a=s.t0+i*.14,p=e5((t-a)/.45);e.style.opacity=t>=a?1:0;e.style.transform=`translateY(${(60*(1-p)).toFixed(1)}px) rotate(${(+e.dataset.r*p+.6*Math.sin(t*1.3+i)).toFixed(2)}deg) scale(${lerp(.85,1,p).toFixed(3)})`});
    stampIn($('hai'),t,ck('s2',1),-8,1.8);const Q=st('s3');const q=$('hq');q.style.opacity=t>=Q?1:0;if(t>=Q)q.style.transform=slamT(t-Q,1.15,4)},
  ev:s=>[...[0,1,2].map(i=>[s.t0+i*.14,'pop',i]),[ck('s2',1),'stamp',.25],[st('s3'),'slam',.3]]},
 round(1,'s4','flash'),
 round(2,'s5','scan'),
 round(3,'s6','scan'),
 /* 5 · napiš tipy */
 {id:'cmt',from:'s7',cls:'white',cap:1,tr:'flash',
  html:()=>`<div class="dots"></div>
   <div class="abs big" id="ct" style="left:70px;top:150px;font-size:56px;white-space:normal;width:400px;line-height:1;opacity:0">Napiš svoje 3 tipy 👇</div>
   <div class="cm" id="cb" style="top:300px;opacity:0"><div class="av">${uzel(9,'#fff')}</div><div><div class="lb" style="color:#666;font-size:12px">TVŮJ TIP</div><div id="cty" style="font-weight:800;font-size:30px;letter-spacing:-.02em;margin-top:4px;min-height:36px"></div></div></div>
   <div class="abs" id="cs" style="left:70px;top:440px;opacity:0"><span class="stamp" style="font-size:40px">STOP ✋</span></div>
   <div class="abs lb" id="csl" style="left:72px;top:520px;color:#333;opacity:0">ODPOVĚDI AŽ PO TIPU</div>`,
  anim:(t,s)=>{const a=s.t0+.05;const c=$('ct');c.style.opacity=t>=a?1:0;if(t>=a)c.style.transform=slamT(t-a,1.1,2);slideIn($('cb'),t,s.t0+.35,18,.28);
    typeTo($('cty'),'1 B · 2 B · 3 A',t,s.t0+.7,12);stampIn($('cs'),t,st('s8')+.05,-5,1.25);fade($('csl'),t,st('s8')+.3)},
  ev:s=>[[s.t0+.05,'slam',.15],[s.t0+.35,'pop2'],[s.t0+.7,'type',1.4],[st('s8')+.05,'stamp',.25]]},
 /* 6 · odpovědi */
 {id:'ansT',from:'s9',cls:'yel',cap:0,tr:'flash',
  html:()=>`<div class="abs big" id="at" style="left:0;right:0;top:330px;text-align:center;font-size:80px;opacity:0">ODPOVĚDI</div>`,
  anim:(t,s)=>{const a=s.t0+.03;const e=$('at');e.style.opacity=t>=a?1:0;if(t>=a)e.style.transform=slamT(t-a,1.5,6)},
  ev:s=>[[s.t0+.03,'slam',.3]]},
 answer(1,'s10','scan',s=>ck('s10',1)+.45),
 answer(2,'s11','scan',s=>ck('s11',1)+.45),
 answer(3,'s12','scan',s=>st('s13')+.05),
 /* 7 · kolik jsi dal, pošli mámě */
 {id:'out',from:'s14',cls:'white',cap:0,tr:'flash',
  html:()=>`<div class="abs" style="left:70px;top:150px">${BADGE()}</div>
   <div class="abs" id="oq" style="left:70px;top:204px;font-weight:900;font-size:56px;letter-spacing:-.04em;line-height:1">Kolik jsi dal?</div>
   <div class="abs" style="left:70px;top:290px;width:400px;display:flex;gap:10px">${['0/3','1/3','2/3','3/3'].map((x,i)=>`<div class="os" style="flex:1;height:70px;border:3px solid #0B0B0B;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:30px;background:${i===3?'#FFD400':'#fff'};opacity:0">${x}</div>`).join('')}</div>
   <div class="abs" id="om" style="left:70px;top:396px;width:400px;height:62px;border-radius:999px;background:#0B0B0B;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:23px;opacity:0">Pošli to mámě 📲</div>
   <div class="abs" id="osg" style="left:70px;top:500px;display:flex;align-items:center;gap:12px;opacity:0"><div style="background:#111;border-radius:8px;padding:8px 11px;display:flex">${uzel(18,'#fff')}</div><div style="font-weight:800;font-size:19px;letter-spacing:-.03em">Better Digital</div></div>`,
  anim:(t,s)=>{slideIn($('oq'),t,s.t0+.04,16,.28);s.el.querySelectorAll('.os').forEach((e,i)=>popIn(e,t,s.t0+.3+i*.1,.2,.6));popIn($('om'),t,st('s15')+.1,.25,.7);slideIn($('osg'),t,st('s15')+.7,10)},
  ev:s=>[[s.t0+.04,'whoosh'],...[0,1,2,3].map(i=>[s.t0+.3+i*.1,'pop',i]),[st('s15')+.1,'notif']]},
];
