# #67 ~ #70 그래픽 새 스타일 (11/21 · 지훈님 결정): ② 카톡 화면(그가 한 말 · 남자들 단톡) + ③ 필름 무드(숫자 · 정리)
# 글 상자 자리(30~60%)는 비우고 위 · 아래에만 · python3 gfx67_70b.py → node style_samples/render.js … → p67g ~ p70g
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style_samples'))
import importlib.util
spec = importlib.util.spec_from_file_location('mk', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style_samples', 'make.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
kt, film = mk.kt, mk.film
H, M = 'him', 'me'
G = [
 (67, 2, film('D-DAY', '', 'ANNIVERSARY')),
 (67, 4, kt('그 사람', [(H, '갖고 싶은 거 있어?', '오후 9:41'), (H, '그냥 말해', '오후 9:41')])),
 (67, 6, kt('그 사람', [(M, '오늘 우리 1주년이야 ☺️', '오후 7:02'), (H, '아, 오늘이었어?', '오후 8:15')])),
 (67, 8, kt('남자들 단톡 (4)', [(H, '기념일 챙기기 귀찮아졌으면', '오후 11:20'), (H, '끝난 거지', '오후 11:20')])),
 (67, 10, film('04', '', 'FOUR SIGNS')),
 (67, 12, kt('그 사람', [(M, '이번 기념일은 내가 예약했어 🍷', '오후 6:10'), (H, '오 진짜? 고마워', '오후 6:12')])),
 (68, 2, film('SIGN', '', 'BEFORE THE CALL')),
 (68, 4, film('01', '', 'WATCHING')),
 (68, 6, kt('친구', [(H, '걔 요즘 어때?', '오전 1:14'), (H, '아니 그냥 궁금해서', '오전 1:14')])),
 (68, 8, kt('남자들 단톡 (4)', [(H, '연락하고 싶은데', '오전 2:03'), (H, '핑계가 없어', '오전 2:03')])),
 (68, 10, film('“ ”', '', 'WAIT')),
 (68, 12, kt('그 사람', [(H, '잘 지내?', '오후 11:48'), (M, '응, 잘 지내. 너는?', '오전 9:20')])),
 (69, 2, film('5', '', 'SMALL THINGS')),
 (69, 4, kt('그 사람', [(H, '나 도착', '오후 11:02'), (H, '오늘 재밌었어', '오후 11:02')])),
 (69, 6, film('04', '', 'YOUR PEOPLE')),
 (69, 8, kt('남자들 단톡 (4)', [(H, '걔가 좋아하는 건', '오후 10:31'), (H, '이상하게 다 기억나', '오후 10:31')])),
 (69, 10, film('“ ”', '', 'WORDS ARE EASY')),
 (69, 12, kt('그 사람', [(M, '저번에 먹고 싶다던 거 사 왔어', '오후 7:40'), (H, '헐 그걸 기억했어?', '오후 7:41')])),
 (70, 2, film('3', '', 'THREE REASONS')),
 (70, 4, kt('그 사람', [(H, '미안해', '오전 12:51'), (H, '잘할게', '오전 12:51')])),
 (70, 6, film('D+3', '', 'THE NEXT DAYS')),
 (70, 8, kt('남자들 단톡 (4)', [(H, '잡긴 잡았는데', '오전 3:12'), (H, '솔직히 무서워서였어', '오전 3:12')])),
 (70, 10, film('1', '', 'ONE MORE CHANCE')),
 (70, 12, film('30', '', 'DAYS')),
]
if __name__ == '__main__':
    D = os.path.dirname(os.path.abspath(__file__))
    html = mk.BASE.replace('<head>', '<head>' + mk.FONT, 1) if '<head>' in mk.BASE else mk.FONT + mk.BASE
    open(os.path.join(D, 'gfx67_70b.html'), 'w', encoding='utf-8').write(html + mk.CSS + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open(os.path.join(D, 'gfx67_70b.json'), 'w'))
    print('ok', len(G))
