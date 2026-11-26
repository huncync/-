# 팔로워 3만 감사 이벤트 · 남자어 번역 퀴즈 10문제 (11/26 개정) — 공지 + 퀴즈 한 게시물(20장)
# 등수: 1등 = 10개 만점 + 주관식 번역 가장 좋은 1명(지훈님 선정) / 2등 = 만점자 추첨 / 3등 = 8개 이상 추첨 / 4 · 5등 = 댓글 추첨
# 문제(11/26 3차): Q1~5 쉬움 · Q6~7 중간(캐러셀 #64 · #65 · #67 · #68 · #69 · #70 · #72) / Q8~9 어려움 · Q10 제일 어려움(릴스 R4 · R9 · R27) · #72(11/26) 이후 올리기
# 정답은 저장소에 두지 않아요(.work/event/answers.txt) · 카톡 · 상담 홍보 없음(11/26 지훈님 결정)
# python3 event30k.py → node style_samples/render.js event30k_g.html event30k_g_out → python3 event30k.py --build → node render66.js cev
import os, sys, shutil, importlib.util
from PIL import Image, ImageOps
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D); sys.path.insert(0, '/home/user/-/carousel/plan90')
from psgen import build
from s48_50 import bright
from hashtags import tags
spec = importlib.util.spec_from_file_location('mk', os.path.join(D, 'style_samples', 'make.py'))
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
kt, film = mk.kt, mk.film
M = 'me'
NO = 'ev'

def Q(n, label, ask, opts, top):  # 문제 한 장: 번호 · 질문 · 보기 4개
    b = [('w', f'Q{n}. {label}', top, 6), ('g', ask, top + 7, 4)]
    return b + [('k', f'{"①②③④"[i]}  {o}', top + 18 + 7 * i, 6) for i, o in enumerate(opts)]

QS = [  # (분류, 질문, 보기) — 11/26 3차 개정: Q1~5 쉬움(캐러셀) · Q6~7 중간(캐러셀) · Q8~9 어려움(릴스) · Q10 제일 어려움(릴스) · 정답은 .work/event/answers.txt
 ('좋아할 때', '집에 가면, 안 물어봐도 먼저 보내는 연락은?', ['"뭐 해?"', '"나 도착."', '"자?"', '"피곤해"']),
 ('확신', '확신 있는 남자는 "천천히" 대신 뭐라고 할까?', ['"언제"', '"사랑해"', '"미안해"', '"우리"']),
 ('서운할 때', '남자의 "괜찮아."는?', ['정말 괜찮다', '귀찮다', '화가 났다', '서운한데, 말하면 쪼잔해 보일까 봐 접는 것']),
 ('기념일', '식은 남자가 기념일에 하는 말은?', ['"작년에 그거 좋아했잖아."', '"아, 오늘이었어?"', '"이번엔 내가 예약했어."', '"뭐 갖고 싶은지 고민했어."']),
 ('붙잡을 때', '진심인 붙잡음은 무엇으로 증명될까?', ['눈물', '긴 사과문', '선물', '달라진 다음 날']),
 ('다른 여자', '휴대폰보다 먼저 바뀌는 것이 아닌 것은?', ['칭찬과 선물이 갑자기 는다', '잠금 화면을 바꾼다', '내 일정을 자세히 묻는다', '작은 질문에도 예민해진다']),
 ('헤어진 남자', '다시 연락하기 전, 세 번째로 하는 행동은?', ['공통 친구에게 안부를 묻는다', '스토리를 빠짐없이 본다', '둘만 아는 걸 SNS에 올린다', '술 마시고 전화한다']),
 ('읽씹 뒤 늦게 온 답장', '"답할 마음이 줄어든" 남자의 답장은?', ['하루 넘게 늦게 온 답장', '늦었지만 내 질문에 답한 답장', '내 질문은 건너뛰고, 아무 일 없던 듯한 답장', '미안하다며 늦은 이유를 말한 답장']),
 ('관계를 끝낼 때', '마음 정리를 끝낸 남자의 진짜 신호는?', ['화를 자주 낸다', '전보다 더 자주 연락한다', '갑자기 조용하고 친절해진다', '먼저 "헤어지자"고 한다']),
 ('다시 연락', '읽씹하던 남자에 대해 맞는 것을 모두 고르면?', []),
]
SLIDES = [
 [('W', '팔로워 3만 감사 이벤트', 50, 6), ('G', '남자어 번역 퀴즈 10', 58, 6), ('k', '(1등 오마카세 런치 20만 원 상당)', 69, 'r')],
 [('w', '여러분 덕분에 3만이 됐어요.', 36, 6), ('g', '그래서 9분께 선물을 드려요.', 45, 'r'), ('k', '(남자가 하는 말, 이번엔 여러분이 번역해 주세요.)', 55, 4)],
 [('w', '🥇 1등 · 1명', 30, 6), ('g', '오마카세 런치 식사권 (20만 원 상당)', 37, 6), ('w', '🥈 2등 · 1명', 48, 6), ('g', '오뎅바 식사권 (10만 원 상당)', 55, 6), ('w', '🥉 3등 · 1명', 66, 6), ('g', '와인바 이용권 (5만 원 상당)', 73, 6)],
 [('w', '4등 · 1명', 34, 6), ('g', '스타벅스 3만 원권', 41, 6), ('w', '5등 · 5명', 52, 6), ('g', '스타벅스 아메리카노', 59, 6), ('k', '(한 분당 한 가지 상품만 받을 수 있어요.)', 70, 'r')],
 [('w', '참여 방법', 28, 6), ('g', '① 팔로우 + 댓글에 갖고 싶은 상품 번호', 36, 4), ('k', '→ 4 · 5등 추첨 (예: "1" · 숫자 하나면 돼요)', 45, 'r'), ('g', '② 같은 댓글에 친구 1명 태그 + 정답 DM', 54, 4), ('k', '→ 1~3등 도전', 63, 'r')],
 [('w', '1~3등은 이렇게 정해요.', 32, 6), ('g', '🥇 10개 만점 + 주관식 번역이 가장 좋은 1명', 40, 4), ('g', '🥈 10개 만점 중 추첨', 49, 4), ('g', '🥉 8개 이상 맞힌 분 중 추첨', 58, 4), ('k', '(만점자가 없으면 가장 많이 맞힌 분 중에서 뽑아요.)', 68, 'r')],
]
for n, (lab, ask, opts) in enumerate(QS, 1):
    SLIDES.append(Q(n, lab, ask, opts, 26 if (len(SLIDES) + 1) % 2 else 34))

