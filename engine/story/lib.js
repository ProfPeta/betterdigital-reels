/* Sdílení pomocníci scén. render(t) musí zůstat čistá funkce času: žádné Date.now(), náhoda jen přes rng(seed). */
const FPS=30;const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-clamp(x),3),e5=x=>1-Math.pow(1-clamp(x),5);
const eio=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const back=x=>{x=clamp(x);const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const lerp=(a,b,p)=>a+(b-a)*p;const $=id=>document.getElementById(id);
function rng(seed){let a=seed>>>0;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const fmt=n=>Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,' ');
function uzel(h,col){const w=h*3.8,sw=h*.12,r=h/2-sw/2;return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="overflow:visible;display:block"><circle cx="${h/2}" cy="${h/2}" r="${r}" fill="none" stroke="${col}" stroke-width="${sw}"/><line x1="${h}" y1="${h/2}" x2="${w-h}" y2="${h/2}" stroke="${col}" stroke-width="${sw}"/><circle cx="${w-h/2}" cy="${h/2}" r="${h/2}" fill="#FFD400"/></svg>`}
const T=window.TL;const st=s=>T.S[s][0],en=s=>T.S[s][1];
const CK={};T.chunks.forEach(([s,i,txt,a,b])=>{(CK[s]=CK[s]||[])[i]=[a,b,txt]});
const ck=(s,i)=>CK[s][i][0];
window.DURATION=T.END;
function slamT(u,s0=1.35,amp=7){const p=e5(u/.1),k=Math.exp(-Math.max(0,u)/.13);
  return `translate(${(amp*k*Math.sin(u*97+1.1)).toFixed(2)}px,${(amp*.7*k*Math.sin(u*83+.3)).toFixed(2)}px) scale(${lerp(s0,1,p).toFixed(4)})`}
const popIn=(e,t,a,d=.22,s0=.6)=>{e.style.opacity=t>=a?1:0;e.style.transform=`scale(${lerp(s0,1,back((t-a)/d)).toFixed(4)})`};
const slideIn=(e,t,a,dy=24,d=.3)=>{const p=e5((t-a)/d);e.style.opacity=t>=a?p:0;e.style.transform=`translateY(${(dy*(1-p)).toFixed(1)}px)`};
const slideX=(e,t,a,dx=60,d=.35)=>{const p=e5((t-a)/d);e.style.opacity=t>=a?p:0;e.style.transform=`translateX(${(dx*(1-p)).toFixed(1)}px)`};
const stampIn=(e,t,a,rot=-8,s0=1.8)=>{e.style.opacity=t>=a?1:0;if(t>=a)e.style.transform=`rotate(${rot}deg) `+slamT(t-a,s0,6)};
const fade=(e,t,a,d=.25)=>{e.style.opacity=clamp((t-a)/d).toFixed(3)};
const typeTo=(e,txt,t,a,cps=22)=>{const n=Math.max(0,Math.floor((t-a)*cps));e.textContent=t>=a?txt.slice(0,n):''};
/* prvky */
const FLAG=w=>`<svg width="${w}" height="${w*2/3}" viewBox="0 0 24 16" style="display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.15)"><rect width="24" height="16" fill="#fff"/><rect y="8" width="24" height="8" fill="#D7141A"/><path d="M0 0 L12 8 L0 16Z" fill="#11457E"/></svg>`;
const PERSON=(c,w=24,dash=0)=>dash?`<svg width="${w}" height="${w*1.25}" viewBox="0 0 30 38"><circle cx="15" cy="9" r="7.5" fill="none" stroke="${c}" stroke-width="1.6" stroke-dasharray="3 3"/><path d="M2 37 C 3 24, 8 20, 15 20 C 22 20, 27 24, 28 37 Z" fill="none" stroke="${c}" stroke-width="1.6" stroke-dasharray="3 3"/></svg>`:`<svg width="${w}" height="${w*1.25}" viewBox="0 0 30 38"><circle cx="15" cy="9" r="8" fill="${c}"/><path d="M1 38 C 2 23, 8 19, 15 19 C 22 19, 28 23, 29 38 Z" fill="${c}"/></svg>`;
const PLANE=`<svg width="34" height="34" viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="#fff"/></svg>`;
const BADGE=()=>`<span class="badge">${(window.CFG&&CFG.series)||'POSTAVILI TO'} <b>${(window.CFG&&CFG.badge)||''}</b>${FLAG(20)}</span>`;
