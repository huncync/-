# #56 글 상자 + 배경 (11/12) — 사진은 보관함(p39 ~ p47)에서 8장, 나머지 6장은 그래픽(p56g)
# python3 gfx56.py → node render56.js gfx → python3 s56.py → node render56.js c56
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_56 as S
import os

PLAN = {
 1: ('p41/src_08', [((0.0, 0.30, 0.56, 0.43), 14), ((0.38, 0.40, 0.58, 0.455), 14), ((0.28, 0.18, 0.62, 0.30), 12)]),    # 표지: 거리 볼록거울 셀카 (차 번호판 · 간판 흐리게)
 3: ('p41/src_03', []),    # 직접 다가간 여자 · 걷는 발
 5: ('p39/src_10', []),    # 매주 가는 곳 · 헬스장 벽
 7: ('p40/src_05', []),    # 일 · 공부 · 작업 책상
 9: ('p43/src_10', []),    # 남자들끼리 · 퇴근길 바이크
 11: ('p42/src_07', []),   # 꾸준히 · 나무와 하늘
 13: ('p40/src_12', []),   # 남자가 먼저 걸게 · 바다
 14: ('p43/src_09', [((0.685, 0.18, 1.0, 0.54), 18), ((0.0, 0.25, 0.22, 0.62), 14), ((0.24, 0.33, 0.39, 0.45), 12)]),   # 마지막 장: 거울 셀카 (벽 포스터 흐리게)
}
SHIFT = {1: 6, 14: 22}
VIVID = {11, 13}

def prep(i, src, regions):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    out = f'p56/{i:02d}.jpg'
    im.save(out, quality=90)
    return out

if __name__ == '__main__':
    os.makedirs('p56', exist_ok=True)
    assert len(S.C56) == 14 and S.CAP56.count('#') == 5
    sl = []
    for i, boxes in enumerate(S.C56, 1):
        boxes = [(k, x, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, x, top, l in boxes]
        if i in PLAN:
            bg = {'src': prep(i, *PLAN[i]), 'style': 'inset:0;width:100%;height:100%;object-fit:cover' + (';filter:saturate(.85) brightness(.9)' if i in VIVID else '')}
        else:
            g = f'p56g/{i:02d}.png'
            bg = {'src': g, 'noshade': not bright(g), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        sl.append((bg, '', boxes))
    open('c56.html', 'w', encoding='utf-8').write(build(sl, no='56'))
    print('ok')