# 11/26 3차 개정 · Q10(제일 어려움): 릴스 R27 내용 "모두 고르기"
def QX(n, lab, ask, stmts, pairs, top=26):  # 보기 문장 ㄱ~ㄹ + 선택지 두 줄
    b = [('w', f'Q{n}. {lab}', top, 6), ('g', ask, top + 7, 4)]
    b += [('k', f'{"ㄱㄴㄷㄹ"[i]}. {t}', top + 18 + 6.5 * i, 6) for i, t in enumerate(stmts)]
    return b + [('w', p, top + 46 + 6.5 * j, 6) for j, p in enumerate(pairs)]
SLIDES[15] = QX(10, '읽씹하던 남자가 다시 연락할 때', '맞는 것을 모두 고르면?',
  ['핑계(링크 · 사진)가 생기면 연락한다', '내가 연락을 더 자주 할수록 빨리 돌아온다', '밤에 온 "자?"는 마음보다 외로움일 때가 많다', '다시 온 연락이 나에게 질문을 하면 진심이다'],
  ['① ㄱ, ㄴ\u3000\u3000\u3000② ㄱ, ㄷ, ㄹ', '③ ㄴ, ㄷ, ㄹ\u3000\u3000④ ㄱ, ㄴ, ㄷ, ㄹ'])
SLIDES += [
 [('w', '보너스 · 주관식 (선택)', 28, 6), ('q', '"요즘 좀 바빠."', 36, 'r'), ('g', '남자 입장에서 한 줄로 번역해 보세요.', 47, 4), ('k', '(1등은 만점자 중 이 답이 가장 좋은 분께 드려요.)', 57, 'r')],
 [('w', '정답은 DM으로 보내주세요.', 34, 6), ('g', '번호 10개를 순서대로 + 주관식 한 줄', 43, 4), ('k', '(댓글에 정답을 쓰면 다른 분들께 보여서 제외돼요.)', 53, 'r')],
 [('w', '꼭 확인하세요', 26, 6), ('g', '비공개 · 가계정 · 게시물 3개 미만은 제외', 34, 4), ('g', '기간 중 팔로우를 취소하면 제외', 43, 4), ('g', '한 사람이 여러 계정으로 참여하면 모두 제외', 52, 4), ('k', '(만 19세 이상만 참여할 수 있어요.)', 62, 'r')],
 [('w', '정답은 전부, 이 계정 게시물 안에 있어요.', 36, 4), ('g', '3만 명, 정말 고마워요.', 45, 6), ('k', '응모 기간 · 발표는 캡션에 있어요', 82, 'r')],
]
PLAN = {1: ('p74n/src_01', (0.0, 0.1, 1.0, 1.0)), 3: ('p73n/src_06', None), 5: ('p74n/src_05', None), 7: ('p73n/src_02', None),
        9: ('p75n/src_02', None), 11: ('p73n/src_03', None), 13: ('p74n/src_02', None), 15: ('p73n/src_05', None),
        17: ('p74n/src_04', None), 19: ('p72n/src_03', None), 20: ('p73n/src_07', (0.0, 0.25, 1.0, 0.95))}
