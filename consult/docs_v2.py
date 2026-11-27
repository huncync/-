# 상담 탭 문서 새 디자인 (11/23 지훈님 결정): 채널 안내문 = ① 다크 골드 · 신청서 · 결과물 = ③ 화이트 리포트
# 글은 menu.py(kakao_docs.py의 채널용 문구) 그대로 → 가격이 바뀌면 이 파일만 다시 돌리면 돼요
# python3 docs_v2.py → node render_docs_v2.js
#   kakao_menu/doc_guide.jpg · doc_form.jpg · doc_report.jpg  (세로 전체 · 채팅에 보내기용)
#   kakao_news/guide_N.jpg · form_N.jpg · report_N.jpg        (4:5 나눈 장 · 카톡 소식용)
import html, re, os, importlib.util as u
e = html.escape
D = os.path.dirname(os.path.abspath(__file__))
s = u.spec_from_file_location('kd', os.path.join(D, 'kakao_docs.py')); K = u.module_from_spec(s); s.loader.exec_module(K)

PRICE = re.compile(r'^(.*?)([\d,]+원)\s*\(정가 ([\d,]+원)\)\s*$')

def blk(h, keep=False):
    return f'<div class="b"{" data-k=1" if keep else ""}>{h}</div>'

def para(lines):
    return '<br>'.join(e(x.strip()) for x in lines)

# ── 채널 안내문 (다크 골드) ──
def guide(text):
    L = text.split('\n'); i = 0; out = []
    tag = L[0].strip('[]'); i = 1
    while not L[i].strip(): i += 1
    h1 = []
    while L[i].strip(): h1.append(L[i]); i += 1
    while not L[i].strip(): i += 1
    lead = []
    while L[i].strip(): lead.append(L[i]); i += 1
    out.append(blk(f'<div class="tag">{e(tag)}</div><h1>{para(h1)}</h1><div class="lead">{para(lead)}</div>'))
    while i < len(L):
        ln = L[i]; st = ln.strip()
        if not st: out.append(blk('<div class="sp"></div>')); i += 1; continue
        if st.startswith('━'): out.append(blk('<div class="hr"></div>')); i += 1; continue
        if st.startswith('💰') and not out[-1:] == []:
            out.append(blk(f'<div class="badge">{e(st[1:].strip())}</div>')); i += 1; continue
        m = re.match(r'^■\s*([ABCT])\.\s*(.*)$', st)
        if m:  # 상품 카드
            code, name = m.groups(); i += 1
            star = '★추천' in name; name = name.replace('★추천', '').strip()
            small = ''
            mm = re.match(r'^(.*?)\s*\((.*)\)$', name)
            if mm: name, small = mm.groups()
            prices, who, items = [], '', []
            while i < len(L) and L[i].strip():
                x = L[i]; t = x.strip()
                if t.startswith('💰'):
                    pm = PRICE.match(t[1:].strip()); prices.append(pm.groups())
                elif t.startswith('- '): items.append(('li', t[2:]))
                elif x.startswith('   '): items.append(('sub', t))
                elif not who: who = t
                else: items.append(('li', t))
                i += 1
            pr = ''.join(f'<div class="pr"><span class="pl">{e(a.strip())}</span><s>{e(o)}</s><b>{e(n.replace("원", ""))}<em>원</em></b></div>' for a, n, o in prices)
            body = ''.join(f'<div class="{k}">{e(t)}</div>' for k, t in items)
            out.append(blk(f'<div class="card{" hot" if star else ""}"><div class="row"><div class="nm"><span class="cd">{code}</span>{e(name)}'
                           f'{"<span class=star>추천</span>" if star else ""}{f"<small>{e(small)}</small>" if small else ""}'
                           f'<div class="who">{e(who)}</div></div><div class="prs">{pr}</div></div>{body}</div>'))
            continue
        if st.startswith('■'):
            out.append(blk(f'<div class="h2">{e(st[1:].strip())}</div>', keep=True)); i += 1; continue
        if st.startswith('※'):
            t = st; i += 1
            while i < len(L) and L[i].startswith('   '): t += '\n' + L[i].strip(); i += 1
            out.append(blk(f'<div class="note">{e(t).replace(chr(10), "<br>")}</div>')); continue
        m = re.match(r'^(\d)\)\s*(.*)$', st)
        if m:  # 신청 방법 단계
            t = [m.group(2)]; i += 1
            while i < len(L) and L[i].startswith('   '): t.append(L[i].strip()); i += 1
            out.append(blk(f'<div class="step"><span class="no">{m.group(1)}</span><div><b>{e(t[0])}</b>{"".join(f"<div class=sub>{e(x)}</div>" for x in t[1:])}</div></div>')); continue
        if st.startswith('- '): out.append(blk(f'<div class="li">{e(st[2:])}</div>'))
        elif ln.startswith('   '): out.append(blk(f'<div class="sub">{e(st)}</div>'))
        else: out.append(blk(f'<div class="ln">{e(st)}</div>'))
        i += 1
    return out

