# 남자심리 처방전 (1:1 분석 결과물 PDF) — python3 rx.py <내용.txt> <출력.html>
# 내용 파일 형식 (손님 개인정보가 들어가므로 저장소 밖 .work/rx/ 에 둬요):
#   #patient 이름 / #plan 상품 / #date 발행일 / #no 처방 번호 / #label 3 FINDINGS|소견 / #qa 6 / #rx 7 (문진 · 처방 섹션 번호)
#   ■ 섹션 제목 · ①~⑨ 또는 Q1. 항목 제목 · "근거"/"논리" 한 줄 · "· " 근거 줄 · "→ " 결론
#   "근거: …"/"논리: …" 한 줄형 · "- " 체크 · step: 순서 · note: 사례(| 줄바꿈) · warn: 경고(|) · quote: 마지막 한 줄
import html, re, sys
e = html.escape
LABEL = {'먼저 한 줄 결론': ('DIAGNOSIS', '진단'), '1': ('CONSTITUTION', '체질 분석'), '2': ('SYMPTOMS', '말 · 행동 번역'),
         '3': ('CONDITION', '현재 상태'), '4': ('FINDINGS', '소견'), '5': ('CONSULTATION', '문진 답변'), '6': ('PROGNOSIS', '예후'),
         '7': ('EVIDENCE', '카톡 검사 결과'), '8': ('CAUSE', '재발 원인'), '9': ('PRESCRIPTION', '복약 지도'), '마지막으로': ('NOTE', '처방의 한마디')}

def q(s):  # 따옴표 안 말은 강조
    s = e(s)
    return re.sub(r'&quot;(.+?)&quot;', r'<span class="qt">“\1”</span>', s)

def parse(path):
    meta, intro, secs = {}, [], []
    cur = item = None
    for raw in open(path, encoding='utf-8').read().split('\n'):
        l = raw.rstrip()
        if not l.strip(): continue
        if l.startswith('#'):
            k, _, v = l[1:].partition(' ')
            if k == 'label':  # #label 3 FINDINGS|소견 — 섹션 번호별 영문 · 한글 꼬리표 덮어쓰기
                n, _, t = v.partition(' '); meta.setdefault('labels', {})[n] = tuple(t.split('|'))
            else: meta[k] = v
            continue
        if l.startswith('■'):
            t = l[1:].strip(); m = re.match(r'(\d+)\.\s*(.+)', t)
            cur = {'key': m.group(1) if m else t, 'title': m.group(2) if m else t, 'blocks': [], 'items': []}
            secs.append(cur); item = None; continue
        if cur is None: intro.append(l); continue
        tgt = item['blocks'] if item else cur['blocks']
        if re.match(r'^[①②③④⑤⑥⑦⑧⑨]\s', l) or re.match(r'^Q\d\.', l):
            item = {'title': l, 'blocks': []}; cur['items'].append(item); continue
        if l in ('근거', '논리'): tgt.append(('label', l)); continue
        m = re.match(r'^(근거|논리):\s*(.+)', l)
        if m: tgt.append(('inline', m.group(1), m.group(2))); continue
        for p, kind in (('· ', 'ev'), ('→ ', 'con'), ('- ', 'chk'), ('step:', 'step'), ('note:', 'note'), ('warn:', 'warn'), ('quote:', 'quote')):
            if l.startswith(p): tgt.append((kind, l[len(p):].strip())); break
        else: tgt.append(('p', l))
    return meta, intro, secs

def blocks_html(bl):
    out, buf, mode, n = [], [], None, 0
    def flush():
        nonlocal buf, mode
        if not buf: return
        if mode == 'ev': out.append('<div class="ev"><div class="tag">근거</div><ul>' + ''.join(f'<li>{q(x)}</li>' for x in buf) + '</ul></div>')
        elif mode == 'lg': out.append('<div class="lg"><div class="tag">논리</div>' + ''.join(f'<p>{q(x)}</p>' for x in buf) + '</div>')
        elif mode == 'p': out.append(''.join(f'<p class="plain">{q(x)}</p>' for x in buf))
        elif mode == 'chk': out.append('<ul class="chk">' + ''.join(f'<li>{q(x)}</li>' for x in buf) + '</ul>')
        elif mode == 'step': out.append('<ol class="steps">' + ''.join(f'<li>{q(x)}</li>' for x in buf) + '</ol>')
        elif mode == 'con': out.append('<div class="con">' + ''.join(f'<p>{q(x)}</p>' for x in buf) + '</div>')
        buf, mode = [], None
    label = None
    for b in bl:
        k = b[0]
        if k == 'label': flush(); label = b[1]; continue
        if k == 'ev': kind = 'ev'
        elif k == 'p': kind = 'lg' if label == '논리' else 'p'
        elif k in ('chk', 'step', 'con'): kind = k
        else: kind = None
        if k == 'con': label = None
        if kind:
            if mode != kind: flush(); mode = kind
            buf.append(b[1]); continue
        flush()
        if k == 'inline':
            out.append(f'<div class="inl"><span class="tag">{e(b[1])}</span><p>{q(b[2])}</p></div>')
        elif k == 'note':
            out.append('<div class="note"><div class="tag">지훈의 사례</div>' + ''.join(f'<p>{q(x)}</p>' for x in b[1].split('|')) + '</div>')
        elif k == 'warn':
            out.append('<div class="warn"><div class="tag">⚠ 주의</div>' + ''.join(f'<p>{q(x)}</p>' for x in b[1].split('|')) + '</div>')
        elif k == 'quote':
            out.append(f'<div class="quote">{q(b[1])}</div>')
    flush()
    return ''.join(out)

