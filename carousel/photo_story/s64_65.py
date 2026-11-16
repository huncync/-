# #64 · #65 글 상자 + 배경 (11/16) — 지훈님 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장 · 모자이크 없음(11/16 결정)
# python3 gfx64_65.py → node render64.js gfx → python3 s64_65.py → node render64.js c64 c65
import os
from PIL import Image, ImageOps
from psgen import build
from s48_50 import bright
import stories_64_65 as S

# 장 → ('폴더/src_NN', 자르기 또는 None)
PLAN = {
 '64': {1: ('p50/src_01', (0.05, 0.08, 0.95, 0.80)),   # 표지 · 앉아서 찍은 거울 셀카
        3: ('p51/src_05', None),    # "괜찮아." · 빈 의자
        5: ('p47/src_08', None),    # "응, 알았어." · 그림자
        7: ('p39/src_06', None),    # "요즘 좀 바빠." · 긴 복도
        9: ('p45/src_09', None),    # 말하는 법을 모르는 거예요 · 노란 나무
        11: ('p51/src_07', None),   # "내가 뭐 서운하게 했어?" · 선반 액자
        13: ('p44/src_07', None),   # 남자친구에게는 이렇게 · 나무
        14: ('p50/src_01', (0.15, 0.10, 0.85, 0.55))},   # 마지막 장 · 같은 셀카 가까이
 '65': {1: ('p44/src_14', (0.35, 0.25, 0.95, 0.90)),   # 표지 · 헬스장 거울 셀카
        3: ('p39/src_03', None),    # "우리 천천히 하자." · 구름 낀 하늘
        5: ('p41/src_03', None),    # "나중에 얘기하자." · 보도 위 그림자
        7: ('p42/src_13', None),    # "너 같은 사람 없어." · 바닥
        9: ('p47/src_11', None),    # 확신 있는 남자는 날짜를 말해요 · 단풍
        11: ('p49/src_05', None),   # "우리 지금 어디쯤이야?" · 나무와 건물
        13: ('p45/src_06', None),   # 다음 약속이 잡히는지 · 하늘과 건물
        14: ('p44/src_14', (0.45, 0.30, 0.82, 0.68))},   # 마지막 장 · 같은 셀카 가까이
}
SHIFT = {1: 6}
SHIFT14 = {'64': 22, '65': 22}
VIVID = {('64', 9), ('64', 13), ('65', 9), ('65', 11)}

def prep(no, i, src, crop=None):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
    if crop: im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    out = f'p{no}/{i:02d}.jpg'
    im.save(out, quality=90)
    return out

if __name__ == '__main__':
    for no, (t, c, cap, pin) in S.DATA.items():
        assert len(c) == 14 and cap.count('#') == 5, no
        os.makedirs(f'p{no}', exist_ok=True)
        sl = []
        for i, boxes in enumerate(c, 1):
            sh = SHIFT14.get(no, 0) if i == 14 else SHIFT.get(i, 0)
            boxes = [(k, x, top + sh if top < 80 else top, l) for k, x, top, l in boxes]
            if i in PLAN[no]:
                bg = {'src': prep(no, i, *PLAN[no][i]), 'style': 'inset:0;width:100%;height:100%;object-fit:cover' + (';filter:saturate(.85) brightness(.9)' if (no, i) in VIVID else '')}
            else:
                g = f'p{no}g/{i:02d}.png'
                bg = {'src': g, 'noshade': not bright(g), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
            sl.append((bg, '', boxes))
        open(f'c{no}.html', 'w', encoding='utf-8').write(build(sl, no=no))
    print('ok')