# ── 신청서 (화이트) ──
def form(text):
    L = text.split('\n'); i = 1; out = []
    out.append(blk('<div class="tag">APPLICATION</div><h1>신청서</h1><div class="lead">남자들끼리 하는 말 · 1:1 남자 심리 분석</div>'))
    while i < len(L):
        ln = L[i]; st = ln.strip()
        if not st: i += 1; continue
        if st.startswith('※'):
            t = []
            while i < len(L) and L[i].strip().startswith('※'): t.append(L[i].strip()[1:].strip()); i += 1
            out.append(blk('<div class="nbox">' + ''.join(f'<div>{e(x)}</div>' for x in t) + '</div>')); continue
        m = re.match(r'^■\s*(\d)\.\s*(.*)$', st)
        if m:
            out.append(blk(f'<div class="h2"><i>{int(m.group(1)):02d}</i>{e(m.group(2))}</div>', keep=True)); i += 1; continue
        m = re.match(r'^(\d+)\)\s*(.*)$', st)
        no, body = (m.group(1), m.group(2)) if m else ('', st)
        consent = body.endswith('→')
        if consent: body = body[:-1].strip()
        lab, hint = body, ''
        if ' ※ ' in body: lab, hint = body.split(' ※ ', 1); hint = '※ ' + hint
        elif ':' in body:
            a, b = body.split(':', 1); lab, hint = a.strip(), b.strip()
        hints = [hint] if hint else []; ans = False; i += 1
        while i < len(L) and L[i].startswith('   '):
            t = L[i].strip()
            if t == '→': ans = True
            else: hints.append(t)
            i += 1
        hh = ''.join(f'<div class="hint">{e(x)}</div>' for x in hints)
        tail = f'<div class="chk">{"동의 / 비동의" if "비동의" in lab else "동의"} <span></span></div>' if consent else ('<div class="ans"></div>' if ans else '<div class="lnf"></div>')
        out.append(blk(f'<div class="field"><div class="lab">{f"<i>{no}</i>" if no else ""}{e(lab)}</div>{hh}{tail}</div>'))
    return out

