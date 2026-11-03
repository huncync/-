# #40 「남자가 술 마시고 하는 말, 진짜 뜻」 (11/3) — 지훈님 사진 14장. 글 상자는 stories_40_43.py 그대로, 배경만 사진으로
# python3 s40.py → p40/01~14.jpg + c40.html → node .work/r40p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import stories_40_43 as S

# 장 → (원본 번호, 전체 흐리기 px, [(x0,y0,x1,y1 비율, px)] 부분 흐리기)
PLAN = [
 (10, 0, [((0, 0.60, 1, 1), 16), ((0.60, 0.42, 0.85, 0.56), 10)]),   # 1 표지: 술집 바 (사람 얼굴 · 맥주 간판 흐리게)
 (2, 0, []),                                                        # 2 밤하늘 서치라이트 · 반은 술, 반은 진심
 (11, 0, []),                                                       # 3 "자?" 밤 12시 · 늦은 밤 버거
 (12, 0, []),                                                       # 4 "보고 싶다" · 바다
 (7, 0, []),                                                        # 5 "내가 진짜 잘할게" · 향수 라벨
 (4, 0, []),                                                        # 6 "너밖에 없어" · 산 위에서 내려다본 도시
 (1, 0, [((0, 0.40, 0.78, 0.57), 10), ((0.66, 0.45, 0.72, 0.52), 8)]),  # 7 "우리 왜 헤어졌지?" · 빨간불 신호 대기 (간판 흐리게)
 (9, 0, []),                                                        # 8 남자들끼리 "폰 뺏어" · 친구들과 돗자리
 (14, 0, [((0.15, 0.48, 0.82, 0.80), 18), ((0.20, 0.30, 0.70, 0.46), 6)]),  # 9 "기억 안 나" 다음 날 · 카페 노트북 (화면 · 사람 흐리게)
 (3, 0, []),                                                        # 10 확인하는 법 · 산에서 쉬는 다리
 (13, 0, [((0.60, 0.52, 1, 0.72), 12)]),                            # 11 그가 먼저 꺼내면 · 기차 타는 날 (지나가는 사람 흐리게)
 (5, 0, [((0.70, 0, 1, 0.20), 12), ((0.25, 0, 0.62, 0.22), 6)]),    # 12 아무 일 없던 척 · 책상 위 물건 (신문 · 상자 글자 흐리게)
 (8, 0, []),                                                        # 13 그날 밤 길게 답하지 마세요 · 상자
 (6, 0, []),                                                        # 14 마지막 장: 카페의 지훈님
]
SHIFT = {14: 14, 3: 18}   # 마지막 장: 얼굴(위쪽)을 비우고 상자를 아래로 · 3장: 버거를 비우고 아래로

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p40/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p40/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C40), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p40/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c40.html', 'w', encoding='utf-8').write(build(slides(), no='40'))
    print('ok')
