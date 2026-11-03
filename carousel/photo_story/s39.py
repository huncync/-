# #39 「이별 통보 받은 날 밤, 남자 머릿속」 (11/3) — 지훈님 사진 14장. 글 상자는 ps01.py 그대로, 배경만 사진으로
# python3 s39.py → p39/01~14.jpg(1080×1350 · 간판 · 로고 흐리게) + c39.html → node .work/r39.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import ps01

# 장 → (원본 번호, 흐리기: 전체 px 또는 [(x0,y0,x1,y1 비율, px)])
PLAN = [
 (8, 0, []),            # 1 표지: 일그러진 거울 셀카 (괜찮은 척하던 그 남자)
 (1, 7, []),            # 2 편의점 맥주 냉장고 (상표 흐리게)
 (11, 0, []),           # 3 따뜻한 펜던트 조명 (술자리)
 (4, 0, []),            # 4 쉬어가는 장: 바닥 돌
 (6, 0, [((0.45, 0.38, 0.62, 0.56), 8)]),   # 5 현관 복도 (멀리 지나가는 사람 흐리게)
 (9, 13, []),           # 6 노트북 화면 (글자 안 읽히게)
 (12, 5, []),           # 7 벽시계 (로고 흐리게) · 멈춰요
 (13, 0, [((0.0, 0.70, 1.0, 1.0), 9)]),     # 8 밤 전선 · 아파트 (아래 표지판 흐리게)
 (2, 0, []),            # 9 도로 위 흰 선
 (14, 0, [((0.20, 0.55, 0.34, 0.66), 10), ((0.38, 0.62, 0.52, 0.70), 8)]),  # 10 밤 골목 (간판 · 번호판 흐리게)
 (5, 0, []),            # 11 엘리베이터 층수 1
 (10, 10, []),          # 12 헬스장 입구 (글자 흐리게) · 멀쩡해 보이는 남자
 (3, 0, [((0.78, 0.66, 1.0, 0.84), 10)]),   # 13 하늘 (오른쪽 아래 현수막 흐리게)
 (7, 0, [((0.05, 0.30, 0.17, 0.55), 6), ((0.70, 0.30, 0.82, 0.56), 6)]),  # 14 엘리베이터 거울 셀카 (안내문 흐리게)
]
SHIFT = {1: 5, 14: -16}   # 표지: 얼굴 아래로 · 마지막 장: 얼굴 위로
MOVE = {3: [-12, 20, 20, 20]}  # 3장: 조명(40~60%)을 비우고 첫 줄은 위, 따옴표 3개는 아래로

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p39/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p39/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, ps01.SLIDES), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        if i in MOVE: bx = [(k, t, top + m, l) for (k, t, top, l), m in zip(bx, MOVE[i])]
        out.append(({'src': f'p39/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c39.html', 'w', encoding='utf-8').write(build(slides(), no='39'))
    print('ok')