# ── 결과물 틀 (화이트) ──
def report(text):
    L = text.split('\n'); i = 1; out = []
    out.append(blk('<div class="tag">REPORT</div><h1>결과물은<br>이렇게 드려요</h1><div class="lead">A · B는 자료가 다 도착한 때부터 72시간 안에 서면으로 드려요.</div>'))
    while i < len(L):
        st = L[i].strip()
        if not st: i += 1; continue
        m = re.match(r'^([ABC])\s*·\s*(.*)$', st)
        if m:
            out.append(blk(f'<div class="h2"><span class="cd">{m.group(1)}</span>{e(m.group(2))}</div>', keep=True)); i += 1; continue
        m = re.match(r'^(\d)\.\s*(.*)$', st) or re.match(r'^(\d~?\d?주차|\d주 뒤):\s*(.*)$', st)
        if m:
            n, t = m.groups(); hint = ''
            if n.isdigit() and ':' in t: t, hint = [x.strip() for x in t.split(':', 1)]
            mm = re.match(r'^(.*?)\s*\((.*)\)$', t)
            if mm and not hint: t, hint = mm.groups()
            num = f'{int(n):02d}' if n.isdigit() else n
            out.append(blk(f'<div class="it"><span class="n{" w" if not n.isdigit() else ""}">{e(num)}</span><div><b>{e(t)}</b>{f"<small>{e(hint)}</small>" if hint else ""}</div></div>')); i += 1; continue
        if st.startswith('✕') and i + 1 < len(L) and L[i + 1].strip().startswith('○'):
            a, b = st[1:].strip(), L[i + 1].strip()[1:].strip()
            out.append(blk(f'<div class="ex"><div><b>BEFORE</b>{e(a)}</div><div class="o"><b>AFTER</b>{e(b)}</div></div>')); i += 2; continue
        if st.startswith('→'): out.append(blk(f'<div class="arrow">{e(st)}</div>'))
        else: out.append(blk(f'<div class="h3">{e(st)}</div>', keep=True))
        i += 1
    return out

