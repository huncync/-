# #48 글 상자 + 배경 (11/9) — 지훈님 사진 7장 + 그래픽 7장
# python3 gfx48.py → node render48.js gfx → python3 s48.py → node render48.js slides
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_48 as S

# 장 → (사진 번호, [(x0,y0,x1,y1 비율, 흐리기 px)])  · 사진 없는 장은 그래픽(p48g)
PLAN = {
 1: (6, [((0, 0.18, 0.12, 0.30), 14), ((0, 0.33, 0.10, 0.57), 14)]),                    # 표지: 헬스장 거울 셀카 (간판 흐리게)
 3: (4, []),                                                                              # 대부분은 진짜 피곤 · 사무실 건물
 5: (5, []),                                                                              # 말할 힘이 없어 · 계단 오르는 발
 7: (3, [((0, 0.04, 0.46, 0.26), 18), ((0.46, 0.38, 0.62, 0.50), 12), ((0, 0.70, 1, 1), 18), ((0.56, 0.47, 0.96, 0.70), 10)]),  # 밥은 먹었어? · 버거 (M 로고 · 영수증 · 쟁반 광고 글자 흐리게)
 9: (1, [((0.45, 0.66, 0.68, 1), 16)]),                                                   # 남자들끼리 · 퇴근길 핸들 (휴대폰 화면 흐리게)
 11: (7, [((0, 0.80, 1, 1), 16)]),                                                        # 당신 만날 힘만 없다면 · 광화문 해 질 녘 (사람 · 차 흐리게)
 14: (2, []),                                                                             # 마지막 장: 얼굴 아래 반
}
SHIFT = {1: 6}

def prep(i, src, regions):
    im = ImageOps.exif_transpose(Image.open(f'p48/src_{src:02d}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    im.save(f'p48/{i:02d}.jpg', quality=90)

if __name__ == '__main__':
    assert len(S.C48) == 14 and S.CAP48.count('#') == 5
    sl = []
    for i, boxes in enumerate(S.C48, 1):
        boxes = [(k, t, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, t, top, l in boxes]
        if i in PLAN:
            prep(i, *PLAN[i])
            bg = {'src': f'p48/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}
        else:
            bg = {'src': f'p48g/{i:02d}.png', 'noshade': not bright(f'p48g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        sl.append((bg, '', boxes))
    open('c48.html', 'w', encoding='utf-8').write(build(sl, no='48'))
    print('ok')
