# #59(11/15 순서 바꿈부터 · 원래 #56 → #57 → #58) 글 상자 + 배경 (11/12) — 사진은 보관함(p39 ~ p47)에서 8장, 나머지 6장은 그래픽(p56g)
# python3 gfx56.py → node render56.js gfx → python3 s56.py → node render56.js c56
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_56 as S
import os

PLAN = {  # 11/16 새 사진(p59s) · (폴더/src_NN, [(x0,y0,x1,y1 비율, 흐리기 px)], 자르기 또는 없음)
 1: ('p59s/src_01', [((0.27, 0.50, 0.37, 0.59), 12), ((0.25, 0.60, 0.35, 0.71), 12)], (0.05, 0.18, 1.0, 1.0)),   # 표지: 거울 셀카 (뒤 술병 · 책 글자 흐리게)
 3: ('p59s/src_05', [((0.56, 0.24, 0.76, 0.42), 14), ((0.72, 0.11, 0.96, 0.19), 12)]),   # 직접 다가간 여자 · 와인 한 잔 (뒤 손님 · 창 글자 흐리게)
 5: ('p59s/src_07', [((0.02, 0.32, 0.26, 0.39), 14), ((0.58, 0.19, 0.99, 0.37), 16), ((0.29, 0.51, 0.47, 0.71), 14), ((0.35, 0.69, 0.53, 0.79), 14), ((0.50, 0.68, 0.66, 0.81), 14), ((0.65, 0.59, 0.99, 0.72), 14)]),  # 매주 가는 곳 · 단골 카페 선반 (가게 이름 · 포스터 · 가격표 흐리게)
 7: ('p59s/src_02', [((0.14, 0.40, 0.40, 0.82), 16), ((0.10, 0.12, 0.72, 0.40), 16), ((0.70, 0.04, 0.86, 0.11), 12)], (0.0, 0.30, 1.0, 1.0)),   # 일 · 공부 · 책과 촛대 (책 제목 · 술 라벨 흐리게)
 9: ('p59s/src_06', [((0.0, 0.40, 0.40, 0.75), 10), ((0.70, 0.45, 0.82, 0.75), 10)]),   # 남자들끼리 · 니트 오브제 (짜인 글자 흐리게)
 11: ('p59s/src_03', []),   # 같은 곳에, 꾸준히 · 흰 난초
 13: ('p59s/src_04', []),   # 남자가 먼저 걸게 · 원뿔 조명
 14: ('p59s/src_01', [((0.27, 0.50, 0.37, 0.59), 12), ((0.25, 0.60, 0.35, 0.71), 12)], (0.25, 0.22, 0.90, 0.95)),   # 마지막 장: 같은 셀카 가까이
}
SHIFT = {1: 6, 14: 22}
VIVID = {3, 5}

def prep(i, src, regions, crop=None):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:   # 가장자리를 부드럽게 흐려요
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        m = Image.new('L', im.size, 0); m.paste(255, b); m = m.filter(ImageFilter.GaussianBlur(int(0.01 * w)))
        im = Image.composite(im.filter(ImageFilter.GaussianBlur(r * w / 1080)), im, m)
    if crop: im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
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
    open('c59.html', 'w', encoding='utf-8').write(build(sl, no='59'))  # 11/14 · 11/15 순서 바꿈 세 번: 이 캐러셀은 #59
    print('ok')
