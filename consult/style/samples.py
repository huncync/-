# 상담 탭 문서 디자인 시안 3종 (11/23) — 채널 안내문 · 신청서 · 결과물 틀 첫 장 (1080×1350)
# python3 samples.py → samples.html → node ../../carousel/photo_story/style_samples/render.js <html> <out>
import os
D = os.path.dirname(os.path.abspath(__file__))
FONT = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700;800&family=Noto+Sans+KR:wght@400;500;700;900&display=block'>"
BASE = "*{box-sizing:border-box;margin:0;padding:0}body{background:#555;font-family:'Noto Sans KR',sans-serif;word-break:keep-all}section{width:1080px;height:1350px;position:relative;overflow:hidden;margin-bottom:20px}.mj{font-family:'Nanum Myeongjo',serif}"

# ① 다크 골드 · 프리미엄 (캐러셀 필름 무드와 같은 톤)
DARK_CSS = """
.dk{background:radial-gradient(120% 80% at 50% 0%,#2a2520,#121110 70%);color:#efe8dc;padding:88px 84px}
.dk .tag{font-size:24px;letter-spacing:.35em;color:#c9a24e}
.dk h1{font-family:'Nanum Myeongjo',serif;font-size:66px;line-height:1.25;margin:22px 0 26px;font-weight:800}
.dk .lead{font-size:30px;line-height:1.6;color:#cfc6b6}
.dk .badge{display:inline-block;margin-top:30px;border:2px solid #c9a24e;color:#e5c172;padding:10px 22px;border-radius:999px;font-size:26px;font-weight:700}
.dk .card{margin-top:30px;border:1.5px solid rgba(201,162,78,.55);border-radius:22px;padding:30px 34px;background:rgba(255,255,255,.03)}
.dk .card.hot{border-color:#e5c172;background:rgba(229,193,114,.08)}
.dk .row{display:flex;justify-content:space-between;align-items:flex-end}
.dk .nm{font-size:34px;font-weight:700}.dk .nm small{display:block;font-size:24px;color:#b9ae9c;font-weight:400;margin-top:6px}
.dk .pr{text-align:right}.dk .pr s{font-size:24px;color:#8d8475}.dk .pr b{display:block;font-family:'Nanum Myeongjo',serif;font-size:58px;color:#e5c172;line-height:1.1}
.dk .pr b em{font-style:normal;font-size:30px;margin-left:4px}
.dk .li{font-size:25px;color:#cfc6b6;margin-top:14px;line-height:1.5}
.dk .star{font-size:22px;background:#e5c172;color:#1a1712;padding:4px 12px;border-radius:8px;margin-left:10px;vertical-align:middle;font-weight:900}
.dk .q{margin-top:26px;border-bottom:1.5px solid rgba(201,162,78,.4);padding-bottom:18px}
.dk .q .n{font-family:'Nanum Myeongjo',serif;color:#e5c172;font-size:34px;margin-right:14px}
.dk .q .t{font-size:30px;font-weight:700}.dk .q .h{font-size:23px;color:#9f9686;margin-top:8px}
.dk .note{font-size:22px;color:#9f9686;line-height:1.6;margin-top:10px}
.dk .sec{display:flex;gap:22px;margin-top:30px}.dk .sec .n{font-family:'Nanum Myeongjo',serif;font-size:48px;color:#e5c172;width:70px}
.dk .sec .t{font-size:31px;font-weight:700}.dk .sec .h{font-size:24px;color:#a99f8e;margin-top:6px;line-height:1.5}
.dk .ex{margin-top:34px;border-radius:18px;background:rgba(255,255,255,.05);padding:26px 30px;font-size:26px;line-height:1.7}
.dk .ex .x{color:#9a8f80;text-decoration:line-through}.dk .ex .o{color:#f3dfae;font-weight:700}
.dk .ft{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;font-size:22px;color:#7d7466;letter-spacing:.08em}
"""
# ② 카톡 대화형 (캐러셀 카톡 화면과 같은 톤)
KT_CSS = """
.kt{background:#b9cddc;padding:0}
.kt .bar{height:120px;background:#a9bfd0;display:flex;align-items:center;padding:0 48px;font-size:34px;font-weight:700;color:#1d2730}
.kt .bar small{font-size:24px;font-weight:500;margin-left:14px;color:#4a5866}
.kt .body{padding:34px 44px}
.kt .msg{display:flex;gap:18px;margin-bottom:22px}.kt .av{width:84px;height:84px;border-radius:30px;background:#2b2b2b;color:#e5c172;font-family:'Nanum Myeongjo',serif;font-size:30px;display:flex;align-items:center;justify-content:center;flex:none}
.kt .who{font-size:22px;color:#33414d;margin-bottom:8px}
.kt .b{background:#fff;border-radius:6px 30px 30px 30px;padding:24px 30px;font-size:29px;line-height:1.55;color:#191919;max-width:820px;box-shadow:0 2px 0 rgba(0,0,0,.05)}
.kt .b + .b{margin-top:12px}
.kt .b h3{font-size:31px;margin-bottom:6px}.kt .b .s{font-size:24px;color:#666}
.kt .pz{display:flex;justify-content:space-between;align-items:center;border-top:1px dashed #ddd;padding-top:14px;margin-top:14px}
.kt .pz s{color:#999;font-size:23px}.kt .pz b{font-size:40px;font-weight:900}
.kt .hot{outline:4px solid #fee500}.kt .y{background:#fee500;border-radius:8px;padding:2px 10px;font-weight:900;font-size:22px;margin-left:8px}
.kt .me{display:flex;justify-content:flex-end;margin:6px 0 22px}.kt .me .b{background:#fee500;border-radius:30px 6px 30px 30px;color:#2a2a2a}
.kt .blank{color:#9a8a1a;letter-spacing:.1em}
"""
# ③ 화이트 리포트 (매거진 · 신뢰감)
WH_CSS = """
.wh{background:#fbfaf7;color:#161514;padding:90px 88px}
.wh .tag{font-size:23px;letter-spacing:.3em;color:#8a2c2c;font-weight:700}
.wh h1{font-family:'Nanum Myeongjo',serif;font-size:70px;line-height:1.22;margin:20px 0 24px;font-weight:800}
.wh .lead{font-size:29px;line-height:1.65;color:#4a4744}
.wh .rule{height:3px;background:#161514;margin:36px 0 6px}.wh .rule2{height:1px;background:#d9d4cc;margin:0}
.wh .it{display:grid;grid-template-columns:86px 1fr auto;gap:18px;padding:28px 0;border-bottom:1px solid #d9d4cc;align-items:center}
.wh .it .n{font-family:'Nanum Myeongjo',serif;font-size:50px;color:#8a2c2c}
.wh .it .t{font-size:33px;font-weight:700}.wh .it .t small{display:block;font-size:23px;color:#77716a;font-weight:400;margin-top:6px}
.wh .it .p{text-align:right}.wh .it .p s{font-size:22px;color:#a39d95}.wh .it .p b{display:block;font-size:40px;font-weight:900}
.wh .chip{display:inline-block;font-size:20px;background:#8a2c2c;color:#fff;padding:3px 10px;border-radius:4px;margin-left:10px;vertical-align:middle}
.wh .open{margin-top:26px;font-size:24px;color:#8a2c2c;font-weight:700}
.wh .f{padding:24px 0;border-bottom:1px solid #d9d4cc}.wh .f .t{font-size:29px;font-weight:700}.wh .f .t i{font-style:normal;font-family:'Nanum Myeongjo',serif;color:#8a2c2c;margin-right:12px}
.wh .f .h{font-size:22px;color:#8c867e;margin-top:6px}.wh .f .ln{height:46px;border-bottom:2px dotted #c9c2b7}
.wh .note{font-size:22px;color:#77716a;line-height:1.6;background:#f1ede6;padding:20px 24px;border-left:4px solid #8a2c2c;margin-top:28px}
.wh .ex{margin-top:30px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.wh .ex div{padding:22px 24px;font-size:24px;line-height:1.6;border:1px solid #d9d4cc}.wh .ex .o{border:2px solid #161514;font-weight:700}
.wh .ex b{display:block;font-size:20px;letter-spacing:.2em;margin-bottom:8px;color:#8a2c2c}
.wh .ft{position:absolute;left:88px;right:88px;bottom:56px;display:flex;justify-content:space-between;font-size:21px;color:#9c968e;border-top:1px solid #d9d4cc;padding-top:18px}
"""

