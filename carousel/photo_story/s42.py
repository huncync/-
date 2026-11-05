# #42 「남자가 아플 때 부르는 사람」 (11/3) — 지훈님 사진 14장. 글 상자는 stories_40_43.py 그대로, 배경만 사진으로
# python3 s40.py → p42/01~14.jpg + c42.html → node .work/r40p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import stories_40_43 as S

# 장 → (원본 번호, 전체 흐리기 px, [(x0,y0,x1,y1 비율, px)] 부분 흐리기)
PLAN = [
 (1, 0, []),                                              # 1 표지: 화장실 거울 셀카
 (9, 0, []),                                              # 2 아픈 걸 잘 말 안 해요 · 흐린 벽
 (10, 0, []),                                             # 3 누구한테 말하는지가 누구한테 기대는지 · 계단 내려가는 발
 (12, 0, [((0, 0.12, 0.36, 1), 12), ((0.77, 0.66, 1, 1), 12), ((0.36, 0.88, 0.77, 1), 8), ((0.72, 0.78, 0.9, 0.88), 8)]),  # 4 "걱정할까 봐" · 전선 (간판 · 전화번호 흐리게)
 (7, 0, []),                                              # 5 당신에게 먼저 말한다면 · 하늘과 나무
 (2, 0, []),                                              # 6 "나 오늘 좀 아파" · 화분
 (8, 0, [((0.16, 0.16, 0.62, 0.82), 16)]),                # 7 잔소리 없는 한 마디 · 캔 (상표 흐리게)
 (13, 0, []),                                             # 8 "약 먹었어? 오늘은 푹 자." · 색 칠한 보도
 (6, 0, [((0.64, 0.58, 0.80, 0.73), 14), ((0.46, 0.49, 0.72, 0.54), 8), ((0.70, 0.79, 0.79, 0.85), 8), ((0.82, 0.68, 1, 0.77), 10), ((0.05, 0.85, 0.95, 0.96), 6)]),  # 9 친구한테만 말하고 · 큰길 (광고 · 간판 · 번호판 흐리게)
 (4, 0, []),                                              # 10 아직 약해질 준비가 · 유리 건물과 하늘
 (11, 0, [((0.38, 0.40, 0.70, 0.59), 22)]),               # 11 곁에 있어 줬다면 · 올려다본 건물 (로고 흐리게)
 (14, 0, []),                                             # 12 쉽게 놓지 못해요 · 흐린 하늘과 안테나
 (5, 22, [((0.24, 0.28, 0.76, 0.76), 60)]),                                    # 13 옆에 있어 주세요 · 돌기둥 (전체를 흐리게 · 주소 안 보이게)
 (3, 0, [((0.57, 0.47, 0.74, 0.56), 12), ((0.91, 0.59, 1, 0.71), 12)]),  # 14 마지막 장: 거울 셀카 (로고 · 포스터 흐리게)
]
SHIFT = {1: -36, 14: -16}   # 표지 · 마지막 장: 얼굴(가운데)을 비우고 상자를 위로

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p42/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p42/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C42), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p42/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c42.html', 'w', encoding='utf-8').write(build(slides(), no="42"))
    print('ok')
