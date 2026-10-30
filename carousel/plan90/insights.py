# 10/30 18:25 인스타 인사이트 (30일) 기준 판단과 방향 — 이전 판은 git 기록에
import html
e = html.escape
ASOF = '10/30 18:25 · 최근 30일'
KPI = [
 ('팔로워', '18,048', '10/28 16,667 → 2일 +1,381 · 10/24 이후 하루 약 355명'),
 ('필요한 속도', '하루 193명', '12/31 3만까지 62일 · 지금 속도면 넘어요(릴스가 계속 터진다는 전제)'),
 ('조회 (30일)', '971만', '릴스 822만 · 게시물 129만 · 스토리 20만'),
 ('순 팔로워 (30일)', '+10,074', '팔로워 아닌 사람 조회 93.6%'),
 ('게시물 조회 (30일)', '129만', '캐러셀 목표 월 150만에 근접'),
 ('스토리 (30일)', '20만', '하루 약 6.7천 회 · 루틴 시작 전 수치'),
]
# (번호, 제목, 형식, 조회(만), 공유, 경과)
CAR = [
 (34, '차단 안 하고 남겨두는 이유', '📸 사진 스토리형 · 이별', 4.3, 58, '1일'),
 (30, '숨기는 남자가 자주 하는 말들', '번역(묶음)', 2.8, 102, '3일'),
 (32, '연락 끊긴 첫날 밤, 머릿속', '머릿속', 1.2, 14, '1일'),
 (33, '식을 때, 싸우는 방식부터', '신호 목록', 0.87, 7, '1일'),
 (31, '"너 없으면 안 돼"', '번역(한 마디)', 0.61, 6, '2일'),
 (29, '말을 줄이게 만드는 법', '반어', 0.56, 2, '3일'),
 (35, '오래 만났는데 왜 설레지 않을까', '📸 사진+영상 · 반어', 0.13, 0, '31분'),
]
VERDICT = [
 ('맞음', '사진 스토리형 첫 편이 하루 만에 4.3만', '#34(사진 14장)가 1일 4.3만 · 공유 58 · 댓글 24. 같은 날 목록형 #33은 8.7천, 이틀 전 #32는 1.2만. 같은 이별 주제 #25는 3일에 4만이었어요. 주제 덕도 있지만 형식 차이가 커요. 사진 스토리형을 기본으로 확정해요.'),
 ('맞음', '릴스 끝 멘트 "팔로우 이유"가 통했어요', '10/29 「연락 다음으로 사라지는 것」 61.2만 → 팔로우 +1.2천(0.20%). 직전 두 릴스는 0.05~0.09%였어요. 공유도 5,428(0.89%)로 316만 원본(1.0%)과 거의 같아요. 2편이 1편만큼 보내졌다는 뜻이에요. 끝 멘트는 모든 릴스에 고정, 「식을 때」는 릴스에서 계속 써요.'),
 ('맞음', '팔로워 3만은 이제 가능한 숫자', '10/24 15,919 → 10/30 18,048. 하루 약 355명으로 필요 속도(193명)를 넘었어요. 릴스가 2주에 한 번씩 50만 이상 나오면 유지돼요.'),
 ('틀림', '한 마디 번역은 확실히 안 돼요', '#31 「너 없으면 안 돼」 2일 6.1천. #23 8.1천에 이어 두 번째. 기준(1만)을 못 넘어서 남아 있던 이별 · 싸움 한 마디 8편도 전부 "그 순간 하는 말들"로 바꿨어요(10/30).'),
 ('주의', '"식을 때" 목록형은 다시 약해졌어요', '#24 5.8만 이후 #33 1일 8.7천. 목록형이라 약한지 주제가 지친 건지는 아직 몰라요. 다음 "식을 때"(11/3 「칭찬보다 먼저 줄어드는 것」)를 사진 스토리형으로 만들어 비교해요.'),
 ('주의', '머릿속 #32는 공유 14', '#22(공유 252)만큼 안 나왔어요. 기준(공유 100)을 못 넘어서 머릿속은 더 늘리지 않고 지금 목차(7편) 그대로.'),
 ('확인', '「인생 여자 놓친 남자 특징」 302만', '고정된 302만 릴스가 팔로우 상위 4개(최소 444)에 없어요. 팔로우가 444 미만이면 전환 0.015% 이하예요. 언제 올렸는지, 끝에 팔로우 멘트가 있었는지 알려주세요. 맨 윗줄 79만 · 49.8만 릴스 제목도요.'),
]
CHANGES = [
 ('1', '사진 스토리형 = 캐러셀 기본 (10/30 확정)', '사진(또는 영상) 14장 + 말 상자. 사진은 하루 한 번 몰아 찍어서 2편 분량(28장)씩 보내주세요. #36부터 같은 방식.'),
 ('2', '한 마디 번역 8편 → 묶음 (10/30 반영)', '10/31 「동굴에 들어갈 때 하는 말들」, 11/18 「결정을 미룰 때」, 12/1 「이별을 예의로 포장할 때」, 12/2 「싸움을 빨리 끝내고 싶을 때」, 12/5 「거리를 두고 싶을 때」, 12/26 「다시 만나자고 할 때」, 12/30 「미련 있을 때」, 12/31 「자기를 낮출 때」.'),
 ('3', '릴스 끝 멘트 고정', '"남자가 하는 말이랑 행동, 남자 입장에서 매일 번역해서 올려요. 놓치기 싫으면 팔로우해두세요." 모든 릴스에.'),
 ('4', '스토리 루틴 시작', '30일 스토리 20만 · 하루 500명 미만. 스토리 탭 하루 3장 루틴을 오늘부터. 2주 뒤 같은 숫자로 비교.'),
 ('5', '구독 확인', '「구독자분들께만 먼저」 게시물 조회 1. 구독자가 거의 없다는 뜻이에요. 지금 구독자 수를 알려주세요. 11/6 미리보기 비율을 그 숫자로 정해요.'),
]
BIO = '''박지훈🇰🇷 | 남자가 말하는 남자심리
🙋‍♂️ 남자 심리, 남자가 직접 합니다
📕 「남자들끼리 하는 말」 1·2권 무료 · 3권 11/11 예약
💬 1:1 분석 · 카카오채널 "신청"
🌿 향을 만듭니다 · DAIEN'''
GOALS = [
 ('캐러셀 조회', '월 150만', '30일 게시물 129만. 사진 스토리형이 하루 4만대를 유지하면 넘어요.'),
 ('팔로워', '12/31까지 3만', '하루 193명 필요 · 최근 6일 하루 약 355명.'),
 ('프로필 → 링크', '1.7% → 4%', '이번에도 개요 탭 링크 클릭이 없어서 다음 점검 때.'),
 ('카카오채널 친구', '11/10까지 1,000명', '지금 몇 명인지 알려주세요(10/28 2명).'),
]
SWAP = [
 ('10/31', '18~19시', '남자가 "혼자 있고 싶어"라고 할 때 (한 마디)', '남자가 동굴에 들어갈 때 하는 말들, 진짜 뜻'),
 ('11/18', '18~19시', '남자가 "생각 좀 해볼게"라고 할 때 (한 마디)', '남자가 결정을 미룰 때 하는 말들, 진짜 뜻'),
 ('12/1', '18~19시', '남자가 "친구로 지내자"고 할 때 (한 마디)', '남자가 이별을 예의로 포장할 때 하는 말들'),
 ('12/2', '18~19시', '남자가 "다 내 잘못이야"라고 할 때 (한 마디)', '남자가 싸움을 빨리 끝내고 싶을 때 하는 말들'),
 ('12/5', '18~19시', '남자가 "우리 잠깐 연락 줄이자"고 할 때 (한 마디)', '남자가 거리를 두고 싶을 때 하는 말들, 진짜 뜻'),
 ('12/26', '18~19시', '남자가 "다시 시작하자"고 할 때 (한 마디)', '남자가 다시 만나자고 할 때 하는 말들, 진짜 뜻'),
 ('12/30', '18~19시', '남자가 "너는 좋은 사람이야"라고 할 때 (한 마디)', '헤어진 남자가 미련 있을 때 하는 말들'),
 ('12/31', '18~19시', '남자가 "나 같은 놈 만나지 마"라고 할 때 (한 마디)', '남자가 자기를 낮출 때 하는 말들, 진짜 뜻'),
]

