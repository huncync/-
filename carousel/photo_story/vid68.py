# #68 표지 · 마지막 장을 영상으로 (11/22 지훈님 요청: 캡처 말고 영상)
# python3 s66_70.py → node render66.js c68 → node render_ov.js c68 1 14 → python3 vid68.py
import vidgen
SRC = 'p68n/IMG_3236.mov'
EQ = 'saturation=0.85:brightness=-0.03'  # 얼굴 장은 색을 덜 빼요 (사진 장 VIVID와 같은 톤)
for n, yoff in ((1, 140), (14, 134)):
    vidgen.make(SRC, f'p68/ov_{n:02d}.png', f'../c68_slide_{n:02d}.mp4', f'../c68_slide_{n:02d}.png', start=0.0, dur=3.8, yoff=yoff, eq=EQ)
    print('mp4', n)
