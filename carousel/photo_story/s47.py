# #47 글 상자 + 그래픽 배경 (p47g) → c47.html → node .work/r47p.js
from psgen import build
from s48_50 import bright
import stories_44_47 as S

if __name__ == '__main__':
    sl = [({'src': f'p47g/{i:02d}.png', 'noshade': not bright(f'p47g/{i:02d}.png'), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}, '', b[2]) for i, b in enumerate(S.C47, 1)]
    open('c47.html', 'w', encoding='utf-8').write(build(sl, no='47'))
    print('ok')
