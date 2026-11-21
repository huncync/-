# 남자심리 처방전 예시 (11/8) — 인스타 고정 피드(4:5 캐러셀) + 스토리(9:16) + 하이라이트 표지
# 내용은 전부 지어낸 예시예요(실제 손님 내용 아님 · 화면에도 "예시" 표시). python3 sample.py → sample/*.html → node render.js
import html, os
e = html.escape
D = os.path.dirname(os.path.abspath(__file__))
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Serif+KR:wght@500;700;900&display=block">'
CSS = '''
* { box-sizing:border-box; margin:0; padding:0; }
:root { --ink:#1d2133; --mut:#585d72; --green:#1f2742; --green2:#efeaf5; --paper:#faf7f1; --line:#e6e0d4; --gold:#b9873a; --red:#b3392e; --goldl:#d9a85b; --night:#141a2e; }
body { background:#444; font-family:'Noto Sans KR',sans-serif; color:var(--ink); word-break:keep-all; }
.s { width:1080px; height:1350px; position:relative; overflow:hidden; margin-bottom:20px; background:var(--paper); padding:84px 80px 110px; display:flex; flex-direction:column; justify-content:center; }
.s:before { content:''; position:absolute; inset:26px; border:2px solid var(--line); border-radius:22px; pointer-events:none; }
.serif { font-family:'Noto Serif KR',serif; }
.eb { font-size:26px; letter-spacing:.22em; color:var(--gold); font-weight:700; }
.step { display:inline-flex; align-items:center; gap:16px; font-size:30px; font-weight:700; color:var(--green); }
.step b { width:64px; height:64px; border-radius:50%; background:var(--green); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-size:32px; }
h1 { font-family:'Noto Serif KR',serif; font-size:76px; line-height:1.18; font-weight:900; letter-spacing:-.02em; margin-top:22px; }
h2 { font-family:'Noto Serif KR',serif; font-size:56px; line-height:1.25; font-weight:900; letter-spacing:-.02em; margin-top:22px; }
.sub { font-size:32px; color:var(--mut); margin-top:20px; line-height:1.55; }
.foot { position:absolute; left:80px; right:80px; bottom:56px; display:flex; justify-content:space-between; font-size:24px; color:var(--mut); }
.sample { position:absolute; right:70px; top:70px; font-size:22px; font-weight:700; color:var(--red); border:2px solid var(--red); border-radius:999px; padding:6px 18px; transform:rotate(4deg); background:#fff8; }
.card { background:#fff; border:2px solid var(--line); border-radius:18px; padding:30px 34px; margin-top:26px; }
.tag { font-size:22px; font-weight:700; letter-spacing:.14em; color:var(--green); margin-bottom:10px; }
.ev { background:var(--paper); border:2px solid var(--line); border-radius:14px; padding:22px 28px; margin-top:16px; }
.ev p { font-size:31px; line-height:1.6; color:#3d4642; }
.lg p { font-size:34px; line-height:1.62; margin-top:6px; }
.con { background:var(--green2); border-left:10px solid var(--green); border-radius:0 14px 14px 0; padding:24px 30px; margin-top:20px; font-size:35px; font-weight:700; color:#1f2742; line-height:1.5; }
.qt { font-weight:700; background:#f5e8cf; border-radius:6px; padding:0 6px; }
.it { font-size:40px; font-weight:900; color:var(--green); border-left:8px solid var(--gold); padding-left:18px; line-height:1.35; }
ul.chk { list-style:none; margin-top:24px; } ul.chk li { font-size:34px; line-height:1.5; padding:16px 0 16px 64px; position:relative; border-bottom:2px dashed var(--line); }
ul.chk li:before { content:'✓'; position:absolute; left:0; top:16px; width:44px; height:44px; border:3px solid var(--green); border-radius:8px; color:var(--green); font-weight:900; text-align:center; line-height:40px; font-size:28px; }
ul.chk li small { display:block; font-size:26px; color:var(--mut); }
.rx { background:#fff; border:2px solid var(--line); border-radius:18px; padding:26px 32px; margin-top:20px; }
.rx b { font-size:37px; font-weight:900; color:var(--green); } .rx b i { font-family:'Noto Serif KR',serif; color:var(--red); margin-right:10px; }
.rx p { font-size:30px; color:#3d4642; margin-top:8px; line-height:1.55; }
.price { display:grid; grid-template-columns:1fr; gap:18px; margin-top:30px; }
.price > div { background:#fff; border:2px solid var(--line); border-radius:18px; padding:24px 32px; display:flex; justify-content:space-between; align-items:center; }
.price > div.hot { border:4px solid var(--green); background:var(--green2); }
.price b { font-size:38px; font-weight:900; } .price span { font-size:26px; color:var(--mut); display:block; margin-top:4px; } .price em { font-style:normal; font-size:40px; font-weight:900; color:var(--green); }
.cta { margin-top:auto; background:var(--green); color:#fff; border-radius:20px; padding:30px 36px; font-size:36px; font-weight:700; line-height:1.45; text-align:center; }
.cta small { display:block; font-size:24px; color:#d9a85b; font-weight:500; margin-top:8px; }
.mini { width:540px; height:660px; margin:36px auto 0; background:linear-gradient(160deg,#2a3152,#141a2e 70%); color:#ece8df; border:3px solid var(--goldl); border-radius:20px; padding:40px; box-shadow:0 30px 60px rgba(0,0,0,.18); transform:rotate(-3deg); position:relative; }
.mini .rxl { font-family:'Noto Serif KR',serif; font-style:italic; font-size:96px; font-weight:900; color:var(--goldl); line-height:1; }
.mini .t { font-family:'Noto Serif KR',serif; font-size:44px; font-weight:900; margin-top:14px; }
.mini table { width:100%; border-collapse:collapse; margin-top:26px; font-size:22px; } .mini td { border:2px solid var(--line); padding:10px 14px; } .mini td { border-color:rgba(236,232,223,.2)!important; } .mini td:first-child { background:rgba(217,168,91,.14); color:var(--goldl); font-weight:700; width:130px; }
.mini .dx { background:rgba(125,106,156,.3); border:1px solid rgba(217,168,91,.4); color:#ece8df; border-radius:12px; padding:20px 22px; margin-top:24px; font-size:22px; line-height:1.6; } .mini .dx b { color:#d9a85b; }
.stamp { position:absolute; width:150px; height:150px; border:5px solid var(--goldl); border-radius:50%; color:var(--goldl); background:rgba(20,26,46,.6); display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:'Noto Serif KR',serif; font-weight:900; font-size:22px; line-height:1.3; transform:rotate(-12deg); opacity:.88; }
.stamp b { font-size:34px; }
.q { background:var(--green2); border-radius:14px; padding:24px 30px; font-size:36px; font-weight:700; margin-top:24px; }
'''
STAMP = '<div class="stamp" style="right:{r}px;bottom:{b}px">남자들끼리<br><b>處方</b>하는 말</div>'
FOOT = lambda i, n: f'<div class="foot"><span>@mszexc · 남자들끼리 하는 말</span><span>{i}/{n}</span></div>'
SAMPLE = '<div class="sample">예시</div>'

