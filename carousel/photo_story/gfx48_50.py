# #48~#50 그래픽 배경 42장 (11/8) — 장 내용에 맞는 그림. 글 상자 자리(30~60%)는 비워 두고 위(0~30%) · 아래(63~92%)에만 그림
# python3 gfx48_50.py → gfx48_50.html → node .work/rg48.js → p48g · p49g · p50g/01~14.png (11/9 번호 밀림: 지금은 p49g · p50g · p51g. 다시 그리면 폴더 이름을 맞춰 주세요)
import random
from gfx46 import BASE

BG = {'dark': 'g dark grain', 'wine': 'g wine', 'ink': 'g ink grain', 'olive': 'g olive grain', 'dawn': 'g dawn grain', 'morn': 'g morn'}
def sec(bg, inner, style=''):
    return f'<section class="{BG.get(bg, "g")}" style="{style}">{inner}</section>'

# ── 모티프 (위 = y 40~400, 아래 = y 860~1240)
def glow(seed, n=24, cols=('#ffb347', '#ff7f50', '#ffd27f', '#c77dff'), y0=0, y1=1250, op=.4):
    random.seed(seed)
    return ''.join(f'<div class="glow" style="left:{random.randint(0,980)}px;top:{random.randint(y0,y1)}px;width:{(s:=random.randint(60,150))}px;height:{s}px;background:{random.choice(cols)};opacity:{op}"></div>' for _ in range(n))
def svg(body): return f'<svg viewBox="0 0 1080 1350">{body}</svg>'
def heart(cx, cy, s=1.0, col='#ff6b81', op=1):
    return f'<path transform="translate({cx},{cy}) scale({s})" d="M0 60 C -50 20 -80 -5 -60 -35 C -42 -60 -10 -55 0 -30 C 10 -55 42 -60 60 -35 C 80 -5 50 20 0 60Z" fill="{col}" opacity="{op}"/>'
def bubbles(rows, y, me='#fee500', him='#3a3f4b', step=80):
    out = ''
    for k, (who, w) in enumerate(rows):
        yy = y + k * step
        if who == 'me': out += f'<div class="bub" style="right:70px;top:{yy}px;width:{w}px;background:{me}"></div>'
        else: out += f'<div class="dot" style="left:60px;top:{yy-6}px;width:70px;height:70px;background:#596080"></div><div class="bub" style="left:150px;top:{yy}px;width:{w}px;background:{him}"></div>'
    return out
def calendar(y, rows=2, fill=.8, seed=1, hi=None, cols=('#5c7cfa', '#20c997', '#ff922b', '#e64980', '#868e96')):
    random.seed(seed); out = ''
    for r in range(rows):
        for c in range(7):
            n = random.randint(2, 4) if random.random() < fill else 0
            border = 'border:4px solid #ffd43b;' if hi == (r, c) else ''
            out += f'<div style="position:absolute;left:{70+c*137}px;top:{y+r*150}px;width:125px;height:135px;border-radius:14px;background:#1f2430;padding:12px;{border}">' + ''.join(f'<div style="height:22px;margin-top:8px;border-radius:6px;background:{random.choice(cols)}"></div>' for _ in range(n)) + '</div>'
    return out
def phone(x, y, w, h, inner, grad='linear-gradient(160deg,#2b3048,#151826)', rot=0):
    return f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:38px;border:9px solid #2b2f38;background:{grad};transform:rotate({rot}deg)">{inner}</div>'
