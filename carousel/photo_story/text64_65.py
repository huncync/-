# 글자형 캐러셀 (11/16 · 10월 「싸운 다음 날, 남자가 하는 말, 진짜 뜻」 #10 형식 그대로) — 저장 · 프로필 방문 · 팔로우용
# 11장: 표지 · 세어보기 · 말 6개(듣는 뜻 / 남자가 하는 뜻 / 이렇게 하세요) · 정리 · 유형 · 남자친구에게 보내는 장
# python3 text64_65.py → node render57.js c64 c65
import re, sys
sys.path.insert(0, '/home/user/-/carousel/plan90')
from hashtags import tags

TPL = open('/home/user/-/carousel/carousel_10.html', encoding='utf-8').read()
HEAD = TPL[:TPL.index('<body')]
END = '📕 남자가 하는 말의 뜻은 「남자들끼리 하는 말」 1·2권에 적었습니다.\n프로필 링크에서 무료로 받아보세요.\n\n'

D = {
 '64': dict(
  t1='남자가<br>서운할 때', t2='하는 말,', sub='"괜찮아"는 정말 괜찮은 걸까요?',
  intro=('남자는 서운하면<br><span class="accent">"서운해" 대신</span><br>이런 말을 해요.', '들어본 말을 세어보세요.<br>마지막에 그의 서운함 방식이 나와요.'),
  who='서운할 때 하는 말',
  P=[('"괜찮아."', '괜찮구나', '안 괜찮아요.<br>말하면 쪼잔해 보일까 봐 접는 거예요.', '"괜찮다는 말 말고, 진짜 기분 하나만 말해줘."'),
     ('"아니야,<br>별거 아니야."', '진짜 별거 아닌가 봐', '별거예요.<br>별거라고 하면 싸움이 될까 봐 덮어요.', '"별거 아니어도, 나는 듣고 싶어."'),
     ('"응, 알았어."', '알았구나', '서운해서 말이 줄어든 거예요.<br>길게 쓰면 서운한 게 티 나니까요.', '짧아졌다고 다그치지 말고, 만났을 때 먼저 물어보세요.'),
     ('"너 하고 싶은<br>대로 해."', '나를 배려해 주네', '내 의견은 어차피<br>안 들어갈 것 같다는 뜻이에요.', '"네 생각도 듣고 싶어. 둘 중에 고르면 뭐야?"'),
     ('"요즘 좀 바빠."', '바쁘구나', '서운한 마음을 정리할 시간이 필요해요.<br>남자는 서운하면 거리를 둬요.', '하루 이틀은 기다려 주고, 그다음엔 가볍게 먼저 연락하세요.'),
     ('"나 원래 이래."', '고칠 생각이 없네', '지적받은 게 서운해서<br>방어하는 거예요.', '지적 대신 부탁으로. "이렇게 해주면 나 진짜 좋을 것 같아."')],
  s9=('남자는 서운하면<br>"괜찮아"로 덮어요.', '괜찮은 게 아니라,<br><span class="accent2">말하는 법을 모르는 거예요.</span>', '그래서 묻는 말이 중요해요.', '"왜 그래?" 대신<br>"내가 뭐 서운하게 했어?"'),
  s10=('그의 서운함 방식', [('0~1개', '바로 말하는형', '서운하면 서운하다고 말해요. 드문 편이에요.'), ('2~3개', '돌려 말하는형', '말하고 싶은 마음은 있어요. 물어봐 주면 나와요.'), ('4~6개', '혼자 삭히는형', '쌓이면 한 번에 멀어져요. 다음 장을 보내세요.')]),
  letter='네가 "괜찮아"라고 할 때,<br>진짜 괜찮은 건지 가끔 헷갈려.<br><br>서운한 거 있으면 작은 거라도 말해줘.<br>나 그거 쪼잔하다고 생각 안 해.<br><b>"그거 좀 서운했어."</b><br>그 한마디면 나도 더 잘할 수 있어.',
  cap='''남자가 서운할 때 하는 말, 진짜 뜻.
"괜찮아"는 정말 괜찮은 걸까요?

① "괜찮아." · 말하면 쪼잔해 보일까 봐 접는 거예요
② "아니야, 별거 아니야." · 별거라고 하면 싸움이 될까 봐
③ "응, 알았어." · 서운해서 말이 줄어든 거예요
④ "너 하고 싶은 대로 해." · 내 의견은 안 들어갈 것 같다는 뜻
⑤ "요즘 좀 바빠." · 서운한 마음을 정리하는 시간
⑥ "나 원래 이래." · 지적받은 게 서운해서 방어하는 거예요

남자는 서운하면 "괜찮아"로 덮어요.
괜찮은 게 아니라, 말하는 법을 모르는 거예요.

💡
"왜 그래?" 대신 "내가 뭐 서운하게 했어?"
마지막 장은 남자친구에게 보내주세요.

''', tg=['#남자속마음', '#연애고민'], pin='여섯 개 중에 몇 개 들어봤어요? 숫자만 남겨주세요 👇'),
 '65': dict(
  t1='남자가<br>확신이 없을 때', t2='하는 말,', to='그 사람에게는', sub='"우리 천천히 하자"는 배려일까요?',
  intro=('남자는 확신이 없으면<br><span class="accent">"모르겠어" 대신</span><br>이런 말을 해요.', '들어본 말을 세어보세요.<br>마지막에 그의 확신 단계가 나와요.'),
  who='확신이 없을 때 하는 말',
  P=[('"우리 천천히<br>하자."', '나를 아껴주는구나', '속도가 아니라<br>방향을 아직 못 정한 거예요.', '"천천히는 좋아. 근데 우리 지금 어디쯤이야?"'),
     ('"아직 정의<br>내리고 싶지 않아."', '부담 주기 싫구나', '다른 선택지를<br>닫고 싶지 않다는 뜻일 수 있어요.', '한 번은 기다려 주되, 기한은 마음속에 정해두세요.'),
     ('"나중에<br>얘기하자."', '지금은 바쁘구나', '그 "나중"은<br>보통 오지 않아요.', '"그럼 이번 주말에 얘기하자." 날짜로 바꾸세요.'),
     ('"나 지금 연애할<br>상황이 아니야."', '상황이 안 좋구나', '상황보다 마음의 문제일 때가 많아요.<br>확신이 있으면 상황을 만들어요.', '상황을 기다려 주지 말고, 행동을 보세요.'),
     ('"너 같은<br>사람 없어."', '나를 정말 좋아하네', '칭찬은 진심이에요.<br>그런데 다음 약속이 없으면 확신은 아니에요.', '말보다 다음 약속이 잡히는지 보세요.'),
     ('"그냥 지금이<br>좋아."', '지금 행복하구나', '앞으로를 그리지 않는다는<br>뜻이기도 해요.', '"지금 좋은 거 알아. 1년 뒤 우리도 그려져?"')],
  s9=('남자는 확신이 없으면<br>말이 흐려져요.', '확신 있는 남자는,<br><span class="accent2">날짜를 말해요.</span>', '"천천히" 대신 "이번 주말에".', '"나중에" 대신 "다음 달에".'),
  s10=('그의 확신 단계', [('0~1개', '확신형', '말보다 약속이 먼저 나와요.'), ('2~3개', '고민형', '마음은 있는데 아직 계산 중이에요.'), ('4~6개', '보류형', '놓치기 싫지만 고르지도 않아요.')]),
  letter='"천천히 하자"는 말, 나 이해해.<br>근데 나는 우리가<br>어디로 가는지 알고 싶어.<br><br>급하게 하자는 게 아니야.<br><b>"우리 이번 달에 한 번 진지하게 얘기하자."</b><br>그 한마디면 나는 기다릴 수 있어.',
  cap='''남자가 확신이 없을 때 하는 말, 진짜 뜻.
"우리 천천히 하자"는 배려일까요?

① "우리 천천히 하자." · 방향을 아직 못 정한 거예요
② "아직 정의 내리고 싶지 않아." · 선택지를 닫고 싶지 않은 것
③ "나중에 얘기하자." · 그 나중은 보통 오지 않아요
④ "나 지금 연애할 상황이 아니야." · 상황보다 마음의 문제
⑤ "너 같은 사람 없어." · 진심이지만, 약속이 없으면 확신은 아니에요
⑥ "그냥 지금이 좋아." · 앞으로를 그리지 않는다는 뜻

확신 있는 남자는 날짜를 말해요.
"천천히" 대신 "이번 주말에", "나중에" 대신 "다음 달에".

💡
말보다 다음 약속이 잡히는지 보세요.
마지막 장은 그 사람에게 보내주세요.

''', tg=['#썸', '#남자속마음'], pin='여섯 개 중에 몇 개 들어봤어요? 숫자만 남겨주세요 👇'),
}

