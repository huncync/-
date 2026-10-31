# 사진 스토리형 캐러셀 (10/29~) — 매 장 지훈님 일상 사진 + 짧은 말 상자, 장마다 문장을 반쯤 열어두고 넘기게
# 상자 4종 (표지는 W · G 큰 상자): w 흰 상자 = 내레이션 · k 검은 상자 = 속마음/괄호 · g 금색 = 핵심 · q 회색 따옴표 = 남자들끼리 실제로 하는 말
# python3 ps01.py → ps01.html (사진 없는 장은 "사진 자리" 안내가 깔려요. 사진을 받으면 PHOTO만 채우면 돼요)
import html, json
e = html.escape

TITLE = '이별 통보 받은 날 밤, 남자 머릿속'
# (사진 파일 또는 None, 사진 설명, [(상자 종류, 글, 위치 top%, 왼쪽 left% 또는 'r'(오른쪽 정렬))])
SLIDES = [
 ('../cover_photo_04.jpg', '밤길 셀카 (흔들려도 좋아요)', [
   ('W', '헤어지자는 말을 듣고,', 56, 6), ('G', '그날 밤, 남자 머릿속', 64, 6), ('k', '(괜찮은 척하던 그 남자요.)', 75, 'r')]),
 (None, '편의점 봉지 · 맥주 두 캔', [
   ('w', '친구들한테 물어보면', 30, 8), ('w', '대부분 이렇게 말해요.', 37, 20), ('q', '"잘 됐어. 홀가분해."', 60, 'r')]),
 (None, '술잔 부딪히는 손 (얼굴 안 나오게)', [
   ('w', '남자들끼리 모이면 제일 먼저 나오는 말.', 26, 6), ('q', '"야, 잘 헤어졌어."', 46, 10), ('q', '"더 좋은 사람 만나."', 54, 'r'), ('q', '"오늘 마시자."', 62, 18)]),
 (None, '컵라면 · 아무 상관 없는 사진 (쉬어가는 장)', [
   ('w', '근데 이 말들은 다,', 38, 8), ('g', '집에 가기 전까지만이에요.', 47, 'r')]),
 (None, '현관 · 불 꺼진 방', [
   ('w', '집에 들어가서 불 켜는 순간,', 30, 8), ('g', '제일 먼저 카톡방을 열어요.', 39, 'r'), ('k', '(나가지도 못하면서.)', 48, 12)]),
 (None, '휴대폰 화면 (대화는 흐리게)', [
   ('w', '마지막 대화를 처음부터 다시 읽어요.', 34, 6), ('g', '어디서부터 틀렸는지 찾으려고.', 56, 'r')]),
 (None, '침대에서 본 천장', [
   ('w', '그리고 이 생각 하나에서 멈춰요.', 38, 6), ('q', '"내가 잡을 수 있었나?"', 50, 'r')]),
 ('../cover_photo_02.jpg', '창밖 · 새벽 (또는 밤 셀카)', [
   ('w', '여기서 남자는 둘로 나뉘어요.', 70, 8)]),
 (None, '운전석 · 신호 대기', [
   ('g', '잡을 수 있었다고 생각한 남자는', 32, 6), ('w', '며칠 안에 연락해요. 아주 짧게.', 41, 'r'), ('k', '("잘 지내?" 같은 거.)', 50, 14)]),
 (None, '빈 벤치 · 산책길', [
   ('g', '잡을 수 없었다고 생각한 남자는', 32, 6), ('w', '연락하지 않아요.', 41, 'r'), ('w', '대신 오래 남아요.', 49, 10)]),
 (None, '출근길 엘리베이터', [
   ('w', '다음 날 아침, 둘 다 똑같아 보여요.', 34, 6), ('k', '(멀쩡하게 출근하니까요.)', 44, 'r')]),
 (None, '카페 테이블 · 커피 한 잔', [
   ('w', '그래서 이렇게 생각하게 돼요.', 32, 6), ('q', '"저 사람은 아무렇지 않구나."', 44, 'r')]),
 (None, '노을 · 퇴근길', [
   ('g', '아니에요.', 34, 8), ('w', '남자는 슬픔을 밤에만 꺼내요.', 43, 'r')]),
 ('../cover_photo_03.jpg', '거울 셀카 (마지막 장 · 얼굴)', [
   ('w', '이것만 기억하세요.', 30, 8), ('g', '남자의 이별은 밤에 오고, 늦게 와요.', 39, 4),
   ('w', '그가 멀쩡해 보여도 당신이 틀린 게 아니에요.', 49, 'r'),
   ('k', '남자가 하는 말의 뜻은 전자책 1·2권에 · 프로필 링크에서 무료로 받아보세요', 82, 'r')]),
]

