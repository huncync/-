# #39 「이별 통보 받은 날 밤, 남자 머릿속」 (11/2) — 이미 쓴 사진을 다시 편집해서 "완전 다른 사진"으로
# 사진 스카우트 2명이 p34~p38에서 디테일 자리를 찾고(크게 자르기), grade.py로 밤 톤 · 흑백 · 따뜻한 밤 + 그레인 + 비네팅
# 영상 장 3개: 5장(현관 앞 발걸음 영상) · 7장(천장 조명 천천히 확대) · 13장(지는 해 천천히 확대)
# python3 s39.py → p39/*.jpg + c39.html → node .work/r39.js (글 상자 렌더) → python3 s39.py video (영상 합성)
import sys
from psgen import build
from grade import crop, kenburns, clip
import ps01

# (원본, 자르기 x,y,w,h, 톤, 옵션)
PLAN = [
 ('p34/07.jpg', (450, 800, 960, 1200), 'night', {}),                     # 1 표지: 오토바이 사이드미러 셀카 (휴대폰으로 얼굴 반)
 ('p38/04.jpg', (1032, 1360, 900, 1125), 'night', {'blur': 3}),          # 2 컵홀더의 캔 (글자 흐리게)
 ('p36/12.jpg', (600, 300, 900, 1125), 'warm-night', {'blur': 3}),       # 3 술병들 (라벨 흐리게)
 ('p34/12.jpg', (200, 430, 960, 1200), 'bw', {}),                        # 4 쉬어가는 장: 재킷 지퍼
 ('VIDEO', 'p35/v1.mov', 2.4, 2.4, (216, 840, 864, 1080), 'night'),       # 5 영상: 유리문 앞에 멈추는 발
 ('p34/08.jpg', (500, 1376, 960, 1200), 'night', {'blur_from': 0.55}),   # 6 핸들 거치대의 휴대폰 (화면 흐리게)
 ('KB', 'p36/13.jpg', (330, 252, 900, 1125), 'night'),                    # 7 영상: 천장 조명 천천히 확대
 ('p34/09.jpg', (300, 0, 960, 1200), 'night', {'blur_from': 0.85}),      # 8 새벽 하늘 (아래 간판 흐리게)
 ('p35/p02.jpg', (0, 200, 1000, 1250), 'night', {}),                     # 9 운전석에서 본 앞 유리 · 0 km/h
 ('p34/07.jpg', (972, 700, 960, 1200), 'night', {'blur': 2}),            # 10 강변 산책길
 ('p36/02.jpg', (600, 900, 960, 1200), 'bw', {}),                        # 11 지하철 문턱을 넘는 신발
 ('p38/12.jpg', (0, 0, 900, 1125), 'warm-night', {'blur': 1.5}),         # 12 카페 테이블 위 잔 하나
 ('KB', 'p34/06.jpg', (880, 0, 960, 1200), 'warm-night'),                 # 13 영상: 지는 해 천천히 확대
 ('p34/13.jpg', (300, 360, 960, 1200), 'night', {}),                     # 14 엘리베이터 거울 셀카 (얼굴)
]
VIDS = [5, 7, 13]

def boxes():
    out = []
    for i, (_, _, bx) in enumerate(ps01.SLIDES, 1):
        bx = list(bx)
        if i == 14:  # 얼굴(56~78%)에 안 닿게 위 상자 3개를 조금 위로
            bx = [(k, t, top - 6 if top < 80 else top, l) for k, t, top, l in bx]
        out.append(bx)
    return out

def stills():
    for i, row in enumerate(PLAN, 1):
        if row[0] == 'VIDEO': continue
        if row[0] == 'KB':  # 2배 크기로 뽑아서 확대해도 선명하게
            _, src, box, mode = row
            crop(src, box, mode, f'p39/kb_{i:02d}.jpg', size=(2160, 2700))
            continue
        src, box, mode, opt = row
        crop(src, box, mode, f'p39/{i:02d}.jpg', **opt)

def slides():
    out = []
    for i, bx in enumerate(boxes(), 1):
        if i in VIDS: bg = {'video': True}
        else: bg = {'src': f'p39/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
        out.append((bg, '', bx))
    return out

def videos():
    for i in VIDS:
        row = PLAN[i - 1]; ov = f'p39/ov_{i:02d}.png'
        out_mp4, out_jpg = f'../c39_slide_{i:02d}.mp4', f'../c39_slide_{i:02d}.png'
        if row[0] == 'VIDEO':
            _, src, start, dur, box, mode = row
            clip(src, ov, out_mp4, out_jpg, start, dur, box, mode)
        else:
            kenburns(f'p39/kb_{i:02d}.jpg', ov, out_mp4, out_jpg, dur=5.0, z1=1.12)

if __name__ == '__main__':
    if sys.argv[1:] == ['video']:
        videos(); print('video ok')
    else:
        stills()
        open('c39.html', 'w', encoding='utf-8').write(build(slides(), no='39'))
        print('ok', len(PLAN))