FONT = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700;800&family=Noto+Sans+KR:wght@400;500;700;900&display=block'>"
CSS = '''
*{box-sizing:border-box;margin:0;padding:0}body{background:#555;font-family:'Noto Sans KR',sans-serif;word-break:keep-all}
.pg{width:1080px;height:1350px;position:relative;overflow:hidden;margin-bottom:20px}
.tall{width:1080px;position:relative;margin-bottom:20px;padding-bottom:150px}
.in{position:absolute;left:84px;right:84px;top:84px;bottom:130px;overflow:hidden}.tall .in{position:static;padding:84px 84px 0}
.ft{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;font-size:22px;letter-spacing:.04em}
.ch{font-size:22px;letter-spacing:.25em;margin-bottom:26px}
h1{font-family:'Nanum Myeongjo',serif;font-weight:800;line-height:1.25}
.tag{font-size:23px;letter-spacing:.32em;font-weight:700}
.sp{height:10px}
/* 다크 골드 */
.dk{background:radial-gradient(120% 60% at 50% 0%,#2a2520,#121110 75%);color:#efe8dc}.dk.tall{background:#121110}
.dk .ft,.dk .ch{color:#8d8475}.dk .tag{color:#c9a24e}.dk h1{font-size:64px;margin:20px 0 24px}
.dk .lead{font-size:29px;line-height:1.6;color:#cfc6b6}
.dk .badge{display:inline-block;margin-top:24px;border:2px solid #c9a24e;color:#e5c172;padding:10px 24px;border-radius:999px;font-size:26px;font-weight:700}
.dk .hr{height:1px;background:linear-gradient(90deg,transparent,#c9a24e,transparent);margin:30px 0 8px}
.dk .card{margin-top:22px;border:1.5px solid rgba(201,162,78,.5);border-radius:22px;padding:28px 32px;background:rgba(255,255,255,.03)}
.dk .card.hot{border:2.5px solid #e5c172;background:rgba(229,193,114,.08)}
.dk .row{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:8px}
.dk .nm{font-size:33px;font-weight:700;line-height:1.3}.dk .nm small{font-size:22px;color:#b9ae9c;font-weight:400;margin-left:10px}
.dk .cd{font-family:'Nanum Myeongjo',serif;color:#e5c172;margin-right:12px}
.dk .who{font-size:23px;color:#b9ae9c;font-weight:400;margin-top:8px}
.dk .star{font-size:20px;background:#e5c172;color:#1a1712;padding:3px 12px;border-radius:8px;margin-left:12px;vertical-align:middle;font-weight:900}
.dk .prs{text-align:right;flex:none}.dk .pr{line-height:1.05}.dk .pr+.pr{margin-top:12px}
.dk .pr .pl{font-size:22px;color:#cfc6b6;margin-right:8px}.dk .pr s{font-size:22px;color:#8d8475}
.dk .pr b{display:block;font-family:'Nanum Myeongjo',serif;font-size:54px;color:#e5c172}.dk .pr b em{font-style:normal;font-size:28px;margin-left:2px}
.dk .li{font-size:25px;line-height:1.55;color:#ddd5c8;padding-left:26px;position:relative;margin-top:6px}
.dk .li:before{content:'';position:absolute;left:4px;top:16px;width:8px;height:8px;background:#c9a24e;transform:rotate(45deg)}
.dk .sub{font-size:23px;line-height:1.5;color:#a99f8e;padding-left:26px}
.dk .h2{font-family:'Nanum Myeongjo',serif;font-size:38px;color:#e5c172;margin:30px 0 10px;padding-bottom:10px;border-bottom:1px solid rgba(201,162,78,.4)}
.dk .ln{font-size:27px;line-height:1.65;color:#e2dacd}
.dk .note{font-size:22px;line-height:1.6;color:#9f9686;margin-top:8px}
.dk .step{display:flex;gap:20px;margin-top:16px;font-size:27px;line-height:1.5}.dk .step b{font-weight:700}
.dk .step .no{flex:none;width:46px;height:46px;border-radius:50%;border:2px solid #c9a24e;color:#e5c172;font-family:'Nanum Myeongjo',serif;display:flex;align-items:center;justify-content:center;font-size:26px}
.dk .step .sub{padding-left:0;margin-top:4px}
/* 화이트 리포트 */
.wh{background:#fbfaf7;color:#161514}.wh .ft{color:#9c968e;border-top:1px solid #d9d4cc;padding-top:18px;bottom:44px}.wh .ch{color:#8a2c2c}
.wh .tag{color:#8a2c2c}.wh h1{font-size:70px;margin:18px 0 18px}.wh .lead{font-size:27px;color:#5a5651;line-height:1.6;padding-bottom:30px;border-bottom:3px solid #161514;margin-bottom:6px}
.wh .nbox{font-size:23px;color:#5f5a54;line-height:1.6;background:#f1ede6;padding:22px 26px;border-left:4px solid #8a2c2c;margin-top:24px}.wh .nbox div+div{margin-top:6px}
.wh .h2{font-family:'Nanum Myeongjo',serif;font-size:42px;margin:40px 0 4px;padding-bottom:14px;border-bottom:2px solid #161514}
.wh .h2 i{font-style:normal;color:#8a2c2c;margin-right:16px}
.wh .h2 .cd{display:inline-block;background:#8a2c2c;color:#fff;font-family:'Noto Sans KR',sans-serif;font-size:26px;font-weight:900;padding:4px 14px;border-radius:6px;margin-right:16px;vertical-align:middle}
.wh .h3{font-size:27px;font-weight:700;margin-top:30px}
.wh .field{padding:22px 0 18px;border-bottom:1px solid #e2ddd5}
.wh .lab{font-size:28px;font-weight:700;line-height:1.45}.wh .lab i{font-style:normal;font-family:'Nanum Myeongjo',serif;color:#8a2c2c;margin-right:12px}
.wh .hint{font-size:22px;color:#837d75;line-height:1.55;margin-top:4px;padding-left:4px}
.wh .lnf{height:40px;border-bottom:2px dotted #c9c2b7}
.wh .ans{height:150px;margin-top:12px;border:1.5px dashed #c9c2b7;border-radius:10px;background:repeating-linear-gradient(transparent 0 48px,#ebe6de 48px 50px)}
.wh .chk{margin-top:10px;font-size:24px;font-weight:700;color:#8a2c2c}.wh .chk span{display:inline-block;width:150px;border-bottom:2px solid #8a2c2c;margin-left:8px}
.wh .it{display:flex;gap:22px;align-items:baseline;padding:24px 0;border-bottom:1px solid #d9d4cc}
.wh .it .n{flex:none;width:80px;font-family:'Nanum Myeongjo',serif;font-size:46px;color:#8a2c2c}.wh .it .n.w{font-size:28px;width:130px}
.wh .it b{font-size:31px;line-height:1.4}.wh .it small{display:block;font-size:23px;color:#77716a;margin-top:6px;line-height:1.5}
.wh .ex{margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.wh .ex div{padding:22px 24px;font-size:24px;line-height:1.6;border:1px solid #d9d4cc}.wh .ex .o{border:2px solid #161514;font-weight:700}
.wh .ex b{display:block;font-size:19px;letter-spacing:.2em;margin-bottom:8px;color:#8a2c2c}
.wh .arrow{font-size:24px;color:#5a5651;margin-top:14px;line-height:1.55}
'''
JS = '''<script>
function flow(id, theme, title, label){
  const src = document.getElementById('src_' + id), blocks = [...src.children];
  let pages = [], cur;
  const newPage = () => { const p = document.createElement('section'); p.className = 'pg ' + theme;
    p.innerHTML = '<div class="in"></div><div class="ft"><span>' + label + '</span><span class="pn"></span></div>';
    document.body.appendChild(p); pages.push(p); cur = p.querySelector('.in');
    if (pages.length > 1) cur.insertAdjacentHTML('beforeend', '<div class="ch">' + title + '</div>'); };
  newPage();
  for (const b of blocks) {
    cur.appendChild(b);
    if (cur.scrollHeight > cur.clientHeight + 1) {
      const moved = [b]; let prev = b.previousElementSibling;
      while (prev && prev.dataset && prev.dataset.k) { moved.unshift(prev); prev = prev.previousElementSibling; }
      newPage(); for (const m of moved) if (!m.querySelector('.sp')) cur.appendChild(m); else m.remove();
    }
  }
  // 장 처음 · 끝의 빈 줄 · 구분선은 지워요
  for (const p of pages) { const ins = p.querySelector('.in');
    while (ins.lastElementChild && ins.lastElementChild.querySelector('.sp,.hr')) ins.lastElementChild.remove(); }
  pages.forEach((p, k) => { p.id = id + '_' + (k + 1); p.querySelector('.pn').textContent = (k + 1) + ' / ' + pages.length; });
  src.remove();
  return pages.length;
}
</script>'''