def post(x, y, w, grad, liked=True, rot=0):  # 인스타 게시물 카드: 사진 + 하트
    h = int(w * 1.25)
    return (f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;transform:rotate({rot}deg);border-radius:20px">'
            f'<div style="position:absolute;left:14px;top:14px;width:36px;height:36px;border-radius:50%;background:#dee2e6"></div><div style="position:absolute;left:60px;top:24px;width:{w//3}px;height:14px;border-radius:7px;background:#dee2e6"></div>'
            f'<div style="position:absolute;left:0;right:0;top:64px;height:{w}px;background:{grad}"></div>'
            f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:100%">{heart(34, h-34, .32, "#ff3b5c" if liked else "none")}<path transform="translate(34,{h-34}) scale(.32)" d="M0 60 C -50 20 -80 -5 -60 -35 C -42 -60 -10 -55 0 -30 C 10 -55 42 -60 60 -35 C 80 -5 50 20 0 60Z" fill="none" stroke="#212529" stroke-width="12"/></svg></div>')
def activity(y, n=4, hot=None):  # 활동 기록: 동그라미 + 줄 + 작은 사진 + 하트
    out = ''
    for k in range(n):
        yy = y + k * 96
        out += (f'<div class="dot" style="left:80px;top:{yy}px;width:72px;height:72px;background:#495057"></div>'
                f'<div style="position:absolute;left:176px;top:{yy+16}px;width:{[460,380,520,420,360][k%5]}px;height:18px;border-radius:9px;background:#868e96"></div>'
                f'<div style="position:absolute;left:176px;top:{yy+44}px;width:200px;height:14px;border-radius:7px;background:#495057"></div>'
                f'<div style="position:absolute;right:80px;top:{yy}px;width:72px;height:72px;border-radius:8px;background:{"linear-gradient(140deg,#ffa8a8,#e599f7)" if k==hot else "#343a40"};{"box-shadow:0 0 0 5px #ff3b5c;" if k==hot else ""}"></div>')
    return out
def chain(x, y, n=3, gap=150):  # 같은 하트 반복
    return svg(''.join(heart(x + k * gap, y, .7, '#ff3b5c', 1 - k * .2) for k in range(n)))
def envelope(x, y, s=1, col='#e9ecef'):
    return f'<svg viewBox="0 0 1080 1350"><g transform="translate({x},{y}) scale({s})"><rect width="300" height="200" rx="18" fill="{col}"/><path d="M0 10 L150 120 L300 10" stroke="#adb5bd" stroke-width="10" fill="none"/></g></svg>'
def mug(x, y, s=1, col='#f1e3c8'):
    return f'<g transform="translate({x},{y}) scale({s})"><rect width="180" height="200" rx="26" fill="{col}"/><path d="M180 50 h40 a50 50 0 0 1 0 100 h-40" stroke="{col}" stroke-width="22" fill="none"/><path d="M50 -30 q20 -30 0 -60 M110 -30 q20 -30 0 -60" stroke="{col}" stroke-width="10" fill="none" opacity=".6" stroke-linecap="round"/></g>'
def flower(x, y, s=1, col='#ff8fab'):
    pet = ''.join(f'<ellipse cx="0" cy="-48" rx="30" ry="50" fill="{col}" transform="rotate({a})"/>' for a in range(0, 360, 60))
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M0 40 Q 10 200 -10 340" stroke="#69db7c" stroke-width="12" fill="none"/><path d="M0 200 q60 -40 90 -10 q-50 30 -90 10" fill="#69db7c"/>{pet}<circle r="30" fill="#ffd43b"/></g>'
def clock(x, y, r=120, h=10, m=50, col='#e9ecef'):
    import math
    ha, ma = math.radians(h * 30 + m * .5 - 90), math.radians(m * 6 - 90)
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" stroke-width="10"/><line x1="{x}" y1="{y}" x2="{x+r*.5*math.cos(ha):.0f}" y2="{y+r*.5*math.sin(ha):.0f}" stroke="{col}" stroke-width="12" stroke-linecap="round"/><line x1="{x}" y1="{y}" x2="{x+r*.8*math.cos(ma):.0f}" y2="{y+r*.8*math.sin(ma):.0f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
def quote(x, y, col='#ffd43b', op=.9, s=1):
    return f'<text x="{x}" y="{y}" font-size="{int(260*s)}" font-family="serif" font-weight="900" fill="{col}" opacity="{op}">“</text>'
def checklist(x, y, w, n, done, light=True):
    bg = '#fffdf7' if light else '#1f2430'; line = '#d9cfbc' if light else '#495057'; tick = '#2e5b4e' if light else '#20c997'
    return (f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;height:{60+n*100}px;background:{bg}">' + ''.join(
        f'<div style="position:absolute;left:44px;top:{40+k*100}px;width:52px;height:52px;border-radius:12px;border:5px solid {tick};{"background:"+tick+";" if k<done else ""}"></div><div style="position:absolute;left:124px;top:{56+k*100}px;width:{w-220}px;height:20px;border-radius:10px;background:{line}"></div>' for k in range(n)) + '</div>')
def two_circles(y, a='#74c0fc', b='#ff8787', gap=0):
    return svg(f'<circle cx="{460-gap}" cy="{y}" r="150" fill="{a}" opacity=".85"/><circle cx="{620+gap}" cy="{y}" r="150" fill="{b}" opacity=".85" style="mix-blend-mode:screen"/>')
def spot(x, y, r=180, col='#fff3bf', op=.5):
    return f'<div class="glow" style="left:{x-r}px;top:{y-r}px;width:{2*r}px;height:{2*r}px;background:{col};opacity:{op}"></div>'

S = {}
# ── #48 편한 사람 (따뜻한 실내 → 반전은 밝게)
S['48'] = [
 sec('wine', glow(1, 14, ('#ffb347', '#ffd27f'), 0, 500, .35) + svg(mug(330, 210, 1.1) + mug(600, 230, .95, '#d9c7a6')) + '<div style="position:absolute;left:220px;top:470px;width:640px;height:90px;border-radius:40px;background:#3b2129"></div>'),
 sec('ink', svg(f'<path d="M80 280 L1000 280" stroke="#ced4da" stroke-width="6" opacity=".5"/><path d="M80 1100 L1000 1100" stroke="#ced4da" stroke-width="6" opacity=".5"/>') + '<div style="position:absolute;left:80px;top:250px;font:900 52px sans-serif;color:#ff8787">♥</div><div style="position:absolute;left:80px;top:1070px;font:900 52px sans-serif;color:#adb5bd">—</div>'),
 sec('', calendar(60, 2, .9, 3) + calendar(880, 2, .9, 4), 'background:#11141b'),
 sec('', bubbles([('me', 520), ('me', 380), ('me', 600)], 80) + bubbles([('me', 300), ('him', 120), ('me', 460)], 900) + '<div style="position:absolute;right:70px;top:1150px;color:#fee500;font:700 30px sans-serif">00:01</div>', 'background:#0f1115'),
 sec('olive', checklist(120, 50, 840, 3, 3, False) + svg(mug(440, 980, .9))),
 sec('dark', svg(f'<circle cx="540" cy="200" r="130" fill="#ffd43b"/><path d="M480 230 Q540 280 600 230" stroke="#2b2b2b" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="495" cy="180" r="12" fill="#2b2b2b"/><circle cx="585" cy="180" r="12" fill="#2b2b2b"/>'
      f'<circle cx="540" cy="1060" r="110" fill="#495057"/><path d="M490 1100 Q540 1060 590 1100" stroke="#212529" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="505" cy="1040" r="10" fill="#212529"/><circle cx="575" cy="1040" r="10" fill="#212529"/>')),
 sec('', bubbles([('him', 560), ('him', 420), ('him', 600)], 80, him='#495057') + bubbles([('me', 120)], 1000), 'background:#0f1115'),
 sec('ink', glow(8, 10, ('#74c0fc', '#a5d8ff'), 900, 1250, .3) + svg(quote(80, 330, '#ffd43b'))),
 sec('morn', spot(860, 160, 160, '#ffd166', .9) + svg(f'<path d="M100 1000 L500 1000 L500 1200 L100 1200Z" fill="#2e5b4e" opacity=".15"/><path d="M580 980 L980 980" stroke="#2e5b4e" stroke-width="10" stroke-linecap="round"/><path d="M780 900 L980 980 L780 1060" stroke="#2e5b4e" stroke-width="10" fill="none" stroke-linecap="round"/>'), ''),
 sec('dark', svg(f'<path d="M300 300 q240 -260 480 0" stroke="#e9ecef" stroke-width="10" fill="none"/><circle cx="540" cy="230" r="60" fill="#ffd43b"/>' + clock(540, 1050, 130, 9, 0, '#868e96'))),
 sec('morn', spot(200, 160, 140, '#ffd166', .9) + calendar(880, 2, .45, 11, hi=(0, 2), cols=('#2e5b4e', '#e8590c', '#1971c2')), ''),
 sec('', bubbles([('me', 360)], 960) + bubbles([('him', 260)], 1060) + svg(quote(80, 330, '#fee500', .8)), 'background:#0f1115'),
 sec('dawn', two_circles(200, '#74c0fc', '#ffa8a8', 70) + svg(f'<circle cx="540" cy="1080" r="120" fill="none" stroke="#fff" stroke-width="10" opacity=".7"/><path d="M540 960 v240 M420 1080 h240" stroke="#fff" stroke-width="8" opacity=".5"/>')),
 sec('dark', glow(14, 18, ('#ffd27f', '#ff8fab', '#a5d8ff'), 0, 380, .35) + svg(heart(540, 1050, 1.8, '#ff6b81', .9))),
]
# ── #49 하트 하나 (인스타 화면 · 밤)
S['49'] = [
 sec('dark', post(250, 50, 360, 'linear-gradient(140deg,#ffa8a8,#e599f7)', True, -5) + post(560, 120, 280, 'linear-gradient(140deg,#74c0fc,#b197fc)', False, 6)),
 sec('', activity(60, 3, hot=1) + activity(900, 3), 'background:#111318'),
 sec('ink', phone(400, 40, 280, 360, svg('') + '<div style="position:absolute;left:30px;right:30px;top:40px;height:180px;border-radius:14px;background:linear-gradient(140deg,#495057,#343a40)"></div>') + svg('<path d="M600 300 q30 20 60 0" stroke="#fff" stroke-width="0"/>' + heart(640, 1050, 1.3, '#ff3b5c', .9))),
 sec('dark', svg('<path d="M540 80 v260" stroke="#e9ecef" stroke-width="40" stroke-linecap="round" opacity=".85"/><path d="M500 60 l40 -40 l40 40" stroke="#e9ecef" stroke-width="16" fill="none" opacity=".85"/>') + glow(4, 10, ('#ffa8a8', '#74c0fc'), 900, 1250, .3)),
 sec('wine', svg(heart(540, 220, 1.6, '#ff3b5c', .9) + '<circle cx="540" cy="1060" r="140" fill="none" stroke="#ffd43b" stroke-width="12"/><text x="540" y="1110" text-anchor="middle" font-size="160" font-weight="900" fill="#ffd43b" font-family="sans-serif">!</text>')),
 sec('dark', chain(310, 210) + svg(f'<circle cx="540" cy="1060" r="90" fill="#adb5bd"/><path d="M400 1260 Q400 1140 540 1140 Q680 1140 680 1260Z" fill="#adb5bd"/>') ),
 sec('', '<div style="position:absolute;left:0;right:0;top:0;height:400px;background:repeating-linear-gradient(180deg,#212529 0 120px,#111318 120px 130px)"></div>' + activity(900, 3, hot=2) + svg('<path d="M980 60 v300" stroke="#ff3b5c" stroke-width="10" stroke-linecap="round"/><path d="M955 330 l25 30 l25 -30" stroke="#ff3b5c" stroke-width="10" fill="none"/>'), 'background:#111318'),
 sec('ink', svg(heart(300, 220, 1.1, '#ff3b5c')) + envelope(560, 120, 1) + svg('<path d="M420 220 h110" stroke="#fff" stroke-width="8" stroke-dasharray="14 14" opacity=".6"/>')),
 sec('', bubbles([('him', 480), ('him', 300)], 900, him='#495057') + svg(quote(80, 330, '#fee500', .8)), 'background:#0f1115'),
 sec('dark', phone(380, 40, 320, 360, '<div style="position:absolute;left:50px;right:50px;top:60px;height:200px;border:6px dashed #ff6b6b;border-radius:10px"></div>') + svg('<circle cx="540" cy="1060" r="150" fill="none" stroke="#ff6b6b" stroke-width="10"/><circle cx="540" cy="1060" r="40" fill="#ff6b6b"/>')),
 sec('', bubbles([('me', 560)], 980) + svg(heart(540, 220, 1.2, '#ffa8a8', .9)), 'background:#0f1115'),
 sec('dawn', svg(heart(470, 220, 1.0, '#ffa8a8') + heart(610, 220, 1.0, '#a5d8ff')) + checklist(240, 900, 600, 2, 2)),
 sec('wine', svg('<text x="540" y="320" text-anchor="middle" font-size="260" font-weight="900" fill="#ff6b6b" opacity=".9" font-family="sans-serif">?</text>' + heart(540, 1050, .8, '#495057'))),
 sec('dark', glow(49, 20, ('#ff8fab', '#ffd6a5', '#a0c4ff'), 0, 380, .35) + svg(heart(540, 1050, 1.8, '#ff6b81', .9))),
]
# ── #50 진짜 사과 (꽃 · 편지 · 따뜻한 새벽)
S['50'] = [
 sec('dawn', svg(flower(540, 230, 1.1, '#ff8fab'))),
 sec('ink', svg('<text x="540" y="330" text-anchor="middle" font-size="200" font-weight="900" fill="#868e96" opacity=".6" font-family="sans-serif">…</text>' + clock(540, 1060, 120, 11, 55, '#868e96'))),
 sec('dark', envelope(390, 100, 1, '#f1e3c8') + svg(flower(540, 980, .8, '#ffa8a8'))),
 sec('', bubbles([('him', 620)], 120, him='#495057') + bubbles([('me', 140)], 1020), 'background:#0f1115'),
 sec('olive', checklist(120, 50, 840, 3, 1, False) + svg('<circle cx="540" cy="1060" r="130" fill="none" stroke="#ffd43b" stroke-width="10"/><circle cx="540" cy="1060" r="40" fill="#ffd43b"/>')),
 sec('dark', svg('<text x="540" y="320" text-anchor="middle" font-size="200" font-weight="900" fill="#ff6b6b" opacity=".85" font-family="sans-serif">근데</text><line x1="300" y1="250" x2="780" y2="250" stroke="#fff" stroke-width="18"/>' + heart(540, 1060, 1.2, '#ffa8a8', .8))),
 sec('morn', calendar(880, 2, .4, 7, hi=(0, 3), cols=('#2e5b4e', '#1971c2')) + spot(860, 170, 140, '#ffd166', .9), ''),
 sec('ink', svg(quote(80, 330, '#ffd43b')) + glow(50, 10, ('#ffd27f',), 900, 1250, .35)),
 sec('dawn', svg('<path d="M200 1150 L380 1150 L380 1050 L560 1050 L560 950 L740 950 L740 850 L920 850" stroke="#fff" stroke-width="12" fill="none" opacity=".8"/>' + flower(540, 220, .8, '#ffc9c9'))),
 sec('wine', svg('<path d="M540 90 L660 310 L420 310Z" fill="none" stroke="#ffd43b" stroke-width="14" stroke-linejoin="round"/><text x="540" y="290" text-anchor="middle" font-size="120" font-weight="900" fill="#ffd43b" font-family="sans-serif">!</text>')),
 sec('', bubbles([('him', 360)], 120, him='#495057') + svg('<path d="M380 1060 h320" stroke="#868e96" stroke-width="14" stroke-linecap="round"/><circle cx="380" cy="1060" r="22" fill="#868e96"/>'), 'background:#0f1115'),
 sec('morn', svg(flower(540, 980, 1.0, '#ff8fab')) + spot(540, 160, 160, '#ffe3b3', .9), ''),
 sec('dark', svg('<path d="M380 330 L540 120 L700 330Z" fill="#495057"/><path d="M540 120 v-60" stroke="#ffd43b" stroke-width="10"/><path d="M540 60 l60 20 l-60 20z" fill="#ffd43b"/>' + '<path d="M380 1180 L700 1180" stroke="#495057" stroke-width="40" stroke-linecap="round"/><path d="M440 1120 L620 1120" stroke="#868e96" stroke-width="30" stroke-linecap="round"/>')),
 sec('dawn', svg(flower(300, 230, .8, '#ffc9c9') + flower(540, 200, 1.0, '#ff8fab') + flower(780, 230, .8, '#ffd8a8'))),
]

if __name__ == '__main__':
    out = BASE
    for k in ('48', '49', '50'):
        assert len(S[k]) == 14, (k, len(S[k]))
        out += ''.join(s.replace('<section class="', f'<section data-k="{k}" class="', 1) for s in S[k])
    open('gfx48_50.html', 'w', encoding='utf-8').write(out + '</body></html>')
    print('ok')