def dark():
    g = f"""<section class="dk"><div class="tag">1:1 MAN'S MIND ANALYSIS</div>
<h1>그 사람이 왜 그러는지,<br>이제 뭐라고 보내야 하는지.</h1>
<div class="lead">남자가 직접, 그 사람의 마음을 번역해 드려요.<br>관상 · 카톡 · 상황을 남자 입장에서 봐요.</div>
<div class="badge">12/31까지 오픈가 · 1/1부터 정가</div>
<div class="card"><div class="row"><div class="nm">A. 남자 심리 분석<small>그가 왜 그러는지 알고 싶은 분</small></div><div class="pr"><s>69,000원</s><b>49,000<em>원</em></b></div></div>
<div class="li">질문지 + 카톡 캡처 10장 + 관상 · 서면 리포트 · 72시간 안에</div></div>
<div class="card hot"><div class="row"><div class="nm">B. 분석 + 대본<span class="star">추천</span><small>"그래서 뭐라고 보내야 해?"까지</small></div><div class="pr"><s>129,000원</s><b>99,000<em>원</em></b></div></div>
<div class="li">A 전체 + 상황별 대본 4종 + 7일 안 피드백 2회</div></div>
<div class="card"><div class="row"><div class="nm">T. 전화 분석<small>30분 · 60분 예약제</small></div><div class="pr"><s>59,000원~</s><b>49,000<em>원~</em></b></div></div></div>
<div class="ft"><span>남자들끼리 하는 말</span><span>1 / 4</span></div></section>"""
    f = f"""<section class="dk"><div class="tag">APPLICATION</div>
<h1>신청서</h1><div class="note">※ 남자 입장에서 상황을 해석해 드리는 서비스예요. 의료 · 치료 목적이 아니에요.<br>※ 다 못 채워도 괜찮아요. 아는 만큼만 적어주시면 나머지는 제가 여쭤볼게요.</div>
<div class="q"><span class="n">00</span><span class="t">신청 상품 · 입금자명</span><div class="h">A / B / C / 전화 중 하나 · 추가 옵션이 있으면 같이</div></div>
<div class="q"><span class="n">01</span><span class="t">이름 · 나이 · MBTI</span><div class="h">나 ___ / 그 ___ (MBTI는 모르면 비워두세요)</div></div>
<div class="q"><span class="n">02</span><span class="t">지금 관계</span><div class="h">연애 중 / 썸 / 헤어짐 / 재회 고민 / 기타</div></div>
<div class="q"><span class="n">03</span><span class="t">만난 기간</span><div class="h">헤어졌다면 사귄 기간 + 헤어진 지 얼마나</div></div>
<div class="q"><span class="n">04</span><span class="t">얼굴 사진 (선택)</span><div class="h">나 1장 · 그 1~2장 · 분석 후 바로 삭제해요</div></div>
<div class="ft"><span>남자들끼리 하는 말 · 신청서</span><span>1 / 4</span></div></section>"""
    r = f"""<section class="dk"><div class="tag">REPORT</div>
<h1>결과물은<br>이렇게 드려요</h1>
<div class="sec"><div class="n">01</div><div><div class="t">관상으로 본 그의 연애 성향</div></div></div>
<div class="sec"><div class="n">02</div><div><div class="t">그의 말 · 행동 번역</div><div class="h">들은 그대로의 말을, 남자 입장으로</div></div></div>
<div class="sec"><div class="n">03</div><div><div class="t">지금 그의 마음 단계</div><div class="h">지친 중 / 흔들리는 중 / 정리하는 중</div></div></div>
<div class="sec"><div class="n">04</div><div><div class="t">갈등이 반복되는 진짜 이유</div></div></div>
<div class="ex"><div class="x">"우리 얘기 좀 해. 언제까지 이럴 건데?"</div><div class="o">→ "그날 내가 좀 날카로웠던 것 같아. 생각나서 연락했어. 편할 때 답해줘."</div></div>
<div class="ft"><span>남자들끼리 하는 말 · 결과물</span><span>A · B 예시</span></div></section>"""
    return g + f + r

