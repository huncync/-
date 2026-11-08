# 스토리용 9:16 (1080×1920): 피드 4:5 장을 초록 배경 가운데에 · 위 제목줄 · 아래 안내(마지막 장은 링크 스티커 자리)
from PIL import Image, ImageDraw, ImageFont
import glob, os
D = os.path.dirname(os.path.abspath(__file__)) + '/sample/'
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fs = sorted(glob.glob(D + 'feed_*.png')); n = len(fs)
for i, f in enumerate(fs, 1):
    bg = Image.new('RGB', (1080, 1920), (46, 91, 78)); d = ImageDraw.Draw(bg)
    card = Image.open(f).convert('RGB').resize((960, 1200), Image.LANCZOS)
    bg.paste(card, (60, 330))
    d.text((540, 230), f'남자심리 처방전 · {i}/{n}', fill=(231, 242, 235), font=ImageFont.truetype(F, 46), anchor='mm')
    tail = '카카오채널 링크 스티커 자리' if i == n else '탭해서 다음 →'
    d.text((540, 1650), tail, fill=(255, 231, 168), font=ImageFont.truetype(F, 40), anchor='mm')
    if i == n: d.rounded_rectangle((300, 1700, 780, 1800), 50, outline=(255, 231, 168), width=3)
    bg.save(D + f'story_{i:02d}.jpg', quality=92)
print('ok', n)
