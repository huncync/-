// 릴스 해결 장면 메모장 그래픽 (투명 배경 1080x1920 · 영상 위에 얹기) · node make_memo.js
// 날짜는 빈칸(○)으로 둬요 · 실제 사연처럼 보이지 않게
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const items = {
  R32_memo: { title: '"헤어지자"고 한 날', rows: ['○월 ○일 · 헤어지자 → ○일 뒤 돌아옴', '○월 ○일 · 헤어지자 → ○일 뒤 돌아옴', '○월 ○일 · '], foot: '세 번 넘으면, 싸움이 아니라 패턴' },
};
const css = `body{margin:0;background:transparent;font-family:'Noto Sans KR',sans-serif}
.wrap{width:1080px;height:1920px;position:relative}
.memo{position:absolute;left:110px;right:110px;top:1000px;background:#fffdf3;border-radius:36px;padding:44px 52px 40px;box-shadow:0 14px 40px rgba(0,0,0,.4);color:#1c1c1c}
.bar{display:flex;justify-content:space-between;font-size:30px;color:#e0a100;font-weight:700;margin-bottom:22px}
h1{margin:0 0 18px;font-size:50px;font-weight:700}
.r{font-size:40px;line-height:1.5;padding:16px 0;border-bottom:2px solid #eee6c8;font-weight:500}
.r:last-of-type{color:#9a9a9a}
.f{margin-top:26px;font-size:36px;font-weight:700;color:#b07800}
.save{position:absolute;left:0;right:0;top:1760px;text-align:center}
.save span{font-size:34px;color:#fff;background:rgba(0,0,0,.55);padding:12px 28px;border-radius:999px}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, m] of Object.entries(items)) {
    const h = `<div class="memo"><div class="bar"><span>‹ 메모</span><span>완료</span></div><h1>${m.title}</h1>${m.rows.map(r => `<div class="r">${r}</div>`).join('')}<div class="f">${m.foot}</div></div><div class="save"><span>📌 저장해두세요</span></div>`;
    await p.setContent(`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@500;700&display=block"><style>${css}</style></head><body><div class="wrap">${h}</div></body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: k + '.png', omitBackground: true });
    console.log(k);
  }
  await b.close();
})();
