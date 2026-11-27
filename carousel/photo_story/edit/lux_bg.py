import numpy as np, cv2
from PIL import Image, ImageOps, ImageFilter
im = np.asarray(ImageOps.exif_transpose(Image.open('src.jpg')).convert('RGB')).copy(); H, W = im.shape[:2]
# 1) 담배 지우기: 손 주변의 밝은 흰 막대만 골라 주변으로 채우기
x0, y0, x1, y1 = 700, 1925, 785, 2005
g = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
cig = np.zeros((H, W), np.uint8)
roi = g[y0:y1, x0:x1]; hsv = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_RGB2HSV)
cig[y0:y1, x0:x1] = ((roi > 95) & (hsv[..., 1] < 70)).astype(np.uint8) * 255
cig = cv2.dilate(cig, np.ones((7, 7), np.uint8))
cig[1928:1970, 744:772] = 255; cig[1976:2005, 738:768] = 255
im = cv2.inpaint(im, cig, 9, cv2.INPAINT_TELEA)
Image.fromarray(im).crop((670, 1855, 870, 2075)).resize((600, 660)).save('cig_after.jpg')
# 2) 사람 마스크
m = np.asarray(Image.open('mask.png')).astype(np.float32) / 255.
m = np.clip((m - 0.15) / 0.7, 0, 1); m = cv2.GaussianBlur(m, (0, 0), 1.5)
# 3) 고급 배경: 어두운 월넛 · 블랙 마블 벽, 금빛 라인 조명, 다운라이트, 광택 바닥
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def noise(scale, oct=5):
    n = np.zeros((H, W), np.float32); a = 1.
    for o in range(oct):
        s = max(2, int(scale * 2 ** o))
        r = rng.random((s, int(s * W / H) + 2)).astype(np.float32)
        n += a * cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC); a *= .5
    return n / n.max()
base = np.stack([np.full((H, W), c, np.float32) for c in (26, 20, 16)], -1)
vert = (1 - yy / H * 0.45)[..., None]; bg = base * vert
# 마블 결
n = noise(3); vein = np.abs(np.sin((xx * 0.004 + yy * 0.0015 + n * 6.0) * np.pi))
vein = np.clip(1 - vein / 0.035, 0, 1) ** 2 * (noise(6) > 0.45)
bg += vein[..., None] * np.array([70, 58, 44], np.float32) * 0.3
bg += (noise(40, 2)[..., None] - .5) * 6
floor_y = int(H * 0.80)
# 벽 패널 금빛 세로 라인 (좌 · 우)
for cx in (int(W * 0.17), int(W * 0.83)):
    d = np.abs(xx - cx); glow = np.exp(-(d / 60) ** 2) * 0.55 + np.exp(-(d / 6) ** 2) * 1.6
    fade = np.clip((floor_y - yy) / 300, 0, 1) * np.clip(yy / 200, 0, 1)
    bg += (glow * fade)[..., None] * np.array([235, 180, 95], np.float32) * 0.55
# 다운라이트 · 벽에 떨어지는 빛
for cx in (int(W * 0.30), int(W * 0.5), int(W * 0.70)):
    cone = np.exp(-((xx - cx) / (90 + (yy) * 0.12)) ** 2) * np.exp(-((yy - 120) / 900) ** 2) * (yy > 60)
    bg += cone[..., None] * np.array([255, 205, 140], np.float32) * 0.35
    spot = np.exp(-(((xx - cx) / 26) ** 2 + ((yy - 70) / 10) ** 2))
    bg += spot[..., None] * np.array([255, 235, 200], np.float32) * 2.2
# 천장 몰딩 선
bg[70:74] += np.array([80, 62, 40], np.float32) * 0.6
# 바닥: 광택 블랙 마블 + 반사
fl = yy >= floor_y
bg[fl] = bg[fl] * 0.55 + np.array([10, 8, 7], np.float32)
bg[floor_y:floor_y + 3] += np.array([150, 115, 70], np.float32)
refl = bg[floor_y - (np.arange(H - floor_y) * 1) - 1][::1]
k = np.exp(-np.arange(H - floor_y) / 180.)[:, None, None]
bg[floor_y:] = bg[floor_y:] * (1 - 0.35 * k) + refl * 0.35 * k
# 비네팅
v = 1 - 0.55 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.55) / (H * 0.8)) ** 2)
bg *= np.clip(v, 0.25, 1)[..., None]
bg = np.clip(bg, 0, 255)
# 4) 사람 색을 배경에 맞춰 살짝 따뜻하게 + 금빛 테두리 빛
p = im.astype(np.float32); p = p * np.array([1.06, 1.0, 0.92]) * 1.04
edge = np.clip(m - cv2.GaussianBlur(m, (0, 0), 6), 0, 1)
p += edge[..., None] * np.array([120, 90, 50], np.float32) * 0.5
# 사람 뒤 은은한 그림자
sh = cv2.GaussianBlur(m, (0, 0), 40); bg *= (1 - 0.35 * sh)[..., None]
out = p * m[..., None] + bg * (1 - m[..., None])
out = np.clip(out, 0, 255).astype(np.uint8)
Image.fromarray(out).save('lux_full.jpg', quality=93)
Image.fromarray(out).resize((W // 4, H // 4)).save('lux_prev.jpg')
