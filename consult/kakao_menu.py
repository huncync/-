# 카카오채널 채팅방 리스트 메뉴 (11/1) — 메뉴 하나 = 이름(20자) + 응답 메시지(400자) + 이미지(800×400) + 버튼(10자)
# python3 kakao_menu.py → kakao_menu/km.html (렌더는 .work/rkm.js) · 채널 글이라 "상담"은 쓰지 않아요(금칙어)
import html
e = html.escape

# (키, 메뉴명, 이미지: 윗줄 · 제목 · 가격 · 항목들, 응답 메시지, 버튼)
MENU = [
 ('m1', 'A. 남자 심리 분석 · 5만', ('그가 왜 그러는지 알고 싶을 때', 'A. 남자 심리 분석', '50,000원',
   ['관상 · 카톡 10장 · 상황을 남자 입장에서', '그의 성향 / 말 번역 / 지금 마음 단계', '서면 리포트 · 72시간 안 · 추가 질문 1회']),
  '''A. 남자 심리 분석 · 50,000원

그가 왜 그러는지 알고 싶은 분께 드려요.

· 관상(본인 · 상대) + 카톡 캡처 10장 + 지금 상황
· 서면 리포트: 그의 성향 / 그가 한 말 번역 / 지금 마음 단계 / 갈등이 반복되는 이유
· 72시간 안에 전달 · 추가 질문 1회
· 주 10건 한정

신청은 채팅으로 "A 신청"이라고 남겨주세요.''', '없음'),
 ('m2', 'B. 분석+대본 · 10만 ★추천', ('그래서 뭐라고 보내야 해?', 'B. 분석 + 대본', '100,000원',
   ['A의 모든 내용', '상황별 대본 4종 · 보낼 시간 · 피할 말', '7일 안 피드백 2회 · 주 5건']),
  '''B. 분석 + 마음을 움직이는 대본 · 100,000원 ★추천

"그래서 뭐라고 보내야 해?"까지 알고 싶은 분께 드려요.

· A의 모든 내용
· 상황별 대본 4종: 첫 연락 / 답장 왔을 때 / 만났을 때 / 반응 없을 때
· 보내기 좋은 시간대와 하지 말아야 할 말
· 7일 안 피드백 2회 (1회 = 메시지 1개 + 캡처 3장)
· 주 5건 한정

오픈 첫 주 · B를 신청하신 첫 10분께 카톡 첨삭 2건을 함께 드려요.
신청은 채팅으로 "B 신청"이라고 남겨주세요.''', '없음'),
 ('m3', 'C. 4주 플랜 · 39만', ('재회 · 관계 회복, 끝까지 같이', 'C. 4주 플랜', '390,000원',
   ['B의 모든 내용', '4주 동안 주 1회 점검 + 다음 대본', '보내기 전 카톡 첨삭 주 3건 · 월 3명']),
  '''C. 재회 · 관계 회복 4주 플랜 · 390,000원

한 번의 답이 아니라, 끝까지 같이 가고 싶은 분께 드려요.

· B의 모든 내용
· 4주 동안 주 1회 점검 + 그다음 대본
· 보내기 전 카톡 첨삭 주 3건
· 4주 뒤 정리 리포트
· 월 3명 한정

신청은 채팅으로 "C 신청"이라고 남겨주세요.
먼저 상황을 짧게 들려주시면 C가 맞는지부터 말씀드릴게요.''', '없음'),
 ('m4', '추가 옵션', ('분석을 받으신 분만', '추가 옵션', '',
   ['카톡 첨삭 1건 2만 · 3건 묶음 5만', '추가 질문 1회 2만 · 24시간 급행 +3만', '답장 왔을 때 긴급 첨삭(6시간) 3만']),
  '''추가 옵션 (분석을 받으신 분만)

· 카톡 첨삭 1건 20,000원 / 3건 묶음 50,000원 (30일 안 사용)
  보내려는 메시지 1개 + 앞 대화 캡처 3장 → 24시간 안에 고친 문장 · 이유 · 보낼 시간 · 다음 한 줄
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
  .pr { position:absolute; right:44px; top:38px; background:#ffcb3d; color:#151515; font-weight:900; font-size:34px; padding:4px 16px; }
  .rec { position:absolute; right:46px; top:100px; font-size:20px; font-weight:900; color:#ffcb3d; letter-spacing:.1em; }
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
ALL_MSG = '''1:1 남자 심리 분석 · 상품 안내

A. 남자 심리 분석 · 50,000원
관상 + 카톡 10장으로 그의 성향 · 말 번역 · 지금 마음 단계 · 72시간 안

B. 분석 + 대본 · 100,000원 ★추천
A + 상황별 대본 4종 · 7일 안 피드백 2회
(오픈 첫 주 · B 첫 10분께 카톡 첨삭 2건)

C. 4주 플랜 · 390,000원 · 월 3명
B + 4주 동안 주 1회 점검 · 첨삭 주 3건

추가 옵션: 첨삭 1건 2만 · 추가 질문 2만 · 급행 +3만

신청: 채팅으로 "A · B · C 신청" (계좌이체)
결과는 100% 장담하지 않으며, 분석 시작 후엔 환불이 어려워요.'''
ALL_CSS = CSS.replace('</style>', '''
  .one { width:800px; height:400px; position:relative; overflow:hidden; background:linear-gradient(150deg,#1d1b18,#0d0d0f 70%); color:#f4f1ea; padding:26px 30px; }
  .one:before { content:''; position:absolute; inset:10px; border:1.5px solid #4a3c22; border-radius:6px; }
  .one .hd1 { display:flex; align-items:baseline; gap:12px; }
  .one .hd1 b { font-size:30px; font-weight:900; letter-spacing:-0.02em; }
  .one .hd1 span { font-family:'Nanum Pen Script',cursive; font-size:26px; color:#d6d1c8; }
  .one .cols { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:14px; }
  .one .c { border:1.5px solid #3a3326; border-radius:10px; padding:12px 14px; background:rgba(255,255,255,.03); position:relative; }
  .one .c.hot { border-color:#ffcb3d; }
  .one .c .t { font-size:21px; font-weight:900; line-height:1.2; }
  .one .c .p { display:inline-block; margin-top:8px; background:#ffcb3d; color:#151515; font-weight:900; font-size:22px; padding:1px 8px; }
  .one .c .s { font-size:15.5px; color:#d9d4cb; margin-top:8px; line-height:1.45; }
  .one .c .r { position:absolute; right:10px; top:10px; font-size:13px; font-weight:900; color:#ffcb3d; }
  .one .op { margin-top:12px; font-size:16px; color:#cfcac1; }
  .one .op b { color:#ffcb3d; }
  .one .ft2 { position:absolute; left:30px; right:30px; bottom:22px; display:flex; justify-content:space-between; font-size:15px; color:#8e8578; }
  .one .ft2 b { color:#f4f1ea; }
</style>''')

def build_one():
    cols = [('A. 남자 심리 분석', '50,000원', '관상 · 카톡 10장<br>성향 · 말 번역 · 마음 단계<br>72시간 안', ''),
            ('B. 분석 + 대본', '100,000원', 'A + 상황별 대본 4종<br>7일 안 피드백 2회<br>주 5건', 'hot'),
            ('C. 4주 플랜', '390,000원', 'B + 주 1회 점검 4번<br>첨삭 주 3건<br>월 3명', '')]
    c = ''.join(f'<div class="c {r}">' + ('<div class="r">★ 추천</div>' if r else '') + f'<div class="t">{e(t)}</div><div class="p">{e(p)}</div><div class="s">{s}</div></div>' for t, p, s, r in cols)
    return ALL_CSS + f'''<section class="one" id="all"><div class="hd1"><b>1:1 남자 심리 분석</b><span>남자가 직접, 그 사람 마음을 번역해 드려요</span></div>
<div class="cols">{c}</div>
<div class="op"><b>추가 옵션</b> · 카톡 첨삭 1건 2만 · 추가 질문 2만 · 24시간 급행 +3만</div>
<div class="op" style="margin-top:6px;font-size:14px;color:#8e8578">결과를 100% 장담하지 않아요 · 분석 시작 전 전액 환불, 시작 후 환불 불가</div>
<div class="ft2"><span>신청은 채팅으로 <b>"A · B · C 신청"</b> · 계좌이체</span><span>@mszexc</span></div></section></body></html>'''

if __name__ == '__main__':
    open('kakao_menu/km_one.html', 'w', encoding='utf-8').write(build_one())
    assert len(ALL_MSG) <= 400 and '상담' not in ALL_MSG and len(ALL_NAME) <= 20, len(ALL_MSG)
    print('one', len(ALL_MSG))
