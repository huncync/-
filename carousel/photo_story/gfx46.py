# #46 그래픽 배경 14장 (11/8) — 사진 대신 장 내용에 맞는 그림(스토리 화면 · 카톡 · 그래프 · 달력 …). 글 상자 자리(30~60%)는 비워 둠
# python3 gfx46.py → gfx46.html → node .work/rg46.js → p46g/01~14.png
BASE = '''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#222}
.g{width:1080px;height:1350px;position:relative;overflow:hidden;margin-bottom:10px}
.dark{background:radial-gradient(ellipse at 30% 10%,#2c3350 0,#141726 55%,#0b0c14 100%)}
.wine{background:radial-gradient(ellipse at 70% 0,#4a2433 0,#1d1018 60%,#0d080b 100%)}
.ink{background:linear-gradient(170deg,#1b2a33,#0b1217 80%)}
.olive{background:linear-gradient(165deg,#28301f,#0f120c 80%)}
.dawn{background:linear-gradient(180deg,#232a4a 0,#5a4a6e 45%,#e2a487 85%,#f3c79c 100%)}
.morn{background:linear-gradient(180deg,#8fb6d8 0,#cfe0e8 45%,#f6e7c8 100%)}
.grain:after{content:'';position:absolute;inset:0;opacity:.08;background-image:radial-gradient(#fff 1px,transparent 1px);background-size:4px 4px}
.ring{position:absolute;border-radius:50%;padding:7px;background:conic-gradient(#f9ce34,#ee2a7b,#6228d7,#f9ce34)}
.ring i{display:block;width:100%;height:100%;border-radius:50%;border:6px solid #141726;background:linear-gradient(140deg,#596080,#2b3048)}
.card{position:absolute;border-radius:28px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.bar{position:absolute;height:8px;border-radius:4px}
.bub{position:absolute;border-radius:26px;height:64px}
.dot{position:absolute;border-radius:50%}
.glow{position:absolute;border-radius:50%;filter:blur(30px)}
svg{position:absolute;inset:0}
</style></head><body>'''
S = []
# 1 표지: 스토리 동그라미 줄 + 큰 스토리 카드(웃는 척) 위쪽
S.append('''<section class="g dark grain">
<div style="position:absolute;left:60px;top:70px;display:flex;gap:34px">'''+''.join(f'<div class="ring" style="position:relative;width:150px;height:150px;{"opacity:.45;" if k>2 else ""}"><i></i></div>' for k in range(5))+'''</div>
<div class="card" style="left:300px;top:300px;width:480px;height:330px;background:linear-gradient(135deg,#f7b267,#f25c54 60%,#9b3b6f);transform:rotate(-4deg)">
 <div class="bar" style="left:24px;right:24px;top:20px;background:rgba(255,255,255,.5)"></div><div class="bar" style="left:24px;width:200px;top:20px;background:#fff"></div>
 <div class="dot" style="width:150px;height:150px;left:165px;top:110px;background:rgba(255,255,255,.25)"></div>
 <svg viewBox="0 0 480 330"><path d="M200 210 Q240 250 280 210" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="210" cy="170" r="9" fill="#fff"/><circle cx="270" cy="170" r="9" fill="#fff"/></svg></div>
</section>''')
# 2 스토리 세 장: 친구 · 술 · 운동 (위) + 하트 (아래)
def story(x, y, r, grad, inner):
    return f'<div class="card" style="left:{x}px;top:{y}px;width:270px;height:400px;background:{grad};transform:rotate({r}deg)"><div class="bar" style="left:16px;right:16px;top:14px;background:rgba(255,255,255,.55)"></div>{inner}</div>'
