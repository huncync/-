# #39 편집 도구 (11/2) — 이미 쓴 사진을 "다른 사진"으로: 디테일 크게 자르기 + 밤 톤 / 흑백 / 따뜻한 밤 + 필름 그레인 + 비네팅
# crop(src, (x,y,w,h), mode, out, blur=0) → 1080×1350 JPG / kenburns(jpg2x, out_mp4, dur, z0, z1) → 천천히 확대되는 영상
import random, subprocess
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops

def _vignette(im, k=0.55):
    w, h = im.size
    m = Image.radial_gradient('L').resize((w, h)).point(lambda v: 255 - int(v * k))
    return Image.composite(im, Image.new('RGB', im.size, (0, 0, 0)), m)

def _grain(im, amt=10, seed=7):
    random.seed(seed)
    w, h = im.size
    n = Image.effect_noise((w // 2, h // 2), amt).resize((w, h)).convert('RGB')
    return ImageChops.add(ImageChops.subtract(im, Image.new('RGB', im.size, (amt, amt, amt))), n.point(lambda v: v * 2 * amt // 255 if amt else 0))

def grade(im, mode):
    im = im.convert('RGB')
    if mode == 'bw':
        g = ImageOps.grayscale(im)
        g = ImageEnhance.Contrast(g).enhance(1.18)
        g = ImageEnhance.Brightness(g).enhance(0.82)
        im = Image.merge('RGB', (g, g, g))
    else:
        im = ImageEnhance.Color(im).enhance(0.35 if mode == 'night' else 0.55)
        im = ImageEnhance.Brightness(im).enhance(0.74 if mode == 'night' else 0.78)
        r, g, b = im.split()
        mul = (0.86, 0.96, 1.12) if mode == 'night' else (1.10, 0.96, 0.80)
        r, g, b = [c.point(lambda v, m=m: min(255, int(v * m) + 6)) for c, m in zip((r, g, b), mul)]
        im = Image.merge('RGB', (r, g, b))
        im = ImageEnhance.Contrast(im).enhance(1.06)
    im = _vignette(im)
    return _grain(im, 9)

def crop(src, box, mode, out, blur=0, size=(1080, 1350), flip=False):
    im = ImageOps.exif_transpose(Image.open(src))
    x, y, w, h = box
    im = im.crop((x, y, x + w, y + h))
    if flip: im = ImageOps.mirror(im)
    im = im.resize(size, Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im = grade(im, mode).filter(ImageFilter.UnsharpMask(2, 40, 3))
    im.save(out, quality=92)
    return out

def kenburns(src2x, overlay_png, out_mp4, out_jpg, dur=5.0, z1=1.12, fps=30):
    n = int(dur * fps)
    vf = (f"[0:v]scale=2160:2700,zoompan=z='1+({z1}-1)*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1350:fps={fps}[v];"
          f"[v][1:v]overlay=0:0,format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', src2x, '-i', overlay_png, '-filter_complex', vf,
                    '-t', str(dur), '-an', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-movflags', '+faststart', out_mp4], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1', '-i', out_mp4, '-frames:v', '1', '-q:v', '3', out_jpg], check=True)

def clip(src, overlay_png, out_mp4, out_jpg, start, dur, box, mode='night'):
    x, y, w, h = box
    eq = 'eq=saturation=0.35:brightness=-0.10:contrast=1.05,colorchannelmixer=rr=0.88:gg=0.96:bb=1.12' if mode == 'night' else \
         'hue=s=0,eq=brightness=-0.08:contrast=1.15'
    vf = (f"[0:v]crop={w}:{h}:{x}:{y},scale=1080:1350,{eq},noise=alls=12:allf=t,vignette=PI/4[v];[v][1:v]overlay=0:0,format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', src, '-i', overlay_png, '-filter_complex', vf,
                    '-an', '-r', '30', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-movflags', '+faststart', out_mp4], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(min(1.0, dur / 2)), '-i', out_mp4, '-frames:v', '1', '-q:v', '3', out_jpg], check=True)