def kakao():
    av = '<div class="av">지훈</div>'
    g = f"""<section class="kt"><div class="bar">‹ 남자가 말하는 남자심리<small>1:1 분석 안내</small></div><div class="body">
<div class="msg">{av}<div><div class="who">지훈</div><div class="b">그 사람이 왜 그러는지,<br>이제 뭐라고 보내야 하는지.<br><span class="s">남자 입장에서 직접 번역해 드려요.</span></div>
<div class="b"><h3>A. 남자 심리 분석</h3><span class="s">질문지 + 카톡 캡처 10장 + 관상 · 72시간 안에</span><div class="pz"><s>정가 69,000원</s><b>49,000원</b></div></div>
<div class="b hot"><h3>B. 분석 + 대본 <span class="y">추천</span></h3><span class="s">A 전체 + 상황별 대본 4종 + 피드백 2회</span><div class="pz"><s>정가 129,000원</s><b>99,000원</b></div></div>
<div class="b"><h3>T. 전화 분석</h3><span class="s">30분 49,000원 · 60분 89,000원 (예약제)</span></div></div></div>
<div class="me"><div class="b">B 신청할게요!</div></div>
<div class="msg">{av}<div><div class="b">12/31까지 오픈가예요 🙂<br><span class="s">채팅으로 상품만 남겨주시면 바로 안내드려요.</span></div></div></div>
</div></section>"""
    f = f"""<section class="kt"><div class="bar">‹ 남자가 말하는 남자심리<small>신청서</small></div><div class="body">
<div class="msg">{av}<div><div class="b">입금 확인됐어요. 아래 질문에 답만 보내주세요.<br><span class="s">다 못 채워도 괜찮아요. 제가 여쭤볼게요.</span></div>
<div class="b"><h3>Q1. 지금 관계가 어때요?</h3><span class="s">연애 중 / 썸 / 헤어짐 / 재회 고민</span></div></div></div>
<div class="me"><div class="b">헤어진 지 2주요 <span class="blank">(예시)</span></div></div>
<div class="msg">{av}<div><div class="b"><h3>Q2. 둘의 이야기를 편하게 적어주세요</h3><span class="s">어떻게 만났는지 · 주로 뭘로 싸웠는지 · 지금 연락 상태</span></div>
<div class="b"><h3>Q3. 해석받고 싶은 그의 말</h3><span class="s">들은 그대로 적어주시면 더 정확해요</span></div></div></div>
<div class="me"><div class="b">"요즘 좀 바빠" 이 말이요 <span class="blank">(예시)</span></div></div>
</div></section>"""
    r = f"""<section class="kt"><div class="bar">‹ 남자가 말하는 남자심리<small>결과물</small></div><div class="body">
<div class="msg">{av}<div><div class="who">지훈 · 분석 결과가 도착했어요</div>
<div class="b"><h3>① 그의 연애 성향</h3><span class="s">관상 · 대화 습관으로 본 성향</span></div>
<div class="b"><h3>② "요즘 좀 바빠"의 진짜 뜻</h3><span class="s">그의 말 · 행동을 남자 입장으로 번역</span></div>
<div class="b"><h3>③ 지금 그의 마음 단계</h3><span class="s">지친 중 / 흔들리는 중 / 정리하는 중</span></div>
<div class="b hot"><h3>④ 이렇게 보내세요 (B)</h3><span class="s">✕ "언제까지 이럴 건데?"<br>○ "그날 내가 좀 날카로웠던 것 같아. 편할 때 답해줘."</span></div></div></div>
</div></section>"""
    return g + f + r