S.append('<section class="g ink grain">'
 + story(70, 40, -7, 'linear-gradient(160deg,#5b7cfa,#2d3a8c)', '<div class="dot" style="width:80px;height:80px;left:50px;top:170px;background:#ffd8a8"></div><div class="dot" style="width:80px;height:80px;left:140px;top:150px;background:#ffc078"></div><div class="dot" style="width:80px;height:80px;left:95px;top:240px;background:#ffe3c2"></div>')
 + story(405, 10, 2, 'linear-gradient(160deg,#ff9f43,#a4372c)', '<svg viewBox="0 0 270 400"><path d="M85 150 h50 l-8 110 h-34z M145 150 h50 l-8 110 h-34z" fill="rgba(255,255,255,.85)"/><rect x="90" y="185" width="40" height="70" fill="#ffd43b"/><rect x="150" y="185" width="40" height="70" fill="#ffd43b"/></svg>')
 + story(735, 50, 8, 'linear-gradient(160deg,#20c997,#0b5d4b)', '<svg viewBox="0 0 270 400"><rect x="40" y="185" width="190" height="22" rx="8" fill="#fff"/><rect x="40" y="150" width="34" height="92" rx="8" fill="#fff"/><rect x="196" y="150" width="34" height="92" rx="8" fill="#fff"/></svg>')
 + '<svg viewBox="0 0 1080 1350"><path d="M540 1120 C 440 1040 380 990 420 930 C 455 880 520 890 540 935 C 560 890 625 880 660 930 C 700 990 640 1040 540 1120Z" fill="#ff6b81" opacity=".85"/></svg>'
 + '<div style="position:absolute;left:470px;top:1150px;color:#fff;font:700 40px sans-serif;opacity:.7">128</div></section>')
# 3 카톡: 내 쪽 말풍선 가득, 그쪽은 짧게
b = ''
ys = [80, 160, 240]
for k, y in enumerate(ys): b += f'<div class="bub" style="right:70px;top:{y}px;width:{[520,380,600][k]}px;background:#fee500"></div>'
b += '<div class="bub" style="left:150px;top:330px;width:120px;background:#3a3f4b"></div><div class="dot" style="left:60px;top:322px;width:72px;height:72px;background:#596080"></div>'
for k, y in enumerate([850, 930, 1010, 1090]): b += f'<div class="bub" style="right:70px;top:{y}px;width:{[460,560,300,420][k]}px;background:#fee500;opacity:{1-k*0.12}"></div>'
b += '<div style="position:absolute;right:540px;top:1110px;color:#fee500;font:700 30px sans-serif">1</div>'
S.append(f'<section class="g" style="background:#0f1115">{b}</section>')
# 4 두 개의 시간선 (순서가 다름)
S.append('''<section class="g olive grain"><svg viewBox="0 0 1080 1350">
<line x1="80" y1="200" x2="1000" y2="200" stroke="#e8e2d0" stroke-width="6" opacity=".6"/><circle cx="220" cy="200" r="34" fill="#ff8787"/><circle cx="560" cy="200" r="18" fill="#e8e2d0"/><circle cx="880" cy="200" r="14" fill="#e8e2d0" opacity=".6"/>
<line x1="80" y1="1060" x2="1000" y2="1060" stroke="#e8e2d0" stroke-width="6" opacity=".6"/><circle cx="220" cy="1060" r="14" fill="#e8e2d0" opacity=".6"/><circle cx="560" cy="1060" r="18" fill="#e8e2d0"/><circle cx="880" cy="1060" r="34" fill="#74c0fc"/>
<text x="80" y="150" fill="#ffa8a8" font-size="40" font-family="sans-serif" font-weight="700">♀</text><text x="80" y="1010" fill="#a5d8ff" font-size="40" font-family="sans-serif" font-weight="700">♂</text></svg></section>''')
# 5 아픔 그래프: 여자는 일찍, 남자는 늦게 (위 · 아래)
S.append('''<section class="g dark grain"><svg viewBox="0 0 1080 1350">
<path d="M80 330 C 200 60, 300 60, 420 250 S 800 320 1000 330" stroke="#ff8787" stroke-width="10" fill="none"/>
<path d="M80 1180 C 400 1180, 600 1170, 760 900 S 950 1150 1000 1170" stroke="#74c0fc" stroke-width="10" fill="none"/>
<line x1="80" y1="340" x2="1000" y2="340" stroke="#fff" opacity=".2" stroke-width="3"/><line x1="80" y1="1190" x2="1000" y2="1190" stroke="#fff" opacity=".2" stroke-width="3"/>
<circle cx="300" cy="120" r="16" fill="#ff8787"/><circle cx="760" cy="905" r="16" fill="#74c0fc"/></svg></section>''')
# 6 달력이 꽉 찬 몇 주
cells = ''
cols = ['#5c7cfa', '#20c997', '#ff922b', '#e64980', '#868e96']
import random
random.seed(6)
for r in range(2):
    for c in range(7):
        cells += f'<div style="position:absolute;left:{70+c*137}px;top:{60+r*150}px;width:125px;height:135px;border-radius:14px;background:#1f2430;padding:12px">' + ''.join(f'<div style="height:22px;margin-top:8px;border-radius:6px;background:{random.choice(cols)}"></div>' for _ in range(random.randint(3, 4))) + '</div>'
