// node render51.js gfx    → p51g/02.png … (gfx51.html 섹션을 그래픽 장 번호로)
// node render51.js slides → ../c51_slide_01.png … 14
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const D = '/home/user/-/carousel/photo_story/';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  if (process.argv[2] === 'gfx') {
    const nos = [2, 4, 6, 8, 10, 12, 13];
    await p.goto('file://' + D + 'gfx51.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const els = await p.$$('section.g');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + 'p51g/' + String(nos[i]).padStart(2, '0') + '.png' });
    console.log('gfx', els.length);
  } else {
    await p.goto('file://' + D + 'c51.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const els = await p.$$('section.slide');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: D + '../c51_slide_' + String(i + 1).padStart(2, '0') + '.png' });
    console.log('slides', els.length);
  }
  await b.close();
})();
