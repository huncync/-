# #81 글 상자 (s76_80.py를 복사 · 11/26 · R10 시험작) + 배경 (11/16) — 지훈님 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장 · 모자이크 없음(11/16 결정)
# python3 gfx66_70.py → node render66.js gfx → python3 s64_65.py → node render66.js c64 c65
import os
from PIL import Image, ImageOps
from psgen import build
from s48_50 import bright
import stories_81 as S

# 장 → ('폴더/src_NN', 자르기 또는 None)
PLAN = {  # 지훈님 사진(보관함) · 표지와 마지막 장은 얼굴 · 첫 장은 사진(게시물 보너스 조건)
 '81': {1: ('p73n/src_07', (0.0, 0.245, 1.0, 1.0)), 3: ('p69n/src_06', None), 5: ('p74n/src_02', None), 7: ('p70n/src_04', None),
        9: ('p73n/src_03', None), 11: ('p75n/src_04', None), 13: ('p69n/src_05', None), 14: ('p73n/src_07', (0.1, 0.3, 0.9, 0.85))},
}
SHIFT = {1: 6}
SHIFT14 = {'81': 22}
ACCENT = {'81': 'yellow'}
POINT = {'81': 13}
VIDEO = set()
VIVID = set()

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
