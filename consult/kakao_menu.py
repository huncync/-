# 카카오채널 채팅방 리스트 메뉴 (11/1) — 메뉴 하나 = 이름(20자) + 응답 메시지(400자) + 이미지(800×400) + 버튼(10자)
# python3 kakao_menu.py → kakao_menu/km.html (렌더는 .work/rkm.js) · 채널 글이라 "상담"은 쓰지 않아요(금칙어)
import html
e = html.escape

# (키, 메뉴명, 이미지: 윗줄 · 제목 · 가격 · 항목들, 응답 메시지, 버튼)
MENU = [
 ('m1', 'A. 남자 심리 분석 · 4.9만', ('그가 왜 그러는지 알고 싶을 때', 'A. 남자 심리 분석', '69,000원|49,000원',
   ['관상 · 카톡 10장 · 상황을 남자 입장에서', '그의 성향 / 말 번역 / 지금 마음 단계', '서면 리포트 · 72시간 안 · 추가 질문 1회']),
  '''A. 남자 심리 분석 · 49,000원 (정가 69,000원 · 12/31까지 오픈가)

그가 왜 그러는지 알고 싶은 분께 드려요.

· 관상(본인 · 상대) + 카톡 캡처 10장 + 지금 상황
· 서면 리포트: 그의 성향 / 그가 한 말 번역 / 지금 마음 단계 / 갈등이 반복되는 이유
· 72시간 안에 전달 · 추가 질문 1회
· 주 10건 한정

신청은 채팅으로 "A 신청"이라고 남겨주세요.''', '없음'),
 ('m2', 'B. 분석+대본 · 9.9만 ★추천', ('그래서 뭐라고 보내야 해?', 'B. 분석 + 대본', '129,000원|99,000원',
   ['A의 모든 내용', '상황별 대본 4종 · 보낼 시간 · 피할 말', '7일 안 피드백 2회 · 주 5건']),
  '''B. 분석 + 보낼 말 대본 · 99,000원 (정가 129,000원 · 12/31까지 오픈가) ★추천

"그래서 뭐라고 보내야 해?"까지 알고 싶은 분께 드려요.

· A의 모든 내용
· 상황별 대본 4종: 첫 연락 / 답장 왔을 때 / 만났을 때 / 반응 없을 때
· 보내기 좋은 시간대와 하지 말아야 할 말
· 7일 안 피드백 2회 (1회 = 메시지 1개 + 캡처 3장)
· 주 5건 한정

B를 신청하신 선착순 10분께 카톡 첨삭 2건을 함께 드려요.
신청은 채팅으로 "B 신청"이라고 남겨주세요.''', '없음'),
 ('m3', 'C. 4주 플랜 · 39만', ('재회 · 관계 회복, 끝까지 같이', 'C. 4주 플랜', '490,000원|390,000원',
   ['B의 모든 내용', '4주 동안 주 1회 점검 + 다음 대본', '보내기 전 카톡 첨삭 주 3건 · 월 3명']),
  '''C. 재회 · 관계 회복 4주 플랜 · 390,000원 (정가 490,000원 · 12/31까지 오픈가)

한 번의 답이 아니라, 끝까지 같이 가고 싶은 분께 드려요.

· B의 모든 내용
· 4주 동안 주 1회 점검 + 그다음 대본
· 보내기 전 카톡 첨삭 주 3건
· 4주 뒤 정리 리포트
· 월 3명 한정

A · B를 받고 30일 안에 C로 바꾸시면, 이미 내신 금액을 빼드려요.
신청은 채팅으로 "C 신청"이라고 남겨주세요.
먼저 상황을 짧게 들려주시면 C가 맞는지부터 말씀드릴게요.''', '없음'),
 ('m7', 'T. 실시간 분석 · 4.9만~', ('미리 분석하고, 통화로 설명해요', 'T. 실시간 분석', '30분:59,000원|49,000원;60분:99,000원|89,000원',
   ['신청서로 미리 심리 분석 → 통화로 설명', '시간 안에서 질문은 원하는 만큼', '전화 · 카톡 중 선택 · 요약 3줄 · 주 5건']),
  '''T. 실시간 분석 · 전화 또는 카톡 (예약제 · 주 5건)

💰 30분 49,000원 (정가 59,000원)
💰 60분 89,000원 (정가 99,000원)
12/31까지 오픈가

· 전화 · 카톡 실시간 중 선택 (가격 같아요)
· 시작 전: A와 같은 신청서 + 카톡 캡처 10장 → 미리 심리 분석
· 30분 · 60분 동안: 분석 결과를 먼저 설명드리고, 남은 시간엔 질문을 원하는 만큼
· 끝난 뒤 핵심 요약 3줄을 카톡으로
· 다음 예약이 비면 30분 단위 연장 (같은 가격)

일정 변경은 하루 전까지 1회
취소: 하루 전까지 전액 · 당일 50% · 불참 시 환불 불가

신청은 채팅으로 "전화 30분 신청" · "카톡 30분 신청"처럼 남겨주세요.''', '없음'),
 ('m4', '한 줄 첨삭 · 옵션', ('보내기 전에 한 번만', 'S. 한 줄 첨삭 · 옵션', '',
   ['S. 한 줄 첨삭 2만 · 처음이신 분도 · 24시간 안', '7일 안 A · B 신청 시 2만 원 빼드려요', '신청자 옵션: 3건 묶음 5만 · 추가 질문 2만 · 급행 +3만']),
  '''S. 보내기 전 한 줄 첨삭 · 20,000원 (처음이신 분도)

· 보내려는 메시지 1개 + 앞 대화 캡처 3장
· 24시간 안에 고친 문장 · 바꾼 이유 · 보낼 시간 · 다음 한 줄
· 7일 안에 A · B를 신청하시면 2만 원을 빼드려요
신청은 채팅으로 "첨삭 신청"이라고 남겨주세요.

추가 옵션 (분석을 받으신 분만)
· 카톡 첨삭 3건 묶음 50,000원 (30일 안 사용)
· 추가 질문 1회 20,000원 (24시간 안)
· 24시간 급행 +30,000원 (A · B · 하루 1건)
· 답장 왔을 때 긴급 첨삭 30,000원 (6시간 안 · 하루 1건)

기한은 채팅 가능 시간 안에서 세요.''', '없음'),
 ('m5', '신청 방법', ('3단계면 끝나요', '신청 방법', '',
   ['① 채팅으로 "A · B · C 신청"', '② 입금 확인 → 신청서 보내드려요', '③ 신청서 + 사진 + 캡처 → 분석 시작']),
  '''신청 방법

① 채팅으로 원하는 상품을 남겨주세요 ("B 신청")
② 입금 안내를 드려요. 입금이 확인되면 신청서를 보내드려요
③ 신청서를 채워 보내고, 사진 · 캡처를 이어서 보내주세요
④ 다 도착한 때부터 72시간 안에 결과물을 드려요

사진은 분석에만 쓰고 끝나면 바로 지워요. 어디에도 공유하지 않아요.''', '없음'),
 ('m6', '꼭 읽어주세요', ('신청 전에 한 번만', '꼭 읽어주세요', '',
   ['남자 입장에서 해석해 드리는 서비스', '결과를 100% 장담하지 않아요', '시작 전 전액 환불 · 시작 후 불가']),
  '''신청 전에 꼭 읽어주세요

· 만 19세 이상만 신청할 수 있어요.
· 남자 입장에서 상황을 해석해 드리는 서비스예요. 의료 · 치료 목적이 아니에요.
· 재회 · 관계 회복 등 원하시는 결과를 100% 장담하지 않아요. 그의 마음과 선택은 그에게 달려 있어서, 제가 드리는 건 가능성을 높이는 해석과 방법이에요.
· 분석 작성을 시작하기 전에는 전액 환불, 시작한 뒤에는 환불이 어려워요.
· 재회 등 결과를 이유로 한 환불은 어려워요.''', '없음'),
]

