// node render.js <html> <outdir> → section 순서대로 01.png, 02.png …
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [html, out] = process.argv.slice(2);
  if (!fs.existsSync(out)) fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const els = await p.$$('section');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${out}/${String(i + 1).padStart(2, '0')}.png` });
  console.log(els.length);
  await b.close();
})();
