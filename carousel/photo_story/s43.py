# #43 「남자가 식을 때, 칭찬보다 먼저 줄어드는 것」 (11/3) — 지훈님 사진 14장. 글 상자는 stories_40_43.py 그대로, 배경만 사진으로
# python3 s40.py → p43/01~14.jpg + c43.html → node .work/r40p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import stories_40_43 as S

# 장 → (원본 번호, 전체 흐리기 px, [(x0,y0,x1,y1 비율, px)] 부분 흐리기)
PLAN = [
 (2, 0, [((0.40, 0.61, 1, 0.85), 14)]),                   # 1 표지: 지하철 스크린도어 셀카 (안내판 흐리게)
 (12, 0, []),                                             # 2 예쁘다는 말은 아직 해요 · 수프
 (13, 0, []),                                             # 3 그보다 먼저 줄어든 게 · 파스타
 (8, 0, []),                                              # 4 질문이에요 · 도로 위 곡선
 (14, 0, []),                                             # 5 "오늘 뭐 했어?" 대신 "아 그래? 좋네." · 스테이크
 (5, 0, [((0.46, 0.45, 0.58, 0.56), 12), ((0.29, 0.43, 0.38, 0.54), 8)]),  # 6 대답만 하고 묻지 않아요 · 복도 (지나가는 사람 흐리게)
 (10, 0, [((0.72, 0.32, 0.94, 0.48), 12), ((0.46, 0.42, 0.53, 0.47), 8), ((0.24, 0.21, 0.73, 0.33), 8), ((0.72, 0.29, 0.92, 0.37), 8), ((0, 0.56, 0.07, 0.73), 10)]),  # 7 "요즘 걔 얘기 들으면 좀 피곤해" · 빨간불 (사람 · 번호판 · 간판 흐리게)
 (11, 0, [((0.48, 0.37, 0.98, 0.61), 10), ((0.96, 0.52, 1, 0.63), 10)]),  # 8 마음이 있을 땐 사소한 것까지 · 오토바이 뒷자리 (간판 흐리게)
 (4, 0, [((0.79, 0.75, 0.91, 0.87), 12)]),                # 9 질문은 궁금해야 나와요 · 하늘 (현수막 흐리게)
 (7, 0, []),                                              # 10 질문이 먼저 줄어요 · 돌바닥
 (6, 0, []),                                              # 11 마지막으로 당신 하루를 물은 게 언제인지 · 엘리베이터 1층
 (1, 0, []),                                              # 12 바쁠 때도 줄어요 · 계단 앞 발
 (9, 0, [((0, 0.24, 0.29, 1), 12), ((0.60, 0.32, 0.87, 0.57), 24), ((0.27, 0.35, 0.37, 0.43), 10), ((0.33, 0.59, 0.53, 0.83), 8)]),  # 13 먼저 물어보세요 · 거울 셀카 옆모습 (포스터 · QR 흐리게)
 (3, 0, [((0.10, 0.30, 0.23, 0.43), 8)]),                 # 14 마지막 장: 엘리베이터 셀카 (안내문 흐리게)
]
SHIFT = {1: 6, 13: 22, 14: -16}   # 표지: 얼굴 아래로 · 13장: 얼굴 아래 셔츠로 · 마지막 장: 얼굴 위로

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p43/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p43/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C43), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p43/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c43.html', 'w', encoding='utf-8').write(build(slides(), no="43"))
    print('ok')
