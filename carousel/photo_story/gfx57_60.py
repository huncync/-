# #57 ~ #60 그래픽 배경 (장 2 · 4 · 6 · 7 · 8 · 10 · 12) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx57_60.py → node render57.js gfx → p57g ~ p60g/NN.png
import json
from gfx48_50 import BASE, sec, svg, glow, bubbles, calendar, heart, clock, mug, spot, phone, post
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
 # ── #57 저장명
 (57, 2, sec('', phone(390, 30, 300, 360, ''.join(f'<div style="position:absolute;left:30px;right:30px;top:{50 + k * 70}px;height:40px;border-radius:12px;background:{"#ff8fab" if k == 2 else "#3a3f4b"}"></div>' for k in range(4))) + svg(heart(540, 1060, 1.3, '#495057')), f'background:{BG}')),
 (57, 4, sec('dark', contact('김지은 소개팅') + svg(people(540, 960, 2, '#adb5bd', 200)))),
 (57, 6, sec('wine', contact('지은 ♥', '#ff8fab') + svg(heart(540, 1060, 1.6, '#ff6b81', .9)))),
 (57, 7, sec('ink', contact('꼬꼬마', '#ffd43b', '#ffa94d') + glow(57, 14, ('#ffd27f', '#ff8fab'), 900, 1250, .35))),
 (57, 8, sec('', svg(say(160, 130, 640, '저장명 뭐야? ㅋㅋ 보여줘 봐', '#3a3f4b', '#e9ecef', 40) + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (57, 10, sec('dark', contact('김지은', '#868e96', '#495057') + svg('<path d="M500 1010 L580 1110 M580 1010 L500 1110" stroke="#495057" stroke-width="14" stroke-linecap="round"/>' + heart(540, 1060, 1.4, '#343a40', .9)))),
 (57, 12, sec('', svg(say(240, 130, 620, '나 뭐라고 저장했어? ㅋㅋ', '#fee500', '#3a3a3a', 40) + heart(540, 1060, 1.4, '#ff8fab', .9)), f'background:{BG}')),
 # ── #58 첫 데이트
 (58, 2, sec('', svg(say(160, 130, 520, '야 오늘 어땠어?', '#3a3f4b', '#e9ecef') + people(540, 960, 2, '#adb5bd', 200)), f'background:{BG}')),
 (58, 4, sec('dark', svg(say(340, 130, 420, '괜찮던데?', '#3a3f4b', '#e9ecef') + clock(540, 1060, 120, 9, 0, '#868e96')))),
 (58, 6, sec('ink', svg(say(200, 130, 680, '집 데려다주고 왔다', '#3a3f4b', '#e9ecef') + '<path d="M420 1180 V1040 L540 950 L660 1040 V1180 Z" fill="none" stroke="#ffd43b" stroke-width="12" stroke-linejoin="round"/>'))),
 (58, 7, sec('wine', calendar(60, 2, .3, 58, hi=(1, 3)) + svg(heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (58, 8, sec('', svg(say(160, 110, 400, '어땠어?', '#3a3f4b', '#e9ecef') + say(300, 240, 540, '…그냥 밥 먹었어', '#3a3f4b', '#868e96') + mug(450, 960, .9)), f'background:{BG}')),
 (58, 10, sec('dark', svg('<circle cx="540" cy="210" r="120" fill="#ffd43b"/><circle cx="590" cy="170" r="110" fill="#14171f"/>' + say(300, 1000, 500, '잘 들어갔어?', '#fee500', '#3a3a3a')))),
 (58, 12, sec('olive', svg(clock(540, 230, 140, 10, 0, '#ced4da')) + spot(540, 1080, 140, '#fff3bf', .45))),
 # ── #59 사진
 (59, 2, sec('', svg(camera(540, 220) + heart(540, 1060, 1.3, '#ff8fab', .9)), f'background:{BG}')),
 (59, 4, sec('dark', svg(thumbs(40, 8) + '<text x="540" y="1130" text-anchor="middle" font-size="160" font-weight="900" fill="#ffd43b" font-family="sans-serif">1장?</text>'))),
 (59, 6, sec('ink', svg('<rect x="300" y="40" width="480" height="340" rx="20" fill="#2b2f3a"/>' + people(540, 120, 1, '#ff8fab') + '<path d="M330 360 L460 260 L560 330 L660 250 L750 360 Z" fill="#495057"/>' + camera(540, 1070, .7, '#868e96')))),
 (59, 7, sec('wine', phone(390, 30, 300, 360, '<div style="position:absolute;left:24px;right:24px;top:40px;bottom:40px;border-radius:16px;background:linear-gradient(150deg,#ffa8a8,#b197fc)"></div>') + svg(say(300, 1000, 520, '이거 잘 나왔다', '#3a3f4b', '#e9ecef')))),
 (59, 8, sec('', svg(say(160, 130, 700, '팔 떨어지는 줄 ㅋㅋ', '#3a3f4b', '#e9ecef') + camera(540, 1070, .8)), f'background:{BG}')),
 (59, 10, sec('dark', svg('<rect x="300" y="40" width="480" height="340" rx="20" fill="#2b2f3a"/>' + people(540, 110, 2, '#adb5bd', 160, hi=1) + heart(540, 1060, 1.3, '#495057')))),
 (59, 12, sec('olive', svg(people(540, 960, 2, '#adb5bd', 200)) + glow(59, 14, ('#ffffff', '#ffd27f'), 0, 380, .45))),
 # ── #60 쓸데없는 연락
 (60, 2, sec('', svg(say(160, 130, 520, 'ㅋㅋㅋ 이거 봐', '#3a3f4b', '#e9ecef')) + post(420, 900, 240, 'linear-gradient(140deg,#ffd43b,#ff8787)', False, -4), f'background:{BG}')),
 (60, 4, sec('dark', post(270, 40, 300, 'linear-gradient(140deg,#74c0fc,#b197fc)', False, -6) + post(560, 80, 260, 'linear-gradient(140deg,#ffa8a8,#ffd43b)', False, 5) + svg(heart(540, 1070, 1.2, '#ff8fab', .9)))),
 (60, 6, sec('morn', spot(860, 160, 150, '#ffd166', .9) + post(410, 920, 260, 'linear-gradient(170deg,#74c0fc,#e7f5ff)', False, -3), '')),
 (60, 7, sec('wine', svg(say(160, 130, 760, '이거 너 좋아하는 거 아냐?', '#3a3f4b', '#e9ecef', 40) + heart(540, 1060, 1.6, '#ff6b81', .9)))),
 (60, 8, sec('', svg(say(160, 130, 720, '걔 생각나서 보냈지', '#3a3f4b', '#e9ecef') + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')), f'background:{BG}')),
 (60, 10, sec('dark', phone(390, 30, 300, 360, '<div style="position:absolute;left:30px;right:30px;top:120px;height:120px;border-radius:16px;border:4px dashed #868e96"></div>') + svg(heart(540, 1060, 1.3, '#343a40')))),
 (60, 12, sec('', bubbles([('him', 360), ('him', 260), ('him', 300)], 70, him='#495057') + svg(heart(540, 1060, 1.6, '#ff8fab', .9)), f'background:{BG}')),
]

if __name__ == '__main__':
    open('gfx57_60.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open('gfx57_60.json', 'w'))
    print('ok', len(G))