G = [
 (2, film('30,000', '', 'THANK YOU')),
 (4, film('9', '', 'GIFTS')),
 (6, film('1·2·3', '', 'HOW TO WIN')),
 (8, film('Q2', '', 'EASY')),
 (10, film('Q4', '', 'EASY')),
 (12, film('Q6', '', 'MIDDLE')),
 (14, film('Q8', '', 'HARD')),
 (16, film('Q10', '', 'HARDEST')),
 (18, kt('mszexc', [(M, '○-○-○-○-○-○-○-○-○-○', '오후 9:00'), (M, '요즘 바빠 = ○○○○○', '오후 9:00')])),
]
CAP = f'''팔로워 3만 감사 이벤트 · 남자어 번역 퀴즈 10 🎁
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
같은 댓글에 친구 1명 태그 + 퀴즈 정답 10개를 DM으로
(예: 1-2-3-4-1-2-3-4-1-2 / 요즘 바빠 = ○○○)
🥇 10개 만점 + 주관식 번역이 가장 좋은 1명 (남자 입장에서 가장 정확하고 짧은 번역)
🥈 10개 만점 중 추첨
🥉 8개 이상 맞힌 분 중 추첨
· 만점자가 없으면 가장 많이 맞힌 분 중에서 뽑아요.
· 주관식은 선택이에요. 안 써도 2 · 3등은 도전할 수 있어요.
💡 정답은 전부 이 계정 게시물 안에 있어요.

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
· 2 · 3 · 4 · 5등 추첨은 화면 녹화로 공개해요.
· 좋은 주관식 답은 동의를 받은 뒤, 이름 없이 콘텐츠로 소개할 수 있어요.
· 본 이벤트는 Instagram과 관련이 없어요.

남자들은 이 말 안 해줘요. 그래서 앞으로도 제가 대신 할게요.

{tags(['#남자속마음', '#연애고민'])}'''
PIN = '갖고 싶은 상품 번호 하나만 남겨주세요 (1~3등 도전은 친구 태그 + 정답 DM) 👇'
STORY = ['3만 감사 이벤트 🎁 1등 오마카세 20만 원 · 남자어 번역 퀴즈 10문제 → 게시물 보러 가기',
         '(중간 힌트) 정답은 전부 이 계정 예전 게시물 안에 있어요 👀',
         '(마감 전날) 오늘 밤 23:59 마감 · 숫자 댓글 하나면 4 · 5등 추첨에 들어가요']

def prep(i, src, crop=None):
    im = ImageOps.exif_transpose(Image.open(os.path.join(D, f'{src}.jpg'))).convert('RGB')
    w, h = im.size
    if crop: im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = ImageOps.fit(im, (1080, 1350), Image.LANCZOS)
    os.makedirs(os.path.join(D, f'p{NO}'), exist_ok=True)
    out = f'p{NO}/{i:02d}.jpg'; im.save(os.path.join(D, out), quality=90); return out

if __name__ == '__main__':
    if '--build' in sys.argv:
        g_dir = os.path.join(D, f'p{NO}g')
        if os.path.isdir(g_dir): shutil.rmtree(g_dir)
        os.makedirs(g_dir)
        for k, (s, _) in enumerate(G, 1): shutil.copy(os.path.join(D, f'event30k_g_out/{k:02d}.png'), os.path.join(g_dir, f'{s:02d}.png'))
        assert len(SLIDES) == 20 and CAP.count('#') == 5 and len(QS) == 10, (len(SLIDES), CAP.count('#'))
        sl = []
        for i, boxes in enumerate(SLIDES, 1):
            if i in PLAN:
                bg = {'src': prep(i, *PLAN[i]), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.85) brightness(.9)'}
            else:
                g = f'p{NO}g/{i:02d}.png'
                bg = {'src': g, 'noshade': not bright(os.path.join(D, g)), 'style': 'inset:0;width:100%;height:100%;object-fit:cover;filter:none'}
            sl.append((bg, '', boxes))
        h = build(sl, no=NO, accent='yellow', point=19).replace('남자들끼리 하는 말 #ev', '팔로워 3만 감사 이벤트')
        open(os.path.join(D, f'c{NO}.html'), 'w', encoding='utf-8').write(h)
        open(os.path.join(D, 'event30k_caption.txt'), 'w', encoding='utf-8').write(CAP + '\n\n[고정 댓글]\n' + PIN + '\n\n[스토리]\n' + '\n'.join(STORY) + '\n')
        print('built', len(SLIDES)); sys.exit()
    html = mk.BASE.replace('<head>', '<head>' + mk.FONT, 1) if '<head>' in mk.BASE else mk.FONT + mk.BASE
    out = os.path.join(D, 'event30k_g_out')
    if os.path.isdir(out): shutil.rmtree(out)
    open(os.path.join(D, 'event30k_g.html'), 'w', encoding='utf-8').write(html + mk.CSS + ''.join(g for _, g in G) + '</body></html>')
    print('gfx', len(G))