def white():
    g = f"""<section class="wh"><div class="tag">1:1 남자 심리 분석</div>
<h1>그 사람의 마음,<br>남자가 번역해 드려요.</h1>
<div class="lead">관상 · 카톡 · 상황을 함께 보고, 남자 입장에서 답을 드려요.</div>
<div class="rule"></div><div class="rule2"></div>
<div class="it"><div class="n">A</div><div class="t">남자 심리 분석<small>그가 왜 그러는지 · 서면 리포트 · 72시간</small></div><div class="p"><s>69,000원</s><b>49,000원</b></div></div>
<div class="it"><div class="n">B</div><div class="t">분석 + 대본<span class="chip">추천</span><small>A + 상황별 대본 4종 + 피드백 2회</small></div><div class="p"><s>129,000원</s><b>99,000원</b></div></div>
<div class="it"><div class="n">C</div><div class="t">4주 플랜<small>매주 점검 + 다음 대본 · 월 3명</small></div><div class="p"><s>490,000원</s><b>390,000원</b></div></div>
<div class="it"><div class="n">T</div><div class="t">전화 분석<small>30분 · 60분 예약제</small></div><div class="p"><s>59,000원~</s><b>49,000원~</b></div></div>
<div class="open">12/31까지 오픈가 · 1/1부터 정가</div>
<div class="ft"><span>남자들끼리 하는 말</span><span>1 / 4</span></div></section>"""
    f = f"""<section class="wh"><div class="tag">APPLICATION</div>
<h1>신청서</h1>
<div class="note">남자 입장에서 상황을 해석해 드리는 서비스예요. 다 못 채워도 괜찮아요. 아는 만큼만 적어주세요.</div>
<div class="f"><div class="t"><i>00</i>신청 상품 · 입금자명</div><div class="ln"></div></div>
<div class="f"><div class="t"><i>01</i>이름 · 나이 · MBTI</div><div class="h">나 ___ / 그 ___</div><div class="ln"></div></div>
<div class="f"><div class="t"><i>02</i>지금 관계</div><div class="h">연애 중 / 썸 / 헤어짐 / 재회 고민 / 기타</div><div class="ln"></div></div>
<div class="f"><div class="t"><i>03</i>만난 기간</div><div class="h">헤어졌다면 사귄 기간 + 헤어진 지 얼마나</div><div class="ln"></div></div>
<div class="ft"><span>남자들끼리 하는 말 · 신청서</span><span>1 / 4</span></div></section>"""
    r = f"""<section class="wh"><div class="tag">REPORT</div>
<h1>결과물은<br>이렇게 드려요</h1>
<div class="rule"></div><div class="rule2"></div>
<div class="it"><div class="n">01</div><div class="t">관상으로 본 그의 연애 성향</div><div></div></div>
<div class="it"><div class="n">02</div><div class="t">그의 말 · 행동 번역<small>들은 그대로의 말을 남자 입장으로</small></div><div></div></div>
<div class="it"><div class="n">03</div><div class="t">지금 그의 마음 단계<small>지친 중 / 흔들리는 중 / 정리하는 중</small></div><div></div></div>
<div class="it"><div class="n">04</div><div class="t">갈등이 반복되는 진짜 이유</div><div></div></div>
<div class="ex"><div><b>BEFORE</b>"우리 얘기 좀 해. 언제까지 이럴 건데?"</div><div class="o"><b>AFTER</b>"그날 내가 좀 날카로웠던 것 같아. 편할 때 답해줘."</div></div>
<div class="ft"><span>남자들끼리 하는 말 · 결과물</span><span>A · B 예시</span></div></section>"""
    return g + f + r

if __name__ == '__main__':
    html = f"<!doctype html><html><head><meta charset='utf-8'>{FONT}<style>{BASE}{DARK_CSS}{KT_CSS}{WH_CSS}</style></head><body>{dark()}{kakao()}{white()}</body></html>"
    open(os.path.join(D, 'samples.html'), 'w', encoding='utf-8').write(html)
    print('ok')
