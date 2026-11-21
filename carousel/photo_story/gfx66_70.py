# #66 ~ #70 그래픽 배경 (장 2 · 4 · 6 · 8 · 10 · 12)
import json
from gfx48_50 import BASE, sec, svg, heart, mug, spot, clock, calendar
from gfx52_55 import people
from gfx48 import say
from gfx57_60 import contact
BG = '#0f1115'
Q = lambda t, col='#ced4da', fs=200: f'<text x="540" y="1140" text-anchor="middle" font-size="{fs}" font-weight="900" fill="{col}" opacity=".85" font-family="Noto Sans KR,sans-serif">{t}</text>'
X = '<path d="M480 1010 L600 1130 M600 1010 L480 1130" stroke="#ff6b6b" stroke-width="18" stroke-linecap="round"/>'
G = [
 (66, 2, sec('dark', svg(people(540, 110, 1, '#adb5bd') + heart(540, 1060, 1.4, '#495057')))),
 (66, 4, sec('', svg(say(240, 130, 600, '오히려 편해', '#3a3f4b', '#e9ecef') + mug(450, 960, .9)), f'background:{BG}')),
 (66, 6, sec('wine', svg(people(540, 110, 3, '#495057') + Q('3', '#ffd43b')))),
 (66, 8, sec('', svg(say(130, 130, 820, '이번엔 진짜 끝이야', '#3a3f4b', '#e9ecef', 40) + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (66, 10, sec('ink', svg(clock(540, 230, 140, 3, 10, '#ced4da') + people(540, 960, 1, '#ffd43b')))),
 (66, 12, sec('', svg(say(200, 130, 680, '잘 지내? 그냥 생각나서', '#fee500', '#3a3a3a', 40) + heart(540, 1060, 1.3, '#ff8fab', .9)), f'background:{BG}')),
 (67, 2, sec('dark', calendar(60, 2, .5, 67, hi=(1, 3)) + svg(heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (67, 4, sec('', svg(say(130, 130, 820, '갖고 싶은 거 있어? 그냥 말해', '#3a3f4b', '#e9ecef', 38) + Q('?')), f'background:{BG}')),
 (67, 6, sec('ink', svg(say(240, 130, 600, '아, 오늘이었어?', '#3a3f4b', '#e9ecef') + X))),
 (67, 8, sec('wine', svg(heart(540, 230, 1.8, '#ff8fab', .9) + people(540, 960, 2, '#adb5bd', 170)))),
 (67, 10, sec('dark', calendar(60, 2, .4, 68) + svg(Q('4', '#ffd43b')))),
 (67, 12, sec('', svg(say(220, 130, 640, '이번엔 내가 챙길게', '#fee500', '#3a3a3a') + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
 (68, 2, sec('dark', svg(clock(540, 230, 140, 11, 50, '#ced4da') + people(540, 960, 1, '#adb5bd')))),
 (68, 4, sec('', svg(say(220, 130, 640, '걔 요즘 어때?', '#3a3f4b', '#e9ecef') + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (68, 6, sec('ink', svg(people(540, 110, 3, '#495057') + people(540, 960, 1, '#ffd43b')))),
 (68, 8, sec('', svg(say(130, 130, 820, '연락하고 싶은데, 핑계가 없어', '#3a3f4b', '#e9ecef', 38) + mug(450, 960, .9)), f'background:{BG}')),
 (68, 10, sec('wine', contact('잘 지내?', '#e9ecef', '#596080', 390) + svg(heart(540, 1060, 1.3, '#495057')))),
 (68, 12, sec('', svg(say(240, 130, 600, '응, 잘 지내. 너는?', '#fee500', '#3a3a3a') + people(540, 960, 2, '#adb5bd', 170)), f'background:{BG}')),
 (69, 2, sec('dark', svg(heart(540, 230, 1.8, '#ff8fab', .9) + people(540, 960, 1, '#ffd43b')))),
 (69, 4, sec('', svg(say(330, 130, 420, '나 도착', '#3a3f4b', '#e9ecef') + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
 (69, 6, sec('ink', svg(people(540, 110, 3, '#ff8fab', 170) + people(540, 960, 2, '#adb5bd', 170)))),
 (69, 8, sec('', svg(say(130, 130, 820, '걔가 좋아하는 건 다 기억나', '#3a3f4b', '#e9ecef', 38) + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (69, 10, sec('wine', svg(Q('5', '#ffd43b')) + spot(540, 220, 150, '#fff3bf', .35))),
 (69, 12, sec('', svg(say(220, 130, 640, '기억해 줘서 고마워', '#fee500', '#3a3a3a') + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
 (70, 2, sec('dark', svg(people(540, 110, 2, '#adb5bd', 170) + Q('?')))),
 (70, 4, sec('', svg(say(220, 130, 640, '미안해, 잘할게', '#3a3f4b', '#e9ecef') + Q('?', '#495057')), f'background:{BG}')),
 (70, 6, sec('ink', calendar(60, 2, .4, 70, hi=(0, 3)) + svg(people(540, 960, 1, '#adb5bd')))),
 (70, 8, sec('', svg(say(130, 130, 820, '솔직히 무서워서 잡았어', '#3a3f4b', '#e9ecef', 40) + mug(450, 960, .9)), f'background:{BG}')),
 (70, 10, sec('wine', svg(heart(540, 230, 1.6, '#ff8fab', .9) + Q('1', '#ffd43b')))),
 (70, 12, sec('', calendar(60, 2, .35, 71, hi=(1, 6)) + svg(say(160, 900, 760, '한 달 안에 보이면, 다시', '#fee500', '#3a3a3a', 40)), f'background:{BG}')),
]
if __name__ == '__main__':
    open('gfx66_70.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open('gfx66_70.json', 'w'))
    print('ok', len(G))
