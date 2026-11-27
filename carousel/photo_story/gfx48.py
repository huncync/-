# #48 그래픽 배경 (2 · 4 · 6 · 8 · 10 · 12 · 13장) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx48.py → gfx48.html → node render48.js (p48g/NN.png)
from gfx48_50 import BASE, sec, svg, glow, bubbles, calendar, clock, mug, two_circles, spot

def say(x, y, w, t, bg='#3a3f4b', fg='#e9ecef', fs=44):  # 말풍선 + 글자
    return f'<rect x="{x}" y="{y}" width="{w}" height="96" rx="40" fill="{bg}"/><text x="{x+36}" y="{y+63}" font-size="{fs}" font-weight="700" fill="{fg}" font-family="Noto Sans KR,sans-serif">{t}</text>'

def battery(x, y, lv=1, col='#ff6b6b'):
    bars = ''.join(f'<rect x="{x+22+k*92}" y="{y+22}" width="78" height="136" rx="10" fill="{col if k < lv else "#2b2f3a"}"/>' for k in range(4))
    return f'<rect x="{x}" y="{y}" width="400" height="180" rx="28" fill="none" stroke="#ced4da" stroke-width="10"/><rect x="{x+404}" y="{y+56}" width="26" height="68" rx="8" fill="#ced4da"/>' + bars

G = {
 2: sec('', svg('<circle cx="100" cy="170" r="38" fill="#596080"/>' + say(160, 122, 440, '오늘 좀 피곤해') + say(560, 1000, 420, '…', '#fee500', '#3a3a3a')), 'background:#0f1115'),
 4: sec('ink', svg(battery(325, 120, 1) + ''.join(f'<circle cx="{420+k*120}" cy="1080" r="22" fill="#868e96" opacity="{1-k*.3}"/>' for k in range(3)))),
 6: sec('dark', two_circles(180, '#74c0fc', '#ffa94d', 140) + svg('<text x="540" y="1150" text-anchor="middle" font-size="220" font-weight="900" fill="#ced4da" opacity=".8" font-family="sans-serif">?</text>')),
 8: sec('dark', svg('<circle cx="540" cy="210" r="120" fill="#ffd43b"/><circle cx="590" cy="170" r="110" fill="#14171f"/>') + calendar(900, 2, .4, 8, hi=(0, 3))),
 10: sec('wine', calendar(60, 2, .95, 10, cols=('#495057', '#5c5f66')) + svg('<path d="M380 1000 L700 1200 M700 1000 L380 1200" stroke="#ff6b6b" stroke-width="22" stroke-linecap="round" opacity=".85"/>')),
 12: sec('', svg(say(340, 120, 670, '오늘은 푹 쉬어. 내일 얘기하자', '#fee500', '#3a3a3a', 40) + mug(450, 960, .9)), 'background:#0f1115'),
 13: sec('dark', svg('<text x="540" y="330" text-anchor="middle" font-size="240" font-weight="900" fill="#ff6b6b" opacity=".85" font-family="sans-serif">?</text>' + clock(540, 1060, 130, 11, 50, '#868e96'))),
}

if __name__ == '__main__':
    open('gfx48.html', 'w', encoding='utf-8').write(BASE + ''.join(G[k] for k in sorted(G)) + '</body></html>')
    print('ok', sorted(G))
