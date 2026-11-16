# #64 · #65 그래픽 배경 (11/16) (장 2 · 4 · 6 · 8 · 10 · 12) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx64_65.py → node render64.js gfx → p64g · p65g/NN.png
import json
from gfx48_50 import BASE, sec, svg, heart, mug, spot, clock, calendar
from gfx52_55 import people
from gfx48 import say

BG = '#0f1115'
Q = lambda t, col='#ced4da': f'<text x="540" y="1140" text-anchor="middle" font-size="200" font-weight="900" fill="{col}" opacity=".85" font-family="sans-serif">{t}</text>'
G = [
 # ── #64 서운할 때
 (64, 2, sec('', svg(say(330, 130, 420, '괜찮아', '#3a3f4b', '#e9ecef') + heart(540, 1060, 1.4, '#495057')), f'background:{BG}')),
 (64, 4, sec('dark', svg(say(160, 130, 760, '아니야, 별거 아니야', '#3a3f4b', '#e9ecef', 40) + mug(450, 960, .9)))),
 (64, 6, sec('ink', svg(say(160, 130, 760, '너 하고 싶은 대로 해', '#3a3f4b', '#e9ecef', 40) + people(540, 960, 2, '#adb5bd', 170)))),
 (64, 8, sec('', svg(say(240, 130, 600, '나 원래 이래', '#3a3f4b', '#e9ecef') + people(540, 960, 1, '#495057')), f'background:{BG}')),
 (64, 10, sec('wine', svg(Q('4+', '#ffd43b')) + spot(540, 220, 150, '#fff3bf', .35))),
 (64, 12, sec('', svg(say(160, 130, 760, '내가 뭐 서운하게 했어?', '#fee500', '#3a3a3a', 40) + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
 # ── #65 확신이 없을 때
 (65, 2, sec('dark', svg(say(220, 130, 640, '우리 천천히 하자', '#3a3f4b', '#e9ecef') + Q('?')))),
 (65, 4, sec('', svg(say(130, 130, 820, '아직 정의 내리고 싶지 않아', '#3a3f4b', '#e9ecef', 38) + people(540, 960, 2, '#adb5bd', 170)), f'background:{BG}')),
 (65, 6, sec('ink', svg(say(130, 130, 820, '나 지금 연애할 상황이 아니야', '#3a3f4b', '#e9ecef', 38) + clock(540, 1060, 110, 11, 55, '#ced4da')))),
 (65, 8, sec('', svg(say(220, 130, 640, '그냥 지금이 좋아', '#3a3f4b', '#e9ecef') + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (65, 10, sec('wine', calendar(60, 2, .4, 65) + svg(Q('4+', '#ffd43b')))),
 (65, 12, sec('', svg(say(160, 130, 760, '그럼 이번 주말에 얘기하자', '#fee500', '#3a3a3a', 40)) + calendar(900, 2, .3, 66, hi=(0, 5)), f'background:{BG}')),
]

if __name__ == '__main__':
    open('gfx64_65.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open('gfx64_65.json', 'w'))
    print('ok', len(G))
