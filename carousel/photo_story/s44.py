# #44 「남자가 여사친 얘기할 때 하는 말들, 진짜 뜻」 (11/3) — 지훈님 사진 14장. 글 상자는 stories_40_43.py 그대로, 배경만 사진으로
# python3 s40.py → p44/01~14.jpg + c44.html → node .work/r40p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import stories_44_47 as S

# 장 → (원본 번호, 전체 흐리기 px, [(x0,y0,x1,y1 비율, px)] 부분 흐리기)
PLAN = [
 (12, 0, [((0.66, 0.50, 1, 0.82), 14), ((0, 0.70, 0.16, 0.80), 10), ((0.16, 0.62, 0.24, 0.72), 8), ((0.52, 0.62, 0.74, 0.70), 8)]),  # 1 표지: 공원 브이 사진 (옆 사람 · 컵 · 봉투 로고 흐리게)
 (11, 0, [((0.04, 0.38, 0.15, 0.52), 10), ((0.64, 0.40, 0.74, 0.67), 10), ((0.34, 0.47, 0.42, 0.53), 6)]),  # 2 남자는 대부분 같은 말 · 엘리베이터 셀카
 (8, 0, [((0.50, 0.78, 0.70, 0.94), 12), ((0.08, 0.82, 0.15, 0.91), 8), ((0.62, 0.74, 0.70, 0.78), 6)]),  # 3 "그냥 친구야" · 거리를 보세요 · 가로수길
 (4, 0, [((0, 0.80, 0.08, 0.88), 10)]),  # 4 "걔는 여자로 안 보여" · 파란 하늘
 (7, 0, []),  # 5 "오래된 친구라 그래" · 나뭇잎
 (2, 0, []),  # 6 "너도 같이 볼래?" · 화분
 (6, 0, [((0.45, 0.33, 0.66, 0.44), 12), ((0.68, 0.44, 1, 0.63), 12)]),  # 7 "질투하는 거야?" · 오토바이 거울 셀카
 (14, 0, [((0.36, 0.48, 0.44, 0.67), 10)]),  # 8 "여친한테는 걔 얘기 굳이 안 해." · 헬스장 셀카
 (9, 0, [((0.12, 0.23, 0.33, 0.30), 12), ((0.64, 0.67, 0.90, 0.73), 12)]),  # 9 봐야 할 세 가지 · 아파트
 (1, 0, []),  # 10 "그냥 친구"의 거리가 아니에요 · 비상구
 (3, 0, []),  # 11 그건 정말 친구예요 · 계단 오르는 발
 (13, 0, [((0.12, 0.43, 0.23, 0.54), 12), ((0.12, 0.61, 0.21, 0.70), 12), ((0.66, 0.69, 0.96, 0.78), 12)]),  # 12 "걔랑 연락 끊어." · 남자는 숨기는 쪽을 · 상자
 (10, 0, []),  # 13 "만나는 날은 나한테도 말해줘." · 엘리베이터 1
 (5, 0, [((0.02, 0.36, 0.34, 0.62), 12), ((0.60, 0.37, 0.71, 0.50), 8)]),  # 14 마지막 장: 거울 셀카
]
SHIFT = {1: 6, 2: -16, 8: -12, 14: 20}   # 얼굴 피해서 상자 옮기기

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p44/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p44/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C44), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p44/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c44.html', 'w', encoding='utf-8').write(build(slides(), no="44"))
    print('ok')
