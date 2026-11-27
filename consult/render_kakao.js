// 카톡 메뉴 이미지 렌더: km.html(m1~m6) · km_one.html(all) · docs.html(card_*, doc_*)
// node render_kakao.js  (python3 kakao_menu.py · python3 kakao_docs.py 다음에)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const D = '/home/user/-/consult/kakao_menu/';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  for (const f of ['km.html', 'km_one.html', 'docs.html']) {
    await p.goto('file://' + D + f, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    for (const el of await p.$$('section[id]')) {
      const id = await el.getAttribute('id');
      await el.screenshot({ path: D + id + '.jpg', type: 'jpeg', quality: 92 });
      console.log(id);
    }
  }
  await b.close();
})();
