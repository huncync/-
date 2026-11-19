# #64 · #65 글 상자 + 배경 (11/16) — 지훈님 사진 8장(보관함 · 표지와 마지막 장은 얼굴) + 그래픽 6장 · 모자이크 없음(11/16 결정)
# python3 gfx64_65.py → node render64.js gfx → python3 s64_65.py → node render64.js c64 c65
import os
from PIL import Image, ImageOps
from psgen import build
from s48_50 import bright
import stories_64_65 as S

# 장 → ('폴더/src_NN', 자르기 또는 None)
PLAN = {
 '64': {1: ('p64n/src_01', (0.0, 0.12, 1.0, 1.0)),   # 11/19 새 사진 · 헬스장 거울 셀카 (표지)
        3: ('p64n/src_02', None),   # "괜찮아." · 쌓인 원판
        5: ('p64n/src_03', None),   # "응, 알았어." · 고글 달린 모자
        7: ('p64n/src_05', None),   # "요즘 좀 바빠." · 오토바이 핸들
        9: ('p64n/src_06', None),   # 말하는 법을 모르는 거예요 · 노란 은행나무
        11: ('p64n/src_04', None),  # "내가 뭐 서운하게 했어?" · 파란 하늘과 빌딩
        13: ('p44/src_07', None),   # 남자친구에게는 이렇게 · 나무 (보관함)
        14: ('p64n/src_01', (0.15, 0.22, 0.90, 0.90))},   # 마지막 장 · 같은 셀카 가까이
 '65': {1: ('p65n/src_01', (0.12, 0.22, 1.0, 1.0)),   # 11/19 새 사진 · 엘리베이터 거울 셀카 (표지)
        3: ('p65n/src_04', None),   # "우리 천천히 하자." · 한강 노을
        5: ('p65n/src_02', None),   # "나중에 얘기하자." · 꺼진 모니터
        7: ('p65n/src_06', None),   # "너 같은 사람 없어." · 향수병과 워크북
        9: ('p65n/src_03', None),   # 확신 있는 남자는 날짜를 말해요 · 파란 하늘과 나무
        11: ('p65n/src_05', None),  # "우리 지금 어디쯤이야?" · 세워 둔 오토바이
        13: ('p65n/src_07', (0.0, 0.28, 1.0, 1.0)),   # 다음 약속이 잡히는지 · 줄지은 향료 병 (위 명찰은 잘라냄)
        14: ('p65n/src_01', (0.32, 0.33, 0.95, 0.95))},   # 마지막 장 · 같은 셀카 가까이
}
SHIFT = {1: 6}
SHIFT14 = {'64': 22, '65': 22}
VIVID = {('64', 9), ('64', 11), ('64', 13), ('65', 3), ('65', 9)}

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
