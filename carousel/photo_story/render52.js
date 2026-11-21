// node render52.js gfx         → gfx52_55.html 섹션을 p52g ~ p55g/NN.png로 (순서는 gfx52_55.json)
// node render52.js c52 c53 …   → ../c52_slide_01.png …
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const D = '/home/user/-/carousel/photo_story/';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  if (process.argv[2] === 'gfx') {
    const order = JSON.parse(fs.readFileSync(D + 'gfx52_55.json', 'utf8'));
    await p.goto('file://' + D + 'gfx52_55.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const els = await p.$$('section.g');
    for (let i = 0; i < els.length; i++) {
      const [n, s] = order[i]; const dir = D + 'p' + n + 'g/';
      if (!fs.existsSync(dir)) fs.mkdirSync(dir);
      await els[i].screenshot({ path: dir + String(s).padStart(2, '0') + '.png' });
    }
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
