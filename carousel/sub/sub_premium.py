# 구독 전용 디자인 (10/28~) — 무료 캐러셀과 한눈에 달라 보이게: 아이보리 종이 · 명조 제목 · 호수 번호 · 박지훈 서명
# python3 sub_premium.py  → s01~s03.html, w1030.html
import sub_data as D

CSS = '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Serif+KR:wght@500;700;900&display=block">
<style>
  :root { --paper:#f4eee3; --ink:#1d1a16; --dim:#7a7064; --gold:#9a6a1f; --line:#ddd2bf; --night:#17140f; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { word-break:keep-all; background:#555; font-family:'Noto Sans KR',sans-serif; color:var(--ink); }
  .slide { width:1080px; height:1350px; background:var(--paper); position:relative; overflow:hidden; padding:150px 100px 140px; display:flex; flex-direction:column; justify-content:center; margin-bottom:20px; }
  .slide:before { content:''; position:absolute; inset:36px; border:2px solid #cdb68a; border-radius:6px; pointer-events:none; }
  .top { position:absolute; left:72px; right:72px; top:62px; display:flex; justify-content:space-between; font-size:30px; letter-spacing:.14em; color:var(--gold); font-weight:700; }
  .foot { position:absolute; left:72px; right:72px; bottom:62px; display:flex; justify-content:space-between; font-size:32px; color:var(--dim); }
  .pen { font-family:'Nanum Pen Script',cursive; -webkit-text-stroke:1.2px currentColor; paint-order:stroke fill; line-height:1.15; }
  .serif { font-family:'Noto Serif KR',serif; font-weight:900; letter-spacing:-0.02em; line-height:1.22; }
  .gold { color:var(--gold); } .dim { color:var(--dim); }
  .kicker { font-size:64px; color:#5b5144; }
  .h-cover { font-size:128px; margin-top:24px; }
  .lede { font-size:44px; line-height:1.6; margin-top:48px; color:#3a332b; font-weight:500; }
  .sign { font-family:'Nanum Pen Script'; font-size:72px; color:var(--gold); -webkit-text-stroke:1px currentColor; }
  .rule { height:2px; background:var(--line); margin:48px 0; }
  /* 문장 장 */
  .prog { display:flex; gap:12px; align-items:center; margin-bottom:36px; }
  .prog b { font-size:34px; color:var(--gold); margin-right:10px; font-variant-numeric:tabular-nums; }
  .prog i { flex:1; height:5px; border-radius:3px; background:var(--line); } .prog i.on { background:var(--gold); }
  .sit { font-family:'Noto Serif KR'; font-weight:700; font-size:50px; line-height:1.35; }
  .chat { margin-top:40px; display:flex; flex-direction:column; gap:18px; }
  .me { align-self:flex-end; max-width:86%; background:#fae36b; border-radius:40px 40px 10px 40px; padding:34px 44px; font-size:50px; line-height:1.5; font-weight:500; box-shadow:0 2px 0 #e0c74e; }
  .him { align-self:flex-start; max-width:80%; background:#fff; border-radius:40px 40px 40px 10px; padding:26px 38px; font-size:42px; line-height:1.45; font-weight:500; box-shadow:0 2px 0 #e3dacb; }
  .copy { align-self:flex-end; font-size:30px; color:var(--dim); margin-top:-6px; }
  .why { margin-top:48px; border-left:6px solid var(--gold); padding:6px 0 6px 30px; font-size:42px; line-height:1.55; color:#2d2822; }
  .why b { color:var(--gold); display:block; font-size:34px; letter-spacing:.06em; margin-bottom:6px; }
  .avoid { margin-top:34px; font-size:38px; color:#a24a3c; } .avoid s { color:#8a8075; }
  /* 답장 장 */
  .rp { margin-top:24px; display:flex; flex-direction:column; gap:18px; }
  .rp .r { background:#fbf7f0; border:2px solid var(--line); border-radius:28px; padding:22px 30px 20px; }
  .rp .r .q { display:flex; gap:16px; align-items:flex-start; }
  .rp .lab { flex:0 0 auto; font-size:30px; font-weight:900; color:var(--dim); padding-top:8px; width:60px; }
  .rp .t { font-size:40px; line-height:1.4; font-weight:500; }
  .rp .t.mine { background:#fae36b; border-radius:22px; padding:6px 20px; display:inline-block; }
  .rp .n { font-size:33px; color:#5b5144; margin:12px 0 0 76px; line-height:1.5; }
  /* 남자들끼리 장 */
  .night { background:var(--night) !important; color:#f1ebe0; }
  .night:before { border-color:#4a3c22 !important; }
  .night .foot { color:#8e8578; } .night .top { color:#d4a95a; }
  .grp { margin-top:40px; display:flex; flex-direction:column; gap:26px; }
  .grp .who { font-size:32px; color:#a99f90; margin-bottom:8px; font-weight:700; }
  .grp .b { background:#2b261e; border-radius:12px 38px 38px 38px; padding:28px 36px; font-size:44px; line-height:1.5; max-width:92%; }
  .mean { margin-top:52px; background:#f4eee3; color:#1d1a16; border-radius:28px; padding:36px 40px; font-size:42px; line-height:1.55; }
  .mean b { color:var(--gold); } .mean small { display:block; font-size:30px; color:var(--gold); font-weight:900; letter-spacing:.08em; margin-bottom:8px; }
  .note { margin-top:26px; font-size:30px; color:#8e8578; }
  /* 편지 장 */
  .letter { font-family:'Nanum Pen Script'; font-size:76px; line-height:1.35; -webkit-text-stroke:1px currentColor; color:#2d2822; }
  .letter b { color:var(--gold); font-weight:400; }
  /* 총정리 */
  .ch { font-family:'Noto Serif KR'; font-weight:900; font-size:64px; line-height:1.2; }
  .cs { font-size:36px; color:var(--dim); margin-top:10px; }
  .ents { margin-top:30px; border-top:2px solid var(--line); }
  .ent { padding:16px 0; border-bottom:2px solid var(--line); }
  .ent .ph { font-family:'Nanum Pen Script'; font-size:58px; line-height:1.1; -webkit-text-stroke:1.1px currentColor; }
  .ent .no { font-family:'Noto Sans KR'; -webkit-text-stroke:0; font-size:30px; font-weight:900; color:var(--gold); margin-right:14px; }
  .ent .mn { font-size:34px; color:#3a332b; margin-top:4px; line-height:1.45; }
</style></head><body>
'''

def top(no, date): return f'<div class="top"><span>구독자 전용 · MEMBERS</span><span>No.{no:02d} · {date}</span></div>'
def foot(t): return f'<div class="foot"><span>@mszexc</span><span>{t}</span></div>'
def bars(i, n): return ''.join(f'<i class="{"on" if k < i else ""}"></i>' for k in range(n))

COVER = {'s01': '연락이<br>뜸해졌을 때', 's02': '싸운<br>다음 날', 's03': '헤어지고<br>연락하고<br>싶을 때'}

def week(idx):
    key, date, theme, items = D.WEEKS[idx]
    X = D.EXTRA[key]; no = idx + 1; d = f'{int(date[5:7])}.{int(date[8:])}'
    T = lambda: top(no, d); F = lambda: foot(f'보내기 전에, 이 문장 · {theme}')
    h = CSS + f'''<section class="slide" id="s1">{T()}
  <div class="pen kicker">보내기 전에, 이 문장</div>
  <div class="serif h-cover">{COVER.get(key, theme)}</div>
  <div class="lede">그대로 보내도 되는 문장 5개,<br>그가 답했을 때 다음 한 줄,<br>남자들끼리 하는 말까지.</div>
  <div class="sign" style="margin-top:56px">— 지훈이 구독자에게만</div>{foot('남자들끼리 하는 말 · 구독자 전용')}</section>
'''
    for i, (sit, msg, why, avoid) in enumerate(items, 1):
        h += f'''<section class="slide">{T()}
  <div class="prog"><b>{i} / 5</b>{bars(i, 5)}</div>
  <div class="sit">{sit}</div>
  <div class="chat"><div class="me">{msg.strip('"')}</div><div class="copy">내 말투로 조금 바꿔도 돼요</div></div>
  <div class="why"><b>왜 통하냐면</b>{why}</div>
  <div class="avoid">✕ 피할 말 · <s>{avoid}</s></div>{F()}</section>
'''
    rows = ''.join(f'<div class="r"><div class="q"><span class="lab">그</span><span class="t">{a}</span></div>'
                   f'<div class="q" style="margin-top:12px"><span class="lab">나</span><span class="t{" mine" if b.startswith(chr(34)) else ""}">{b.strip(chr(34))}</span></div>'
                   f'<div class="n">{c}</div></div>' for a, b, c in X['reply'])
    h += f'''<section class="slide">{T()}
  <div class="serif" style="font-size:76px">그가 이렇게 답하면</div>
  <div class="cs" style="margin-top:8px">답장별로 다음 한 줄</div>
  <div class="rp">{rows}</div>{F()}</section>
'''
    g = ''.join(f'<div><div class="who">{w}</div><div class="b">{s}</div></div>' for w, s in X['bro'])
    h += f'''<section class="slide night">{T()}
  <div class="pen" style="font-size:66px;color:#d4a95a">남자들끼리는 이렇게 말해요</div>
  <div class="grp">{g}</div>
  <div class="mean"><small>번역</small>{X['bro_mean']}</div>
  <div class="note">흔히 오가는 대화를 예시로 옮겼어요</div>{foot('남자들끼리 하는 말 · 구독자 전용')}</section>
'''
    h += f'''<section class="slide">{T()}
  <div class="letter">문장보다 <b>타이밍</b>이 먼저예요.<br>화가 가라앉은 다음,<br>그가 쉬는 시간에 보내세요.<br>보내고 나서는 재촉하지 마세요.</div>
  <div class="sign" style="margin-top:56px;text-align:right">— 지훈</div>
  <div class="lede" style="font-size:36px;color:#7a7064">저장해두고 보내기 전에 꺼내 보세요.<br>다음 주 수요일에 또 보내드릴게요.</div>{foot('남자들끼리 하는 말 · 구독자 전용')}</section>
</body></html>'''
    if key == 's03':
        h = h.replace('문장보다 <b>타이밍</b>이 먼저예요.<br>화가 가라앉은 다음,<br>그가 쉬는 시간에 보내세요.<br>보내고 나서는 재촉하지 마세요.',
                      '답이 올지는 <b>그가</b> 정해요.<br>어떤 사람으로 남을지는<br><b>당신이</b> 정해요.<br>보내기 전에 한 번만 읽어보세요.')
    open(f'{key}.html', 'w', encoding='utf-8').write(h)

RECAP = {
 'no': 1, 'date': '10.30', 'range': '10/22~10/28',
 'cards': [
  ('신호', '식을 때와 진심일 때', '행동이 말보다 먼저 바뀌어요', [
   ('#19', '"너 가고 싶은 데"', '장소는 안 정하고, 끝나는 시간부터 말해요.'),
   ('#24', '뒤돌아보지 않아요', '스킨십보다 눈 맞춤 · 앉는 자리가 먼저 멀어져요.'),
   ('#21', '연락이 숙제가 되면', '남자는 한 번에 끊지 않고, 조금씩 미뤄요.'),
   ('#29', '말이 줄어드는 건', '할 말이 없어서가 아니라, 말해봤자라서예요.'),
   ('#27', '귀찮은 걸 감수해요', '진심은 연락보다 귀찮은 쪽에서 먼저 보여요.')]),
  ('번역', '그가 한 말', '같은 말도 상황마다 뜻이 달라요', [
   ('#20', '"다음엔 내가 살게"', '썸에서 진짜 신호예요. 다음을 만들고 싶은 거예요.'),
   ('#23', '"나중에 다 말해줄게"', '안 오는 "나중"이 세 번 쌓이면, 그게 대답이에요.'),
   ('#28', '"때가 되면 하겠지"', '지금은 결혼 생각이 없다는 뜻이에요.'),
   ('#30', '"너 나 못 믿어?"', '질문을 당신의 문제로 바꾸는 말이에요.'),
   ('#31', '"너 없으면 안 돼"', '당신의 시간을 지켜주면 사랑, 막으면 불안이에요.')]),
  ('싸움 · 이별', '그의 머릿속', '이 밤과 이 시기, 그는', [
   ('#32', '연락 끊긴 첫날 밤', '그도 못 자요. 문장이 정리될 때까지 안 보낼 뿐.'),
   ('#26', '여자의 "알아서 해"', '허락이 아니라 "나를 얼마나 알아?"라는 질문이에요.'),
   ('#25', '"그동안 고마웠어"', '안 잡는 남자 중, 이미 정리가 끝난 사람의 말이에요.'),
   ('#22', '헤어지고 3개월', '당신이 괜찮아질 때쯤, 그가 흔들려요.')]),
 ],
 'one': ('한 번은 기분,', '반복되면 대답이에요.', '한 번 들은 말로 단정하지 마세요.<br>같은 말, 같은 행동이 쌓이는지 보세요.<br>쌓이고 있다면 그때 대화를 꺼내세요.'),
}

def recap(R, out):
    T = lambda: top(R['no'], R['date']); F = lambda: foot(f'이번 주 총정리 · {R["range"]}')
    h = CSS + f'''<section class="slide" id="s1">{T()}
  <div class="pen kicker">이번 주 총정리 · {R['range']}</div>
  <div class="serif h-cover">14편을<br><span class="gold">3장에</span></div>
  <div class="lede">신호 · 번역 · 싸움과 이별.<br>한 편에 한 줄씩, 저장해두고<br>헷갈릴 때 꺼내 보세요.</div>
  <div class="sign" style="margin-top:56px">— 지훈이 구독자에게만</div>{foot('남자들끼리 하는 말 · 구독자 전용')}</section>
'''
    n = len(R['cards'])
    for i, (a, b, s, ents) in enumerate(R['cards'], 1):
        rows = ''.join(f'<div class="ent"><div class="ph"><span class="no">{no}</span>{p}</div><div class="mn">{m}</div></div>' for no, p, m in ents)
        h += f'''<section class="slide" style="justify-content:flex-start;padding-top:150px">{T()}
  <div class="prog"><b>{i} / {n}</b>{bars(i, n)}</div>
  <div class="ch">{a} · <span class="gold">{b}</span></div><div class="cs">{s}</div><div class="ents">{rows}</div>{F()}</section>
'''
    o1, o2, ob = R['one']
    h += f'''<section class="slide">{T()}
  <div class="pen" style="font-size:60px;color:#5b5144">이번 주, 하나만 기억한다면</div>
  <div class="serif" style="font-size:96px;margin-top:20px">{o1}<br><span class="gold">{o2}</span></div>
  <div class="lede">{ob}</div>
  <div class="sign" style="margin-top:56px;text-align:right">— 지훈</div>{foot('남자들끼리 하는 말 · 구독자 전용')}</section>
</body></html>'''
    open(out, 'w', encoding='utf-8').write(h)

if __name__ == '__main__':
    for i in range(len(D.WEEKS)): week(i)
    recap(RECAP, 'w1030.html')
    print('ok', [w[0] for w in D.WEEKS], 'w1030')
