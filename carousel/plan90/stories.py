# 작업실 스토리 탭 — python3 stories.py <index.html>
# 원칙: 스토리는 이미 팔로우한 사람만 봐요. 보는 사람을 늘리려면 "누르게" 해야 해요(투표 · 퀴즈 · 질문 · 슬라이더 · 링크).
import html, sys
e = html.escape

TIP = ('<b>냉정하게: 스토리 조회는 이미 팔로우한 사람에게서만 나와요.</b> 그래서 늘리는 길은 두 가지예요. '
       '① 스토리에 반응(투표 · 퀴즈 · 답장 · 공유)한 사람에게 다음 스토리가 앞줄에 뜨게 하기, '
       '② 매일 같은 시간대에 끊기지 않게 올리기(며칠 쉬면 앞줄에서 밀려요). 둘 다 널리 알려진 운영 원리이고, 이 계정에서는 아직 검증 전이에요. '
       '그래서 <b>"보여주는" 스토리(새 게시물 알림만)보다 "누르게 하는" 스토리</b>로 짰어요. 하루 3장, 5분이면 돼요.')

DAILY = [
 ('①', '11~12시 · 캐러셀 올린 직후', '게시물 공유 + 투표 스티커', '표지를 반쯤 가리고 "넘겨서 확인 →" 한 줄. 투표는 두 개 중 하나 고르는 질문으로. 정답 없는 질문이 많이 눌려요.'),
 ('②', '18~19시 · 캐러셀 올린 직후', '번역 퀴즈 스티커', '"남자가 이 말을 하면?" 3지선다. 정답은 방금 올린 게시물에 있다고 적어요. 퀴즈를 틀린 사람이 게시물로 가요.'),
 ('③', '21~22시 · 밤', '한 줄 공감 + 슬라이더 (릴스 날엔 릴스 공유)', '그날 캐러셀의 반전 장 문장 하나 + 이모지 슬라이더(💔). 목 · 일 릴스 날엔 릴스를 공유하고 투표 하나.'),
]
WEEKLY = [
 ('수', '질문 상자 "그 사람이 한 말, 한 마디만"', '목요일 스토리에 3개만 골라 한 줄씩 번역해요. 상황 · 사연은 받지 않고 "말"만. 끝에 "내 상황 전체는 카톡 채널에 \'신청\'" 한 줄.'),
 ('일', '카카오채널 링크 스티커', '"전자책 1·2권, 채널 추가하면 바로 와요." 11/10 친구 1,000명 목표용.'),
 ('금', '구독 미리보기', '그 주 총정리 카드 표지 + "구독자 전용" 한 줄 + 구독 버튼.'),
]
DONT = ['한 번에 6장 이상 몰아서 올리기 (중간에 넘겨버려요 · 나눠 올리면 그때마다 앞줄로 와요)',
        '글자가 꽉 찬 캡처 (1초 안에 읽혀야 해요)',
        '판매 스토리 매일 (상담 · 3권 · 구독 안내는 합쳐서 주 2~3번까지)',
        '날짜 · 요일 예고 ("내일 올라와요") — 계정 원칙대로 안 써요']
ASK = '최근 스토리 1장 조회수를 알려주세요(아무거나 3장). 팔로워 대비 몇 %인지가 지금 기준이에요. 2주 뒤 같은 숫자로 비교해요.'

