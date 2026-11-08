// The Future's mark: a wireframe globe with continent outlines, hidden-line
// (back hemisphere culled), Alpenglühen gradient. Same geometry, tilt and
// coastline data as the live globe in the-future.world/templates/base.html.
//   node scripts/gen_globe.mjs [out.svg] [spinDeg=-20] [stroke=0.9]
// globe_coast.txt: Natural Earth 110m land (public domain), simplified 0.9°.
import fs from 'fs';
const out = process.argv[2] || 'favicons/globe.svg';
const spin = (+(process.argv[3] ?? -20)) * Math.PI / 180;
const sw = +(process.argv[4] ?? 0.9);
const S = 32, C = 16, R = 14.2, TILT = 0.41;
const coast = fs.readFileSync(new URL('globe_coast.txt', import.meta.url), 'utf8').trim();
function ll(lon, lat) {
  const la = lat * Math.PI / 180, lo = lon * Math.PI / 180;
  return [Math.cos(la) * Math.cos(lo), Math.sin(la), -Math.cos(la) * Math.sin(lo)];
}
function rot([x, y, z]) { // spin about the axis, then the fixed tilt (as the renderer: X then Y order adapted)
  const cy = Math.cos(spin), sy = Math.sin(spin);
  const x1 = x * cy + z * sy, z1 = -x * sy + z * cy;
  const cx = Math.cos(TILT), sx = Math.sin(TILT);
  return [x1, y * cx - z1 * sx, y * sx + z1 * cx];
}
const f = n => n.toFixed(1);
function polyline(pts) { // split into front-facing runs
  const runs = []; let cur = [];
  for (const p of pts) { const q = rot(p); if (q[2] > 0.02) cur.push(q); else { if (cur.length > 1) runs.push(cur); cur = []; } }
  if (cur.length > 1) runs.push(cur);
  return runs.map(r => 'M' + r.map(q => f(C + q[0] * R) + ' ' + f(C - q[1] * R)).join('L')).join('');
}
let grid = '';
for (let i = 1; i < 6; i++) { const lat = -90 + 180 * i / 6, pts = []; for (let j = 0; j <= 96; j++) pts.push(ll(-180 + 360 * j / 96, lat)); grid += polyline(pts); }
for (let i = 0; i < 12; i++) { const lon = -180 + 360 * i / 12, pts = []; for (let j = 0; j <= 96; j++) pts.push(ll(lon, -90 + 180 * j / 96)); grid += polyline(pts); }
let land = '';
for (const ring of coast.split('|')) land += polyline(ring.split(' ').map(s => { const [a, b] = s.split(',').map(Number); return ll(a, b); }));
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${S} ${S}">
  <defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="2" y1="2" x2="30" y2="30"><stop offset="0" stop-color="#f43f5e"/><stop offset=".35" stop-color="#c026d3"/><stop offset=".7" stop-color="#6d28d9"/><stop offset="1" stop-color="#4338ca"/></linearGradient></defs>
  <g fill="none" stroke="url(#g)" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="${C}" cy="${C}" r="${R}" stroke-width="${sw * 1.1}"/>
    <path d="${grid}" stroke-width="${sw * 0.45}" opacity=".55"/>
    <path d="${land}" stroke-width="${sw}"/>
  </g>
</svg>
`;
fs.writeFileSync(out, svg);
console.log(out, svg.length, 'bytes');
