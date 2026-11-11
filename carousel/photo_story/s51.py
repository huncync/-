# #51 「남자가 "미안해" 해도 사과가 아닌 경우」 (11/11) — 지훈님 사진 7장(8칸) + 그래픽 6장(p51g 그대로)
# python3 s51.py → node render48.js c51
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_49_51 as S

# 장 → (사진 번호, [(x0,y0,x1,y1 비율, 흐리기 px)], 자르기(x0,y0,x1,y1) 또는 None)
PLAN = {
 1: (1, [((0.11, 0.32, 0.20, 0.44), 14), ((0.72, 0.33, 0.80, 0.55), 14)], None),   # 표지: 엘리베이터 거울 셀카 (안내문 · 전화번호 흐리게)
 3: (3, [], None),                                                                   # 진짜 미안한 남자는 "무엇이" · 6F 엘리베이터
 5: (4, [], None),                                                                   # 첫 번째 신호 · 벽 조명
 8: (7, [], None),                                                                   # 남자들끼리 · 샹들리에
 9: (5, [], None),                                                                   # 말보다 행동이 먼저 · 소파
 12: (2, [], None),                                                                  # 한 번은 받아 주세요 · DAIEN 상자 (지훈님 브랜드)
 13: (6, [((0.50, 0.42, 1, 0.85), 10)], None),                                       # 자존심을 내려놓는 일 · 선반 꽃 (잡지 글자 흐리게)
 14: (1, [((0.11, 0.32, 0.20, 0.44), 14), ((0.72, 0.33, 0.80, 0.55), 14)], (0.18, 0.30, 0.82, 0.92)),  # 마지막 장: 같은 셀카를 가까이
}
SHIFT = {1: 6, 14: 22}

def prep(i, src, regions, crop):
    im = ImageOps.exif_transpose(Image.open(f'p51/src_{src:02d}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    if crop: im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    im.save(f'p51/{i:02d}.jpg', quality=90)

if __name__ == '__main__':
    t, c, cap, pin = S.DATA['51']
    assert len(c) == 14 and cap.count('#') == 5
    sl = []
    for i, boxes in enumerate(c, 1):
        boxes = [(k, x, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, x, top, l in boxes]
        if i in PLAN:
            prep(i, *PLAN[i])
            bg = {'src': f'p51/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}
        else:
            bg = {'src': f'p51g/{i:02d}.png', 'noshade': not bright(f'p51g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        sl.append((bg, '', boxes))
    open('c51.html', 'w', encoding='utf-8').write(build(sl, no='51'))
    print('ok')
