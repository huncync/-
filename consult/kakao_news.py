# 카톡 채널 소식용 (11/2) — 긴 안내문 · 신청서 · 결과물 이미지를 폰 화면 4:5(1080×1350)로 나눠요. 글줄 사이 빈 곳에서 자르기
# python3 kakao_news.py (kakao_docs.py → rdocs.js로 kakao_menu/doc_*.jpg를 먼저 만든 뒤)
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os
D = os.path.dirname(os.path.abspath(__file__))
BG = (0xf4, 0xee, 0xe3); LINE = (0xcd, 0xb6, 0x8a); INK = (0x7a, 0x70, 0x64)
W, H, TOP, BOT = 1080, 1350, 64, 96
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)

def page(sl, label):
    pg = Image.new('RGB', (W, H), BG); pg.paste(sl, ((W - sl.width) // 2, TOP))
    d = ImageDraw.Draw(pg)
    d.rectangle((0, TOP + sl.height, W, H), fill=BG)
    d.rounded_rectangle((24, 24, W - 25, H - 25), radius=6, outline=LINE, width=2)
    if label: d.text((W / 2, H - 58), label, fill=INK, font=FONT, anchor='mm')
    return pg

def split(name, out, fit_one=False):
    im = Image.open(f'{D}/kakao_menu/{name}.jpg').convert('RGB')
    body = im.crop((0, 40, W, im.height - 40)); maxh = H - TOP - BOT
    if fit_one:
        s = maxh / body.height
        page(body.resize((int(W * s), maxh), Image.LANCZOS), '').save(f'{D}/kakao_news/{out}_1.jpg', quality=90); return 1
    a = np.asarray(body).astype(int)[:, 80:1000]
    blank = np.abs(a - np.array(BG)).max(axis=2).max(axis=1) < 18
    cuts, y = [0], 0
    while body.height - y > maxh:  # 남은 범위 안에서 가장 긴 빈 줄 묶음(섹션 사이)에서 자르기
        best, run, c = (0, y + maxh), 0, y + 600
        for r in range(y + 600, y + maxh):
            run = run + 1 if blank[r] else 0
            if run >= best[0]: best = (run, r - run // 2)
        c = best[1]
        cuts.append(c); y = c
    cuts.append(body.height); n = len(cuts) - 1
    for p in range(n):
        page(body.crop((0, cuts[p], W, cuts[p + 1])), f'{p + 1} / {n}').save(f'{D}/kakao_news/{out}_{p + 1}.jpg', quality=90)
    return n

if __name__ == '__main__':
    os.makedirs(f'{D}/kakao_news', exist_ok=True)
    for f in os.listdir(f'{D}/kakao_news'): os.remove(f'{D}/kakao_news/{f}')
    print(split('doc_guide', 'guide'), split('doc_report', 'report', fit_one=True), split('doc_form', 'form'))
