# #50 「남자친구의 "좋아요", 넘기면 안 되는 3가지」 (11/10) — 지훈님 사진 7장 + 그래픽 7장(p50g 그대로)
# python3 s50.py → node render48.js c50
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_49_51 as S

# 장 → (사진 번호, [(x0,y0,x1,y1 비율, 흐리기 px)])  · 나머지 장은 그래픽(p50g)
PLAN = {
 1: (1, [((0.26, 0.10, 0.62, 0.20), 14)]),                                   # 표지: 헬스장 벤치 거울 셀카 (간판 흐리게)
 3: (4, []),                                                                 # 좋아요는 대부분 생각 없이 · 걷는 발
 5: (7, []),                                                                 # 그냥 넘기면 안 돼요 · 뿌연 유리
 9: (3, []),                                                                 # 남자들끼리 · WE ARE
 11: (2, []),                                                                # "신경 쓰였어" · TOGETHER
 12: (6, [((0.06, 0.88, 0.40, 1), 12)]),                                     # 미안 하는 남자는 괜찮아요 · STRONGER (원판 로고 흐리게)
 14: (5, []),                                                                # 마지막 장: 거울 셀카
}
SHIFT = {1: 6, 14: 22}  # 마지막 장: 글 상자를 얼굴 아래로
VIVID = set()  # 실내 사진이라 기본 필터 그대로

def prep(i, src, regions):
    im = ImageOps.exif_transpose(Image.open(f'p50/src_{src:02d}.jpg')).convert('RGB')
    w, h = im.size
    for (x0, y0, x1, y1), r in regions:
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    im.save(f'p50/{i:02d}.jpg', quality=90)

if __name__ == '__main__':
    t, c, cap, pin = S.DATA['50']
    assert len(c) == 14 and cap.count('#') == 5
    sl = []
    for i, boxes in enumerate(c, 1):
        boxes = [(k, x, top + SHIFT.get(i, 0) if top < 80 else top, l) for k, x, top, l in boxes]
        if i in PLAN:
            prep(i, *PLAN[i])
            bg = {'src': f'p50/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover' + (';filter:saturate(.85) brightness(.9)' if i in VIVID else '')}
        else:
            bg = {'src': f'p50g/{i:02d}.png', 'noshade': not bright(f'p50g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        sl.append((bg, '', boxes))
    open('c50.html', 'w', encoding='utf-8').write(build(sl, no='50'))
    print('ok')
