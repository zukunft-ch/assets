import { chromium } from 'playwright';
import fs from 'fs';
// Render the brand images from the icon + wordmark with real fonts (Playwright).
//   node scripts/render_brand.mjs '<repos JSON>' '<og JSON>'
//   repos: [["repo-name","one line"], ...]   -> out/social-<repo>.png (1280x640)
//   og:    [["de","die zukunft.","Wir bauen sie.","Eine neue Schweizer Partei","die-zukunft.ch"], ...] -> out/og-<lang>.png
//   articles (3rd arg): [["de","Title","Aktuelles","7. November 2026","die-zukunft.ch","<slug>"], ...] -> out/<slug>.<lang>.png
//   Always renders out/apple-touch-icon.png, icon-192.png, icon-512.png, org-avatar.png.
// Env: OUT (default ./out/), FONTS (default ../avenir/static/fonts, i.e. the theme clone next to this repo).
// Other sites (the-future.world): ICON_FILE (path to the mark SVG), BRAND_WM, BRAND_SUB, BRAND_HOST
//   (wordmark, tagline and host on the social previews; defaults are the Swiss chapter's).
// Needs: npm i playwright, plus Google Chrome installed (channel: 'chrome').
import path from 'path';
const OUT = (process.env.OUT || path.resolve('out')) + '/';
const FONTS = process.env.FONTS || path.resolve('../avenir/static/fonts');
fs.mkdirSync(OUT, { recursive: true });
const ICON = 'data:image/svg+xml;base64,' + fs.readFileSync(process.env.ICON_FILE || new URL('../favicons/favicon.svg', import.meta.url)).toString('base64');
const BRAND_WM = process.env.BRAND_WM || 'die zukunft.', BRAND_SUB = process.env.BRAND_SUB || 'Eine neue Schweizer Partei', BRAND_HOST = process.env.BRAND_HOST || 'die-zukunft.ch';
const FONT_CSS = `@font-face{font-family:"Clash Display";font-weight:700;src:url("file://${FONTS}/clash-display-700.woff2")}
@font-face{font-family:"Switzer";font-weight:100 900;src:url("file://${FONTS}/switzer-variable.woff2")}`;
const GRAD = 'linear-gradient(100deg,#f43f5e 0%,#c026d3 33%,#6d28d9 67%,#4338ca 100%)';
const b = await chromium.launch({ channel: 'chrome' });
async function shot(html, w, h, out, transparent=false) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await p.setContent('<!doctype html><meta charset=utf-8><style>'+FONT_CSS+'*{margin:0;box-sizing:border-box}html,body{width:'+w+'px;height:'+h+'px;overflow:hidden}</style>'+html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
  await p.screenshot({ path: out, omitBackground: transparent }); await p.close();
}
// app icons: G2 on white, inside the maskable safe zone (icon ~60% of the tile)
const tile = (s, pct) => '<body style="background:#fff;display:grid;place-items:center"><img src="'+ICON+'" style="width:'+Math.round(s*pct)+'px;height:'+Math.round(s*pct)+'px"></body>';
await shot(tile(180,.72), 180, 180, OUT+'apple-touch-icon.png');
await shot(tile(192,.72), 192, 192, OUT+'icon-192.png');
await shot(tile(512,.60), 512, 512, OUT+'icon-512.png');
// org avatar
await shot(tile(1024,.74), 1024, 1024, OUT+'org-avatar.png');
// social previews
const repos = JSON.parse(process.argv[2]);
for (const [name, line] of repos) {
  const html = '<body style="background:#eef0ec;font-family:Switzer;color:#121517;padding:72px 84px;display:flex;flex-direction:column;justify-content:space-between;background-image:radial-gradient(120% 80% at 50% -10%,#fff 0%,rgba(255,255,255,0) 60%)">'
   + '<div style="display:flex;align-items:center;gap:16px;font:500 22px ui-monospace,SF Mono,Menlo,monospace;letter-spacing:.06em;color:#4f565b;text-transform:uppercase"><span style="width:42px;height:3px;border-radius:3px;background:'+GRAD+'"></span>github.com/zukunft-ch/'+name+'</div>'
   + '<div style="display:flex;align-items:center;gap:44px"><img src="'+ICON+'" style="width:200px;height:200px"><div>'
   + '<div style="font-family:Clash Display;font-weight:700;font-size:118px;line-height:.9;letter-spacing:-.022em;background:'+GRAD+';-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;padding-bottom:.07em;white-space:nowrap">'+BRAND_WM+'</div>'
   + '<div style="font-size:30px;font-weight:600;letter-spacing:-.02em;margin-top:18px;max-width:760px;line-height:1.25">'+line+'</div></div></div>'
   + '<div style="display:flex;justify-content:space-between;font:500 20px ui-monospace,SF Mono,Menlo,monospace;letter-spacing:.06em;color:#6b7276;text-transform:uppercase"><span>'+BRAND_SUB+'</span><span>'+BRAND_HOST+'</span></div></body>';
  await shot(html, 1280, 640, OUT+'social-'+name+'.png');
}
// OG images per language (1200x630)
const og = JSON.parse(process.argv[3] || '[]');
for (const [lang, wm, line, sub, host] of og) {
  const html = '<body style="background:#eef0ec;font-family:Switzer;color:#121517;padding:64px 76px;display:flex;flex-direction:column;justify-content:space-between;background-image:radial-gradient(120% 80% at 50% -10%,#fff 0%,rgba(255,255,255,0) 60%)">'
   + '<div style="display:flex;align-items:center;gap:16px;font:500 21px ui-monospace,SF Mono,Menlo,monospace;letter-spacing:.06em;color:#4f565b;text-transform:uppercase"><span style="width:42px;height:3px;border-radius:3px;background:'+GRAD+'"></span>'+sub+'</div>'
   + '<div style="display:flex;align-items:center;gap:40px"><img src="'+ICON+'" style="width:190px;height:190px"><div>'
   + '<div style="font-family:Clash Display;font-weight:700;font-size:112px;line-height:.9;letter-spacing:-.022em;background:'+GRAD+';-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;padding-bottom:.07em;white-space:nowrap">'+wm+'</div>'
   + '<div style="font-size:34px;font-weight:620;letter-spacing:-.025em;margin-top:16px;max-width:700px;line-height:1.2">'+line+'</div></div></div>'
   + '<div style="display:flex;justify-content:flex-end;font:500 20px ui-monospace,SF Mono,Menlo,monospace;letter-spacing:.06em;color:#6b7276;text-transform:uppercase"><span>'+host+'</span></div></body>';
  await shot(html, 1200, 630, OUT+'og-'+lang+'.png');
}
// Article OG cards (1200x630): [["de","Title","Aktuelles","7. November 2026","die-zukunft.ch","<slug>"], ...]
const art = JSON.parse(process.argv[4] || '[]');
for (const [lang, title, kicker, date, host, slug] of art) {
  const html = '<body style="background:#eef0ec;font-family:Switzer;color:#121517;padding:60px 72px;display:flex;flex-direction:column;justify-content:space-between;background-image:radial-gradient(120% 80% at 50% -10%,#fff 0%,rgba(255,255,255,0) 60%)">'
   + '<div style="display:flex;align-items:center;justify-content:space-between"><div style="display:flex;align-items:center;gap:16px;font:500 21px ui-monospace,SF Mono,Menlo,monospace;letter-spacing:.06em;color:#4f565b;text-transform:uppercase"><span style="width:42px;height:3px;border-radius:3px;background:'+GRAD+'"></span>'+kicker+' · '+date+'</div><img src="'+ICON+'" style="width:92px;height:92px"></div>'
   + '<div style="font-size:'+(title.length>60?62:72)+'px;font-weight:650;letter-spacing:-.04em;line-height:1.02;max-width:1000px;text-wrap:balance">'+title+'</div>'
   + '<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-family:Clash Display;font-weight:700;font-size:44px;letter-spacing:-.015em;background:'+GRAD+';-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;padding-bottom:.07em">'+({de:'die zukunft.',fr:'le futur.',it:'il futuro.',en:'the future.'}[lang])+'</span><span style="font:500 20px ui-monospace,SF Mono,Menlo,monospace;letter-spacing:.06em;color:#6b7276;text-transform:uppercase">'+host+'</span></div></body>';
  await shot(html, 1200, 630, OUT+slug+'.'+lang+'.png');
}
await b.close();
