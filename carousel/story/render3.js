const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file:///home/user/-/carousel/story/quiz3.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await (await p.$('#a')).screenshot({ path: '/home/user/-/carousel/story/quiz3.jpg', type: 'jpeg', quality: 90 }); await b.close(); })();
