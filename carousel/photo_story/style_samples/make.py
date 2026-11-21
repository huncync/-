# 그래픽 새 스타일 시안 3종 (11/21) — #67 4장 · 7장에 적용해 비교
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gfx46 import BASE
FONT = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700;800&family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@400;700;900&display=block'>"
CSS = '''<style>
.s{width:1080px;height:1350px;position:relative;overflow:hidden;margin-bottom:10px}
/* A 노트 */
.note{background:#f3ede2;background-image:repeating-linear-gradient(transparent 0 58px,#e3d8c6 58px 60px);}
.note:before{content:'';position:absolute;left:120px;top:0;bottom:0;width:3px;background:#e7a9a0}
.note .q{position:absolute;left:170px;right:80px;top:110px;font-family:'Nanum Pen Script';font-size:96px;line-height:1.15;color:#2b2622}
.note .u{position:absolute;left:170px;top:300px;width:560px;height:14px;background:#ffcb3d;opacity:.7;border-radius:7px;transform:rotate(-1deg)}
.note .ft{position:absolute;left:170px;bottom:120px;font-family:'Nanum Pen Script';font-size:52px;color:#8a7d6b}
.note .pin{position:absolute;right:120px;bottom:110px;width:130px;height:130px;border-radius:50%;border:5px solid #c0392b;color:#c0392b;font:900 30px 'Noto Sans KR';display:grid;place-items:center;transform:rotate(-12deg);opacity:.75}
/* B 카톡 화면 */
.kt{background:#b2c7d9}
.kt .hd{position:absolute;left:0;right:0;top:0;height:120px;background:#a9bfd1;display:flex;align-items:center;padding:0 40px;font:700 40px 'Noto Sans KR';color:#1d2630}
.kt .hd i{font-style:normal;margin-right:24px;font-size:44px}
.kt .b{position:absolute;max-width:640px;padding:16px 26px;border-radius:26px;font:500 34px/1.3 'Noto Sans KR';color:#191919}
.kt .him{left:150px;background:#fff;border-top-left-radius:6px}
.kt .av{position:absolute;left:40px;width:80px;height:80px;border-radius:30px;background:#d7dde3}
.kt .me{right:40px;background:#fee500;border-top-right-radius:6px}
.kt .t{position:absolute;font:400 24px 'Noto Sans KR';color:#556270}
.kt .in{position:absolute;left:0;right:0;bottom:0;height:130px;background:#fff;display:flex;align-items:center;padding:0 40px;gap:20px}
.kt .in span{flex:1;height:70px;border-radius:35px;background:#f2f3f5}
.kt .in b{width:70px;height:70px;border-radius:50%;background:#fee500}
/* C 필름 무드 */
.film{background:radial-gradient(ellipse at 50% 35%,#2a2420 0%,#0d0b0a 70%)}
.film:after{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='200' height='200' filter='url(%23n)' opacity='.18'/></svg>");mix-blend-mode:overlay}
.film .big{position:absolute;left:0;right:0;top:40px;text-align:center;font:800 330px/1 'Nanum Myeongjo';color:transparent;-webkit-text-stroke:3px #c9a86a;opacity:.9}
.film .q2{position:absolute;left:90px;right:90px;bottom:170px;text-align:center;font:700 54px/1.4 'Nanum Myeongjo';color:#e9dcc4}
.film .ln{position:absolute;left:440px;right:440px;bottom:130px;height:2px;background:#c9a86a}
.film .cap{position:absolute;left:0;right:0;bottom:80px;text-align:center;font:400 24px 'Noto Sans KR';letter-spacing:.3em;color:#8d7d64}
</style>'''
def note(q, ft, pin=''):
    return f'<section class="s note"><div class="q">{q}</div><div class="u"></div><div class="ft">{ft}</div>' + (f'<div class="pin">{pin}</div>' if pin else '') + '</section>'
def kt(name, msgs):
    out = f'<section class="s kt"><div class="hd"><i>‹</i>{name}</div>'
    y = 150
    for who, t, tm in msgs:
        if who == 'him': out += f'<div class="av" style="top:{y}px"></div><div class="b him" style="top:{y}px">{t}</div><div class="t" style="left:160px;top:{y+78}px">{tm}</div>'
        else: out += f'<div class="b me" style="top:{y}px">{t}</div><div class="t" style="right:44px;top:{y+78}px">{tm}</div>'
        y += 112
    return out + '</section>'
def film(big, q, cap):
    return f'<section class="s film"><div class="big">{big}</div><div class="q2">{q}</div><div class="ln"></div><div class="cap">{cap}</div></section>'
S = [
 ('A4', note('"갖고 싶은 거 있어?<br>그냥 말해."', '고르는 수고를 하기 싫은 거예요', '두 번째')),
 ('A7', note('"기념일 챙기기 귀찮아졌으면,<br>끝난 거지."', '남자들끼리 하는 말 · 노트', '진짜')),
 ('B4', kt('그 사람', [('him', '갖고 싶은 거 있어?', '오후 9:41'), ('him', '그냥 말해', '오후 9:41'), ('me', '…', '오후 9:52')])),
 ('B7', kt('남자들 단톡 (4)', [('him', '기념일 챙기기 귀찮아졌으면', '오후 11:20'), ('him', '끝난 거지', '오후 11:20'), ('him', 'ㅇㅇ 그렇지', '오후 11:21')])),
 ('C4', film('02', '"갖고 싶은 거 있어? 그냥 말해."', 'THE SECOND SIGN')),
 ('C7', film('“ ”', '기념일 챙기기 귀찮아졌으면,<br>끝난 거지.', 'MEN TALK')),
]
html = BASE.replace('<head>', '<head>' + FONT, 1) if '<head>' in BASE else FONT + BASE
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples.html'), 'w', encoding='utf-8').write(html + CSS + ''.join(s for _, s in S) + '</body></html>')
print([k for k, _ in S])
