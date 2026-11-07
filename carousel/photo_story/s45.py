# #45 「헤어진 남자가 생일에 연락하는 이유」 (11/3) — 지훈님 사진 14장. 글 상자는 stories_40_43.py 그대로, 배경만 사진으로
# python3 s40.py → p45/01~14.jpg + c45.html → node .work/r40p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import stories_44_47 as S

# 장 → (원본 번호, 전체 흐리기 px, [(x0,y0,x1,y1 비율, px)] 부분 흐리기)
PLAN = [
 (8, 0, []),                                              # 1 표지: 트리 조명
 (13, 0, []),                                             # 2 생일 날, 그 사람 이름이 떠요 · 회 한 상
 (5, 0, []),                                              # 3 "왜 이제 와서?" · 걷는 발
 (7, 0, [((0, 0.62, 0.12, 0.88), 10)]),                   # 4 생일은 유일한 핑계 · 고양이 택시
 (1, 0, []),                                              # 5 몇 번을 썼다 지워요 · 거울과 수도꼭지
 (14, 0, [((0.06, 0.26, 0.62, 0.94), 16)]),               # 6 "생일인데 축하 정도는" · 위스키 (라벨 흐리게)
 (9, 0, [((0.28, 0.80, 0.72, 1), 12), ((0, 0.86, 0.18, 0.94), 10), ((0.82, 0.86, 1, 0.92), 8)]),  # 7 미련, 미안함, 확인 · 노란 나무 (간판 흐리게)
 (3, 10, []),                                             # 8 미련이라면 · 쇼윈도 오토바이 (로고 안 보이게 전체 흐리게)
 (6, 0, [((0.05, 0.19, 0.49, 0.57), 16), ((0.12, 0.77, 0.43, 1), 12), ((0.53, 0.82, 0.66, 0.92), 8)]),  # 9 미안함이라면 · 건물 사이 하늘 (광고 화면 흐리게)
 (10, 0, [((0, 0, 1, 0.22), 12), ((0.37, 0.41, 0.51, 0.49), 10), ((0.57, 0.54, 0.67, 0.63), 8), ((0.60, 0.40, 0.72, 0.44), 6)]),  # 10 확인이라면 · 핸들 (차 · 사람 · 스티커 흐리게)
 (11, 0, [((0, 0.38, 1, 1), 10), ((0.78, 0.13, 1, 0.21), 10)]),  # 11 답장 다음 한 마디 · 전선과 하늘 (간판 흐리게)
 (2, 22, []),                                             # 12 "고마워. 잘 지내." · 벽돌 벽 (글자 흐리게)
 (4, 22, []),                                             # 13 생일이 아닌 날에도 · 빛 (포스터 전체 흐리게)
 (12, 0, [((0.40, 0.42, 0.50, 0.48), 8), ((0.62, 0.38, 0.80, 0.46), 8)]),  # 14 마지막 장: 자전거 앞 지훈님 (표지판 흐리게)
]
SHIFT = {14: -13}   # 마지막 장: 얼굴(가운데)을 비우고 상자를 위로

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p45/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p45/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C45), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p45/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c45.html', 'w', encoding='utf-8').write(build(slides(), no="45"))
    print('ok')
