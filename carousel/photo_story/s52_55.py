# #52 ~ #55 글 상자 + 배경 (11/10) — 사진은 보관함(p39 ~ p47)에서 7장, 나머지 7장은 그래픽(p52g ~ p55g)
# python3 gfx52_55.py → node render52.js gfx → python3 s52_55.py → node render52.js c52 c53 c54 c55
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_52_55 as S

# 장 → ('폴더/src_NN', [(x0,y0,x1,y1 비율, 흐리기 px)])  · 표지(1)와 마지막(14)은 얼굴 사진
PLAN = {
 '52': {1: ('p52s/src_01', [((0.72, 0.46, 0.85, 0.65), 16), ((0.85, 0.71, 1, 0.85), 16), ((0.04, 0.63, 0.16, 0.78), 14), ((0.69, 0.72, 0.84, 0.81), 14)]),  # 11/11 새 사진: 헬스장 거울 셀카 (Reebok · VERVE · 원판 로고 흐리게)
        3: ('p52s/src_05', []), 5: ('p52s/src_06', []), 9: ('p52s/src_04', []), 11: ('p52s/src_03', []),
        13: ('p52s/src_07', [((0.14, 0.80, 0.42, 0.86), 14), ((0.12, 0.88, 0.62, 1), 14)]),   # 단풍 빌딩 (반사 글자 · 병원 간판 흐리게)
        14: ('p52s/src_02', [((0.08, 0.36, 0.17, 0.48), 14), ((0.67, 0.36, 0.76, 0.57), 14)])},  # 엘리베이터 셀카 (안내문 · 전화번호 흐리게)
 '53': {1: ('p44/src_05', []), 3: ('p41/src_04', []), 5: ('p45/src_05', []), 9: ('p41/src_11', []),
        11: ('p42/src_06', []), 13: ('p47/src_10', []), 14: ('p45/src_12', [])},
 '54': {1: ('p44/src_14', []), 3: ('p43/src_10', []), 5: ('p39/src_13', []), 9: ('p40/src_15', [((0.08, 0.30, 0.42, 0.75), 16)]),
        11: ('p43/src_13', []), 13: ('p44/src_09', []), 14: ('p44/src_11', [])},
 '55': {1: ('p42/src_03', [((0.56, 0.48, 0.75, 0.57), 14)]), 3: ('p39/src_14', []), 5: ('p42/src_09', []), 9: ('p47/src_08', []),
        11: ('p41/src_03', []), 13: ('p47/src_11', []), 14: ('p43/src_03', [])},
}
SHIFT = {1: 6}
VIVID = {('52', 13)}  # 낮 단풍은 색을 덜 빼요
SHIFT14 = {'55': 22, '52': -12}  # 마지막 장 글 상자가 얼굴을 가리면 아래로

def prep(no, i, src, regions):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    out = f'p{no}/{i:02d}.jpg'
    im.save(out, quality=90)
    return out

if __name__ == '__main__':
    import os
    for no, (t, c, cap, pin) in S.DATA.items():
        assert len(c) == 14 and cap.count('#') == 5, no
        os.makedirs(f'p{no}', exist_ok=True)
        sl = []
        for i, boxes in enumerate(c, 1):
            sh = SHIFT14.get(no, 0) if i == 14 else SHIFT.get(i, 0)
            boxes = [(k, x, top + sh if top < 80 else top, l) for k, x, top, l in boxes]
            if i in PLAN[no]:
                bg = {'src': prep(no, i, *PLAN[no][i]), 'style': 'inset:0;width:100%;height:100%;object-fit:cover' + (';filter:saturate(.85) brightness(.9)' if (no, i) in VIVID else '')}
            else:
                g = f'p{no}g/{i:02d}.png'
                bg = {'src': g, 'noshade': not bright(g), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
            sl.append((bg, '', boxes))
        open(f'c{no}.html', 'w', encoding='utf-8').write(build(sl, no=no))
    print('ok')
