# #46 「남자가 헤어지고 바로 괜찮아 보이는 이유」 (11/8) — 사진 대신 장마다 내용에 맞는 그래픽 배경 14장 (gfx46.py)
# python3 gfx46.py → node .work/rg46.js (p46g/*.png) → python3 s46.py → node .work/r46p.js
from psgen import build
import stories_44_47 as S
SHIFT = {}
def slides():
    out = []
    for i, (_, _, boxes) in enumerate(S.C46, 1):
        bx = [(k, t, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p46g/{i:02d}.png', 'noshade': i != 13, 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}, '', bx))
    return out
if __name__ == '__main__':
    open('c46.html', 'w', encoding='utf-8').write(build(slides(), no='46'))
    print('ok')
