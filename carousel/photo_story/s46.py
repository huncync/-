# #46 「남자가 헤어지고 바로 괜찮아 보이는 이유」 (11/8) — 사진 은행(#34~#42에 쓴 사진) + 그래픽 배경 3장
# 규칙: 최근 4편(#42~#45)에 쓴 사진은 쓰지 않기 · 얼굴은 표지 · 마지막 장만
# python3 s46.py → p46g/01~14.jpg + c46.html → node .work/r46p.js
import random
from PIL import Image, ImageOps, ImageFilter, ImageDraw
from psgen import build
import stories_44_47 as S

W, H = 1080, 1350

def g_bokeh(seed, top, bot, dots):  # 밤 그라데이션 + 흐린 빛 방울
    random.seed(seed)
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    lay = Image.new('RGB', (W, H), (0, 0, 0)); ld = ImageDraw.Draw(lay)
    for _ in range(dots):
        x, y, r = random.randint(0, W), random.randint(0, int(H * 0.75)), random.randint(18, 70)
        c = random.choice([(255, 196, 120), (255, 160, 90), (150, 180, 255), (255, 220, 170)])
        ld.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v * random.uniform(.35, .7)) for v in c))
    lay = lay.filter(ImageFilter.GaussianBlur(14))
    from PIL import ImageChops
    im = ImageChops.add(im, lay)
    n = Image.effect_noise((W, H), 18).convert('RGB'); return Image.blend(im, n, .05)

def g_dawn(seed):  # 새벽 하늘 그라데이션 + 낮은 해
    im = g_bokeh(seed, (34, 40, 70), (226, 160, 132), 0); d = ImageDraw.Draw(im)
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse((W * .45, H * .62, W * 1.05, H * 1.05), fill=230)
    im.paste((255, 214, 170), (0, 0), glow.filter(ImageFilter.GaussianBlur(90)))
    return im

def g_story(seed):  # 스토리 화면처럼: 위쪽 진행 막대 + 흐린 화면
    im = g_bokeh(seed, (40, 26, 44), (12, 10, 18), 18).filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(im)
    n, gap, x0 = 6, 10, 40; w = (W - 2 * x0 - gap * (n - 1)) / n
    for i in range(n):
        x = x0 + i * (w + gap)
        d.rounded_rectangle((x, 30, x + w, 36), 3, fill=(255, 255, 255) if i < 3 else (120, 120, 130))
    d.ellipse((40, 58, 104, 122), outline=(230, 120, 160), width=4); d.ellipse((50, 68, 94, 112), fill=(90, 90, 100))
    d.rounded_rectangle((120, 76, 330, 102), 12, fill=(200, 200, 210))
    return im

# (원본 또는 그래픽, 흐리기 px, [(x0,y0,x1,y1 비율, px)])
PLAN = [
 ('p35/p07.jpg', 0, []),                                   # 1 표지: 얼굴 클로즈업
 ('p37/08.jpg', 2, []),                                    # 2 스토리엔 친구들 · 술자리 · 운동 · 밤의 빛나는 건물
 (lambda: g_bokeh(3, (22, 26, 48), (8, 8, 16), 26), 0, []),  # 3 "나만 진심이었나?" · 그래픽(밤 빛 번짐)
 ('p36/05.jpg', 0, []),                                    # 4 순서가 달라요 · 계단
 ('p34/06.jpg', 0, []),                                    # 5 한참 뒤에 아파요 · 강 위 해
 ('p34/08.jpg', 0, [((0.25, 0.45, 0.65, 1), 16)]),         # 6 일부러 바쁘게 · 밤 오토바이 (화면 흐리게)
 ('p36/12.jpg', 6, []),                                    # 7 "오늘 마시자" · 술병 (라벨 흐리게)
 ('p41/12.jpg', 0, [((0, 0.08, 0.5, 0.5), 12), ((0, 0.86, 0.45, 1), 12)]),  # 8 운동 · 일 · 친구 · 원판 (로고 흐리게)
 ('p36/13.jpg', 0, []),                                    # 9 바쁜 게 끝나는 날 · 천장 조명
 ('p36/08.jpg', 0, []),                                    # 10 미련은 늦게 와요 · 밤 골목
 (lambda: g_dawn(11), 0, []),                              # 11 이미 마음이 떠났던 경우 · 그래픽(새벽)
 (lambda: g_story(12), 0, []),                             # 12 그의 스토리는 점수가 아니에요 · 그래픽(스토리 화면)
 ('p40/04.jpg', 0, []),                                    # 13 당신 하루를 채우세요 · 산 위 풍경
 ('p35/p01.jpg', 0, [((0.70, 0.10, 0.98, 0.40), 8)]),      # 14 마지막 장: 엘리베이터 거울 셀카 (안내문 흐리게)
]
SHIFT = {1: 18, 14: 14}   # 표지 · 마지막 장: 얼굴을 비우고 상자를 아래로

def prep(i, src, blur, regions):
    if callable(src):
        im = src()
    else:
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        w, h = im.size
        for (x0, y0, x1, y1), r in regions:
            b = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
            im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(r * w / 1080)), b[:2])
        im = ImageOps.fit(im, (W, H), Image.LANCZOS)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    im.save(f'p46g/{i:02d}.jpg', quality=90)

def slides():
    out = []
    for i, ((src, blur, reg), (_, _, boxes)) in enumerate(zip(PLAN, S.C46), 1):
        prep(i, src, blur, reg)
        d = SHIFT.get(i, 0)
        bx = [(k, t, top + d if top < 80 else top, l) for k, t, top, l in boxes]
        out.append(({'src': f'p46g/{i:02d}.jpg', 'style': 'inset:0;width:100%;height:100%;object-fit:cover'}, '', bx))
    return out

if __name__ == '__main__':
    open('c46.html', 'w', encoding='utf-8').write(build(slides(), no='46'))
    print('ok')
