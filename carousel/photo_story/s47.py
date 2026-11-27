# #47 글 상자 + 배경 (11/9) — 지훈님 사진 7장 + 그래픽 7장 섞기
# 원칙: 사람 · 장면이 필요한 장(표지 · 마지막 · 분위기)은 사진, 카톡 · 그래프처럼 '설명'이 필요한 장은 그래픽
# python3 gfx47.py → node .work/rg47.js (p47g) → python3 s47.py → node .work/r47p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_44_47 as S

# 장 → ('g', None) 그래픽 그대로 | (사진 번호, 흐리기 px, [(x0,y0,x1,y1 비율, px)])
PLAN = {
 1: (3, 0, []),                                           # 표지: 화장실 거울 셀카
 4: (5, 0, []),                                           # 이유는 여러 가지 · 회의실 의자들
 6: (9, 0, []),                                           # 정리가 안 됐어요 · 엉킨 나무와 벽돌담
 8: (4, 0, []),                                           # "말 많이 하면 꼭 싸우더라" · 하얀 조명
 9: (8, 0, []),                                           # 마음이 멀어지는 중 · 보도 위 그림자와 금
 11: (12, 0, []),                                         # 챙기는 건 남아 있다면 · 초록불 아래 나무
 13: (13, 0, [((0.12, 0.12, 0.30, 0.18), 12), ((0.50, 0.90, 1, 1), 12), ((0.56, 0.74, 0.80, 0.78), 10), ((0, 0.88, 0.25, 1), 10)]),  # 말할 문을 열어 두기 · 건물 사이 하늘 (간판 흐리게)
 14: (6, 0, [((0, 0.38, 0.06, 0.48), 8)]),                # 마지막 장: 거울 반사 셀카
}
SHIFT = {1: 6, 14: 18}

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p47/src_{src:02d}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p47/{i:02d}.jpg', quality=90)

if __name__ == '__main__':
    sl = []
    for i, b in enumerate(S.C47, 1):
        boxes = [(k, t, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, t, top, l in b[2]]
        if i in PLAN:
            prep(i, *PLAN[i])
            bg = {'src': f'p47/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}
        else:
            bg = {'src': f'p47g/{i:02d}.png', 'noshade': not bright(f'p47g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        sl.append((bg, '', boxes))
    open('c47.html', 'w', encoding='utf-8').write(build(sl, no='47'))
    print('ok')
