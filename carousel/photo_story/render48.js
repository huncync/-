// node render48.js gfx    → p48g/02.png … (gfx48.html 섹션을 그래픽 장 번호로)
// node render48.js slides → ../c48_slide_01.png … 14
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const D = '/home/user/-/carousel/photo_story/';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  if (process.argv[2] === 'gfx') {
    const nos = [2, 4, 6, 8, 10, 12, 13];
    await p.goto('file://' + D + 'gfx48.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const els = await p.$$('section.g');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + 'p48g/' + String(nos[i]).padStart(2, '0') + '.png' });
    console.log('gfx', els.length);
  } else {
    const keys = process.argv[2] === 'slides' ? ['c48'] : process.argv.slice(2);  // node render48.js c49 c50 c51
    for (const k of keys) {
      await p.goto('file://' + D + k + '.html', { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      const els = await p.$$('section.slide');
      for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + '../' + k + '_slide_' + String(i + 1).padStart(2, '0') + '.png' });
      console.log(k, els.length);
    }
  }
  await b.close();
})();
