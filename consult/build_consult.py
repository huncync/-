# menu.py · dm.py → menu.md + 작업실 상담 탭 (python3 build_consult.py <index.html>)
import html, sys, importlib.util, os
e = html.escape
D = os.path.dirname(os.path.abspath(__file__))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(D, n + '.py')); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
M, DM, K = load('menu'), load('dm'), load('kakao')

md = ['# 남자 심리 분석 · 상품 메뉴', '']
for c, n, p, who, items, cap in M.MAIN:
    md += [f'## {c}. {n} · {p}', f'{who} (한도: {cap})'] + [f'- {x}' for x in items] + ['']
md += ['## 추가 옵션 (신청자 전용)'] + [f'- {n} · {p} — {d}' for n, p, d in M.OPTS] + ['']
md += ['## 운영 원칙'] + [f'{i}. {x}' for i, x in enumerate(M.NOTES, 1)] + ['']
for h, body in (('채널 안내문', M.GUIDE), ('신청서', M.FORM), ('결과물 틀', M.REPORT)):
    md += [f'## {h}', '```', body, '```', '']
open(os.path.join(D, 'menu.md'), 'w', encoding='utf-8').write('\n'.join(md))

cards = ''.join(
    f'<div class="pc-card{" rec" if c == "B" else ""}"><div class="pc-top"><span class="pc-code">{c}</span><span class="pc-name">{e(n)}</span></div>'
    f'<div class="pc-price">{e(p)}</div><div class="pc-who">{e(who)}</div><ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul><div class="pc-cap">한도 · {e(cap)}</div></div>'
    for c, n, p, who, items, cap in M.MAIN)
opts = ''.join(f'<li><b>{e(n)}</b><span>{e(p)}</span><em>{e(d)}</em></li>' for n, p, d in M.OPTS)
notes = ''.join(f'<li>{e(x)}</li>' for x in M.NOTES)
menu_html = f'''    <h2>상품 메뉴</h2>
    <div class="pc-grid">{cards}</div>
    <h2>추가 옵션<small>신청자 전용</small></h2>
    <ul class="pc-opts">{opts}</ul>
    <h2>운영 원칙</h2>
    <ol class="pc-notes">{notes}</ol>
'''
flow = ''.join(f'<li><span class="n">{i}</span><span class="t"><b>{e(a)}</b> · {e(b)}</span><span></span></li>' for i, (a, b) in enumerate(DM.FLOW, 1))
rules = ''.join(f'<li>{e(r)}</li>' for r in DM.RULES)
tpl = ''.join(f'<details class="cap"><summary>{e(t)}</summary><div class="row" style="padding:0 14px"><button class="btn gold" data-ct="cs-{k}">복사</button></div><pre id="cs-{k}">{e(x)}</pre></details>' for k, t, x in DM.T)
launch = ''.join(f'<li><span class="d">{e(a)}</span><span class="m"><b>{e(b)}</b></span></li>' for a, b in DM.LAUNCH)
note = ''.join(f'<div><b>{e(a)}:</b> {e(b)}</div>' for a, b in DM.NOTE)
dm_html = f'''    <h2>DM → 유료 상담 전환<small>DM에서는 상담하지 않고, 길만 안내</small></h2>
    <ol class="topics">{flow}</ol>
    <ol class="pc-notes" style="margin-top:10px">{rules}</ol>
    <h2>DM 답장 문구<small>인스타 "저장된 답장"에 등록</small></h2>
    {tpl}
    <h2>오픈 순서</h2>
    <ol class="plan subplan">{launch}</ol>
    <div class="note">{note}</div>
'''

# 채널용 안내문: 카카오 소개 메시지에서 "상담"이 금칙어라 채널에 올리는 판은 "상담"을 뺀다
GUIDE_CH = (M.GUIDE.replace('전문 심리상담이 아닙니다', '의료 · 치료 목적의 서비스가 아닙니다')
            .replace('상담 자리가 열리기', '분석 자리가 열리기').replace('상담', '분석'))
assert '상담' not in GUIDE_CH
for i, s in enumerate(K.STEPS):
    if s[0] == '5' and not any(c[0] == 'kk-guide-ch' for c in s[4]):
        K.STEPS[i] = s[:4] + ([('kk-guide-ch', '소식 ① 채널용 안내문 ("상담" 뺀 판)', GUIDE_CH)] + s[4],)
    if s[0] == '2' and len(s[4]) == 1:
        K.STEPS[i] = s[:4] + (s[4] + [(f'kk-intro{j}', f'소개 메시지 다른 안 {j}', x) for j, x in enumerate(K.INTRO_ALT, 1)],)
st = ''.join(f'<div class="ik"><small>{e(a)}</small><b>{e(b)}</b><span>{e(c)}</span></div>' for a, b, c in K.STATUS)
def kcopy(cid, lab, body):
    return f'<details class="cap"><summary>{e(lab)}</summary><div class="row" style="padding:0 14px"><button class="btn gold" data-ct="{cid}">복사</button></div><pre id="{cid}">{e(body)}</pre></details>'
steps = ''.join(f'<li><span class="n">{n}</span><span class="t"><b>{e(ti)}</b> <span class="dim">· {e(wh)}</span><br>{desc}{"".join(kcopy(*c) for c in cps)}</span><span></span></li>' for n, ti, wh, desc, cps in K.STEPS)
kakao_html = f'''    <h2>카카오채널 세팅<small>「{e(K.NAME)}」 · 10/28 캡처 기준 · 순서대로</small></h2>
    <style>.kks .ik {{ background:#141416; border:1px solid #2a2a2d; border-radius:12px; padding:10px 12px; }} .kks .ik small {{ display:block; font-size:12px; opacity:.7; }} .kks .ik b {{ display:block; font-size:18px; margin:2px 0; }} .kks .ik span {{ font-size:12px; opacity:.75; }} .kks .kg {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }} .kk ol.topics li .t details {{ margin-top:8px; }}</style>
    <div class="kks"><div class="kg">{st}</div>
    <div class="tip" style="margin-top:10px">{K.VERDICT}</div>
    <ol class="topics">{steps}</ol>
    <div class="note"><div><b>링크 넣는 곳:</b> {e(K.WHERE)}</div></div></div>
'''
dm_html = kakao_html + dm_html

def swap(t, start, end, new):
    a = t.index(start); b = t.index(end, a); return t[:a] + new + t[b:]
def pre(t, pid, body):
    a = t.index(f'<pre id="{pid}">') + len(f'<pre id="{pid}">'); b = t.index('</pre>', a); return t[:a] + e(body) + t[b:]

P = sys.argv[1]
t = open(P, encoding='utf-8').read()
c0 = t.index('id="p-consult"')
head, t2 = t[:c0], t[c0:]
t2 = swap(t2, '    <h2>상품 메뉴</h2>', '    <h2>카카오채널 이미지', menu_html)
t2 = swap(t2, '    <h2>카카오채널 세팅' if '    <h2>카카오채널 세팅' in t2 else '    <h2>DM → 유료 상담 전환', '    <h2>복사해서 쓰기</h2>', dm_html)
for pid, body in (('cs-guide', M.GUIDE), ('cs-form', M.FORM), ('cs-report', M.REPORT)):
    t2 = pre(t2, pid, body)
open(P, 'w', encoding='utf-8').write(head + t2)
print('ok', len(M.MAIN), 'products', len(M.OPTS), 'options')