for r in range(2):
    for c in range(7):
        cells += f'<div style="position:absolute;left:{70+c*137}px;top:{880+r*150}px;width:125px;height:135px;border-radius:14px;background:#1f2430;padding:12px">' + ''.join(f'<div style="height:22px;margin-top:8px;border-radius:6px;background:{random.choice(cols)}"></div>' for _ in range(random.randint(3, 4))) + '</div>'
S.append(f'<section class="g" style="background:#11141b">{cells}</section>')
# 7 술집 조명 (따뜻한 빛 번짐 + 잔 두 개 실루엣)
gl = ''.join(f'<div class="glow" style="left:{random.randint(0,980)}px;top:{random.randint(0,1250)}px;width:{(s:=random.randint(60,150))}px;height:{s}px;background:{random.choice(["#ffb347","#ff7f50","#ffd27f","#c77dff"])};opacity:.45"></div>' for _ in range(28))
S.append(f'<section class="g wine">{gl}<svg viewBox="0 0 1080 1350"><path d="M380 1020 h120 l-14 220 h-92z M580 1020 h120 l-14 220 h-92z" fill="#0d080b" opacity=".9"/></svg></section>')
# 8 운동 · 일 · 친구: 세 개의 진행 막대 (꽉 참)
row = lambda y, col, ic: f'<div style="position:absolute;left:90px;top:{y}px;width:900px;height:120px;border-radius:24px;background:#1d2228"></div><div style="position:absolute;left:90px;top:{y}px;width:860px;height:120px;border-radius:24px;background:{col}"></div><div style="position:absolute;left:120px;top:{y+30}px;width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,.85)"></div>'
S.append('<section class="g" style="background:#0e1114">' + row(60, '#20c997', '') + row(210, '#5c7cfa', '') + row(950, '#ff922b', '') + '<div style="position:absolute;left:90px;top:1110px;width:900px;height:120px;border-radius:24px;border:4px dashed #495057"></div></section>')
# 9 텅 빈 방 · 창밖 달 (바쁜 게 끝난 밤)
S.append('''<section class="g ink"><div style="position:absolute;left:300px;top:60px;width:480px;height:330px;border:14px solid #2a3640;border-radius:10px;background:linear-gradient(180deg,#0d1b2a,#1b263b)"><div class="dot" style="left:300px;top:60px;width:90px;height:90px;background:#f1f3c4;box-shadow:0 0 60px #f1f3c4"></div><div style="position:absolute;left:226px;top:0;width:14px;height:100%;background:#2a3640"></div></div>
<div style="position:absolute;left:0;right:0;top:1000px;height:350px;background:#0a1015"></div><div style="position:absolute;left:330px;top:960px;width:420px;height:60px;border-radius:12px;background:#1c262e"></div>
<div style="position:absolute;left:470px;top:880px;width:140px;height:90px;border-radius:12px 12px 0 0;background:#151d23;border:4px solid #26323b"></div><div class="dot" style="left:515px;top:905px;width:50px;height:50px;background:#2b3a46"></div></section>''')
# 10 두 선이 엇갈림 (그녀는 내려가고, 그는 늦게 올라감)
S.append('''<section class="g dark grain"><svg viewBox="0 0 1080 1350">
<path d="M80 120 C 400 140 600 260 1000 330" stroke="#ff8787" stroke-width="10" fill="none"/>
<path d="M80 1220 C 500 1210 760 1100 1000 920" stroke="#74c0fc" stroke-width="10" fill="none"/>
<path d="M1000 330 L1000 920" stroke="#fff" stroke-width="3" stroke-dasharray="14 14" opacity=".35"/>
<circle cx="1000" cy="330" r="16" fill="#ff8787"/><circle cx="1000" cy="920" r="16" fill="#74c0fc"/></svg></section>''')
# 11 새벽 (이미 떠난 마음)
S.append('''<section class="g dawn grain"><div class="glow" style="left:600px;top:1050px;width:420px;height:420px;background:#ffe3b3;opacity:.9"></div>
<svg viewBox="0 0 1080 1350"><path d="M0 1180 L180 1120 L300 1160 L460 1090 L640 1150 L820 1100 L1080 1160 L1080 1350 L0 1350Z" fill="#2b2238" opacity=".85"/>
<path d="M720 160 l40 -10 l-20 30z M800 120 l30 -8 l-15 22z" fill="#2b2238" opacity=".7"/></svg></section>''')
# 12 스토리 화면 (진행 막대 + 흐린 화면)
gl = ''.join(f'<div class="glow" style="left:{random.randint(0,980)}px;top:{random.randint(150,1250)}px;width:{(s:=random.randint(60,140))}px;height:{s}px;background:{random.choice(["#ff8fab","#ffd6a5","#a0c4ff","#cdb4db"])};opacity:.35"></div>' for _ in range(20))
bars = ''.join(f'<div class="bar" style="left:{40+k*170}px;width:160px;top:34px;background:{"#fff" if k<3 else "rgba(255,255,255,.35)"}"></div>' for k in range(6))
S.append(f'<section class="g" style="background:linear-gradient(180deg,#2a1b2e,#0e0b12)">{gl}{bars}<div class="ring" style="left:40px;top:66px;width:84px;height:84px"><i></i></div><div style="position:absolute;left:140px;top:92px;width:220px;height:28px;border-radius:14px;background:rgba(255,255,255,.75)"></div><div style="position:absolute;left:40px;right:40px;bottom:120px;height:90px;border-radius:45px;border:3px solid rgba(255,255,255,.5)"></div></section>')
# 13 아침 · 내 하루 (해 + 체크리스트 카드)
S.append('''<section class="g morn"><div class="dot" style="left:760px;top:80px;width:200px;height:200px;background:#ffd166;box-shadow:0 0 90px #ffd166"></div>
<div class="card" style="left:120px;top:860px;width:840px;height:380px;background:#fffdf7;box-shadow:0 20px 50px rgba(0,0,0,.12)">'''+''.join(f'<div style="position:absolute;left:50px;top:{50+k*105}px;width:54px;height:54px;border-radius:12px;border:5px solid #2e5b4e;{"background:#2e5b4e;" if k<2 else ""}"></div><div style="position:absolute;left:130px;top:{66+k*105}px;width:{[520,420,560][k]}px;height:22px;border-radius:11px;background:#d9cfbc"></div>' for k in range(3))+'''</div></section>''')
# 14 휴대폰 속 밝은 스토리 vs 화면 밖 어두운 얼굴 실루엣
S.append('''<section class="g" style="background:linear-gradient(180deg,#14161d,#07080b)">
<div class="card" style="left:560px;top:40px;width:200px;height:340px;border-radius:30px;border:8px solid #2b2f38;background:linear-gradient(160deg,#ffb88c,#de6262)"><div class="bar" style="left:22px;right:22px;top:26px;background:rgba(255,255,255,.6)"></div>
<svg viewBox="0 0 330 620" style="width:100%;height:100%"><circle cx="165" cy="300" r="90" fill="rgba(255,255,255,.25)"/><path d="M120 320 Q165 370 210 320" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="135" cy="270" r="9" fill="#fff"/><circle cx="195" cy="270" r="9" fill="#fff"/></svg></div>
<svg viewBox="0 0 1080 1350"><circle cx="800" cy="1020" r="120" fill="#1c1f27"/><path d="M620 1350 Q620 1160 800 1160 Q980 1160 980 1350Z" fill="#1c1f27"/><path d="M760 1050 Q800 1030 840 1050" stroke="#3a3f4b" stroke-width="8" fill="none" stroke-linecap="round"/></svg></section>''')
open('gfx46.html', 'w', encoding='utf-8').write(BASE + ''.join(S) + '</body></html>')
print(len(S))