def slides():
    S = []
    S.append(f'''<div class="eb">MEN'S PSYCHOLOGY · PRESCRIPTION</div>
<h1>그 사람 마음,<br>처방전으로<br>받아보세요</h1>
<div class="sub">1:1 남자 심리 분석은 이렇게 진행돼요.<br>남자가 직접 읽고, 남자 입장에서 씁니다.</div>
<div class="mini"><div class="rxl">Rx</div><div class="t">남자심리 처방전</div>
<table><tr><td>환자명</td><td>OO 님</td></tr><tr><td>처방 구분</td><td>A · 남자 심리 분석</td></tr><tr><td>처방</td><td>박지훈 (@mszexc)</td></tr></table>
<div class="dx">그는 아직 당신을 좋아합니다.<br><b>다만 지금 필요한 건 확인이 아니라 시간입니다.</b></div>{STAMP.format(r=-60, b=60)}</div>''')
    S.append(f'''<div class="step"><b>1</b>신청서를 써 주세요</div>
<h2>둘의 이야기를<br>편하게 적어 주세요</h2>
<ul class="chk">
<li>어떻게 만났고, 지금 어떤 상황인지<small>누가 먼저 다가갔는지 · 주로 무엇 때문에 싸웠는지</small></li>
<li>해석받고 싶은 그의 말 · 행동<small>들은 그대로 적어 주시면 더 정확해요</small></li>
<li>카톡 캡처 (최대 10장)<small>최근 대화 + 분위기가 바뀐 때</small></li>
<li>꼭 답받고 싶은 질문 1~3개</li>
</ul>
<div class="sub" style="margin-top:26px">얼굴 사진(관상)은 선택이에요. 다 못 채워도 괜찮아요.</div>''')
    S.append(f'''{SAMPLE}<div class="step"><b>2</b>그의 말을 번역해 드려요</div>
<div class="card"><div class="it">"요즘 일이 좀 많아서 그래"</div>
<div class="ev"><div class="tag">근거</div><p>· 카톡 10/12 <span class="qt">"이번 주는 좀 바쁠 듯"</span><br>· 카톡 10/19 <span class="qt">"정리되면 연락할게"</span></p></div>
<div class="lg" style="margin-top:20px"><div class="tag">논리</div><p>바쁜 남자는 "언제 보자"를 같이 말해요.<br>날짜 없이 미루기만 한다면, 지금은 거리를 재고 있는 거예요.</p></div>
<div class="con">→ 바빠서가 아니라, 생각을 정리할 시간이 필요한 거예요.</div></div>''')
    S.append(f'''{SAMPLE}<div class="step"><b>3</b>모든 해석에 근거를 붙여요</div>
<h2>"그냥 느낌"이 아니라<br>당신 카톡에서 찾아요</h2>
<div class="card"><div class="tag">카톡 검사 결과</div>
<div class="ev"><p>· 10/05 답장 평균 10분 → 10/20 평균 3시간<br>· 먼저 보낸 카톡 주 5회 → 주 1회<br>· "보고 싶다" 마지막 10/08</p></div>
<div class="con">→ 연락은 줄었지만 끊지는 않았어요.<br>마음이 식은 게 아니라, 멈춰 서 있는 상태예요.</div></div>''')
    S.append(f'''{SAMPLE}<div class="step"><b>4</b>당신의 질문에 답해요</div>
<div class="q">Q. 지금 먼저 연락해도 될까요?</div>
<div class="card"><div class="lg"><div class="tag">논리</div><p>지금 연락하면 그에게는 "또 확인하려 한다"로 들려요.<br>남자는 정리할 시간을 존중받을 때 먼저 돌아와요.</p></div>
<div class="con">→ 일주일은 기다리세요.<br>보낼 때는 질문 말고, 짧은 안부 한 줄로.</div></div>
<div class="sub" style="margin-top:26px">질문은 1~3개, 하나도 빼놓지 않고 답해 드려요.</div>''')
    S.append(f'''{SAMPLE}<div class="step"><b>5</b>처방까지 드려요</div>
<h2>그래서, 이제<br>무엇을 하면 되는지</h2>
<div class="rx"><b><i>Rx</i>먼저 연락하지 마십시오</b><p>정리할 시간을 존중받을 때, 남자는 먼저 돌아옵니다.</p></div>
<div class="rx"><b><i>Rx</i>"서운해" 대신 "응원해"</b><p>반복되는 서운함은 "다 내 탓인가"로 들립니다.</p></div>
<div class="rx"><b><i>Rx</i>일주일 뒤, 짧은 안부 한 줄</b><p>답장은 재촉하지 마십시오.</p></div>''')
    S.append(f'''<div class="step"><b>6</b>A4 처방전으로 받아요</div>
<h2>72시간 안에<br>PDF 처방전으로 보내드려요</h2>
<ul class="chk">
<li>진단 · 그의 연애 성향</li>
<li>말 · 행동 번역 (근거 + 논리)</li>
<li>카톡 검사 결과 · 갈등이 반복된 이유</li>
<li>질문에 대한 답 · 처방</li>
</ul>
<div class="mini" style="width:420px;height:300px;margin-top:30px;transform:rotate(2deg);padding:28px"><div class="rxl" style="font-size:64px">Rx</div><div class="t" style="font-size:32px">남자심리 처방전</div><div class="sub" style="font-size:20px;margin-top:8px">A4 9~13쪽 · 손님마다 따로 작성</div>{STAMP.format(r=-36, b=-46)}</div>''')
    S.append(f'''<div class="eb">HOW TO APPLY</div>
<h2>신청은<br>카카오채널 채팅으로</h2>
<div class="price">
<div><div><b>A · 남자 심리 분석</b><span>성향 · 말 번역 · 마음 단계 · 질문 답</span></div><em>5만</em></div>
<div class="hot"><div><b>B · 분석 + 대본 ★</b><span>A + 상황별 대본 4종 · 피드백 2회</span></div><em>10만</em></div>
<div><div><b>C · 4주 플랜</b><span>B + 4주 점검 · 첨삭 · 월 3명</span></div><em>39만</em></div>
</div>
<div class="cta">카카오채널 「남자가 말하는 남자심리」<br>지금 상황을 한두 줄 보내주세요<small>프로필 링크에서 바로 · 남자 입장 해석이며 의료 · 치료 목적이 아닙니다</small></div>''')
    return S

def page(slides, cls='s'):
    n = len(slides)
    body = ''.join(f'<section class="{cls}" id="s{i}">{s}{FOOT(i, n)}</section>' for i, s in enumerate(slides, 1))
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>{body}</body></html>'

HL = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">{FONTS}<style>{CSS}
.hl {{ width:1080px; height:1920px; background:linear-gradient(160deg,#2a3152,#141a2e 70%); display:flex; align-items:center; justify-content:center; }}
.hl div {{ width:620px; height:620px; border-radius:50%; background:var(--paper); border:10px solid #d9a85b; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.hl b {{ font-family:'Noto Serif KR',serif; font-style:italic; font-size:240px; color:var(--green); line-height:1; }}
.hl span {{ font-size:54px; font-weight:900; color:var(--green); margin-top:10px; }}
</style></head><body><section class="hl"><div><b>Rx</b><span>처방전</span></div></section></body></html>'''

if __name__ == '__main__':
    os.makedirs(f'{D}/sample', exist_ok=True)
    open(f'{D}/sample/feed.html', 'w', encoding='utf-8').write(page(slides()))
    open(f'{D}/sample/highlight.html', 'w', encoding='utf-8').write(HL)
    print('ok', len(slides()))