# 7일치 (날짜, [(시간, 무엇, 스티커, 문구)])
KIT = [
 ('10/29 목', [
  ('①', '#33 공유', '투표', '요즘 싸움이 줄었다면?\n😌 편해진 거  /  🥶 식은 거'),
  ('②', '#34 공유', '퀴즈', '헤어진 남자가 차단을 안 했다면?\nA 아직 미련이 있어서\nB 감정이 다 정리돼서\nC 둘 다 가능 ✅\n(6가지 이유는 방금 게시물에)'),
  ('③', '릴스 「연락 다음으로 사라지는 것」 공유', '투표', '요즘 그 사람, 내 하루를 물어보나요?\n🙋 물어봐  /  🙅 안 물어봐'),
 ]),
 ('10/30 금', [
  ('①', '#35 공유', '투표', '둘이 만나면 대화는?\n💬 우리 얘기  /  🧾 생활 얘기'),
  ('②', '#36 공유', '퀴즈', '헤어진 그 사람이 내 셀카에만 좋아요를 눌렀다면?\nA 실수로 누른 것\nB "아직 보고 있어" ✅\nC 새 사람이 생겨서\n(6가지는 방금 게시물에)'),
  ('③', '구독 미리보기', '구독 버튼', '이번 주 캐러셀 14편, 3장으로 정리했어요\n구독자 전용 🔒'),
 ]),
 ('10/31 토', [
  ('①', '합본 「남자가 하는 말, 진짜 뜻 총정리」 공유', '투표', '남자 말 중 제일 헷갈리는 건?\n⏳ "나중에"  /  📵 "바빠"'),
  ('②', '「혼자 있고 싶어」 공유', '투표', '남자친구가 "혼자 있고 싶어" 하면?\n🙆 기다린다  /  🙋 이유를 묻는다'),
  ('③', '한 줄 공감', '이모지 슬라이더 💔', '남자는 화낼 때보다\n조용할 때 더 멀어요.'),
 ]),
 ('11/1 일', [
  ('①', '「놓치기 싫을 때 하는 행동」 공유', '투표', '그 사람, 요즘 나를 놓치기 싫어 보여요?\n💛 응  /  🤔 모르겠어'),
  ('②', '「이별 통보 받은 날 밤, 남자 머릿속」 공유', '투표', '헤어지자는 말 들은 그날 밤, 그는?\n😴 잤다  /  🌙 못 잤다'),
  ('③', '릴스 「읽고 답 안 할 때」 공유 + 카카오채널', '링크 스티커', '전자책 1·2권, 채널 추가하면 바로 와요 👇\n(스티커 문구: 1·2권 받기)'),
 ]),
 ('11/2 월', [
  ('①', '「술 마시고 하는 말」 공유', '투표', '술 마시고 한 말, 믿어요?\n🍺 진심  /  🙅 술김'),
  ('②', '「스토리 보는 이유」 공유', '투표', '헤어진 그 사람이 내 스토리를 본다면?\n👀 미련  /  🤷 습관'),
  ('③', '한 줄 공감', '이모지 슬라이더 💔', '좋아요는 문을 두드린 게 아니라\n창문으로 본 거예요.'),
 ]),
 ('11/3 화', [
  ('①', '「돌아오지 않게 만드는 법」 공유', '투표', '헤어진 뒤 먼저 연락해 본 적 있어요?\n📱 있다  /  🤐 없다'),
  ('②', '「칭찬보다 먼저 줄어드는 것」 공유', '투표', '요즘 그 사람 칭찬, 예전보다?\n⬆ 늘었다  /  ⬇ 줄었다'),
  ('③', '한 줄 공감', '이모지 슬라이더 💛', '편안함 위에 가끔\n"처음"을 얹어주세요.'),
 ]),
 ('11/4 수', [
  ('①', '「그 사람 그냥 친구야」 공유', '투표', '남자친구가 "그냥 친구야" 하면?\n🙆 믿는다  /  🤔 글쎄'),
  ('②', '「생일에 연락하는 이유」 공유', '투표', '헤어진 그 사람, 생일에 연락 왔어요?\n🎂 왔다  /  🔕 안 왔다'),
  ('③', '질문 상자', '질문 스티커', '그 사람이 한 말, 한 마디만 남겨주세요\n남자 입장에서 3개 골라 번역해요\n(상황 · 사연 말고 "말"만)'),
 ]),
]

def build():
    daily = ''.join(f'<li><span class="n">{n}</span><span class="t"><b>{e(w)}</b> · {e(what)}<br><span class="dim">{e(how)}</span></span><span></span></li>' for n, w, what, how in DAILY)
    weekly = ''.join(f'<li><span class="d">{e(d)}</span><span class="m"><b>{e(a)}</b><em>{e(b)}</em></span></li>' for d, a, b in WEEKLY)
    dont = ''.join(f'<li>{e(x)}</li>' for x in DONT)
    days = ''
    for di, (d, rows) in enumerate(KIT):
        items = ''.join(f'<div class="sk"><div class="sh"><b>{e(n)}</b> {e(w)} <span class="stk">{e(stk)}</span></div>'
                        f'<div class="row"><button class="btn gold" data-ct="st{di}{i}">복사</button></div><pre id="st{di}{i}">{e(txt)}</pre></div>'
                        for i, (n, w, stk, txt) in enumerate(rows))
        days += f'<details class="cap"{" open" if di == 0 else ""}><summary>{e(d)}</summary><div style="padding:0 14px 12px">{items}</div></details>'
    return f'''
    <style>
      #p-story .sk {{ border-top:1px solid var(--line); padding:10px 0 4px; }}
      #p-story .sk:first-child {{ border-top:0; }}
      #p-story .sh {{ font-size:14px; margin-bottom:6px; }}
      #p-story .stk {{ display:inline-block; font-size:11px; font-weight:800; color:#111; background:#e0b46a; border-radius:999px; padding:1px 8px; margin-left:6px; }}
    </style>
    <div class="tip">{TIP}</div>
    <h2>매일 3장<small>캐러셀 올린 직후에 하나씩 · 몰아서 올리지 않기</small></h2>
    <ol class="topics">{daily}</ol>
    <h2>요일별 하나 더</h2>
    <ol class="plan subplan">{weekly}</ol>
    <h2>7일치 문구<small>스티커 이름 그대로 · 퀴즈는 ✅를 정답으로 지정하고, 올릴 땐 ✅ 표시는 지워요</small></h2>
    {days}
    <h2>하지 않을 것</h2>
    <ol class="pc-notes">{dont}</ol>
    <div class="note"><div><b>알려주세요:</b> {e(ASK)}</div></div>
'''

if __name__ == '__main__':
    P = sys.argv[1]
    t = open(P, encoding='utf-8').read()
    if 'id="tab-story"' not in t:
        a = '    <button class="tab" role="tab" id="tab-consult"'
        assert t.count(a) == 1
        t = t.replace(a, '    <button class="tab" role="tab" id="tab-story" aria-controls="p-story" aria-selected="false">스토리</button>\n' + a)
        a = '  <section class="panel" id="p-consult"'
        assert t.count(a) == 1
        t = t.replace(a, '  <section class="panel" id="p-story" role="tabpanel" aria-labelledby="tab-story" hidden>\n  </section>\n' + a)
    a = t.index('<section class="panel" id="p-story"'); a2 = t.index('>', a) + 1; b = t.index('</section>', a)
    t = t[:a2] + build() + '  ' + t[b:]
    open(P, 'w', encoding='utf-8').write(t)
    print('ok', len(KIT), 'days')
