// 영상 장 글 상자만 투명 PNG로: node render_ov.js c68 1 14 → p68/ov_01.png, p68/ov_14.png (vidgen.py가 영상 위에 얹어요)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const D = '/home/user/-/carousel/photo_story/';
(async () => {
  const [k, ...nums] = process.argv.slice(2);
  const no = k.replace('c', '');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + D + k + '.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: 'html,body{background:transparent !important}' });
  for (const n of nums) {
    await (await p.$('#s' + n)).screenshot({ path: D + 'p' + no + '/ov_' + String(n).padStart(2, '0') + '.png', omitBackground: true });
    console.log('ov', n);
  }
  await b.close();
})();
