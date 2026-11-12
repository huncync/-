# #56 그래픽 배경 (2 · 4 · 6 · 8 · 10 · 12장) — 글 상자 자리(30~60%)는 비우고 위 · 아래에만 그림
# python3 gfx56.py → node render56.js gfx → p56g/NN.png
from gfx48_50 import BASE, sec, svg, glow, calendar, heart, phone
from gfx52_55 import people
from gfx48 import say

BG = '#0f1115'
def ring(cx, cy, r, col):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="18"/>'
G = [
 (2, sec('', svg(people(540, 110, 3, '#495057') + '<text x="540" y="1150" text-anchor="middle" font-size="220" font-weight="900" fill="#ffd43b" opacity=".9" font-family="sans-serif">?</text>'), f'background:{BG}')),
 (4, sec('dark', svg(people(330, 110, 1, '#adb5bd') + people(750, 110, 1, '#ff8fab') + '<path d="M410 200 Q540 120 670 200" stroke="#ffd43b" stroke-width="8" fill="none" stroke-dasharray="16 12"/>' + people(540, 960, 1, '#ffd43b')))),
 (6, sec('ink', calendar(60, 2, .25, 56, hi=(0, 2)) + svg(heart(540, 1060, 1.3, '#ff8fab', .9)))),
 (8, sec('wine', svg(ring(470, 230, 110, '#ffd43b') + ring(610, 230, 110, '#e9ecef') + '<path d="M380 1080 h320" stroke="#495057" stroke-width="18" stroke-linecap="round"/>') + glow(56, 12, ('#ffd27f', '#ffffff'), 900, 1250, .3))),
 (10, sec('dark', phone(400, 50, 280, 360, '<div style="position:absolute;left:30px;right:30px;top:40px;height:200px;border-radius:16px;background:linear-gradient(140deg,#ffa8a8,#b197fc);transform:rotate(-8deg)"></div>') + svg('<circle cx="430" cy="1060" r="70" fill="none" stroke="#ff6b6b" stroke-width="12"/><path d="M400 1030 L460 1090 M460 1030 L400 1090" stroke="#ff6b6b" stroke-width="12"/><circle cx="650" cy="1060" r="70" fill="none" stroke="#868e96" stroke-width="12"/>' + heart(650, 1055, .55, '#868e96')))),
 (12, sec('', svg('<circle cx="540" cy="210" r="130" fill="#ffd43b"/><path d="M480 240 Q540 290 600 240" stroke="#2b2b2b" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="495" cy="190" r="12" fill="#2b2b2b"/><circle cx="585" cy="190" r="12" fill="#2b2b2b"/>' + people(540, 970, 1, '#adb5bd')) + glow(57, 12, ('#ffd27f', '#ff8fab'), 900, 1250, .3), f'background:{BG}')),
]

if __name__ == '__main__':
    open('gfx56.html', 'w', encoding='utf-8').write(BASE + ''.join(g for _, g in G) + '</body></html>')
    print('ok', [n for n, _ in G])
