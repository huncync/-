# 카카오채널 채팅방 메뉴용 문서 이미지 (11/1) — 채널 안내문 · 신청서 · 결과물 틀
# 메뉴 이미지는 2:1(800×400)이라 긴 문서는 안 읽혀요 → ① 메뉴용 2:1 카드 ② 채팅 · 소식에 보낼 세로 전체 이미지, 두 가지로 만들어요
# python3 kakao_docs.py → kakao_menu/docs.html (렌더는 .work/rdocs.js)
import html, importlib.util as u, os
e = html.escape
D = os.path.dirname(os.path.abspath(__file__))
s = u.spec_from_file_location('m', os.path.join(D, 'menu.py')); M = u.module_from_spec(s); s.loader.exec_module(M)

GUIDE_CH = M.GUIDE.replace('전문 심리상담이 아닙니다', '의료 · 치료 목적의 서비스가 아닙니다').replace('상담', '분석')
FORM = M.FORM
REPORT = M.REPORT.replace('[결과물 틀]', '[결과물은 이렇게 드려요]')
assert '상담' not in GUIDE_CH + FORM + REPORT

def lines_html(text):
    out = []
    for ln in text.split('\n'):
        s = ln.rstrip()
        if not s.strip(): out.append('<div class="sp"></div>'); continue
        t = e(s.strip())
        if s.startswith('[') and s.endswith(']'): out.append(f'<div class="ttl">{e(s[1:-1])}</div>')
        elif s.startswith('■'): out.append(f'<div class="sec">{e(s[1:].strip())}</div>')
        elif s.lstrip().startswith('※'): out.append(f'<div class="note">{t}</div>')
        elif s.startswith('   '): out.append(f'<div class="sub">{t}</div>')
        elif s.lstrip().startswith('- '): out.append(f'<div class="li">{e(s.strip()[2:])}</div>')
        elif s[:1] in 'ABC' and ' · ' in s[:6]: out.append(f'<div class="sec">{t}</div>')
        else: out.append(f'<div class="ln">{t}</div>')
    return ''.join(out)

CARDS = [  # (id, 윗줄, 제목, 항목들)
 ('card_guide', '남자가 직접, 그 사람 마음을 번역해 드려요', '1:1 남자 심리 분석 안내',
  ['A 5만 · B 10만 ★추천 · C 39만 (월 3명)', '관상 · 카톡 · 상황을 남자 입장에서', '채팅으로 "A · B · C 신청" → 계좌이체']),
 ('card_form', '입금 확인 후 보내드려요', '신청서 · 이것만 준비하세요',
  ['얼굴 사진 (나 1장 · 그 1~2장 · 부담되면 생략 OK)', '둘의 이야기 + 그의 카톡 · 만날 때 모습', '카톡 캡처 10장 · 꼭 답받고 싶은 질문']),
 ('card_report', '72시간 안에 서면으로', '결과물은 이렇게 드려요',
  ['A · 성향 / 말 번역 / 마음 단계 / 갈등 이유', 'B · A + 상황별 대본 4종 + 피드백 2회', 'C · B + 4주 점검 · 첨삭 주 3건 · 정리 리포트']),
]
DOCS = [('doc_guide', GUIDE_CH), ('doc_form', FORM), ('doc_report', REPORT)]

# 메뉴 응답 메시지 (400자 안)
MSG = {
 'card_guide': '''1:1 남자 심리 분석 안내

A. 남자 심리 분석 · 50,000원
B. 분석 + 대본 · 100,000원 ★추천
C. 4주 플랜 · 390,000원 (월 3명)

자세한 안내문은 채팅으로 "안내문"이라고 남겨주시면 이미지로 보내드려요.
신청은 채팅으로 "A · B · C 신청"이라고 남겨주세요.''',
 'card_form': '''신청서는 입금이 확인되면 채팅으로 보내드려요.
복사해서 빈칸만 채워 보내주시면 돼요.

미리 준비해 두시면 빨라요.
· 얼굴 사진 (나 1장 · 그 1~2장, 1년 안 · 보정 없이)
· 둘의 이야기 (어떻게 만났고, 지금 어떤지)
· 그가 만날 때와 카톡할 때 어떻게 다른지
· 카톡 캡처 10장 (최근 대화 + 분위기가 바뀐 때)
· 꼭 답받고 싶은 질문 1~3개

사진은 분석에만 쓰고 끝나면 바로 지워요.
얼굴 사진이 부담스러우시면 안 보내셔도 괜찮아요.''',
 'card_report': '''결과물은 이렇게 드려요 (자료가 다 도착한 때부터 72시간 안)

A · 그의 연애 성향(관상) / 그의 말 번역 / 지금 마음 단계 / 갈등이 반복되는 이유 / 질문에 대한 답
B · A + 상황별 대본 4종 (첫 연락 · 답장 왔을 때 · 만났을 때 · 반응 없을 때) + 7일 안 피드백 2회
C · B + 4주 동안 주 1회 점검과 다음 대본 · 첨삭 주 3건 · 4주 뒤 정리 리포트

결과를 100% 장담하지는 않아요. 가능성을 높이는 해석과 방법을 드려요.''',
}

