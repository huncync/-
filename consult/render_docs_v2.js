// 새 디자인 문서 렌더 (11/23): python3 docs_v2.py → node render_docs_v2.js
// 세로 전체 → kakao_menu/doc_*.jpg · 4:5 장 → kakao_news/*_N.jpg (예전 장은 지우고 새로)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const D = '/home/user/-/consult/';
const DOCS = [['guide', 'dk', '1:1 남자 심리 분석 안내', '남자들끼리 하는 말 · 채널 안내문'],
              ['form', 'wh', 'APPLICATION · 신청서', '남자들끼리 하는 말 · 신청서'],
              ['report', 'wh', 'REPORT · 결과물', '남자들끼리 하는 말 · 결과물']];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + D + 'kakao_menu/docs_v2.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const [id] of DOCS) {
    await (await p.$('#doc_' + id)).screenshot({ path: D + 'kakao_menu/doc_' + id + '.jpg', type: 'jpeg', quality: 90 });
    console.log('doc_' + id);
  }
  const N = D + 'kakao_news/';
  for (const f of fs.readdirSync(N)) fs.unlinkSync(N + f);
  for (const [id, th, title, label] of DOCS) {
    const n = await p.evaluate(a => flow(...a), [id, th, title, label]);
    for (let k = 1; k <= n; k++) await (await p.$('#' + id + '_' + k)).screenshot({ path: N + id + '_' + k + '.jpg', type: 'jpeg', quality: 90 });
    console.log(id, n);
  }
  await b.close();
})();
