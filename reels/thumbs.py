# 릴스 썸네일 (10/29~) — 프로필 격자에서 캐러셀(사진 스토리형)과 한 묶음으로 보이게
# 1080×1920. 프로필 격자는 가운데 3:4(위아래 240px 잘림)만 보여서, 글자 · 얼굴은 y 240~1680 안에.
# python3 thumbs.py → thumbs.html (렌더는 scratchpad의 rthumb.js)
import html
e = html.escape

# key: (사진, 사진 위치, 작은 윗줄, 큰 제목 흰 줄, 큰 제목 금색 줄)
TH = {
 'r3': ('../carousel/cover_photo_02.jpg', '50% 35%', '남자가 식을 때,', '연락 다음으로', '사라지는 것'),
 'r6': (None, '50% 30%', '남자가 직접 말해요', '여자가 질문 폭탄을', '던지는 진짜 이유'),
}

CSS = '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@500;700;900&display=block">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:#333; font-family:'Noto Sans KR',sans-serif; word-break:keep-all; }
  .t { width:1080px; height:1920px; position:relative; overflow:hidden; margin-bottom:20px; background:linear-gradient(160deg,#3a3631,#191816 70%); }
  .t img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:saturate(.5) brightness(.8) contrast(.95); }
  .t .shade { position:absolute; left:0; right:0; bottom:0; height:62%; background:linear-gradient(transparent, rgba(0,0,0,.6)); }
  .t .ph { position:absolute; left:0; right:0; top:46%; text-align:center; color:#8a8378; font-size:36px; }
  .t .txt { position:absolute; left:64px; right:64px; top:1030px; }
  .t .s { font-family:'Nanum Pen Script',cursive; font-size:76px; color:#f4f1ea; -webkit-text-stroke:1px currentColor; text-shadow:0 2px 12px rgba(0,0,0,.6); margin-bottom:14px; }
  .t .b { display:inline-block; font-size:96px; font-weight:900; letter-spacing:-0.035em; line-height:1.2; padding:10px 26px; margin-top:12px; }
  .t .b.w { background:#fff; color:#151515; border:3px solid #151515; }
  .t .b.g { background:#ffcb3d; color:#151515; }
  .t .h { position:absolute; left:64px; top:1560px; font-size:34px; color:rgba(255,255,255,.8); text-shadow:0 1px 6px rgba(0,0,0,.6); }
</style></head><body>
'''

def build():
    out = CSS
    for k, (src, pos, small, w, g) in TH.items():
        bg = f'<img src="{e(src)}" style="object-position:{pos}">' if src else '<div class="ph">사진 자리 · 릴스 영상에서 얼굴 나온 한 장면</div>'
        out += (f'<section class="t" id="{k}">{bg}<div class="shade"></div><div class="txt"><div class="s">{e(small)}</div>'
                f'<div class="b w">{e(w)}</div><br><div class="b g">{e(g)}</div></div><div class="h">@mszexc · 남자들끼리 하는 말</div></section>\n')
    return out + '</body></html>'

if __name__ == '__main__':
    open('thumbs.html', 'w', encoding='utf-8').write(build())
    print('ok', list(TH))