def block():
    k = ''.join(f'<div class="ik"><small>{e(a)}</small><b>{e(b)}</b><span>{e(c)}</span></div>' for a, b, c in KPI)
    mx = max(r[3] for r in CAR)
    rows = ''.join(
        f'<li><span class="in">#{n:02d}</span><span class="it">{e(t)}<em>{e(s)} · {e(age)} · 공유 {sh or '—'}</em></span>'
        f'<span class="ib"><i style="width:{max(2, round(v / mx * 100))}%"></i></span><span class="iv">{v:g}만</span></li>'
        for n, t, s, v, sh, age in CAR)
    col = {'맞음': '#a9d18e', '틀림': '#e07a7a', '주의': '#e0b46a', '확인': '#8fb3d6'}
    ver = ''.join(f'<div class="iv2"><span class="tag" style="background:{col[a]}">{e(a)}</span><b>{e(b)}</b><p>{e(c)}</p></div>' for a, b, c in VERDICT)
    chg = ''.join(f'<li><span class="n">{n}</span><span class="t"><b>{e(a)}</b><br><span class="dim">{e(b)}</span></span><span></span></li>' for n, a, b in CHANGES)
    gl = ''.join(f'<div class="ik"><small>{e(a)}</small><b>{e(b)}</b><span>{e(c)}</span></div>' for a, b, c in GOALS)
    sw = ''.join(f'<li><span class="d">{e(d)}<i>{e(s)}</i></span><span class="m"><s class="dim">{e(o)}</s><br><b>{e(nw)}</b></span></li>' for d, s, o, nw in SWAP)
    return f'''    <style>
      .ins .ik {{ background:#141416; border:1px solid #2a2a2d; border-radius:12px; padding:10px 12px; }}
      .ins .ik small {{ display:block; font-size:12px; opacity:.7; }} .ins .ik b {{ display:block; font-size:20px; margin:2px 0; }} .ins .ik span {{ font-size:12px; opacity:.75; }}
      .ins .kg {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }}
      .ins ol.ic {{ list-style:none; padding:0; margin:8px 0 0; }}
      .ins ol.ic li {{ display:grid; grid-template-columns:34px 1fr 64px 48px; gap:8px; align-items:center; padding:7px 0; border-bottom:1px solid #2a2a2d; font-size:13px; }}
      .ins .it em {{ display:block; font-style:normal; font-size:11px; opacity:.65; }}
      .ins .ib {{ height:6px; background:#2a2a2d; border-radius:3px; overflow:hidden; }} .ins .ib i {{ display:block; height:100%; background:#e0b46a; }}
      .ins .iv {{ text-align:right; font-variant-numeric:tabular-nums; font-weight:700; }} .ins .in {{ opacity:.6; font-size:12px; }}
      .ins .iv2 {{ padding:10px 0; border-bottom:1px solid #2a2a2d; }} .ins .iv2 p {{ margin:4px 0 0; font-size:13px; opacity:.85; line-height:1.55; }}
      .ins .iv2 .tag {{ display:inline-block; color:#111; font-size:11px; font-weight:900; border-radius:999px; padding:1px 8px; margin-right:6px; }}
      .ins pre {{ white-space:pre-wrap; }}
    </style>
    <details class="ins cap" open><summary><b>인사이트 점검 · {e(ASOF)}</b></summary><div style="padding:0 14px 14px">
    <div class="kg">{k}</div>
    <h2>캐러셀 성적표<small>조회수 · 올린 지 얼마나 됐는지 같이 보세요</small></h2>
    <ol class="ic">{rows}</ol>
    <h2>냉정한 판단</h2>{ver}
    <h2>바꿀 것<small>중요한 순서</small></h2><ol class="topics">{chg}</ol>
    <h2>소개글 예시</h2><div class="row"><button class="btn gold" data-ct="ins-bio">복사</button></div><pre id="ins-bio">{e(BIO)}</pre>
    <h2>새 목표</h2><div class="kg">{gl}</div>
    <h2>목차 교체<small>10/30 반영 완료 · 순번과 날짜는 그대로 · 8편</small></h2><ol class="plan subplan">{sw}</ol>
    </div></details>
'''