def page(no, d):
    S = f'<div class="series">남자들끼리 하는 말 #{no}</div>'
    out = [f'''<section class="slide" id="s1">
  <div class="cover-c">
    <div class="small">남자가 직접 번역합니다</div>
    <div class="pen mt-s" style="font-size:132px !important">{d['t1']}<br>{d['t2']}<br><span class="accent">진짜 뜻</span></div>
    <div class="body mt-m" style="color:#d6d1c8">{d['sub']}</div>
  </div>
  <div class="handle">@mszexc</div>
  <div class="series">넘겨서 세어보세요 →</div>
</section>''', f'''<section class="slide" id="s2">
  <div class="pen h2">{d['intro'][0]}</div>
  <div class="body mt-m">{d['intro'][1]}</div>
  <div><div class="counter"><span class="n">0</span><span class="t">/ 6</span></div></div>
  <div class="byline">남자인 제가 직접 말합니다 · <b>박지훈</b></div>
  {S}
</section>''']
    for k, (ph, hear, mean, do) in enumerate(d['P'], 1):
        bars = ''.join(f'<i class="{"on" if j <= k else ""}"></i>' for j in range(1, 7))
        out.append(f'''<section class="slide" id="s{k + 2}">
  <div class="prog"><span class="lbl">{k} / 6</span>{bars}</div>
  <div class="who">{d['who']} {k}</div>
  <div class="phrase">{ph}</div>
  <div class="tr">
    <div class="r"><div class="k cold">당신이 듣는 뜻</div><div class="v dim">{hear}</div></div>
    <div class="r"><div class="k accent">남자가 하는 뜻</div><div class="v">{mean}</div></div>
  </div>
  <div class="do"><b>이렇게 하세요</b> · {do}</div>
  {S}
</section>''')
    a, b, c, e2 = d['s9']
    out.append(f'''<section class="slide inv" id="s9">
  <div class="body dim2">{a}</div>
  <div class="pen mt-m" style="font-size:112px;line-height:1.15">{b}</div>
  <div class="rule" style="background:#d9d2c4"></div>
  <div class="body">{c}</div>
  <div class="body dim2 mt-s">{e2}</div>
  {S}
</section>''')
    name, ty = d['s10']
    tys = ''.join(f'<div class="ty{" hi" if i == 2 else ""}"><div class="h"><span class="c">{c}</span><span class="n"{" style=\"color:var(--accent)\"" if i == 2 else ""}>{n}</span></div><div class="d">{t}</div></div>' for i, (c, n, t) in enumerate(ty))
    out.append(f'''<section class="slide" id="s10" style="justify-content:flex-start; padding-top:110px">
  <div class="pen h3">몇 개 들어봤나요?<br><span class="accent">{name}</span></div>
  <div class="types">{tys}</div>
  <div class="howto">댓글로 <b>몇 형인지</b>만 남겨주세요.<br>같은 고민인 친구가 있다면 보내주세요.</div>
  {S}
</section>''')
    out.append(f'''<section class="slide" id="s11" style="justify-content:flex-start; padding-top:120px">
  <div class="body dim">{d.get('to', '남자친구에게는')}</div>
  <div class="pen h3 mt-s"><span class="accent">이 장만</span> 보내주세요.</div>
  <div class="letter" style="font-size:40px;line-height:1.6;padding:44px 52px">{d['letter']}</div>
  <div class="howto" style="margin-top:36px">보낼 땐 <b>종이비행기 ➤</b><br><span style="color:var(--dim);font-size:34px">남자가 하는 말의 뜻은 전자책 1·2권에<br>프로필 링크에서 무료로 받아보세요</span></div>
  <div class="handle">@mszexc</div>
  {S}
</section>''')
    return HEAD + '<body>\n' + '\n'.join(out) + '\n</body></html>'

def caption(no):
    d = D[no]
    return d['cap'] + END + tags(d['tg'])

if __name__ == '__main__':
    for no, d in D.items():
        assert caption(no).count('#') == 5
        open(f'c{no}.html', 'w', encoding='utf-8').write(page(no, d))
    print('ok')
