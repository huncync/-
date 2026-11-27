// node render.js → sample/feed_01~08.png (1080×1350) + highlight.png (1080×1920)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const D = __dirname + '/sample/';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + D + 'feed.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const els = await p.$$('section.s');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + 'feed_' + String(i + 1).padStart(2, '0') + '.png' });
  await p.goto('file://' + D + 'highlight.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await (await p.$('section')).screenshot({ path: D + 'highlight.png' });
  await b.close();
})();
