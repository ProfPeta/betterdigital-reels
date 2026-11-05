/* Shared lead-gen CTA end card for the "Stejný úkol. Dva světy." series.
   Requires: scene(), el(), rise(), slam(), eo(), back(), eio() from the host page. */
function ctaScene(start, end, keyword, next) {
  scene(start, end, 'y', inner => {
    const box = el('div', 'abs', null, inner);
    Object.assign(box.style, {left: '32px', right: '32px', top: 0, bottom: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', paddingBottom: '150px'});
    const l1 = el('div', 'mono', null, box); l1.textContent = 'Chceš to mít taky?'; Object.assign(l1.style, {opacity: 0, color: 'rgba(11,11,11,.6)'});
    const a = el('div', null, 'Napiš', box); Object.assign(a.style, {fontSize: '64px', fontWeight: 850, letterSpacing: '-.045em', lineHeight: 1.02, marginTop: '10px', opacity: 0});
    const chip = el('div', null, keyword, box); Object.assign(chip.style, {alignSelf: 'flex-start', background: '#0B0B0B', color: '#FFD400', fontSize: '60px', fontWeight: 850, letterSpacing: '-.02em', lineHeight: 1, padding: '6px 14px 10px', marginTop: '6px', opacity: 0, transformOrigin: '0 50%'});
    const b = el('div', null, 'do komentářů.', box); Object.assign(b.style, {fontSize: '40px', fontWeight: 820, letterSpacing: '-.04em', lineHeight: 1.05, marginTop: '8px', opacity: 0});
    const c = el('div', null, 'Pošlu ti, jak by to fungovalo u vás.', box); Object.assign(c.style, {fontSize: '20px', fontWeight: 600, marginTop: '14px', opacity: 0});
    const sig = el('div', null, null, box); Object.assign(sig.style, {display: 'flex', alignItems: 'center', gap: '12px', marginTop: '44px', opacity: 0});
    const blk = el('div', null, null, sig); Object.assign(blk.style, {background: '#0B0B0B', borderRadius: '8px', padding: '9px 12px', display: 'flex', alignItems: 'center'});
    blk.innerHTML = '<svg width="74" height="22" viewBox="0 0 74 22"><circle cx="11" cy="11" r="8.5" fill="none" stroke="#fff" stroke-width="3"/><line x1="20" y1="11" x2="52" y2="11" stroke="#fff" stroke-width="3"/><circle cx="63" cy="11" r="10" fill="#FFD400"/></svg>';
    const tx = el('div', null, `<div style="font-size:19px;font-weight:800;letter-spacing:-.03em">Better Digital</div><div class="mono" style="font-size:11px;margin-top:3px;color:rgba(11,11,11,.65)">${next}</div>`, sig);
    return {l1, a, chip, b, c, sig};
  }, (k, lt) => {
    rise(k.l1, lt, .05, .3); rise(k.a, lt, .18, .3); slam(k.chip, lt, .42, .2); rise(k.b, lt, .7, .3); rise(k.c, lt, 1.0, .35); rise(k.sig, lt, 1.35, .35);
  }, .015);
}