CSS = '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&family=Noto+Sans+KR:wght@400;500;700;900&display=block">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:#444; font-family:'Noto Sans KR',sans-serif; word-break:keep-all; }
  .k { width:800px; height:400px; position:relative; overflow:hidden; margin-bottom:12px; background:linear-gradient(150deg,#1d1b18,#0d0d0f 70%); color:#f4f1ea; padding:34px 44px; }
  .k:before { content:''; position:absolute; inset:14px; border:1.5px solid #4a3c22; border-radius:6px; }
  .top { font-family:'Nanum Pen Script',cursive; font-size:36px; color:#d6d1c8; line-height:1; }
  .ti { font-size:44px; font-weight:900; letter-spacing:-0.03em; margin-top:10px; line-height:1.15; }
  ul { list-style:none; margin-top:26px; }
  li { font-size:27px; font-weight:500; line-height:1.5; padding-left:26px; position:relative; color:#e6e1d8; }
  li:before { content:''; position:absolute; left:2px; top:17px; width:10px; height:10px; background:#ffcb3d; }
  .ft { position:absolute; left:44px; right:44px; bottom:30px; display:flex; justify-content:space-between; font-size:19px; color:#8e8578; }
  .doc { width:1080px; background:#f4eee3; color:#1d1a16; padding:70px 72px 80px; margin-bottom:12px; position:relative; }
  .doc:before { content:''; position:absolute; inset:24px; border:2px solid #cdb68a; border-radius:6px; pointer-events:none; }
  .doc .ttl { font-size:44px; font-weight:900; letter-spacing:-0.02em; margin-bottom:10px; }
  .doc .sec { font-size:34px; font-weight:900; margin-top:26px; padding:6px 16px; background:#1d1a16; color:#f4eee3; display:inline-block; }
  .doc .ln { font-size:30px; line-height:1.6; font-weight:500; }
  .doc .li { font-size:30px; line-height:1.6; padding-left:28px; position:relative; }
  .doc .li:before { content:''; position:absolute; left:4px; top:20px; width:10px; height:10px; background:#9a6a1f; }
  .doc .sub { font-size:27px; line-height:1.55; color:#5b5144; padding-left:28px; }
  .doc .note { font-size:26px; line-height:1.55; color:#7a5a22; margin-top:4px; }
  .doc .sp { height:14px; }
  .doc .ft2 { margin-top:36px; display:flex; justify-content:space-between; font-size:24px; color:#7a7064; }
</style></head><body>
'''

def build():
    out = CSS
    for cid, top, ti, items in CARDS:
        out += (f'<section class="k" id="{cid}"><div class="top">{e(top)}</div><div class="ti">{e(ti)}</div>'
                f'<ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>'
                f'<div class="ft"><span>남자들끼리 하는 말 · 1:1 남자 심리 분석</span><span>@mszexc</span></div></section>\n')
    for did, text in DOCS:
        out += f'<section class="doc" id="{did}">{lines_html(text)}<div class="ft2"><span>남자들끼리 하는 말 · 1:1 남자 심리 분석</span><span>@mszexc</span></div></section>\n'
    return out + '</body></html>'

if __name__ == '__main__':
    open(os.path.join(D, 'kakao_menu', 'docs.html'), 'w', encoding='utf-8').write(build())
    for k, v in MSG.items():
        assert len(v) <= 400 and '상담' not in v, (k, len(v))
        print(k, len(v))
