# #61 ~ #63 글 상자 + 배경 (11/15) — 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장(p61g ~ p63g)
# python3 gfx61_63.py → node render61.js gfx → python3 s61_63.py → node render61.js c61 c62 c63
import os
from PIL import Image, ImageOps, ImageFilter
from psgen import build
from s48_50 import bright
import stories_61_63 as S

# 장 → ('폴더/src_NN', [(x0,y0,x1,y1 비율, 흐리기 px)], 자르기 또는 없음)
PLAN = {
 '61': {1: ('p61n/src_01', [], (0.12, 0.22, 0.92, 0.82)),   # 11/17 새 사진 · 검은 타일 거울 셀카 (담배만 지움 · 재떨이는 잘라냄)
        3: ('p61n/src_02', []),    # 고마운 일엔 아무 말도 · 맥주 캔과 먹다 남은 김밥
        5: ('p61n/src_04', []),    # 지난 일을 다시 꺼내세요 · 기린 맥주병
        7: ('p61n/src_05', []),    # "됐어, 말하기 싫어" · 걸어가는 뒷모습 (영상 IMG_1029에서)
        9: ('p61n/src_06', []),    # 떠나기로 정하면 착해져요 · 밤 활주로, 비행기로 걸어가는 사람들 (영상 IMG_1045)
        11: ('p61n/src_03', []),   # "오늘 데리러 와줘서 고마워" · 초록불 횡단보도
        13: ('p61n/src_07', []),   # 쌓인 날들 · 비행기 엔진 (영상 IMG_1048)
        14: ('p61n/src_01', [], (0.25, 0.30, 0.80, 0.82))},   # 마지막 장 · 같은 셀카 가까이
 '62': {1: ('p62n/src_01', [], (0.0, 0.15, 1.0, 1.0)),   # 11/18 새 사진 · 엘리베이터 거울 셀카 (표지)
        3: ('p40/src_12', []),                                    # 마음이 어디쯤인지 · 바다
        5: ('p39/src_13', [((0, 0.84, 1, 1), 14)]),               # "좋은 애였어" · 밤 전봇대 (아래 간판 흐리게)
        7: ('p47/src_09', []),                                    # "아무렇지도 않아" · 벽돌담과 나무
        9: ('p41/src_02', []),                                    # 친구들은 다 알아요 · 노란 연석 그림자
        11: ('p43/src_04', []),                                   # 연락할 이유로 삼지 마세요 · 하늘과 건물
        13: ('p49/src_06', []),                                   # 친구 앞에서 나와요 · 파란 하늘
        14: ('p62n/src_01', [], (0.05, 0.25, 0.80, 0.90))},   # 마지막 장 · 같은 셀카 가까이 (11/18)
 '63': {1: ('p55s/src_01', [((0.74, 0.26, 0.90, 0.46), 14), ((0.73, 0.44, 0.89, 0.58), 14)], (0.08, 0.12, 0.96, 1.0)),  # 표지 · 엘리베이터 셀카 (안내 스티커 흐리게 · #60 표지와 겹치지 않게)
        3: ('p44/src_06', []),                                    # 남자들끼리는 · 거울 속 휴대폰
        5: ('p51/src_04', []),                                    # 저장 이름이 애매해요 · 동그란 벽 조명
        7: ('p40/src_14', [((0.12, 0.47, 0.90, 0.82), 16), ((0.35, 0.25, 0.75, 0.45), 12)]),  # 셋이 겹치면 · 카페 노트북 (화면 · 손님 흐리게)
        9: ('p47/src_04', []),                                    # 먼저 말해 주는 남자 · 하얀 조명
        11: ('p39/src_11', []),                                   # 이렇게 물어보세요 · 펜던트 조명
        13: ('p44/src_04', []),                                   # 그 남자의 태도 · 하늘
        14: ('p42/src_01', [], (0.15, 0.15, 0.90, 0.95))},        # 마지막 장 · 거울 셀카
}

# 11/16 지훈님 결정: 모자이크(흐리기) 하지 않기 → 아래에서 흐리기 목록을 비워요
PLAN = {k: {i: (v[0], [], *v[2:]) for i, v in p.items()} for k, p in PLAN.items()}
SHIFT = {1: 6}
SHIFT14 = {'61': 22, '62': 22, '63': 22}
VIVID = {('61', 9), ('62', 3), ('62', 13), ('63', 13)}

def prep(no, i, src, regions, crop=None):
    im = ImageOps.exif_transpose(Image.open(f'{src}.jpg')).convert('RGB')
    w, h = im.size
    for reg in regions:
        (x0, y0, x1, y1), r = reg[:2]
        b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        bl = im.filter(ImageFilter.GaussianBlur(r * w / 1080))
        m = Image.new('L', im.size, 0); m.paste(255, b); m = m.filter(ImageFilter.GaussianBlur(int(0.01 * w)))  # 가장자리 부드럽게
        im = Image.composite(bl, im, m)
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
