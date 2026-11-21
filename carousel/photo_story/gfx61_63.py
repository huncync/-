# #61 ~ #63 그래픽 배경 (11/15) (장 2 · 4 · 6 · 8 · 10 · 12) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx61_63.py → node render61.js gfx → p61g ~ p63g/NN.png
import json
from gfx48_50 import BASE, sec, svg, heart, mug, spot, clock, bubbles
from gfx52_55 import people
from gfx48 import say
from gfx57_60 import contact

BG = '#0f1115'
X = '<path d="M480 1010 L600 1130 M600 1010 L480 1130" stroke="#ff6b6b" stroke-width="18" stroke-linecap="round"/>'
DOWN = '<rect x="390" y="60" width="300" height="360" rx="40" fill="#1c1f26" stroke="#495057" stroke-width="10"/><circle cx="540" cy="140" r="14" fill="#495057"/>'
G = [
 # ── #61 떠날 준비
 (61, 2, sec('dark', svg(people(540, 110, 2, '#adb5bd', 170) + heart(540, 1060, 1.4, '#495057')))),
 (61, 4, sec('', svg(say(200, 130, 680, '농담이었어~', '#3a3f4b', '#e9ecef') + people(540, 960, 3, '#495057')), f'background:{BG}')),
 (61, 6, sec('ink', svg(clock(540, 230, 140, 1, 30, '#ced4da') + heart(540, 1060, 1.3, '#495057')))),
 (61, 8, sec('', svg(say(160, 130, 760, '그냥 조용히 있을래', '#3a3f4b', '#e9ecef', 40) + mug(450, 960, .9)), f'background:{BG}')),
 (61, 10, sec('wine', svg(say(330, 130, 420, '고마워', '#fee500', '#3a3a3a') + heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (61, 12, sec('', svg(say(200, 130, 680, '오늘 일만 얘기하자', '#fee500', '#3a3a3a') + people(540, 960, 2, '#adb5bd', 170)), f'background:{BG}')),
 # ── #62 친구들한테 하는 말
 (62, 2, sec('', svg(say(200, 130, 680, '그때 걔가 말이야…', '#3a3f4b', '#e9ecef') + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (62, 4, sec('dark', svg(say(220, 130, 640, '걔 얘기 하지 마', '#3a3f4b', '#e9ecef') + people(540, 960, 1, '#adb5bd')))),
 (62, 6, sec('ink', svg(say(160, 130, 760, '내가 너무 못 해줬지', '#3a3f4b', '#e9ecef', 40) + heart(540, 1060, 1.4, '#74c0fc', .7)))),
 (62, 8, sec('', svg(say(160, 130, 760, '걔 요즘 잘 지낸대?', '#3a3f4b', '#e9ecef') + people(540, 960, 3, '#495057')), f'background:{BG}')),
 (62, 10, sec('dark', svg(people(540, 110, 3, '#495057') + '<text x="540" y="1130" text-anchor="middle" font-size="160" font-weight="900" fill="#495057" font-family="sans-serif">…</text>'))),
 (62, 12, sec('wine', svg(people(540, 960, 1, '#ffd43b')) + spot(540, 220, 150, '#fff3bf', .45))),
 # ── #63 휴대폰 속 그 이름
 (63, 2, sec('', contact('김대리') + svg(heart(540, 1060, 1.3, '#495057')), f'background:{BG}')),
 (63, 4, sec('dark', svg(DOWN + people(540, 960, 1, '#adb5bd')))),
 (63, 6, sec('', bubbles([('him', 420), ('him', 360), ('him', 300)], 70) + svg(heart(540, 1060, 1.3, '#495057')), f'background:{BG}')),
 (63, 8, sec('ink', svg(say(160, 130, 760, '그냥 친구면 왜 숨겨', '#3a3f4b', '#e9ecef') + mug(450, 960, .9)))),
 (63, 10, sec('wine', svg(DOWN + X))),
 (63, 12, sec('', svg(say(130, 130, 820, '아까 연락 온 사람 누구야?', '#fee500', '#3a3a3a', 38) + people(540, 960, 2, '#adb5bd', 170)), f'background:{BG}')),
]

if __name__ == '__main__':
    open('gfx61_63.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open('gfx61_63.json', 'w'))
    print('ok', len(G))
