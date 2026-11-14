# #57 ~ #60 그래픽 배경 (11/13 · 2판 소재) (장 2 · 4 · 6 · 7 · 8 · 10 · 12) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx57_60.py → node render57.js gfx → p57g ~ p60g/NN.png
import json
from gfx48_50 import BASE, sec, svg, glow, bubbles, calendar, heart, clock, mug, spot, phone, post, two_circles
from gfx52_55 import people
from gfx48 import say

BG = '#0f1115'
def contact(name, col='#e9ecef', av='#596080', x=390):  # 휴대폰 연락처 화면
    inner = (f'<div style="position:absolute;left:0;right:0;top:70px;text-align:center"><div style="width:110px;height:110px;border-radius:50%;background:{av};margin:0 auto"></div>'
             f'<div style="margin-top:26px;font:800 40px Noto Sans KR,sans-serif;color:{col}">{name}</div></div>')
    return phone(x, 30, 300, 360, inner)
def camera(cx, cy, s=1, col='#e9ecef'):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><rect x="-130" y="-80" width="260" height="170" rx="26" fill="none" stroke="{col}" stroke-width="12"/>'
            f'<rect x="-60" y="-110" width="80" height="34" rx="8" fill="{col}"/><circle cx="0" cy="5" r="52" fill="none" stroke="{col}" stroke-width="12"/></g>')
def thumbs(y, n, cols=('#ffa8a8', '#b197fc', '#74c0fc', '#ffd43b', '#63e6be')):
    return ''.join(f'<rect x="{150 + (k % 4) * 200}" y="{y + (k // 4) * 170}" width="170" height="150" rx="12" fill="{cols[k % len(cols)]}" opacity=".85"/>' for k in range(n))

