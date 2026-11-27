# 담배 지우기(정밀) + 고급 사무실 배경(통창 너머 도시 · 월넛 벽 · 브론즈 창틀 · 라인 조명)
import numpy as np, cv2
from PIL import Image, ImageOps
im = np.asarray(ImageOps.exif_transpose(Image.open('src.jpg')).convert('RGB')).copy(); H, W = im.shape[:2]
rng = np.random.default_rng(3)
# 1) 담배만 정밀하게 지우기 (손 모양은 그대로)
x0, y0, x1, y1 = 700, 1915, 790, 2010
sub = im[y0:y1, x0:x1].astype(np.int16); hsv = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_RGB2HSV)
mk = np.zeros((H, W), np.uint8)
mk[y0:y1, x0:x1] = ((sub.mean(-1) > 70) & (hsv[..., 1] < 90)).astype(np.uint8) * 255
mk = cv2.dilate(mk, np.ones((5, 5), np.uint8))
mk[1984:2001, 744:761] = np.maximum(mk[1984:2001, 744:761], ((im[1984:2001, 744:761].mean(-1) > 55)).astype(np.uint8) * 255)
im = cv2.inpaint(im, mk, 3, cv2.INPAINT_NS)
mk2 = np.zeros((H, W), np.uint8); mk2[1980:2006, 740:766] = 255
im = cv2.inpaint(im, mk2, 6, cv2.INPAINT_TELEA); mk = np.maximum(mk, mk2)
gr = rng.normal(0, 4, im.shape) * (cv2.GaussianBlur(mk, (0, 0), 2)[..., None] / 255.)
im = np.clip(im + gr, 0, 255).astype(np.uint8)
Image.fromarray(im).crop((660, 1840, 840, 2060)).resize((540, 660)).save('hand_after.jpg')
# 2) 사람 마스크
m = np.asarray(Image.open('mask.png')).astype(np.float32) / 255.
m = np.clip((m - 0.15) / 0.7, 0, 1); m = cv2.GaussianBlur(m, (0, 0), 1.5)
# 3) 사무실 배경
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
bg = np.zeros((H, W, 3), np.float32)
wx0, wx1, wy0, wy1 = int(W * .10), int(W * .90), int(H * .07), int(H * .79)
# 월넛 벽 (세로 결)
grain = cv2.resize(rng.random((40, W // 3)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
grain = cv2.GaussianBlur(grain, (0, 0), sigmaX=1, sigmaY=40)
wood = np.array([88, 56, 36], np.float32) * (0.75 + 0.5 * grain[..., None])
bg[:] = wood * (0.55 + 0.45 * np.clip(1 - np.abs(xx - W / 2) / (W * .7), 0, 1))[..., None]
# 통창 + 도시(해 질 녘 톤 · 얕은 심도)
city = np.asarray(ImageOps.fit(ImageOps.exif_transpose(Image.open('city.jpg')).convert('RGB'), (wx1 - wx0, wy1 - wy0), Image.LANCZOS)).astype(np.float32)
city = cv2.GaussianBlur(city, (0, 0), 5)
sky = np.linspace(0, 1, wy1 - wy0)[:, None, None]
city = city * np.array([0.78, 0.82, 0.98]) * 0.72 + (1 - sky) * np.array([30, 22, 10])
bg[wy0:wy1, wx0:wx1] = city
# 창틀 (브론즈) · 세로 3칸 + 가로 1줄
bronze = np.array([62, 48, 34], np.float32)
for x in np.linspace(wx0, wx1, 4).astype(int):
    bg[wy0:wy1, max(0, x - 14):x + 14] = bronze
    bg[wy0:wy1, max(0, x - 14):x - 10] += 40
bg[wy0 + int((wy1 - wy0) * .62) - 10:wy0 + int((wy1 - wy0) * .62) + 10, wx0:wx1] = bronze
bg[wy0 - 14:wy0 + 14, wx0:wx1] = bronze; bg[wy1 - 14:wy1 + 14, wx0:wx1] = bronze
# 유리에 비친 실내 조명
for cx in (wx0 + 260, wx1 - 300):
    bg += (np.exp(-(((xx - cx) / 120) ** 2 + ((yy - wy0 - 300) / 60) ** 2)) * 0.35)[..., None] * np.array([255, 210, 150])
# 천장 · 라인 조명
bg[:wy0 - 14] = np.array([22, 18, 15]) * (0.8 + 0.2 * grain[:wy0 - 14, :, None])
for ly in (int(wy0 * .45),):
    bg += (np.exp(-((yy - ly) / 5) ** 2) * (np.abs(xx - W / 2) < W * .38))[..., None] * np.array([255, 235, 200]) * 0.9
    bg += (np.exp(-((yy - ly) / 60) ** 2) * (np.abs(xx - W / 2) < W * .40))[..., None] * np.array([120, 95, 60]) * 0.4
# 바닥: 어두운 원목 + 창 반사
fy = wy1 + 14
fl = np.array([48, 34, 25], np.float32) * (0.8 + 0.4 * cv2.GaussianBlur(cv2.resize(rng.random((W // 4, 30)).astype(np.float32), (W, H)), (0, 0), sigmaX=60, sigmaY=1)[..., None])
bg[fy:] = fl[fy:]
ref = bg[fy - 1 - np.arange(H - fy)][:, :, :]
k = (np.exp(-np.arange(H - fy) / 140.) * 0.3)[:, None, None]
bg[fy:] = bg[fy:] * (1 - k) + cv2.GaussianBlur(ref, (0, 0), 8) * k
# 비네팅
v = 1 - 0.45 * (((xx - W / 2) / (W * .8)) ** 2 + ((yy - H * .5) / (H * .85)) ** 2)
bg = np.clip(bg * np.clip(v, .3, 1)[..., None], 0, 255)
# 4) 인물: 창 역광에 맞춰 조금 밝게 + 차가운 테두리 빛, 바닥 그림자
p = im.astype(np.float32) * np.array([1.05, 1.02, 0.98]) * 1.12
edge = np.clip(m - cv2.GaussianBlur(m, (0, 0), 5), 0, 1)
p += edge[..., None] * np.array([150, 160, 175]) * 0.45
sh = cv2.GaussianBlur(m, (0, 0), 45); bg *= (1 - 0.3 * sh)[..., None]
out = np.clip(p * m[..., None] + bg * (1 - m[..., None]), 0, 255).astype(np.uint8)
Image.fromarray(out).save('office_full.jpg', quality=93)
Image.fromarray(out).resize((W // 4, H // 4)).save('office_prev.jpg')
