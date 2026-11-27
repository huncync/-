# 거울에 붙은 글자(가게 이름)를 획만 골라 지워요 — 흐리기로 하면 머리까지 뿌옇게 번져서
# python3 clean_logo.py 원본.jpg 결과.jpg x0 y0 x1 y1   (비율)
import sys, cv2, numpy as np
from PIL import Image, ImageOps, ImageFilter
src, dst = sys.argv[1:3]; fx0, fy0, fx1, fy1 = map(float, sys.argv[3:7])
im = np.array(ImageOps.exif_transpose(Image.open(src)).convert('RGB'))
h, w = im.shape[:2]
x0, y0, x1, y1 = int(fx0 * w), int(fy0 * h), int(fx1 * w), int(fy1 * h)
roi = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)[y0:y1, x0:x1]
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
m = ((cv2.morphologyEx(roi, cv2.MORPH_BLACKHAT, k) > 16) | (cv2.morphologyEx(roi, cv2.MORPH_TOPHAT, k) > 16)).astype(np.uint8) * 255
m = cv2.dilate(m, np.ones((7, 7), np.uint8))
mask = np.zeros((h, w), np.uint8); mask[y0:y1, x0:x1] = m
out = cv2.inpaint(cv2.cvtColor(im, cv2.COLOR_RGB2BGR), mask, 7, cv2.INPAINT_TELEA)
o = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
soft = Image.fromarray(cv2.GaussianBlur(mask, (0, 0), 6))   # 지운 자리만 살짝 더 부드럽게
o = Image.composite(o.filter(ImageFilter.GaussianBlur(4)), o, soft)
o.save(dst, quality=95)
