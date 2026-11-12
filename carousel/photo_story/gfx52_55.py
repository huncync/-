# #52 ~ #55 그래픽 배경 (장 2 · 4 · 6 · 7 · 8 · 10 · 12) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx52_55.py → gfx52_55.html + gfx52_55.json → node render52.js gfx → p52g ~ p55g/NN.png
import json
from gfx48_50 import BASE, sec, svg, glow, bubbles, calendar, heart, clock, mug, two_circles, spot, quote, phone, envelope
from gfx48 import say

def battery(x, y, lv=1, col='#ff6b6b'):
    bars = ''.join(f'<rect x="{x+22+k*92}" y="{y+22}" width="78" height="136" rx="10" fill="{col if k < lv else "#2b2f3a"}"/>' for k in range(4))
    return f'<rect x="{x}" y="{y}" width="400" height="180" rx="28" fill="none" stroke="#ced4da" stroke-width="10"/><rect x="{x+404}" y="{y+56}" width="26" height="68" rx="8" fill="#ced4da"/>' + bars
def people(cx, y, n=3, col='#adb5bd', gap=170, hi=None):  # 사람 아이콘 줄 (hi = 비운 자리)
    out = ''
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * gap
        if hi == k:
            out += f'<circle cx="{x}" cy="{y}" r="50" fill="none" stroke="#ffd43b" stroke-width="6" stroke-dasharray="14 10"/><path d="M{x-80} {y+190} Q{x-80} {y+80} {x} {y+80} Q{x+80} {y+80} {x+80} {y+190}" fill="none" stroke="#ffd43b" stroke-width="6" stroke-dasharray="14 10"/>'
        else:
            out += f'<circle cx="{x}" cy="{y}" r="50" fill="{col}"/><path d="M{x-80} {y+190} Q{x-80} {y+80} {x} {y+80} Q{x+80} {y+80} {x+80} {y+190}Z" fill="{col}"/>'
    return out
def dayline(y, days, hi, col='#ffd43b'):  # 1 · 3 · 5 · 7일 점
    out = f'<path d="M140 {y} H940" stroke="#495057" stroke-width="8"/>'
    for k, d in enumerate(days):
        x = 140 + k * (800 / (len(days) - 1))
        on = d == hi
        out += f'<circle cx="{x}" cy="{y}" r="{38 if on else 24}" fill="{col if on else "#495057"}"/><text x="{x}" y="{y+100}" text-anchor="middle" font-size="44" font-weight="800" fill="{col if on else "#868e96"}" font-family="Noto Sans KR,sans-serif">{d}일</text>'
    return out

