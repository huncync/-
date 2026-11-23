# #66 ~ #70 글 상자 + 배경 (11/16) — 지훈님 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장 · 모자이크 없음(11/16 결정)
# python3 gfx66_70.py → node render66.js gfx → python3 s64_65.py → node render66.js c64 c65
import os
from PIL import Image, ImageOps
from psgen import build
from s48_50 import bright
import stories_66_70 as S

# 장 → ('폴더/src_NN', 자르기 또는 None)
PLAN = {  # 지훈님 사진(보관함) · 표지와 마지막 장은 얼굴 · (폴더/src_NN, 자르기 또는 None)
 '66': {1: ('p39/src_07', (0.0, 0.18, 1.0, 1.0)), 3: ('p39/src_06', None), 5: ('p43/src_08', None), 7: ('p47/src_08', None),
        9: ('p49/src_04', None), 11: ('p40/src_04', None), 13: ('p42/src_12', None), 14: ('p39/src_07', (0.15, 0.22, 0.90, 0.80))},
 '67': {1: ('p50/src_05', (0.0, 0.18, 1.0, 1.0)), 3: ('p40/src_11', None), 5: ('p45/src_14', None), 7: ('p40/src_07', None),
        9: ('p45/src_08', None), 11: ('p47/src_04', None), 13: ('p43/src_14', None), 14: ('p50/src_05', (0.15, 0.2, 0.95, 0.85))},
 '68': {1: ('p68n/face_a', (0.0, 0.0, 1.0, 0.70)), 3: ('p68n/src_01', None), 5: ('p68n/src_06', None), 7: ('p68n/src_05', None),  # 11/22 새 사진 + 영상 캡처
        9: ('p68n/src_02', None), 11: ('p68n/src_04', None), 13: ('p68n/src_03', None), 14: ('p68n/face_b', (0.0, 0.07, 1.0, 0.77))},
 '69': {1: ('p69n/src_07', (0.15, 0.25, 0.95, 1.0)), 3: ('p69n/src_02', None), 5: ('p69n/src_03', None), 7: ('p69n/src_04', None),  # 11/23 새 사진
        9: ('p69n/src_01', None), 11: ('p69n/src_05', None), 13: ('p69n/src_06', None), 14: ('p69n/src_07', (0.2, 0.3, 0.9, 0.956))},
 '70': {1: ('p47/src_03', (0.0, 0.15, 1.0, 1.0)), 3: ('p42/src_09', None), 5: ('p49/src_01', None), 7: ('p41/src_05', None),
        9: ('p44/src_10', None), 11: ('p40/src_02', None), 13: ('p45/src_06', None), 14: ('p47/src_03', (0.12, 0.2, 0.92, 0.85))},
}
SHIFT = {1: 6}
SHIFT14 = {k: 22 for k in ('66', '67', '68', '69', '70')}
# 영상 장 (11/22): 글 상자만 그리고 영상은 vid68.py가 얹어요
# 11/23 자막 칸 포인트 (#69부터): 주제별 강조색 + 핵심 한 장 반전
ACCENT = {'69': 'green', '70': 'coral'}
POINT = {'69': 13, '70': 13}
VIDEO = {('68', 1), ('68', 14)}
VIVID = {('67', 9), ('68', 1), ('68', 11), ('68', 14), ('69', 1), ('69', 3), ('69', 5), ('69', 7), ('69', 9), ('69', 11), ('69', 13), ('69', 14)}  # 11/23 크리스마스 사진은 색을 살려요

def prep(no, i, src, crop=None):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
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
            if (no, i) in VIDEO:
                bg = {'video': True}
            elif i in PLAN[no]:
                bg = {'src': prep(no, i, *PLAN[no][i]), 'style': 'inset:0;width:100%;height:100%;object-fit:cover' + (';filter:saturate(.85) brightness(.9)' if (no, i) in VIVID else '')}
            else:
                g = f'p{no}g/{i:02d}.png'
                bg = {'src': g, 'noshade': not bright(g), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
            sl.append((bg, '', boxes))
        open(f'c{no}.html', 'w', encoding='utf-8').write(build(sl, no=no, accent=ACCENT.get(no), point=POINT.get(no)))
    print('ok')
