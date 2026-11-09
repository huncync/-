# #49~#51 글 상자 + 그래픽 배경 (p49g · p50g · p51g) → c49.html ~ c51.html → node render48.js c49 c50 c51 (11/9 번호 한 칸씩 밀림 · 파일 이름은 그대로)
from psgen import build
from PIL import Image, ImageStat

def bright(path):  # 아래 글자줄 자리가 밝으면 그림자(shade)를 깔아 @mszexc · 시리즈 번호가 읽히게
    im = Image.open(path).convert('L'); w, h = im.size
    return ImageStat.Stat(im.crop((0, int(h * .9), w, h))).mean[0] > 110
import stories_49_51 as S

if __name__ == '__main__':
    for k, (t, c, cap, pin) in S.DATA.items():
        assert len(c) == 14 and cap.count('#') == 5, k
        sl = [({'src': f'p{k}g/{i:02d}.png', 'noshade': not bright(f'p{k}g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}, '', b) for i, b in enumerate(c, 1)]
        open(f'c{k}.html', 'w', encoding='utf-8').write(build(sl, no=k))
    print('ok')