G = [
 # ── #57 놓치면 안 되는 여자
 (57, 2, sec('', svg(say(160, 130, 700, '야, 그 여자는 놓치지 마라', '#3a3f4b', '#e9ecef', 40) + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (57, 4, sec('dark', svg(people(540, 110, 3, '#495057') + people(540, 110, 1, '#ffd43b') + heart(540, 1060, 1.3, '#ff8fab', .9)))),
 (57, 6, sec('wine', svg(say(380, 130, 320, '고마워', '#fee500', '#3a3a3a') + heart(540, 1060, 1.6, '#ff6b81', .9)))),
 (57, 7, sec('ink', svg(people(540, 960, 1, '#ffd43b')) + spot(540, 220, 150, '#fff3bf', .45))),
 (57, 8, sec('', svg(say(160, 130, 700, '걔는 나 안 깎아내려', '#3a3f4b', '#e9ecef') + mug(450, 960, .9)), f'background:{BG}')),
 (57, 10, sec('dark', svg(people(540, 110, 3, '#495057') + '<path d="M540 940 L660 1160 L420 1160Z" fill="none" stroke="#ffd43b" stroke-width="14" stroke-linejoin="round"/><text x="540" y="1140" text-anchor="middle" font-size="120" font-weight="900" fill="#ffd43b" font-family="sans-serif">!</text>'))),
 (57, 12, sec('', svg(say(200, 130, 680, '오늘 진짜 고마웠어', '#fee500', '#3a3a3a') + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
 # ── #58 무서워하는 순간
 (58, 2, sec('', svg('<text x="540" y="330" text-anchor="middle" font-size="240" font-weight="900" fill="#74c0fc" opacity=".85" font-family="sans-serif">?</text>' + people(540, 960, 1, '#adb5bd')), f'background:{BG}')),
 (58, 4, sec('dark', svg(clock(540, 230, 140, 11, 55, '#ced4da') + '<path d="M380 1080 h320" stroke="#495057" stroke-width="18" stroke-linecap="round"/>'))),
 (58, 6, sec('ink', svg(people(540, 110, 3, '#ff8fab', 170) + people(540, 960, 1, '#adb5bd')))),
 (58, 7, sec('wine', svg(''.join(f'<path transform="translate({x},{y})" d="M0 -40 C 25 -5 30 15 0 40 C -30 15 -25 -5 0 -40Z" fill="#74c0fc" opacity=".8"/>' for x, y in [(440, 180), (540, 240), (640, 170)]) + people(540, 960, 1, '#adb5bd')))),
 (58, 8, sec('', svg(say(160, 130, 760, '아무것도 못 하겠더라', '#3a3f4b', '#e9ecef', 40) + mug(450, 960, .9)), f'background:{BG}')),
 (58, 10, sec('dark', glow(58, 16, ('#a5d8ff', '#74c0fc', '#ffffff'), 0, 380, .4) + svg(heart(540, 1060, 1.4, '#74c0fc', .7)))),
 (58, 12, sec('', svg(say(220, 130, 660, '옆에만 있어줘', '#fee500', '#3a3a3a') + people(540, 960, 2, '#adb5bd', 170)), f'background:{BG}')),
 # ── #59 잘해주는 vs 좋아하는
 (59, 2, sec('dark', two_circles(200, '#74c0fc', '#ff8787', 140) + svg('<text x="540" y="1140" text-anchor="middle" font-size="200" font-weight="900" fill="#ced4da" opacity=".85" font-family="sans-serif">?</text>'))),
 (59, 4, sec('ink', svg(people(540, 110, 4, '#868e96', 170) + heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (59, 6, sec('', bubbles([('him', 420), ('me', 300), ('him', 360)], 70) + svg(heart(540, 1060, 1.3, '#495057')), f'background:{BG}')),
 (59, 7, sec('wine', calendar(60, 2, .35, 59, hi=(1, 5)) + svg(heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (59, 8, sec('', svg(say(160, 130, 760, '원래 다 잘해줘', '#3a3f4b', '#e9ecef') + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (59, 10, sec('dark', svg(''.join(f'<rect x="330" y="{60 + k * 90}" width="60" height="60" rx="12" fill="#20c997"/><path d="M343 {90 + k * 90} l15 15 l25 -30" stroke="#0f1115" stroke-width="10" fill="none"/><rect x="420" y="{78 + k * 90}" width="330" height="24" rx="12" fill="#495057"/>' for k in range(4)) + heart(540, 1060, 1.3, '#495057')))),
 (59, 12, sec('', svg(say(240, 130, 600, '이번 주말엔 뭐 해?', '#fee500', '#3a3a3a')) + calendar(900, 2, .3, 60, hi=(0, 5)), f'background:{BG}')),
 # ── #60 3개월 차
 (60, 2, sec('dark', calendar(60, 2, .6, 61) + svg('<text x="540" y="1140" text-anchor="middle" font-size="180" font-weight="900" fill="#ffd43b" font-family="Noto Sans KR,sans-serif">3개월</text>'))),
 (60, 4, sec('wine', svg('<path d="M560 60 L440 250 L540 250 L480 400 L660 190 L560 190 L620 60Z" fill="#ffd43b" opacity=".9"/>' + heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (60, 6, sec('ink', svg(people(540, 110, 3, '#adb5bd') + people(540, 960, 2, '#ff8fab', 170)))),
 (60, 7, sec('dark', calendar(60, 2, .4, 62, hi=(1, 6)) + svg('<path d="M380 1060 h240 l-40 -40 M620 1060 l-40 40" stroke="#ffd43b" stroke-width="16" fill="none" stroke-linecap="round"/>'))),
 (60, 8, sec('', svg(say(160, 130, 760, '3개월 지나니까 편해졌어', '#3a3f4b', '#e9ecef', 40) + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (60, 10, sec('wine', svg(say(200, 130, 680, '너 처음이랑 달라졌어', '#3a3f4b', '#e9ecef') + '<path d="M480 1010 L600 1130 M600 1010 L480 1130" stroke="#ff6b6b" stroke-width="18" stroke-linecap="round"/>'))),
 (60, 12, sec('', svg(say(220, 130, 640, '다음엔 이렇게 하자', '#fee500', '#3a3a3a') + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
]

if __name__ == '__main__':
    open('gfx57_60.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open('gfx57_60.json', 'w'))
    print('ok', len(G))
