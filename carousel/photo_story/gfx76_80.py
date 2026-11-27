# #76 ~ #80 그래픽 6장씩 (11/23) — 카톡 화면(그가 한 말 · 남자들 단톡) + 필름 무드(숫자 · 정리) · gfx67_70b.py와 같은 방식
# python3 gfx76_80.py → node style_samples/render.js gfx76_80.html gfx76_80_out → 아래 __main__이 p76g ~ p80g로 복사(--copy)
import os, sys, json, shutil, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('mk', os.path.join(D, 'style_samples', 'make.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
kt, film = mk.kt, mk.film
H, M = 'him', 'me'
G = [
 (76, 2, film('4', '', 'GASLIGHTING')),
 (76, 4, kt('그 사람', [(M, '어제 나한테 그렇게 말했잖아', '오후 10:12'), (H, '그런 말 한 적 없는데?', '오후 10:15')])),
 (76, 6, kt('그 사람', [(M, '나 그 말 좀 서운했어', '오후 11:02'), (H, '너 너무 예민한 거 아니야?', '오후 11:03')])),
 (76, 8, kt('남자들 단톡 (4)', [(H, '걔는 내가 맞다고 하면', '오전 1:40'), (H, '결국 수긍해', '오전 1:40')])),
 (76, 10, film('2+', '', 'A PATTERN')),
 (76, 12, film('“ ”', '', 'TRUST YOUR MEMORY')),
 (77, 2, film('4', '', 'JUST END IT')),
 (77, 4, kt('그 사람', [(H, '알았어 내가 잘못했어', '오후 11:30'), (H, '그만하자 피곤하다', '오후 11:31')])),
 (77, 6, kt('그 사람', [(H, '뭘 원하는지 말해', '오전 12:05'), (H, '다 해줄게', '오전 12:05')])),
 (77, 8, kt('남자들 단톡 (4)', [(H, '싸울 땐 그냥', '오전 1:12'), (H, '미안하다고 하는 게 제일 빨라', '오전 1:12')])),
 (77, 10, film('2+', '', 'NOT SOLVED')),
 (77, 12, kt('그 사람', [(H, '어제 그 얘기 말인데', '오후 12:40'), (H, '나 좀 생각해 봤어', '오후 12:41')])),
 (78, 2, film('4', '', 'WHAT HE NEVER DOES')),
 (78, 4, kt('그 사람', [(H, '토요일 약속 그대로지?', '오후 6:20'), (H, '금요일 야근이라 미리 말해 두려고', '오후 6:21')])),
 (78, 6, film('0', '', 'NO SILENT DAYS')),
 (78, 8, kt('남자들 단톡 (4)', [(H, '진짜 좋아하면', '오전 12:50'), (H, '애매하게 굴 여유가 없더라', '오전 12:50')])),
 (78, 10, film('4/4', '', 'TRUST HIM')),
 (78, 12, kt('그 사람', [(M, '너랑 있으면 마음이 편해', '오후 10:44'), (H, '나도 ㅎㅎ', '오후 10:45')])),
 (79, 2, film('3', '', 'AFTER A FEW DRINKS')),
 (79, 4, kt('친구', [(H, '어제 걔가 술 마시고', '오후 1:20'), (H, '너 얘기 엄청 하더라', '오후 1:20')])),
 (79, 6, film('“ ”', '', 'REGRET')),
 (79, 8, kt('남자들 단톡 (4)', [(H, '요즘 걔 어떻게 지낸대?', '오전 1:58'), (H, '아니 그냥', '오전 1:58')])),
 (79, 10, kt('그 사람', [(H, '잘 지내?', '오전 2:14')])),
 (79, 12, film('AM', '', 'THE MORNING AFTER')),
 (80, 2, film('23:00', '', 'BEFORE SLEEP')),
 (80, 4, kt('그 사람', [(M, '자?', '오후 11:48'), (M, '잘 자', '오후 11:59')])),
 (80, 6, kt('그 사람', [(M, '오늘 어땠어?', '오후 11:20'), (H, '피곤해 내일 얘기하자', '오후 11:52')])),
 (80, 8, kt('남자들 단톡 (4)', [(H, '요즘 밤에 연락하는 게', '오전 12:30'), (H, '좀 일 같아', '오전 12:30')])),
 (80, 10, film('3+', '', 'COOLING DOWN')),
 (80, 12, kt('그 사람', [(M, '오늘은 내가 먼저 잘 자 할게', '오후 11:10'), (H, '고마워 너도 잘 자', '오후 11:12')])),
]
if __name__ == '__main__':
    if '--copy' in sys.argv:
        order = json.load(open(os.path.join(D, 'gfx76_80.json')))
        for k, (n, s) in enumerate(order, 1):
            os.makedirs(os.path.join(D, f'p{n}g'), exist_ok=True)
            shutil.copy(os.path.join(D, f'gfx76_80_out/{k:02d}.png'), os.path.join(D, f'p{n}g/{s:02d}.png'))
        print('copied', len(order)); sys.exit()
    html = mk.BASE.replace('<head>', '<head>' + mk.FONT, 1) if '<head>' in mk.BASE else mk.FONT + mk.BASE
    open(os.path.join(D, 'gfx76_80.html'), 'w', encoding='utf-8').write(html + mk.CSS + ''.join(g for _, _, g in G) + '</body></html>')
    json.dump([[n, s] for n, s, _ in G], open(os.path.join(D, 'gfx76_80.json'), 'w'))
    print('ok', len(G))