BG = '#0f1115'
G = [
 # ── #52 권태기
 (52, 2, sec('', svg(say(160, 130, 520, '헤어지자', '#3a3f4b', '#868e96') + '<path d="M170 178 H660" stroke="#ff6b6b" stroke-width="10"/>' + heart(540, 1050, 1.4, '#495057')), f'background:{BG}')),
 (52, 4, sec('dark', bubbles([('him', 360)], 120, him='#495057') + calendar(900, 2, .3, 52))),
 (52, 6, sec('ink', svg(mug(330, 150, 1) + mug(600, 170, .9, '#d9c7a6') + '<rect x="300" y="1000" width="480" height="40" rx="20" fill="#343a40"/>'))),
 (52, 7, sec('dark', bubbles([('me', 520), ('him', 160)], 70) + svg('<text x="540" y="1130" text-anchor="middle" font-size="220" font-weight="900" fill="#495057" font-family="sans-serif">?</text>'))),
 (52, 8, sec('wine', calendar(60, 2, .9, 53, cols=('#5c5f66', '#495057')) + svg('<text x="540" y="1120" text-anchor="middle" font-size="120" font-weight="900" fill="#868e96" font-family="Noto Sans KR,sans-serif">다음에</text>'))),
 (52, 10, sec('dark', svg(heart(540, 230, 1.6, '#ff6b81', .9) + '<path d="M500 140 L560 230 L510 300" stroke="#0f1115" stroke-width="18" fill="none"/>' + battery(325, 980, 1)))),
 (52, 12, sec('', svg(say(220, 120, 760, '이번 주는 내가 정할게', '#fee500', '#3a3a3a', 42)) + glow(52, 14, ('#ffd27f', '#ff8fab'), 900, 1250, .35), f'background:{BG}')),
 # ── #53 너 요즘 변했어
 (53, 2, sec('', svg('<text x="540" y="330" text-anchor="middle" font-size="240" font-weight="900" fill="#ff8787" opacity=".85" font-family="sans-serif">?</text>' + say(300, 1000, 480, '너 요즘 변했어', '#3a3f4b', '#e9ecef')), f'background:{BG}')),
 (53, 4, sec('dark', bubbles([('me', 420), ('me', 300), ('me', 360)], 60) + svg(clock(540, 1060, 130, 1, 30, '#868e96')))),
 (53, 6, sec('wine', svg('<rect x="390" y="80" width="300" height="320" rx="20" fill="#2b2f3a"/><circle cx="640" cy="240" r="16" fill="#ffd43b"/><path d="M320 1060 H760" stroke="#495057" stroke-width="24" stroke-linecap="round"/>'))),
 (53, 7, sec('dark', svg('<text x="540" y="320" text-anchor="middle" font-size="200" font-weight="900" fill="#ff6b6b" opacity=".85" font-family="sans-serif">!</text>' + heart(540, 1060, 1.2, '#495057')))),
 (53, 8, sec('ink', svg(clock(540, 230, 140, 11, 55, '#ced4da')) + calendar(940, 2, .95, 54, cols=('#5c7cfa', '#868e96')))),
 (53, 10, sec('dark', svg('<circle cx="540" cy="230" r="150" fill="none" stroke="#ffd43b" stroke-width="12"/><circle cx="540" cy="230" r="40" fill="#ffd43b"/>' + heart(540, 1060, 1.4, '#ff8fab', .9)))),
 (53, 12, sec('olive', svg('<rect x="300" y="80" width="480" height="300" rx="24" fill="#2b2f3a"/>' + ''.join(f'<rect x="340" y="{120+k*80}" width="40" height="40" rx="8" fill="{"#20c997" if k == 0 else "#495057"}"/><rect x="400" y="{130+k*80}" width="320" height="20" rx="10" fill="#495057"/>' for k in range(3)) + mug(450, 960, .9)))),
 # ── #54 친구들이 먼저 알아요
 (54, 2, sec('dark', svg(people(540, 120, 3) + heart(540, 1060, 1.4, '#495057')))),
 (54, 4, sec('', svg(people(540, 110, 3, '#868e96') + say(320, 980, 440, '내 여자친구?', '#3a3f4b', '#868e96')), f'background:{BG}')),
 (54, 6, sec('ink', phone(400, 60, 280, 340, '<div style="position:absolute;left:0;right:0;top:120px;text-align:center;font:900 42px sans-serif;color:#ff6b6b">부재중 3</div>') + svg(people(540, 1000, 3, '#495057')))),
 (54, 7, sec('dark', svg(people(540, 110, 4, '#adb5bd', 170, hi=3) + '<circle cx="540" cy="1060" r="120" fill="none" stroke="#ff6b6b" stroke-width="12"/><path d="M455 975 L625 1145" stroke="#ff6b6b" stroke-width="12"/>'))),
 (54, 8, sec('wine', svg(say(160, 130, 600, '요즘 좀 그래…', '#3a3f4b', '#e9ecef') + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')))),
 (54, 10, sec('dark', svg('<path d="M540 90 L660 310 L420 310Z" fill="none" stroke="#ffd43b" stroke-width="14" stroke-linejoin="round"/><text x="540" y="290" text-anchor="middle" font-size="120" font-weight="900" fill="#ffd43b" font-family="sans-serif">!</text>' + clock(540, 1060, 120, 9, 15, '#868e96')))),
 (54, 12, sec('olive', svg(people(540, 960, 3, '#adb5bd')) + glow(54, 14, ('#ffd27f', '#a5d8ff'), 0, 380, .35))),
 # ── #55 헤어지고 일주일
 (55, 2, sec('', svg(dayline(240, [1, 3, 5, 7], 7) + heart(540, 1060, 1.4, '#495057')), f'background:{BG}')),
 (55, 4, sec('ink', phone(400, 50, 280, 360, '<div style="position:absolute;left:30px;right:30px;top:150px;height:40px;border-radius:20px;background:#3a3f4b"></div>') + svg(clock(540, 1060, 120, 2, 10, '#868e96')))),
 (55, 6, sec('dark', svg(dayline(220, [1, 3, 5, 7], 3) + '<rect x="380" y="960" width="320" height="200" rx="20" fill="none" stroke="#495057" stroke-width="8" stroke-dasharray="20 14"/>'))),
 (55, 7, sec('wine', svg(dayline(220, [1, 3, 5, 7], 5) + mug(330, 960, .9) + mug(620, 980, .8, '#d9c7a6')))),
 (55, 8, sec('dark', svg(say(300, 130, 480, '오히려 편해', '#3a3f4b', '#e9ecef') + say(260, 260, 560, '괜찮아. 진짜로', '#3a3f4b', '#e9ecef')) + glow(55, 10, ('#a5d8ff',), 900, 1250, .25))),
 (55, 10, sec('ink', phone(400, 60, 280, 340, '<div style="position:absolute;left:30px;right:30px;bottom:40px;height:44px;border-radius:22px;border:3px dashed #868e96"></div>') + svg('<path d="M380 1080 h320" stroke="#495057" stroke-width="18" stroke-linecap="round"/>'))),
 (55, 12, sec('morn', spot(860, 160, 150, '#ffd166', .9) + svg(heart(540, 1060, 1.4, '#ff8fab', .85)), '')),
]

if __name__ == '__main__':
    open('gfx52_55.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open('gfx52_55.json', 'w'))
    print('ok', len(G))
