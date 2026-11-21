# #49 「남자에게 "편한 사람"으로만 남는 법」 (11/10) — 지훈님 사진 7장 + 그래픽 7장(p49g 그대로)
# python3 s49.py → node render48.js c49
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_49_51 as S

# 장 → (사진 번호, [(x0,y0,x1,y1 비율, 흐리기 px)])  · 나머지 장은 그래픽(p49g)
PLAN = {
 1: (4, [((0.27, 0.43, 0.34, 0.60), 10)]),                                    # 표지: 유리창에 비친 셀카 (뒤 행인 흐리게)
 8: (2, [((0, 0.24, 0.24, 0.38), 14), ((0.36, 0.75, 0.65, 0.88), 14)]),     # 남자들끼리 · 헬스장 원판 (로고 흐리게)
 9: (6, []),                                                                 # 아니요, 반대로 하세요 · 파란 하늘
 10: (3, [((0.72, 0.71, 1, 0.83), 12)]),                                     # 다 잡힌 건 궁금하지 않아요 · 노란 잎 (간판 흐리게)
 11: (5, [((0.12, 0.76, 0.62, 1), 14)]),                                     # 내 하루는 내 것으로 · 빌딩과 단풍 (병원 간판 흐리게)
 13: (7, []),                                                                # '자기 삶' · 햇빛 받은 나무
 14: (1, []),                                                                # 마지막 장: 벽에 비친 그림자
}
SHIFT = {1: 6}
VIVID = {9, 10, 11, 13}  # 낮 단풍 · 하늘은 기본 필터(채도 .5)를 약하게: 색이 살아 있게

def prep(i, src, regions):
    im = ImageOps.exif_transpose(Image.open(f'p49/src_{src:02d}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    im.save(f'p49/{i:02d}.jpg', quality=90)

if __name__ == '__main__':
    t, c, cap, pin = S.DATA['49']
    assert len(c) == 14 and cap.count('#') == 5
    sl = []
    for i, boxes in enumerate(c, 1):
        boxes = [(k, x, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, x, top, l in boxes]
        if i in PLAN:
            prep(i, *PLAN[i])
            bg = {'src': f'p49/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover' + (';filter:saturate(.85) brightness(.9)' if i in VIVID else '')}
        else:
            bg = {'src': f'p49g/{i:02d}.png', 'noshade': not bright(f'p49g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        sl.append((bg, '', boxes))
    open('c49.html', 'w', encoding='utf-8').write(build(sl, no='49'))
    print('ok')
