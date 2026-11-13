# #57 ~ #60 글 상자 + 배경 (11/13) — 사진 7장(보관함) + 그래픽 7장(p57g ~ p60g)
# python3 gfx57_60.py → node render57.js gfx → python3 s57_60.py → node render57.js c57 c58 c59 c60
import os
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_57_60 as S

# 장 → ('폴더/src_NN', [(x0,y0,x1,y1 비율, 흐리기 px)], 자르기 또는 없음) · 표지(1)와 마지막(14)은 얼굴 사진
PLAN = {
 '57': {1: ('p51/src_01', [((0.11, 0.32, 0.20, 0.44), 14), ((0.72, 0.33, 0.80, 0.55), 14)]), 3: ('p51/src_04', []), 5: ('p40/src_05', []), 9: ('p47/src_10', []),
        11: ('p49/src_05', [((0.12, 0.76, 0.62, 1), 14)]), 13: ('p51/src_05', []), 14: ('p44/src_06', [])},
 '58': {1: ('p50/src_01', [((0.26, 0.10, 0.62, 0.20), 14)]), 3: ('p55s/src_05', [((0.02, 0.05, 0.12, 0.16), 12), ((0.86, 0.0, 1, 0.56), 16), ((0.62, 0.6, 0.69, 0.72), 10)]),
        5: ('p40/src_15', [((0.08, 0.30, 0.42, 0.75), 16)]), 9: ('p43/src_13', []), 11: ('p55s/src_07', []), 13: ('p39/src_14', []),
        14: ('p50/src_05', [])},
 '59': {1: ('p48/src_06', [((0, 0.18, 0.12, 0.30), 14), ((0, 0.33, 0.10, 0.57), 14)]), 3: ('p49/src_06', []), 5: ('p49/src_07', []),
        9: ('p52s/src_07', [((0.14, 0.80, 0.42, 0.86), 14), ((0.12, 0.88, 0.62, 1), 14)]), 11: ('p40/src_12', []), 13: ('p49/src_01', []),
        14: ('p52s/src_02', [((0.08, 0.36, 0.17, 0.48), 14), ((0.67, 0.36, 0.76, 0.57), 14)])},
 '60': {1: ('p44/src_11', []), 3: ('p51/src_06', [((0.50, 0.42, 1, 0.85), 10)]), 5: ('p43/src_10', []), 9: ('p55s/src_03', [((0.72, 0.86, 1, 1), 10)]),
        11: ('p51/src_07', []), 13: ('p42/src_07', []), 14: ('p42/src_03', [((0.56, 0.48, 0.75, 0.57), 14)])},
}
SHIFT = {1: 6}
SHIFT14 = {}
VIVID = {('59', 3), ('59', 5), ('59', 9), ('59', 11), ('60', 13), ('57', 9)}

def prep(no, i, src, regions, crop=None):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    if crop: im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    out = f'p{no}/{i:02d}.jpg'
    im.save(out, quality=90)
    return out

if __name__ == '__main__':
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
