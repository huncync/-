# #76 ~ #80 글 상자 (s66_70.py를 복사 · 11/23) + 배경 (11/16) — 지훈님 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장 · 모자이크 없음(11/16 결정)
# python3 gfx66_70.py → node render66.js gfx → python3 s64_65.py → node render66.js c64 c65
import os
from PIL import Image, ImageOps
from psgen import build
from s48_50 import bright
import stories_76_80 as S

# 장 → ('폴더/src_NN', 자르기 또는 None)
PLAN = {  # 지훈님 사진(보관함) · 표지와 마지막 장은 얼굴 · (폴더/src_NN, 자르기 또는 None)
 '76': {1: ('p44/src_11', (0.0, 0.1, 1.0, 1.0)), 3: ('p41/src_02', None), 5: ('p47/src_08', None), 7: ('p48/src_05', None),
        9: ('p44/src_10', None), 11: ('p48/src_04', None), 13: ('p47/src_13', None), 14: ('p44/src_11', (0.15, 0.4, 0.85, 0.95))},
 '77': {1: ('p77n/src_01', (0.0, 0.25, 0.62, 0.83)), 3: ('p77n/src_02', None), 5: ('p77n/src_03', None), 7: ('p77n/src_04', None),  # 11/27 새 사진
        9: ('p77n/src_05', None), 11: ('p77n/src_06', None), 13: ('p49/src_06', None), 14: ('p77n/src_01', (0.06, 0.29, 0.46, 0.665))},
 '78': {1: ('p44/src_14', (0.0, 0.05, 1.0, 0.95)), 3: ('p41/src_01', None), 5: ('p42/src_06', None), 7: ('p45/src_09', None),
        9: ('p49/src_03', None), 11: ('p40/src_04', None), 13: ('p51/src_04', None), 14: ('p44/src_14', (0.15, 0.38, 0.85, 0.92))},
 '79': {1: ('p48/src_06', (0.0, 0.1, 1.0, 1.0)), 3: ('p39/src_01', None), 5: ('p43/src_13', None), 7: ('p39/src_12', None),
        9: ('p39/src_14', None), 11: ('p40/src_13', None), 13: ('p47/src_09', None), 14: ('p48/src_06', (0.1, 0.32, 0.9, 0.92))},
 '80': {1: ('p42/src_03', (0.0, 0.1, 1.0, 1.0)), 3: ('p51/src_06', None), 5: ('p51/src_03', None), 7: ('p47/src_04', None),
        9: ('p42/src_09', None), 11: ('p47/src_05', None), 13: ('p41/src_04', None), 14: ('p42/src_03', (0.1, 0.36, 0.9, 0.95))},
}
SHIFT = {1: 6}
SHIFT14 = {k: 22 for k in ('76', '77', '78', '79', '80')}
# 영상 장 (11/22): 글 상자만 그리고 영상은 vid68.py가 얹어요
# 11/23 자막 칸 포인트 (#69부터): 주제별 강조색 + 핵심 한 장 반전
ACCENT = {'76': 'coral', '77': 'yellow', '78': 'green', '79': 'coral', '80': 'yellow'}
POINT = {k: 13 for k in ('76', '77', '78', '79', '80')}
VIDEO = set()
VIVID = {('77', 1), ('77', 3), ('77', 9), ('77', 14)}

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