CSS = '''
@page { size: A4; margin: 16mm 15mm 18mm; }
:root { --ink:#1d2133; --mut:#585d72; --green:#1f2742; --green2:#efeaf5; --paper:#faf7f1; --line:#e6e0d4; --gold:#b9873a; --red:#b3392e; --red2:#fbecea; --night:#141a2e; --night2:#2a3152; --goldl:#d9a85b; --onn:#ece8df; --mauve:#7d6a9c; }
* { box-sizing:border-box; margin:0; padding:0; }
html, body { background:#fff; color:var(--ink); font-family:'Noto Sans KR', sans-serif; font-size:10.4pt; line-height:1.72; word-break:keep-all; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.serif { font-family:'Noto Serif KR', serif; }
/* 표지 */
.cover { height: 258mm; display:flex; flex-direction:column; border-radius:4mm; padding:12mm 12mm 13mm; position:relative; color:var(--onn);
  background: radial-gradient(ellipse at 85% 0, #4a4470 0, transparent 55%), radial-gradient(ellipse at 0 100%, rgba(217,168,91,.18) 0, transparent 45%), linear-gradient(160deg, var(--night2), var(--night) 70%); break-after: page; overflow:hidden; }
.cover:after { content:''; position:absolute; inset:3mm; border:0.6px solid rgba(217,168,91,.45); border-radius:3mm; pointer-events:none; }
.brand { display:flex; justify-content:space-between; align-items:center; font-size:9pt; color:rgba(236,232,223,.6); letter-spacing:.08em; }
.brand b { color:var(--goldl); letter-spacing:.02em; }
.rx { font-family:'Noto Serif KR', serif; font-size:54pt; font-weight:700; color:var(--goldl); line-height:1; margin-top:6mm; }
.rx small { font-size:13pt; color:var(--gold); letter-spacing:.3em; display:block; margin-top:3mm; }
h1.t { font-family:'Noto Serif KR', serif; font-size:31pt; font-weight:700; letter-spacing:-.02em; margin-top:6mm; line-height:1.2; }
.sub { color:var(--mut); font-size:11pt; margin-top:3mm; }
.cover .sub { color:rgba(236,232,223,.72); }
table.pt { width:100%; border-collapse:collapse; margin-top:9mm; font-size:10.5pt; background:rgba(255,255,255,.04); color:var(--onn); }
table.pt th, table.pt td { border:1px solid rgba(236,232,223,.18); padding:2.6mm 4mm; text-align:left; }
table.pt th { width:30mm; background:rgba(217,168,91,.12); color:var(--goldl); font-weight:700; }
.dx { margin-top:7mm; background:rgba(125,106,156,.28); border:1px solid rgba(217,168,91,.35); color:var(--onn); border-radius:3mm; padding:6mm 8mm; }
.dx .tag { color:var(--goldl); font-size:8.5pt; letter-spacing:.2em; font-weight:700; }
.dx p { font-size:12.2pt; line-height:1.75; margin-top:2mm; }
.dx .qt { color:var(--goldl); background:none; }
.dx p:last-child { font-weight:700; color:var(--goldl); font-size:13.5pt; }
.foot { margin-top:auto; padding-top:6mm; display:flex; justify-content:space-between; align-items:flex-end; }
.doc { font-size:9.5pt; color:var(--mut); line-height:1.6; }
.doc b { color:var(--ink); font-size:12pt; }
.cover .doc { color:rgba(236,232,223,.65); } .cover .doc b { color:var(--onn); }
.cover .stamp { color:var(--goldl); border-color:var(--goldl); outline-color:var(--goldl); }
.stamp { width:30mm; height:30mm; border:2.2px solid var(--red); border-radius:50%; color:var(--red); display:flex; flex-direction:column; align-items:center; justify-content:center;
  font-family:'Noto Serif KR', serif; font-weight:700; font-size:9pt; line-height:1.3; text-align:center; transform:rotate(-12deg); opacity:.85; outline:0.8px solid var(--red); outline-offset:-2.2mm; }
.stamp b { font-size:13pt; }
/* 본문 */
.intro { background:var(--paper); border:1px solid var(--line); border-radius:3mm; padding:6mm 7mm; margin-bottom:8mm; }
.intro p { font-size:11pt; }
.sec { margin-top:9mm; }
.sh { display:block; border-bottom:2px solid var(--green); padding-bottom:2mm; margin-bottom:5mm; break-after:avoid; break-inside:avoid; }
.sh > div { display:inline-block; vertical-align:baseline; margin-left:4mm; }
.sh .num { font-family:'Noto Serif KR', serif; font-size:24pt; font-weight:700; color:var(--green); line-height:1; }
.sh .eb { font-size:8pt; letter-spacing:.22em; color:var(--gold); font-weight:700; display:block; }
.sh h2 { font-family:'Noto Serif KR', serif; font-size:16pt; font-weight:700; line-height:1.3; }
.item { margin:0 0 6mm; }
.it { break-inside:avoid; font-weight:700; font-size:11.6pt; color:var(--green); margin-bottom:2.5mm; padding-left:3.5mm; border-left:3px solid var(--gold); break-after:avoid; line-height:1.5; }
.tag { font-size:7.8pt; font-weight:700; letter-spacing:.12em; color:var(--green); margin-bottom:1mm; }
.ev { background:var(--paper); border:1px solid var(--line); border-radius:2mm; padding:3mm 4.5mm; margin-bottom:2.5mm; break-inside:avoid; }
.ev ul { list-style:none; } .ev li { font-size:9.6pt; color:#3d4642; padding-left:3.5mm; position:relative; line-height:1.65; }
.ev li:before { content:''; position:absolute; left:0; top:2.6mm; width:1.4mm; height:1.4mm; background:var(--gold); border-radius:50%; }
.lg { padding:1mm 1mm 0 1mm; margin-bottom:2.5mm; }
.lg p, .plain { margin-bottom:1mm; }
.plain { margin-bottom:2.5mm; }
.con { background:var(--green2); border-left:4px solid var(--green); border-radius:0 2mm 2mm 0; padding:3mm 4.5mm; margin-top:1mm; break-inside:avoid; }
.con p { font-weight:700; color:#1f2742; }
.con p:before { content:'→ '; color:var(--gold); }
.note { background:#fff8e8; border:1px dashed var(--gold); border-radius:2mm; padding:3.5mm 5mm; margin:2.5mm 0; break-inside:avoid; }
.note .tag { color:var(--gold); }
.warn { background:var(--red2); border-left:4px solid var(--red); border-radius:0 2mm 2mm 0; padding:3.5mm 5mm; margin-top:3mm; break-inside:avoid; }
.warn .tag { color:var(--red); } .warn p { font-weight:700; color:#6e231b; }
.inl { display:flex; gap:3mm; margin-bottom:1.5mm; } .inl .tag { flex:0 0 9mm; margin-top:1mm; } .inl p { flex:1; }
.steps { list-style:none; counter-reset:s; margin:3mm 0 4mm; border:1px solid var(--line); border-radius:2mm; padding:3mm 5mm; background:var(--paper); break-inside:avoid; }
.steps li { counter-increment:s; padding-left:9mm; position:relative; margin:1.2mm 0; }
.steps li:before { content:counter(s); position:absolute; left:0; top:0.4mm; width:6mm; height:6mm; border-radius:50%; background:var(--green); color:#fff; font-size:8.5pt; font-weight:700; text-align:center; line-height:6mm; }
.chk { list-style:none; margin:2mm 0 3mm; } .chk li { padding-left:8mm; position:relative; margin:1.4mm 0; }
.chk li:before { content:'✓'; position:absolute; left:0; top:-0.2mm; width:5.5mm; height:5.5mm; border:1.4px solid var(--green); border-radius:1mm; color:var(--green); font-weight:900; font-size:9pt; text-align:center; line-height:5.2mm; }
.qt { font-weight:700; color:#1d2133; background:#f5e8cf; border-radius:1mm; padding:0 0.8mm; -webkit-box-decoration-break:clone; box-decoration-break:clone; }
.rxsec .item { border:1px solid var(--line); border-radius:3mm; padding:4mm 5mm 3mm; background:#fff; break-inside:avoid; }
.rxsec .it { border-left:none; padding-left:0; font-size:12pt; }
.rxsec .it:before { content:'Rx  '; font-style:italic; color:var(--red); font-family:'Noto Serif KR', serif; }
.qa .it { color:var(--ink); background:var(--green2); border-left:none; padding:2.5mm 4mm; border-radius:2mm; }
.last { background:var(--paper); border-radius:3mm; padding:7mm 8mm; border:1px solid var(--line); break-inside:avoid; }
.last .plain { font-size:11pt; margin-bottom:1mm; }
.quote { font-family:'Noto Serif KR', serif; font-weight:700; font-size:14pt; color:var(--green); text-align:center; margin-top:6mm; padding-top:5mm; border-top:1px solid var(--line); line-height:1.6; }
.disc { margin-top:9mm; font-size:8.6pt; color:var(--mut); text-align:center; line-height:1.6; }
.sign { margin-top:7mm; display:flex; justify-content:flex-end; align-items:center; gap:6mm; }
'''

