// node render_sub.js s08 s09 ...  → sXX_slide_01~09.png (1080x1350)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const k of process.argv.slice(2)) {
    await p.goto('file://' + __dirname + '/' + k + '.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    const ss = await p.$$('section.slide');
    for (let i = 0; i < ss.length; i++) {
      await ss[i].screenshot({ path: `${__dirname}/${k}_slide_${String(i + 1).padStart(2, '0')}.png` });
    }
    const over = await p.$$eval('section.slide', els =>
      els.map((e, i) => (e.scrollHeight > e.clientHeight + 2 ? i + 1 : 0)).filter(Boolean));
    console.log(k, ss.length, over.length ? 'OVERFLOW ' + over : 'ok');
  }
  await b.close();
})();
