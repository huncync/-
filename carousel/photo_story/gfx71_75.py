# #71 ~ #75 그래픽 6장씩 (11/23) — 카톡 화면(그가 한 말 · 남자들 단톡) + 필름 무드(숫자 · 정리) · gfx67_70b.py와 같은 방식
# python3 gfx71_75.py → node style_samples/render.js gfx71_75.html gfx71_75_out → 아래 __main__이 p71g ~ p75g로 복사(--copy)
import os, sys, json, shutil, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('mk', os.path.join(D, 'style_samples', 'make.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
kt, film = mk.kt, mk.film
H, M = 'him', 'me'
G = [
 (71, 2, film('4', '', 'LETTING GO')),
 (71, 4, kt('그 사람', [(M, '다음 달에 제주도 갈까?', '오후 9:12'), (H, '그때 봐서', '오후 10:40')])),
 (71, 6, film('02', '', 'OUT OF SIGHT')),
 (71, 8, kt('남자들 단톡 (4)', [(H, '요즘 좀 애매해', '오전 1:22'), (H, '정리해야 할 것 같아', '오전 1:22')])),
 (71, 10, film('“ ”', '', 'QUIET IS NOT PEACE')),
 (71, 12, kt('그 사람', [(M, '요즘 우리 좀 멀어진 것 같아. 너는 어때?', '오후 11:03'), (H, '아냐 그냥 피곤해서', '오전 12:41')])),
 (72, 2, film('3', '', 'BEFORE THE PHONE')),
 (72, 4, kt('그 사람', [(H, '오늘 왜 이렇게 예뻐?', '오후 7:20'), (H, '이거 너 주려고 샀어', '오후 7:21')])),
 (72, 6, kt('그 사람', [(H, '주말에 뭐 해?', '오후 2:05'), (H, '몇 시에 끝나?', '오후 2:05')])),
 (72, 8, kt('남자들 단톡 (4)', [(H, '괜히 찔려서', '오전 12:18'), (H, '더 짜증 나더라', '오전 12:18')])),
 (72, 10, film('1', '', 'NOT YET')),
 (72, 12, film('LOCK', '', 'LEAVE IT')),
 (73, 2, film('5', '', 'HOW TO LOSE IT')),
 (73, 4, kt('그 사람', [(M, '너 저번에도 그랬잖아', '오후 11:40'), (H, '...', '오후 11:52')])),
 (73, 6, kt('친구들 (3)', [(H, '헐 또 싸웠어?', '오전 12:10'), (H, '캡처 보내봐', '오전 12:10')])),
 (73, 8, kt('남자들 단톡 (4)', [(H, '싸우는 건 괜찮은데', '오전 2:15'), (H, '헤어지자는 말은 진짜 지쳐', '오전 2:15')])),
 (73, 10, film('3+', '', 'IT IS THE WAY')),
 (73, 12, kt('그 사람', [(M, '우리 화해한 거다?', '오후 10:02'), (H, '응 ㅎㅎ 화해', '오후 10:03')])),
 (74, 2, film('4', '', 'BEFORE THE RING')),
 (74, 4, kt('그 사람', [(H, '너는 아이 좋아해?', '오후 9:47')])),
 (74, 6, kt('그 사람', [(H, '너희 부모님은 어떤 분이셔?', '오후 8:31')])),
 (74, 8, kt('남자들 단톡 (4)', [(H, '이 사람이랑은', '오전 1:05'), (H, '현실 얘기도 해 보고 싶더라', '오전 1:05')])),
 (74, 10, film('2+', '', 'HE SEES TOMORROW')),
 (74, 12, kt('그 사람', [(M, '나는 이렇게 생각해. 너는?', '오후 10:20'), (H, '나도 비슷해. 좀 더 얘기해 보자', '오후 10:22')])),
 (75, 2, film('12.24', '', 'DECEMBER')),
 (75, 4, kt('그 사람', [(H, '잘 지내?', '오후 11:48'), (H, '거리에 트리 보니까 생각나서', '오후 11:48')])),
 (75, 6, film('LAST', '', 'CHRISTMAS')),
 (75, 8, kt('남자들 단톡 (4)', [(H, '올해 넘기기 전에', '오전 1:30'), (H, '연락 한 번은 해 볼까', '오전 1:30')])),
 (75, 10, kt('그 사람', [(H, '한번 볼래?', '오후 8:14'), (H, '다음 주 토요일 어때?', '오후 8:15')])),
 (75, 12, film('12.26', '', 'THE DAY AFTER')),
]
if __name__ == '__main__':
    if '--copy' in sys.argv:
        order = json.load(open(os.path.join(D, 'gfx71_75.json')))
        for k, (n, s) in enumerate(order, 1):
            os.makedirs(os.path.join(D, f'p{n}g'), exist_ok=True)
            shutil.copy(os.path.join(D, f'gfx71_75_out/{k:02d}.png'), os.path.join(D, f'p{n}g/{s:02d}.png'))
        print('copied', len(order)); sys.exit()
    html = mk.BASE.replace('<head>', '<head>' + mk.FONT, 1) if '<head>' in mk.BASE else mk.FONT + mk.BASE
    open(os.path.join(D, 'gfx71_75.html'), 'w', encoding='utf-8').write(html + mk.CSS + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open(os.path.join(D, 'gfx71_75.json'), 'w'))
    print('ok', len(G))