def build(path):
    meta, intro, secs = parse(path)
    dx = next((s for s in secs if s['key'] == '먼저 한 줄 결론'), None)
    pt = meta.get('patient', '')
    stamp = '<div class="stamp">남자들끼리<br><b>處方</b>하는 말</div>'
    cover = f'''<section class="cover">
  <div class="brand"><b>남자들끼리 하는 말 · 1:1 남자 심리 분석</b><span>No. {e(meta.get('no',''))}</span></div>
  <div class="rx"><i>Rx</i><small>PRESCRIPTION</small></div>
  <h1 class="t">남자심리 처방전</h1>
  <div class="sub">그 사람이 왜 그랬는지, 남자 입장에서 진단하고 처방합니다.</div>
  <table class="pt"><tr><th>환자명</th><td>{e(pt)} 님</td></tr><tr><th>처방 구분</th><td>{e(meta.get('plan',''))}</td></tr>
  <tr><th>발행일</th><td>{e(meta.get('date',''))}</td></tr><tr><th>처방</th><td>박지훈 (@mszexc)</td></tr></table>
  <div class="dx"><div class="tag">DIAGNOSIS · 진단</div>{''.join(f'<p>{q(x[1])}</p>' for x in dx['blocks']) if dx else ''}</div>
  <div class="foot"><div class="doc">처방 · <b>박지훈</b><br>남자가 직접 말하는 남자 심리<br>카카오채널 「남자가 말하는 남자심리」</div>{stamp}</div>
</section>'''
    body = [f'<div class="intro">{"".join(f"<p>{q(x)}</p>" for x in intro)}</div>']
    for s in secs:
        if s is dx: continue
        eb, kr = meta.get('labels', {}).get(s['key']) or LABEL.get(s['key'], ('', ''))
        num = s['key'] if s['key'].isdigit() else '✦'
        cls = 'sec' + (' rxsec' if s['key'] == meta.get('rx', '9') else '') + (' qa' if s['key'] == meta.get('qa', '5') else '')
        head = f'<div class="sh"><span class="num">{num if num != "✦" else "✦"}</span><div><span class="eb">{e(eb)} · {e(kr)}</span><h2>{e(s["title"])}</h2></div></div>'
        inner = blocks_html(s['blocks'])
        items = ''.join(f'<div class="item"><div class="it">{q(it["title"])}</div>{blocks_html(it["blocks"])}</div>' for it in s['items'])
        if s['key'] == '마지막으로':
            inner = f'<div class="last">{inner}</div>'
        body.append(f'<section class="{cls}">{head}{inner}{items}</section>')
    body.append('<div class="sign"><div class="doc" style="text-align:right">처방 · <b>박지훈</b><br>남자들끼리 하는 말</div>' + stamp + '</div>')
    body.append('<p class="disc">남자 입장에서 해석해 드린 내용입니다. 그의 마음과 선택은 그 사람에게 달려 있어서 100% 장담할 수는 없습니다.<br>의료 · 치료 목적의 처방이 아닙니다. 이 처방전은 ' + e(pt) + ' 님만을 위해 작성되었습니다.</p>')
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>남자심리 처방전 · {e(pt)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Serif+KR:wght@500;700&display=block">
<style>{CSS}</style></head><body>{cover}{"".join(body)}</body></html>'''

if __name__ == '__main__':
    open(sys.argv[2], 'w', encoding='utf-8').write(build(sys.argv[1]))
    print('ok')
