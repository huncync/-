# #41 「헤어진 남자가 스토리를 보는 이유」 (11/3) — 지훈님 사진 14장. 글 상자는 stories_40_43.py 그대로, 배경만 사진으로
# python3 s40.py → p41/01~14.jpg + c41.html → node .work/r40p.js
from PIL import Image, ImageOps, ImageFilter
from psgen import build
import stories_40_43 as S

# 장 → (원본 번호, 전체 흐리기 px, [(x0,y0,x1,y1 비율, px)] 부분 흐리기)
PLAN = [
 (8, 0, [((0, 0.22, 1, 0.38), 9)]),                       # 1 표지: 볼록거울 셀카 (간판 · 번호판 흐리게)
 (11, 0, [((0, 0, 1, 0.24), 14)]),                        # 2 스토리 본 사람 목록, 꽤 앞쪽 · 번호 붙은 의자 01~04 (화면 흐리게)
 (14, 0, []),                                             # 3 "아직 나한테 마음이 있나?" · 화이트보드 낙서 「여자」
 (7, 0, []),                                              # 4 이유는 셋 중 하나 · 하늘과 안테나
 (9, 0, [((0.74, 0, 1, 0.26), 12)]),                      # 5 잘 지내는지 확인 · 창밖 단풍 (가게 간판 흐리게)
 (2, 0, []),                                              # 6 새 사람이 생겼는지 · 노란 선 위 그림자
 (13, 0, []),                                             # 7 세 번째 · 트랙 3번 레인
 (10, 0, []),                                             # 8 "뜨니까 보게 되더라" · 불 켜진 P
 (6, 0, []),                                              # 9 언제 보는지를 보세요 · 바닥 표시
 (3, 0, []),                                              # 10 올리자마자 본다면, 기다리고 있었던 · 서 있는 발
 (4, 0, [((0.06, 0.68, 0.32, 1), 12), ((0.62, 0.80, 0.80, 1), 12)]),  # 11 며칠 지나서 몰아서 · 건물 사이 하늘 (간판 흐리게)
 (12, 0, [((0, 0.08, 0.50, 0.50), 10), ((0, 0.86, 0.45, 1), 10)]),     # 12 보기만 하고 연락이 없다면 · 원판 25kg (로고 흐리게)
 (1, 0, []),                                              # 13 당신 하루는 당신을 위해 · 화분
 (5, 0, []),                                              # 14 마지막 장: 보는 건 미련, 연락은 결심 · 노란 선
]
SHIFT = {1: -28}   # 표지: 얼굴(가운데)을 비우고 상자를 위로

def prep(i, src, blur, regions):
    im = ImageOps.exif_transpose(Image.open(f'p41/src_{src:02d}.jpg')).convert('RGB')
    W, H = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * W / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p41/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C41), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p41/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c41.html', 'w', encoding='utf-8').write(build(slides(), no="41"))
    print('ok')