CSS = '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@500;700;900&display=block">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:#444; font-family:'Noto Sans KR',sans-serif; word-break:keep-all; }
  .k { width:800px; height:400px; position:relative; overflow:hidden; margin-bottom:12px; background:linear-gradient(150deg,#1d1b18,#0d0d0f 70%); color:#f4f1ea; padding:34px 44px; }
  .k:before { content:''; position:absolute; inset:14px; border:1.5px solid #4a3c22; border-radius:6px; }
  .top { font-family:'Nanum Pen Script',cursive; font-size:36px; color:#d6d1c8; line-height:1; }
  .ti { font-size:44px; font-weight:900; letter-spacing:-0.03em; margin-top:10px; line-height:1.15; }
  .pr { position:absolute; right:44px; top:52px; background:#ffcb3d; color:#151515; font-weight:900; font-size:34px; padding:4px 16px; }
  .was { position:absolute; right:46px; top:24px; font-size:20px; color:#a9a39a; } .was s { color:#c9c3b9; }
  .till { position:absolute; right:46px; top:104px; font-size:18px; font-weight:700; color:#ffcb3d; }
  .prs { position:absolute; right:44px; top:34px; display:grid; gap:8px; justify-items:end; }
  .pr2 { display:flex; align-items:center; gap:10px; }
  .pr2 .lb { font-size:24px; font-weight:900; color:#f4f1ea; }
  .pr2 .w2 { font-size:17px; color:#a9a39a; }
  .pr2 b { background:#ffcb3d; color:#151515; font-weight:900; font-size:32px; padding:2px 12px; }
  .till2 { font-size:18px; font-weight:700; color:#ffcb3d; }
  .rec { position:absolute; right:46px; top:132px; font-size:20px; font-weight:900; color:#ffcb3d; letter-spacing:.1em; }
  ul { list-style:none; margin-top:26px; }
  li { font-size:27px; font-weight:500; line-height:1.5; padding-left:26px; position:relative; color:#e6e1d8; }
  li:before { content:''; position:absolute; left:2px; top:17px; width:10px; height:10px; background:#ffcb3d; }
  .ft { position:absolute; left:44px; right:44px; bottom:30px; display:flex; justify-content:space-between; font-size:19px; color:#8e8578; }
</style></head><body>
'''

def build():
    out = CSS
    for key, name, (top, ti, pr, items), msg, btn in MENU:
        rec = '<div class="rec">★ 추천</div>' if key == 'm2' else ''
        if ';' in pr:  # 시간별 가격 여러 줄 (전화 분석)
            rows = ''.join(f'<div class="pr2"><span class="lb">{e(lb)}</span><span class="w2">정가 <s>{e(w)}</s></span><b>{e(n)}</b></div>'
                           for lb, wn in (x.split(':') for x in pr.split(';')) for w, n in [wn.split('|')])
            prh = f'<div class="prs">{rows}<div class="till2">12/31까지 오픈가</div></div>'
        elif '|' in pr:
            was, now = pr.split('|'); prh = f'<div class="was">정가 <s>{e(was)}</s></div><div class="pr">{e(now)}</div><div class="till">12/31까지 오픈가</div>'
        else:
            prh = f'<div class="pr">{e(pr)}</div>' if pr else ''
        out += (f'<section class="k" id="{key}"><div class="top">{e(top)}</div><div class="ti">{e(ti)}</div>{prh}{rec}'
                f'<ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>'
                f'<div class="ft"><span>남자들끼리 하는 말 · 1:1 남자 심리 분석</span><span>@mszexc</span></div></section>\n')
    return out + '</body></html>'

if __name__ == '__main__':
    import os
    os.makedirs('kakao_menu', exist_ok=True)
    open('kakao_menu/km.html', 'w', encoding='utf-8').write(build())
    for key, name, _, msg, btn in MENU:
        assert len(name) <= 20, (name, len(name))
        assert len(msg) <= 400, (key, len(msg))
        assert '상담' not in msg + name, key
        print(key, len(name), len(msg))

# 11/1: 이미지를 한 장만 넣을 때 — 메뉴 하나(「상품 · 가격 보기」)에 이 한 장 + 아래 메시지(400자 안)
ALL_NAME = '상품 · 가격 보기'
ALL_MSG = '''1:1 남자 심리 분석 · 12/31까지 오픈가

A. 남자 심리 분석 · 49,000원 (정가 69,000원)
관상 + 카톡 10장 · 성향 · 말 번역 · 마음 단계 · 72시간 안

B. 분석 + 보낼 말 대본 · 99,000원 (정가 129,000원) ★추천
A + 상황별 대본 4종 · 7일 안 피드백 2회

C. 4주 플랜 · 390,000원 (정가 490,000원) · 월 3명
B + 주 1회 점검 4번 · 첨삭 주 3건

T. 실시간(전화 · 카톡) · 30분 4.9만 · 60분 8.9만
S. 보내기 전 한 줄 첨삭 · 2만 (처음이신 분도)

신청: 채팅으로 "A · B · C · T · S 신청" (계좌이체 · 만 19세 이상)
결과는 100% 장담하지 않아요 · 시작 후엔 환불이 어려워요.'''
ALL_CSS = CSS.replace('</style>', '''
  .one { width:800px; height:400px; position:relative; overflow:hidden; background:linear-gradient(150deg,#1d1b18,#0d0d0f 70%); color:#f4f1ea; padding:20px 30px; }
  .one:before { content:''; position:absolute; inset:10px; border:1.5px solid #4a3c22; border-radius:6px; }
  .one .hd1 { display:flex; align-items:baseline; gap:12px; }
  .one .hd1 b { font-size:30px; font-weight:900; letter-spacing:-0.02em; }
  .one .hd1 span { font-family:'Nanum Pen Script',cursive; font-size:26px; color:#d6d1c8; }
  .one .cols { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:10px; }
  .one .c { border:1.5px solid #3a3326; border-radius:10px; padding:9px 14px; background:rgba(255,255,255,.03); position:relative; }
  .one .c.hot { border-color:#ffcb3d; }
  .one .c .t { font-size:21px; font-weight:900; line-height:1.2; }
  .one .c .p { display:inline-block; margin-top:8px; background:#ffcb3d; color:#151515; font-weight:900; font-size:22px; padding:1px 8px; }
  .one .c .w { font-size:13px; color:#a9a39a; margin-top:6px; }
  .one .c .s { font-size:15px; color:#d9d4cb; margin-top:5px; line-height:1.35; }
  .one .c .r { position:absolute; right:10px; top:10px; font-size:13px; font-weight:900; color:#ffcb3d; }
  .one .op { margin-top:8px; font-size:16px; color:#cfcac1; }
  .one .op b { color:#ffcb3d; }
  .one .ft2 { position:absolute; left:30px; right:30px; bottom:18px; display:flex; justify-content:space-between; font-size:15px; color:#8e8578; }
  .one .ft2 b { color:#f4f1ea; }
</style>''')

def build_one():
    cols = [('A. 남자 심리 분석', '69,000원|49,000원', '관상 · 카톡 10장<br>성향 · 말 번역 · 마음 단계<br>72시간 안', ''),
            ('B. 분석 + 대본', '129,000원|99,000원', 'A + 상황별 대본 4종<br>7일 안 피드백 2회<br>주 5건', 'hot'),
            ('C. 4주 플랜', '490,000원|390,000원', 'B + 주 1회 점검 4번<br>첨삭 주 3건<br>월 3명', '')]
    c = ''.join(f'<div class="c {r}">' + ('<div class="r">★ 추천</div>' if r else '') + f'<div class="t">{e(t)}</div><div class="w">정가 <s>{e(p.split("|")[0])}</s></div><div class="p">{e(p.split("|")[1])}</div><div class="s">{s}</div></div>' for t, p, s, r in cols)
    return ALL_CSS + f'''<section class="one" id="all"><div class="hd1"><b>1:1 남자 심리 분석</b><span>12/31까지 오픈가</span></div>
<div class="cols">{c}</div>
<div class="op"><b>📞 실시간 분석(전화 · 카톡)</b> · 30분 <s style="color:#8e8578">5.9만</s> 4.9만 · 60분 <s style="color:#8e8578">9.9만</s> 8.9만 · 예약제</div>
<div class="op" style="margin-top:4px"><b>✍️ S. 한 줄 첨삭</b> · 2만 · 처음이신 분도 · 7일 안 A · B 신청 시 2만 원 빼드려요</div>
<div class="op" style="margin-top:6px;font-size:14px;color:#8e8578">결과를 100% 장담하지 않아요 · 분석 시작 전 전액 환불, 시작 후 환불 불가</div>
<div class="ft2"><span>신청은 채팅으로 <b>"A · B · C · T · S 신청"</b> · 계좌이체 · 만 19세 이상</span><span>@mszexc</span></div></section></body></html>'''

if __name__ == '__main__':
    open('kakao_menu/km_one.html', 'w', encoding='utf-8').write(build_one())
    assert len(ALL_MSG) <= 400 and '상담' not in ALL_MSG and len(ALL_NAME) <= 20, len(ALL_MSG)
    print('one', len(ALL_MSG))
