# #81 그래픽 6장 (11/26 · R10 시험작) — 카톡 화면(그가 한 말 · 남자들 단톡) + 필름 무드(숫자 · 정리) · gfx67_70b.py와 같은 방식
# python3 gfx81.py → node style_samples/render.js gfx81.html gfx81_out → 아래 __main__이 p76g ~ p80g로 복사(--copy)
import os, sys, json, shutil, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('mk', os.path.join(D, 'style_samples', 'make.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
kt, film = mk.kt, mk.film
H, M = 'him', 'me'
G = [
 (81, 2, film('“ ”', '', 'NOT ANGER')),
 (81, 4, kt('그 사람', [(M, '나 그 얘기 진짜 서운했어', '오후 11:20'), (H, '울지 말고 말로 해', '오후 11:21')])),
 (81, 6, kt('그 사람', [(H, '알았어 내가 다 잘못했어', '오후 11:34'), (H, '그만 울어', '오후 11:34')])),
 (81, 8, kt('남자들 단톡 (4)', [(H, '여친 울면', '오전 1:05'), (H, '진짜 아무것도 못 하겠더라', '오전 1:05')])),
 (81, 10, kt('그 사람', [(M, '화난 거 아니야', '오후 11:40'), (M, '이 얘기가 나한테 중요해서 그래', '오후 11:40')])),
 (81, 12, kt('그 사람', [(H, '천천히 말해', '오후 11:42'), (H, '다 들을게', '오후 11:42')])),
]
if __name__ == '__main__':
    if '--copy' in sys.argv:
        order = json.load(open(os.path.join(D, 'gfx81.json')))
        for k, (n, s) in enumerate(order, 1):
            os.makedirs(os.path.join(D, f'p{n}g'), exist_ok=True)
            shutil.copy(os.path.join(D, f'gfx81_out/{k:02d}.png'), os.path.join(D, f'p{n}g/{s:02d}.png'))
        print('copied', len(order)); sys.exit()
    html = mk.BASE.replace('<head>', '<head>' + mk.FONT, 1) if '<head>' in mk.BASE else mk.FONT + mk.BASE
    open(os.path.join(D, 'gfx81.html'), 'w', encoding='utf-8').write(html + mk.CSS + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open(os.path.join(D, 'gfx81.json'), 'w'))
    print('ok', len(G))
