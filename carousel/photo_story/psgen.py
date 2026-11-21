# 사진 스토리형 공통 생성기 — GUIDE.md 규칙
# 장 = (배경, 설명, 상자들). 배경: 사진 경로 | 색 이름(night · warm · gray · wine · blue · olive) — 색 배경은 사진 받기 전 임시
# 상자: W · G = 표지용 큰 상자 / w 흰(내레이션) · k 검은(속마음) · g 금색(핵심) · q 따옴표(남자들끼리 하는 말)
import html
e = html.escape

TINT = {'night': ('#232b3a', '#0d1017'), 'warm': ('#3d3026', '#15100c'), 'gray': ('#3b3b3b', '#121212'),
        'wine': ('#3d2129', '#140a0d'), 'blue': ('#1f3140', '#0a1117'), 'olive': ('#33362a', '#11120d')}

CSS = '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=block">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { word-break:keep-all; background:#333; font-family:'Noto Sans KR',sans-serif; }
  .slide { width:1080px; height:1350px; position:relative; overflow:hidden; margin-bottom:20px; background:#1a1917; }
  /* 사진은 채도 · 밝기를 눌러 배경으로 물러나게, 상자는 진한 색으로 앞으로 (10/29 시선 점검) */
  .slide img.bg { position:absolute; filter:saturate(.5) brightness(.82) contrast(.95); }
  .slide.vid { background:transparent; }
  .tint { position:absolute; inset:0; }
  .tint:after { content:''; position:absolute; inset:0; background:radial-gradient(ellipse at 30% 20%, rgba(255,255,255,.07), transparent 60%); }
  .bx { position:absolute; max-width:84%; font-size:46px; line-height:1.38; font-weight:500; padding:16px 28px; letter-spacing:-0.01em; }
  .bx.w { background:#fff; color:#151515; border:2px solid #151515; }
  .bx.k { background:#111; color:#f2f2f2; font-size:38px; }
  .bx.g { background:#ffcb3d; color:#151515; font-weight:700; }
  .bx.q { background:#f4f1ea; color:#151515; border-left:10px solid #f0c674; font-weight:700; }
  .bx.W { background:#fff; color:#151515; border:2px solid #151515; font-size:62px; font-weight:700; }
  .bx.G { background:#ffcb3d; color:#151515; font-size:76px; font-weight:900; letter-spacing:-0.03em; line-height:1.25; }
  .num { position:absolute; right:40px; top:40px; font-size:28px; color:#fff; background:rgba(0,0,0,.45); border-radius:999px; padding:6px 18px; }
  .hd { position:absolute; left:40px; bottom:36px; font-size:28px; color:rgba(255,255,255,.75); text-shadow:0 1px 6px rgba(0,0,0,.6); }
  .ser { position:absolute; right:40px; bottom:36px; font-size:30px; color:rgba(255,255,255,.8); letter-spacing:.03em; text-shadow:0 1px 6px rgba(0,0,0,.6); }
  .phd { position:absolute; left:0; right:0; bottom:130px; text-align:center; font-size:34px; color:#8a8378; }
  .phd b { display:block; font-size:30px; color:#6d675e; letter-spacing:.1em; margin-bottom:8px; }
  .shade { position:absolute; left:0; right:0; bottom:0; height:60%; background:linear-gradient(transparent, rgba(0,0,0,.55)); }
</style></head><body>
'''

def build(slides, no=None):
    out = CSS; n = len(slides)
    for i, (bg, desc, boxes) in enumerate(slides, 1):
        cls = 'slide'
        if isinstance(bg, dict) and bg.get('video'):  # 영상 장: 글 상자만 투명하게 그려서 영상 위에 얹어요 (vidgen.py)
            b = '<div class="shade"></div>'; cls = 'slide vid'
        elif isinstance(bg, dict):  # {'src':..., 'style':...} 사진 확대 · 위치
            b = f'<img class="bg" src="{e(bg["src"])}" style="{bg["style"]}">' + ('' if bg.get('noshade') else '<div class="shade"></div>')
        elif bg is None:  # 사진 자리 (설명 표시)
            b = f'<div class="tint" style="background:linear-gradient(160deg,#3a3631,#191816 70%)"></div><div class="phd"><b>사진 자리</b>{e(desc)}</div>'
        elif bg in TINT:
            a, c = TINT[bg]; b = f'<div class="tint" style="background:linear-gradient(165deg,{a},{c} 75%)"></div>'
        else:
            b = f'<img class="bg" src="{e(bg)}" style="inset:0;width:100%;height:100%;object-fit:cover"><div class="shade"></div>'
        bx = ''
        for kind, text, top, left in boxes:
            pos = f'top:{top}%;' + ('right:6%;' if left == 'r' else f'left:{left}%;')
            bx += f'<div class="bx {kind}" style="{pos}">{e(text)}</div>'
        ser = ('넘겨보세요 →' if i == 1 else f'남자들끼리 하는 말 #{no}') if no else ''
        out += f'<section class="{cls}" id="s{i}">{b}{bx}<div class="num">{i}/{n}</div><div class="hd">@mszexc</div><div class="ser">{ser}</div></section>\n'
    return out + '</body></html>'

EBOOK = ('k', '남자가 하는 말의 뜻은 전자책 1·2권에 · 프로필 링크에서 무료로 받아보세요', 82, 'r')
