# 팔로워 3만 감사 이벤트 · 남자어 번역 퀴즈 (11/26) — 공지 + 퀴즈를 한 게시물(14장)로
# 정답은 저장소에 두지 않아요(.work/event/answers.txt) · 카톡 · 상담 홍보 없음(11/26 지훈님 결정)
# python3 event30k.py → node style_samples/render.js event30k_g.html event30k_g_out → python3 event30k.py --build → node render66.js cev
import os, sys, json, shutil, importlib.util
from PIL import Image, ImageOps
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D); sys.path.insert(0, '/home/user/-/carousel/plan90')
from psgen import build
from s48_50 import bright
from hashtags import tags
spec = importlib.util.spec_from_file_location('mk', os.path.join(D, 'style_samples', 'make.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
kt, film = mk.kt, mk.film
H, M = 'him', 'me'
NO = 'ev'
O = lambda n, t, top: ('k', f'{n}  {t}', top, 6)  # 보기 한 줄

SLIDES = [
 # 1 표지 (얼굴)
 [('W', '팔로워 3만 감사 이벤트', 50, 6), ('G', '남자어 번역 퀴즈', 58, 6), ('k', '(1등 오마카세 런치 20만 원 상당)', 69, 'r')],
 # 2 그래픽
 [('w', '여러분 덕분에 3만이 됐어요.', 36, 6), ('g', '그래서 9분께 선물을 드려요.', 45, 'r'), ('k', '(남자가 하는 말, 이번엔 여러분이 번역해 주세요.)', 55, 4)],
 # 3 상품 1~3 (선물 사진)
 [('w', '🥇 1등 · 1명', 30, 6), ('g', '오마카세 런치 식사권 (20만 원 상당)', 37, 6), ('w', '🥈 2등 · 1명', 48, 6), ('g', '오뎅바 식사권 (10만 원 상당)', 55, 6), ('w', '🥉 3등 · 1명', 66, 6), ('g', '와인바 이용권 (5만 원 상당)', 73, 6)],
 # 4 그래픽
 [('w', '4등 · 1명', 34, 6), ('g', '스타벅스 3만 원권', 41, 6), ('w', '5등 · 5명', 52, 6), ('g', '스타벅스 아메리카노', 59, 6), ('k', '(한 분당 한 가지 상품만 받을 수 있어요.)', 70, 'r')],
 # 5 참여 방법 (모두)
 [('w', '참여 방법 ① · 모두', 30, 6), ('g', '@mszexc 팔로우', 39, 6), ('g', '이 게시물 댓글에 갖고 싶은 상품 번호', 48, 6), ('k', '(예: "1" · 숫자 하나면 돼요 → 4 · 5등 추첨)', 58, 'r')],
 # 6 그래픽
 [('w', '참여 방법 ② · 1~3등 도전', 30, 6), ('g', '같은 댓글에 친구 1명 태그', 39, 6), ('g', '퀴즈 정답 5개를 DM으로', 48, 6), ('k', '(5개 다 맞힌 분 중에서 1~3등을 추첨해요.)', 58, 'r')],
 # 7 Q1
 [('w', 'Q1. 서운할 때', 28, 6), ('q', '"괜찮아."', 36, 'r'), O('①', '진짜 괜찮다', 47), O('②', '서운한데, 말하면 쪼잔해 보일까 봐 접는 것', 54), O('③', '귀찮아서 대화를 끝내고 싶다', 61), O('④', '이미 마음이 식었다', 68)],
 # 8 그래픽 Q2
 [('w', 'Q2. 확신이 없을 때', 34, 6), ('q', '"나중에 얘기하자."', 42, 'r'), O('①', '지금 너무 바빠서', 52), O('②', '생각할 시간이 필요해서', 59), O('③', '그 "나중"은 보통 오지 않는다', 66), O('④', '화해하고 싶어서', 73)],
 # 9 Q3
 [('w', 'Q3. 헤어진 뒤, 밤에', 28, 6), ('q', '"잘 지내?"', 36, 'r'), O('①', '연락하기 전, 이미 오래 고민한 연락', 47), O('②', '실수로 보낸 연락', 54), O('③', '그냥 하는 인사', 61), O('④', '새 여자친구가 생겼다는 신호', 68)],
 # 10 그래픽 Q4
 [('w', 'Q4. 싸움을 빨리 끝내고 싶을 때', 34, 6), ('q', '"알았어, 내가 잘못했어."', 42, 'r'), O('①', '진심으로 반성했다', 52), O('②', '헤어지자는 뜻이다', 59), O('③', '당신 말이 다 맞다', 66), O('④', '뭘 잘못했는지 몰라도, 일단 멈추고 싶다', 73)],
 # 11 Q5
 [('w', 'Q5. 좋아하는 여자에게만', 28, 6), ('q', '"나 도착."', 36, 'r'), O('①', '그냥 습관이다', 47), O('②', '안 물어봐도 먼저 알려주고 싶은 마음', 54), O('③', '감시받는 느낌이라서', 61), O('④', '할 말이 없어서', 68)],
 # 12 그래픽 · DM 예시
 [('w', '정답은 DM으로 보내주세요.', 34, 6), ('g', '번호 5개를 순서대로, 한 줄로', 43, 6), ('k', '(댓글에 정답을 쓰면 다른 분들께 보여서 제외돼요.)', 53, 'r')],
 # 13 꼭 확인하세요 (반전)
 [('w', '꼭 확인하세요', 26, 6), ('g', '비공개 · 가계정 · 게시물 3개 미만은 제외', 34, 4), ('g', '기간 중 팔로우를 취소하면 제외', 43, 4), ('g', '한 사람이 여러 계정으로 참여하면 모두 제외', 52, 4), ('k', '(만 19세 이상만 참여할 수 있어요.)', 62, 'r')],
 # 14 마지막 (얼굴)
 [('w', '3만 명, 정말 고마워요.', 36, 6), ('g', '남자들은 이 말 안 해줘요. 그래서 앞으로도 제가 대신 할게요.', 44, 4), ('k', '응모 기간 · 발표는 캡션에 있어요', 82, 'r')],
]
PLAN = {1: ('p74n/src_01', (0.0, 0.1, 1.0, 1.0)), 3: ('p73n/src_06', None), 5: ('p74n/src_05', None), 7: ('p73n/src_02', None),
        9: ('p75n/src_02', None), 11: ('p73n/src_03', None), 13: ('p72n/src_03', None), 14: ('p73n/src_07', (0.0, 0.25, 1.0, 0.95))}
G = [
 (2, film('30,000', '', 'THANK YOU')),
 (4, film('9', '', 'GIFTS')),
 (6, film('Q', '', 'FIVE QUESTIONS')),
 (8, kt('그 사람', [(H, '나중에 얘기하자', '오후 11:20')])),
 (10, kt('그 사람', [(H, '알았어 내가 잘못했어', '오전 12:14')])),
 (12, kt('mszexc', [(M, '○-○-○-○-○', '오후 9:00')])),
]
CAP = f'''팔로워 3만 감사 이벤트 · 남자어 번역 퀴즈 🎁
여러분 덕분에 3만이 됐어요. 고마운 마음을 담아 9분께 선물을 드려요.

🥇 1등 (1명) 오마카세 런치 식사권 · 20만 원 상당
🥈 2등 (1명) 오뎅바 식사권 · 10만 원 상당
🥉 3등 (1명) 와인바 이용권 · 5만 원 상당
4등 (1명) 스타벅스 3만 원권
5등 (5명) 스타벅스 아메리카노

✅ 참여 방법 ① 모두
@mszexc 팔로우 + 이 게시물 댓글에 갖고 싶은 상품 번호 하나 (예: 1)
→ 4 · 5등 추첨

✅ 참여 방법 ② 1~3등 도전
같은 댓글에 친구 1명 태그 + 퀴즈 정답 5개를 DM으로 (예: 1-2-3-4-1)
→ 5개 다 맞힌 분 중에서 1~3등 추첨

📅 응모 기간 · ○/○(○) ~ ○/○(○) 23:59
📢 발표 · ○/○(○) 이 계정 스토리 (아이디 일부만 공개 · 당첨자께는 DM)

꼭 확인하세요
· 비공개 계정, 가계정, 게시물 3개 미만 계정은 제외돼요.
· 기간 중 팔로우를 취소하거나, 한 사람이 여러 계정으로 참여하면 제외돼요.
· 댓글에 정답을 쓰면 제외돼요. 정답은 DM으로만 받아요.
· 만 19세 이상만 참여할 수 있어요. 한 분당 한 가지 상품만 받을 수 있어요.
· 식사권 가게 이용이 어려우시면 같은 금액의 상품권으로 바꿔 드려요.
· 1 · 2등 제세공과금은 주최 측이 부담해요.
· 당첨자 연락처는 경품 발송에만 쓰고, 발송 후 바로 지워요.
· 추첨은 화면 녹화로 공개해요.
· 본 이벤트는 Instagram과 관련이 없어요.

남자들은 이 말 안 해줘요. 그래서 앞으로도 제가 대신 할게요.

{tags(['#남자속마음', '#연애고민'])}'''
PIN = '갖고 싶은 상품 번호 하나만 남겨주세요 (1~3등 도전은 친구 태그 + 정답 DM) 👇'

def prep(i, src, crop=None):
    im = ImageOps.exif_transpose(Image.open(os.path.join(D, f'{src}.jpg'))).convert('RGB')
    w, h = im.size
    if crop: im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    os.makedirs(os.path.join(D, f'p{NO}'), exist_ok=True)
    out = f'p{NO}/{i:02d}.jpg'; im.save(os.path.join(D, out), quality=90); return out

if __name__ == '__main__':
    if '--build' in sys.argv:
        os.makedirs(os.path.join(D, f'p{NO}g'), exist_ok=True)
        for k, (s, _) in enumerate(G, 1): shutil.copy(os.path.join(D, f'event30k_g_out/{k:02d}.png'), os.path.join(D, f'p{NO}g/{s:02d}.png'))
        assert len(SLIDES) == 14 and CAP.count('#') == 5, CAP.count('#')
        sl = []
        for i, boxes in enumerate(SLIDES, 1):
            if i in PLAN:
                bg = {'src': prep(i, *PLAN[i]), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.85) brightness(.9)'}
            else:
                g = f'p{NO}g/{i:02d}.png'
                bg = {'src': g, 'noshade': not bright(os.path.join(D, g)), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
            sl.append((bg, '', boxes))
        h = build(sl, no=NO, accent='yellow', point=13).replace('남자들끼리 하는 말 #ev', '팔로워 3만 감사 이벤트')
        open(os.path.join(D, f'c{NO}.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(D, 'event30k_caption.txt'), 'w', encoding='utf-8').write(CAP + '\n\n[고정 댓글]\n' + PIN + '\n')
        print('built'); sys.exit()
    html = mk.BASE.replace('<head>', '<head>' + mk.FONT, 1) if '<head>' in mk.BASE else mk.FONT + mk.BASE
    open(os.path.join(D, 'event30k_g.html'), 'w', encoding='utf-8').write(html + mk.CSS + ''.join(g for _, g in G) + '</body></html>')
    print('gfx', len(G))