DOCS = [  # (id, 블록, 테마, 이어지는 장 머리, 바닥 글)
 ('guide', guide(K.GUIDE_CH), 'dk', '1:1 남자 심리 분석 안내', '남자들끼리 하는 말 · 채널 안내문'),
 ('form', form(K.FORM), 'wh', 'APPLICATION · 신청서', '남자들끼리 하는 말 · 신청서'),
 ('report', report(K.REPORT), 'wh', 'REPORT · 결과물', '남자들끼리 하는 말 · 결과물'),
]

def build():
    h = f"<!doctype html><html lang='ko'><head><meta charset='utf-8'>{FONT}<style>{CSS}</style>{JS}</head><body>"
    for did, blocks, th, title, label in DOCS:  # 세로 전체
        h += f"<section class='tall {th}' id='doc_{did}'><div class='in'>{''.join(blocks)}</div><div class='ft'><span>{e(label)}</span><span>@mszexc</span></div></section>"
    for did, blocks, th, title, label in DOCS:  # 4:5로 나눌 원본 (렌더 때 flow()가 장으로 나눠요)
        h += f"<div id='src_{did}' class='{th}' style='width:912px'>{''.join(blocks)}</div>"
    return h + '</body></html>'

if __name__ == '__main__':
    t = build()
    assert '상담' not in t.replace('상담탭', '')
    open(os.path.join(D, 'kakao_menu', 'docs_v2.html'), 'w', encoding='utf-8').write(t)
    print('ok', [(d, len(b)) for d, b, *_ in DOCS])