CAPTION = '''헤어지자는 말을 들은 그날 밤, 남자는 뭘 할까요?

남자들은 낮에는 괜찮고,
밤에는 정직합니다.

친구들 앞에서는 "잘 됐어."
집에 와서는 카톡방을 처음부터 다시 읽어요.
어디서부터 틀렸는지 찾으려고.

그리고 둘로 나뉘어요.
잡을 수 있었다고 생각한 남자는 며칠 안에 짧게 연락하고,
잡을 수 없었다고 생각한 남자는 연락 대신 오래 남아요.

💡
그가 멀쩡해 보인다고
당신의 시간이 틀린 게 아니에요.
남자의 이별은 밤에 오고, 늦게 와요.

헤어지고 혼자 버티는 친구에게 보내주세요.

📕 남자가 하는 말의 뜻은 「남자들끼리 하는 말」 1·2권에 적었습니다.
프로필 링크에서 무료로 받아보세요.

#남자심리 #연애심리 #이별 #재회 #남자들끼리하는말'''
PIN = '그 사람은 며칠 만에 연락이 왔나요? 숫자만 남겨주세요 👇 (안 왔으면 0)'

CSS = '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=block">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { word-break:keep-all; background:#333; font-family:'Noto Sans KR',sans-serif; }
  .slide { width:1080px; height:1350px; position:relative; overflow:hidden; margin-bottom:20px; background:#1a1917; }
  .slide img.bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:brightness(.92); }
  .ph { position:absolute; inset:0; background:linear-gradient(160deg,#3a3631,#191816 70%); }
  .ph span { position:absolute; left:0; right:0; bottom:120px; text-align:center; font-size:34px; color:#8a8378; }
  .ph span b { display:block; font-size:30px; color:#6d675e; letter-spacing:.1em; margin-bottom:8px; }
  .bx { position:absolute; max-width:84%; font-size:46px; line-height:1.38; font-weight:500; padding:16px 28px; letter-spacing:-0.01em; }
  .bx.w { background:#fff; color:#151515; border:2px solid #151515; }
  .bx.k { background:#111; color:#f2f2f2; font-size:38px; }
  .bx.g { background:#f0c674; color:#151515; font-weight:700; }
  .bx.W { background:#fff; color:#151515; border:2px solid #151515; font-size:62px; font-weight:700; }
  .bx.G { background:#f0c674; color:#151515; font-size:76px; font-weight:900; letter-spacing:-0.03em; }
  .bx.q { background:#f4f1ea; color:#151515; border-left:10px solid #f0c674; font-weight:700; }
  .num { position:absolute; right:40px; top:40px; font-size:28px; color:#fff; background:rgba(0,0,0,.45); border-radius:999px; padding:6px 18px; }
  .hd { position:absolute; left:40px; bottom:36px; font-size:28px; color:rgba(255,255,255,.75); text-shadow:0 1px 6px rgba(0,0,0,.6); }
</style></head><body>
'''

def build():
    out = CSS
    n = len(SLIDES)
    for i, (photo, desc, boxes) in enumerate(SLIDES, 1):
        bg = f'<img class="bg" src="{e(photo)}">' if photo else f'<div class="ph"><span><b>사진 자리</b>{e(desc)}</span></div>'
        bx = ''
        for kind, text, top, left in boxes:
            pos = f'top:{top}%;' + ('right:6%;' if left == 'r' else f'left:{left}%;')
            bx += f'<div class="bx {kind}" style="{pos}">{e(text)}</div>'
        out += f'<section class="slide" id="s{i}">{bg}{bx}<div class="num">{i}/{n}</div><div class="hd">@mszexc</div></section>\n'
    return out + '</body></html>'

if __name__ == '__main__':
    from psgen import build as gbuild
    open('ps01.html', 'w', encoding='utf-8').write(gbuild(SLIDES, no=40))  # 11/1 18~19시 = #40
    json.dump({'title': TITLE, 'caption': CAPTION, 'pin': PIN, 'shots': [d for _, d, _ in SLIDES]}, open('ps01.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', len(SLIDES))
