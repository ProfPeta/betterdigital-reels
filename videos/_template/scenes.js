/* Šablona příběhu: háček, kdo, zvrat, pointa, otázka. Pomocníci: engine/story/lib.js. Obsah drž v x 74–466, y 130–650, titulky jsou na y 664. */
const SCN=[
 /* 1 · háček: první snímek musí ukázat konflikt nebo výsledek, ne logo */
 {id:'hook',from:'s1',cls:'blk',cap:1,
  html:()=>`<div class="abs" style="left:74px;top:132px">${BADGE()}</div>
   <div class="abs big" id="h1" style="left:74px;top:220px;font-size:92px;color:var(--y);white-space:normal;width:392px">Výsledek</div>`,
  anim:(t,s)=>{$('h1').style.transform=slamT(t-s.t0,1.05,2)},
  ev:s=>[[s.t0+.02,'slam',.2]]},
 /* 2 · kdo: fotka a jmenovka. Fotku přidej do photos/photos.json */
 {id:'who',from:'s2',cls:'dk',cap:1,tr:'scan',
  html:()=>`<div class="dots"></div><div class="card" id="w1" style="left:74px;top:220px;width:392px;padding:16px 18px;opacity:0"><div style="font-weight:900;font-size:36px;letter-spacing:-.03em">Jméno Příjmení</div><div class="lb" style="color:#555;margin-top:4px">KDO TO JE</div></div>`,
  anim:(t,s)=>{slideIn($('w1'),t,s.t0+.1,22,.3)},
  ev:s=>[[s.t0+.1,'pop2']]},
 /* 3 · zvrat */
 {id:'turn',from:'s3',cls:'white',cap:1,year:2020,tr:'flash',
  html:()=>`<div class="dots"></div><div class="abs" id="t1" style="left:96px;top:280px;opacity:0"><span class="stamp">ZVRAT</span></div>`,
  anim:(t,s)=>{stampIn($('t1'),t,s.t0+.15,-6,1.6)},
  ev:s=>[[s.t0+.15,'stamp',.3]]},
 /* 4 · pointa */
 {id:'punch',from:'s4',cls:'yel',cap:1,tr:'flash',
  html:()=>`<div class="abs big" id="p1" style="left:74px;top:280px;font-size:70px;white-space:normal;width:392px;opacity:0">Pointa</div>`,
  anim:(t,s)=>{popIn($('p1'),t,s.t0+.05,.22,.8)},
  ev:s=>[[s.t0+.05,'pop2']]},
 /* 5 · otázka na jedno slovo, bez titulků */
 {id:'cta',from:'s5',cls:'white',cap:0,tr:'flash',
  html:()=>`<div class="abs" style="left:74px;top:150px">${BADGE()}</div>
   <div class="abs" id="cq" style="left:74px;top:204px;width:392px;font-weight:900;font-size:50px;letter-spacing:-.04em;line-height:1.02">Otázka na jedno slovo?</div>
   ${[['ANO','#0B0B0B','#FFD400'],['NE','#fff','#E5322D']].map(([a,c,bg],i)=>`<div class="abs co" data-i="${i}" style="left:74px;top:${352+i*74}px;width:392px;height:62px;border:2.5px solid #111;border-radius:14px;background:${bg};display:flex;align-items:center;padding:0 20px;opacity:0"><span style="font-weight:900;font-size:30px;letter-spacing:-.03em;color:${c}">${a}</span></div>`).join('')}
   <div class="abs" id="csg" style="left:74px;top:540px;display:flex;align-items:center;gap:12px;opacity:0"><div style="background:#111;border-radius:8px;padding:8px 11px;display:flex">${uzel(18,'#fff')}</div><div style="font-weight:800;font-size:19px;letter-spacing:-.03em">Better Digital</div></div>`,
  anim:(t,s)=>{slideIn($('cq'),t,s.t0+.05,16,.3);s.el.querySelectorAll('.co').forEach((e,i)=>slideX(e,t,s.t0+.5+i*.2,-40,.3));slideIn($('csg'),t,s.t0+1,10)},
  ev:s=>[[s.t0+.05,'whoosh'],[s.t0+.5,'pop',0],[s.t0+.7,'pop',1]]},
];
