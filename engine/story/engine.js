/* Sestavení scén, časová osa, titulky, přechody, efekt zrna. Díl dodá pole SCN ve scenes.js. */
/* ------------------------------------------------------------ sestavení */
const stage=$('stage');
SCN.forEach((s,i)=>{s.t0=i?st(s.from)-.06:0;});
SCN.forEach((s,i)=>{s.t1=i+1<SCN.length?SCN[i+1].t0:T.END;const el=document.createElement('div');el.className='sc '+s.cls;el.id='sc_'+s.id;
  el.innerHTML=`<div class="cam">${s.html()}</div>`;stage.appendChild(el);s.el=el;s.cam=el.querySelector('.cam')});
const TR=SCN.filter((s,i)=>i&&s.tr).map(s=>[s.t0,s.tr]);
const EV=[];SCN.forEach(s=>{if(s.ev)EV.push(...s.ev(s))});
TR.forEach(([t0,ty])=>{if(ty==='glitch')EV.push([t0-.05,'glitch',.25]);if(ty==='flash')EV.push([t0,'hit']);if(ty==='scan')EV.push([t0,'swish'])});
EV.sort((a,b)=>a[0]-b[0]);window.EV=EV;window.SCN=SCN;
const SHK=EV.filter(e=>e[1]==='shk');
const YEARS=CFG.years||[],Y0=CFG.y0||2000,Y1=CFG.y1||2026,yx=y=>(y-Y0)/(Y1-Y0)*392;
$('tl').innerHTML='<div class="ln"></div><div class="pg"></div>'+YEARS.map(y=>`<i class="ev" data-y="${y}" style="left:${yx(y).toFixed(1)}px"></i>`).join('')+'<div class="cur"></div><div class="yr"></div>';
const GRAIN=CFG.grain===undefined?7:CFG.grain;const GC=$('grain').getContext('2d'),GI=GC.createImageData(180,320);
function grain(f){const r=rng(7000+f),d=GI.data;for(let i=0;i<d.length;i+=4){const v=r()*255|0;d[i]=d[i+1]=d[i+2]=v;d[i+3]=GRAIN}GC.putImageData(GI,0,0)}
window.render=function(t){
  let k=SCN.length-1;for(let i=0;i<SCN.length;i++)if(t<SCN[i].t1){k=i;break}
  const s=SCN[k],u=t-s.t0;const prev=k>0?SCN[k-1]:null;
  const scan=s.tr==='scan'&&prev&&u<.28;
  SCN.forEach(q=>{const on=q===s||(scan&&q===prev);q.el.style.display=on?'block':'none';q.el.style.zIndex=q===s?2:1;q.el.style.clipPath='none'});
  if(scan){const p=eio(u/.28);s.el.style.clipPath=`inset(0 0 ${(100*(1-p)).toFixed(2)}% 0)`;prev.anim&&prev.anim(t,prev);$('scanl').style.display='block';$('scanl').style.top=(960*p-1).toFixed(1)+'px'}else $('scanl').style.display='none';
  s.cam.style.transform=`scale(${(1+.012*Math.min(u,6)/6).toFixed(4)})`;
  s.anim&&s.anim(t,s);
  let sx=0,sy=0;for(const [a,,amp] of SHK)if(t>=a&&t<a+.6){const e=amp*Math.exp(-(t-a)/.12);sx+=e*Math.sin((t-a)*95+a);sy+=e*.7*Math.sin((t-a)*83+a*2)}
  stage.style.transform=sx||sy?`translate(${sx.toFixed(2)}px,${sy.toFixed(2)}px)`:'none';
  const g=$('gl');let gh='';for(const [a,ty] of TR)if(ty==='glitch'&&t>=a-.08&&t<a+.14){const r=rng(400+Math.floor(t*FPS));for(let i=0;i<9;i++){const y=r()*960,h=3+r()*30;gh+=`<i style="position:absolute;left:${(-60+r()*120).toFixed(0)}px;top:${y.toFixed(0)}px;width:${(300+r()*400).toFixed(0)}px;height:${h.toFixed(1)}px;background:${['#fff','#FFD400','#0B0B0B'][Math.floor(r()*3)]};opacity:${(.35+r()*.5).toFixed(2)}"></i>`}
    stage.style.filter=`drop-shadow(${(6*(r()-.5)).toFixed(1)}px 0 0 rgba(255,212,0,.8)) drop-shadow(${(6*(r()-.5)).toFixed(1)}px 0 0 rgba(255,255,255,.5))`}
  g.innerHTML=gh;if(!gh)stage.style.filter='none';
  /* titulky */
  const cap=$('cap');let html='';const capOn=s.cap||s.capS;if(capOn){for(const [cs,i,txt,a,b] of T.chunks){if((!s.capS||s.capS.includes(cs))&&t>=a-(cs==='s1'&&i===0?1:0)&&t<b+.02&&t>=s.t0-.01){html=txt.replace(/\*(.+?)\*/g,'<b>$1</b>');break}}}
  cap.innerHTML=html?`<span>${html}</span>`:'';cap.style.top=(s.capY||664)+'px';
  /* časová osa */
  const tl=$('tl');tl.className=(s.cls==='white'||s.cls==='yel')?'dk2':'';const py=k>0&&SCN[k-1].year?SCN[k-1].year:s.year;const yy=s.year?lerp(py||s.year,s.year,eio(u/.35)):0;tl.style.opacity=s.year?1:0;
  if(s.year){const x=yx(yy);tl.querySelector('.pg').style.width=x.toFixed(1)+'px';tl.querySelector('.cur').style.left=x.toFixed(1)+'px';const yr=tl.querySelector('.yr');yr.style.left=clamp(x,18,374).toFixed(1)+'px';yr.textContent=Math.round(yy);
    tl.querySelectorAll('.ev').forEach(e=>e.classList.toggle('p',+e.dataset.y<=yy+.01))}
  let fl=0;for(const [a,ty] of TR)if(ty==='flash'&&t>=a&&t<a+.14)fl=Math.max(fl,.55*(1-(t-a)/.14));
  if(!s.tr&&k>0&&u<.08)fl=Math.max(fl,.15*(1-u/.08));$('flash').style.opacity=fl.toFixed(3);
  grain(Math.floor(t*FPS+1e-6));
};
const FL=['900 20px IT','850 20px IT','800 20px IT','700 20px IT','600 20px IT','20px JB'];
Promise.all(FL.map(f=>document.fonts.load(f,'ěščřžýáíéúůťďňĚŠČŘŽ„“…—·−✕✓⚠↗→▲□×–')))
 .then(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))))
 .then(()=>document.fonts.ready).then(()=>{window.READY=true;render(0)});
