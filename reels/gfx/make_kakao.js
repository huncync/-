// 릴스 해결 장면에 얹는 카톡 말풍선 (투명 배경 PNG · 1080x1920 영상 위에 그대로 얹기)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const items = {
  R9_solution: [['me', '알겠어. 그동안 고마웠어.']],
  R9_lastwords: [['him', '너는 좋은 사람이야.'], ['him', '내가 부족해서 그래.'], ['him', '잘 지내.']],
  R10_solution: [['her', '화난 거 아니야.\n이 얘기가 나한테 중요해서 그래.'], ['him', '천천히 말해. 다 들을게.']],
  R32_solution: [['him', '우리 그만하자.'], ['her', '응, 알겠어.']],
};
const only = process.argv.slice(2);
const css = `body{margin:0;background:transparent;font-family:'Noto Sans KR',sans-serif}
.wrap{width:1080px;height:1920px;position:relative}
.box{position:absolute;left:90px;right:90px;top:1080px;display:flex;flex-direction:column;gap:34px}
.b{max-width:760px;padding:30px 40px;border-radius:44px;font-size:50px;line-height:1.45;font-weight:700;white-space:pre-line;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.me,.her{align-self:flex-end;background:#fee500;color:#191919;border-top-right-radius:12px}
.him{align-self:flex-start;background:#fff;color:#191919;border-top-left-radius:12px}
.who{font-size:30px;color:#fff;margin:0 10px -22px;text-shadow:0 2px 8px rgba(0,0,0,.6)}
.who.r{align-self:flex-end}.save{align-self:center;margin-top:16px;font-size:34px;color:#fff;background:rgba(0,0,0,.55);padding:12px 28px;border-radius:999px}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [k, rows] of Object.entries(items)) {
    if (only.length && !only.includes(k)) continue;
    const h = rows.map(([w, t]) => (w === 'me' || (w === 'him' && k === 'R9_lastwords' && rows.indexOf(rows.find(r => r[1] === t)) > 0) ? '' : `<div class="who ${w === 'her' ? 'r' : ''}">${w === 'her' ? '그녀' : '그'}</div>`) + `<div class="b ${w}">${t}</div>`).join('');
    await p.setContent(`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=block"><style>${css}</style></head><body><div class="wrap"><div class="box">${h}${k.endsWith('_solution') ? '<div class="save">📌 저장해두세요</div>' : ''}</div></div></body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: k + '.png', omitBackground: true });
    console.log(k);
  }
  await b.close();
})();
