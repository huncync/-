# #71 ~ #75 글 상자 (s66_70.py를 복사 · 11/23) + 배경 (11/16) — 지훈님 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장 · 모자이크 없음(11/16 결정)
# python3 gfx66_70.py → node render66.js gfx → python3 s64_65.py → node render66.js c64 c65
import os
from PIL import Image, ImageOps
from psgen import build
from s48_50 import bright
import stories_71_75 as S

# 장 → ('폴더/src_NN', 자르기 또는 None)
PLAN = {  # 지훈님 사진(보관함) · 표지와 마지막 장은 얼굴 · (폴더/src_NN, 자르기 또는 None)
 '71': {1: ('p43/src_03', (0.0, 0.1, 1.0, 1.0)), 3: ('p45/src_07', None), 5: ('p44/src_06', None), 7: ('p40/src_10', None),
        9: ('p39/src_04', None), 11: ('p39/src_11', None), 13: ('p47/src_10', None), 14: ('p43/src_03', (0.1, 0.15, 0.9, 0.8))},
 '72': {1: ('p72n/src_01', (0.0, 0.12, 1.0, 0.97)), 3: ('p72n/src_05', None), 5: ('p72n/src_03', None), 7: ('p72n/src_04', None),  # 11/24 새 사진
        9: ('p72n/src_02', None), 11: ('p51/src_05', None), 13: ('p44/src_09', None), 14: ('p72n/src_01', (0.1, 0.3, 0.9, 0.93))},
 '73': {1: ('p73n/src_01', (0.0, 0.15, 1.0, 1.0)), 3: ('p73n/src_05', None), 5: ('p73n/src_02', None), 7: ('p73n/src_04', None),  # 11/25 새 사진
        9: ('p43/src_10', None), 11: ('p73n/src_06', None), 13: ('p73n/src_03', None), 14: ('p73n/src_07', (0.0, 0.2, 1.0, 0.95))},
 '74': {1: ('p74n/src_01', (0.0, 0.1, 1.0, 1.0)), 3: ('p74n/src_02', None), 5: ('p74n/src_03', None), 7: ('p40/src_15', None),  # 11/25 새 사진
        9: ('p74n/src_04', None), 11: ('p74n/src_05', None), 13: ('p40/src_12', None), 14: ('p74n/src_01', (0.1, 0.25, 0.9, 0.92))},
 '75': {1: ('p75n/src_01', (0.22, 0.38, 0.82, 0.98)), 3: ('p75n/src_02', None), 5: ('p45/src_03', None), 7: ('p75n/src_04', None),  # 11/26 새 사진 · 7장은 노트북 화면(이메일)이 안 보이게 원본을 위쪽만 잘라 저장
        9: ('p75n/src_03', None), 11: ('p51/src_07', None), 13: ('p47/src_11', None), 14: ('p75n/src_01', (0.3, 0.4, 0.75, 0.86))},
}
SHIFT = {1: 6}
SHIFT14 = {k: 22 for k in ('71', '72', '73', '74', '75')}
# 영상 장 (11/22): 글 상자만 그리고 영상은 vid68.py가 얹어요
# 11/23 자막 칸 포인트 (#69부터): 주제별 강조색 + 핵심 한 장 반전
ACCENT = {'71': 'yellow', '72': 'coral', '73': 'yellow', '74': 'green', '75': 'coral'}
POINT = {k: 13 for k in ('71', '72', '73', '74', '75')}
VIDEO = set()
VIVID = {('75', 1), ('75', 3), ('75', 14), ('74', 3), ('74', 5), ('73', 3), ('73', 7), ('73', 13), ('72', 1), ('72', 3), ('72', 9), ('72', 14)}

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
