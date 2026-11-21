// node render56.js gfx → p56g/NN.png  ·  node render56.js c56 → ../c56_slide_NN.png
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const D = '/home/user/-/carousel/photo_story/';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  if (process.argv[2] === 'gfx') {
    const nos = [2, 4, 6, 8, 10, 12];
    if (!fs.existsSync(D + 'p56g')) fs.mkdirSync(D + 'p56g');
    await p.goto('file://' + D + 'gfx56.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const els = await p.$$('section.g');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + 'p56g/' + String(nos[i]).padStart(2, '0') + '.png' });
    console.log('gfx', els.length);
  } else {
    for (const k of process.argv.slice(2)) {
      await p.goto('file://' + D + k + '.html', { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      const els = await p.$$('section.slide');
      for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + '../' + k + '_slide_' + String(i + 1).padStart(2, '0') + '.png' });
      console.log(k, els.length);
    }
  }
  await b.close();
})();
