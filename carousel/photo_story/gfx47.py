# #47 그래픽 배경 14장 (11/9) — 「남자의 말이 줄어들 때, 머릿속에서 일어나는 일」 · gfx48_50.py 모티프 재사용
# python3 gfx47.py → gfx47.html → node .work/rg47.js → p47g/01~14.png
from gfx48_50 import BASE, sec, svg, glow, bubbles, calendar, heart, quote, two_circles, mug, spot, clock

S = [
 sec('', bubbles([('him', 620), ('him', 420), ('him', 220), ('him', 90)], 70, him='#495057', step=86), 'background:#0f1115'),
 sec('', bubbles([('me', 520), ('him', 70), ('me', 400)], 70) + bubbles([('me', 460), ('him', 90), ('him', 70)], 900), 'background:#0f1115'),
 sec('wine', svg('<text x="540" y="330" text-anchor="middle" font-size="260" font-weight="900" fill="#74c0fc" opacity=".85" font-family="sans-serif">?</text>' + clock(540, 1060, 120, 1, 10, '#868e96'))),
 sec('dark', svg(''.join(f'<circle cx="{240 + k*200}" cy="220" r="46" fill="{c}"/>' for k, c in enumerate(['#5c7cfa', '#20c997', '#ff922b', '#868e96']))) + glow(47, 8, ('#a5d8ff',), 900, 1250, .25)),
 sec('', calendar(60, 2, .95, 5) + svg('<circle cx="540" cy="1060" r="120" fill="none" stroke="#ffd43b" stroke-width="10"/><text x="540" y="1100" text-anchor="middle" font-size="110" font-weight="900" fill="#ffd43b" font-family="sans-serif">₩</text>'), 'background:#11141b'),
 sec('ink', svg('<path d="M200 220 C 300 60, 420 380, 520 200 S 700 60, 760 260 S 900 360, 880 140" stroke="#ced4da" stroke-width="10" fill="none" stroke-linecap="round"/>'
               '<path d="M220 1080 C 340 960, 460 1200, 560 1060 S 760 940, 860 1100" stroke="#868e96" stroke-width="8" fill="none" stroke-linecap="round" opacity=".7"/>')),
 sec('wine', svg('<path d="M560 60 L440 250 L540 250 L480 400 L660 190 L560 190 L620 60Z" fill="#ffd43b" opacity=".9"/>' + '<path d="M380 1080 h320" stroke="#495057" stroke-width="18" stroke-linecap="round"/>')),
 sec('ink', svg(quote(80, 330, '#ffd43b')) + glow(470, 10, ('#ffd27f',), 900, 1250, .3)),
 sec('dark', two_circles(200, '#74c0fc', '#ff8787', 160) + svg('<path d="M380 1080 h320" stroke="#495057" stroke-width="8" stroke-dasharray="20 18"/>')),
 sec('dark', svg('<path d="M80 300 C 300 300 600 250 1000 120" stroke="#74c0fc" stroke-width="10" fill="none"/><path d="M80 1100 C 400 1100 700 1150 1000 1220" stroke="#ff8787" stroke-width="10" fill="none"/>')),
 sec('olive', bubbles([('him', 300)], 120, him='#495057') + svg(mug(450, 960, .9))),
 sec('', '<div style="position:absolute;left:60px;right:60px;top:60px;height:330px;border-radius:30px;border:4px dashed #343a40"></div><div style="position:absolute;left:60px;right:60px;top:900px;height:330px;border-radius:30px;border:4px dashed #343a40"></div>', 'background:#0f1115'),
 sec('morn', spot(860, 160, 150, '#ffd166', .9) + svg('<rect x="400" y="860" width="280" height="400" rx="16" fill="#2e5b4e" opacity=".85"/><rect x="420" y="880" width="180" height="360" fill="#fffdf7" transform="skewY(-8) translate(0,60)"/><circle cx="440" cy="1060" r="10" fill="#2e5b4e"/>'), ''),
 sec('dark', glow(1447, 18, ('#ffd27f', '#a5d8ff', '#ff8fab'), 0, 380, .35) + svg(heart(540, 1050, 1.8, '#ff6b81', .9))),
]

if __name__ == '__main__':
    assert len(S) == 14
    open('gfx47.html', 'w', encoding='utf-8').write(BASE + ''.join(S) + '</body></html>')
    print('ok')
