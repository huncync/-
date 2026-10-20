import json, html, datetime as dt, re, sys
from collections import Counter
e=html.escape
d=json.load(open('plan90.json'))
rows=d['rows']
LAB={'S1':('신호','#e0b46a'),'S2':('번역','#8fb3d6'),'S3':('비교','#d9a3a3'),'S4':('진심','#b9d38f'),'S5':('이별','#b8a3d9'),'C':('반어','#7fd1c7'),'S6':('그녀','#bdbdbd'),'S7':('3권','#f0d264'),'H':('합본','#f2a65a'),'Q':('사연','#ffffff')}
ORDER=['S1','S2','S3','C','S4','S5','S6','S7','H','Q']
DOW='월화수목금토일'
PH=[('1단계 · 공식 굳히기','10/16 ~ 11/4','검증된 시리즈를 매일 2편. 첫 2주에 하루 2편이 편당 조회를 깎는지 확인',dt.date(2026,10,16),dt.date(2026,11,4)),
    ('2단계 · 3권 예고와 예약','11/5 ~ 11/17','저녁(18~19시)은 3권 주제로. 11/11~17 마지막 장 = 예약 29,000원',dt.date(2026,11,5),dt.date(2026,11,17)),
    ('3단계 · 시리즈 확장','11/18 ~ 12/12','잘된 시리즈에 편수 몰기. 12/2 3권 발송 → 후기·질문 활용',dt.date(2026,11,18),dt.date(2026,12,12)),
    ('4단계 · 연말·새해 시즌','12/13 ~ 1/13','크리스마스·연말·새해 소재가 가장 잘 퍼지는 시기',dt.date(2026,12,13),dt.date(2027,1,13))]
CAPS=json.load(open('captions90.json'))
R=json.load(open('reels90.json')); RB={x['date']:x for x in R}
def capdet(no):
    k=f'#{no:02d}'
    if k not in CAPS: return ''
    _,c,p=CAPS[k]
    return (f'<details class="pc"><summary>캡션 · 고정 댓글</summary><div class="row"><button class="btn gold" data-ct="p90cap{no}">캡션 복사</button><button class="btn" data-ct="p90pin{no}">고정 댓글 복사</button></div>'
            f'<pre id="p90cap{no}">{e(c)}</pre><div class="pl">고정 댓글</div><pre id="p90pin{no}">{e(p)}</pre></details>')

import importlib.util, os
def reeldet(n):
    f=f'/home/user/-/reels/R{n}.py'
    if not os.path.exists(f): return ''
    spec=importlib.util.spec_from_file_location(f'R{n}',f); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); X=m.R
    k=f'r{n}'
    st='\n\n'.join(f"[{a} · {b}]\n{c}" for a,b,c,_ in X['script'])
    rows=''.join(f'<div class="sc"><div class="st">{e(a)} <b>{e(b2)}</b></div><div class="sl">{e(c)}</div>'+(f'<div class="sn">{e(d)}</div>' if d else '')+'</div>' for a,b2,c,d in X['script'])
    return (f'<details class="pc"><summary>대본 · 캡션 · 고정 댓글 ({e(X["len"])})</summary>'
     f'<div class="toptxt"><small>{e(X["label"])}</small>{"<br>".join(e(x) for x in X["top"])}</div>'
     f'<div class="row"><button class="btn gold" data-ct="{k}script">대본 복사</button><button class="btn" data-ct="{k}cap">캡션 복사</button><button class="btn" data-ct="{k}pin">고정 댓글 복사</button></div>'
     f'<div class="scs">{rows}</div><pre id="{k}script" hidden>{e(st)}</pre>'
     f'<div class="pl">촬영 메모</div><ul class="shoot">{"".join("<li>"+e(s)+"</li>" for s in X["shoot"])}</ul>'
     f'<div class="pl">캡션</div><pre id="{k}cap">{e(X["caption"])}</pre><div class="pl">고정 댓글</div><pre id="{k}pin">{e(X["pin"])}</pre></details>')
byday={}; n=7
for r in rows:
    r=list(r); r.append(n); n+=1; byday.setdefault(r[0],[]).append(r)
md=['# 90일 캐러셀 목차 (10/16 ~ 1/13, 하루 2편 · 11~12시 / 18~19시)\n']
parts=[]
for name,rng,desc,a,b in PH:
    parts.append(f'<h2>{name}<small>{rng}</small></h2><p class="lead">{desc}</p><ol class="p90">')
    md.append(f'## {name} ({rng})\n{desc}\n')
    day=a
    while day<=b:
        lines=''
        items=sorted(byday.get(day.isoformat(),[]),key=lambda r:r[1])
        rl=RB.get(day.isoformat())
        seq=[('c',items[0])]+([('r',rl)] if rl else [])+[('c',x) for x in items[1:]]
        for kind,obj in seq:
            if kind=='r':
                lk=(f' → 캐러셀 #{obj["link_no"]:02d} ({int(obj["link_date"][5:7])}/{int(obj["link_date"][8:])}) 예고' if obj['link_no'] else (' · 그녀의 진짜 이유 (잔소리 공식)' if obj.get('kind')=='W' else ''))
                lines+=(f'<div class="pl9 rl"><span class="tm">21시</span><span class="sr" style="background:{"#c86bff" if obj.get("kind")=="W" else "#ff5c8a"};color:#fff">릴스</span>'
                        f'<span class="tt">{e(obj["title"])}<em>R{obj["no"]}{lk}{" · "+e(obj["done"]) if obj["done"] else ""}</em></span></div>')
                md.append(f'- {day.month}/{day.day}({DOW[day.weekday()]}) 21시 [릴스] R{obj["no"]} {obj["title"]}{lk}')
                continue
            _,slot,s,t,note,no=obj
            lab,col=LAB[s]
            lines+=(f'<div class="pl9 cr"><span class="tm">{"11~12시" if slot==0 else "18~19시"}</span><span class="sr" style="background:{col}">{lab}</span>'
                    f'<span class="tt">{e(t)}<em>#{no:02d}{" · "+e(note) if note else ""}</em>{capdet(no)}</span></div>')
            md.append(f'- {day.month}/{day.day}({DOW[day.weekday()]}) {"11~12시" if slot==0 else "18~19시"} [{lab}] #{no:02d} {t}'+(f' — {note}' if note else ''))
        wk=' class="wk"' if day.weekday()>=5 else ''
        parts.append(f'<li{wk}><span class="d">{day.month}/{day.day}<i>{DOW[day.weekday()]}</i></span><div>{lines}</div></li>')
        day+=dt.timedelta(1)
    parts.append('</ol>'); md.append('')
spare=[(k,t) for k,v in d['left'].items() for t in v]
parts.append('<h2>예비 소재<small>반응 좋은 시리즈가 나오면 바로 교체 투입</small></h2><ol class="topics">'+''.join(f'<li><span class="n"><span class="sr" style="background:{LAB[k][1]}">{LAB[k][0]}</span></span><span class="t">{e(t)}</span><span></span></li>' for k,t in spare)+'</ol>')
md.append('## 예비 소재\n'+'\n'.join(f'- [{LAB[k][0]}] {t}' for k,t in spare)+'\n')
c=Counter(r[2] for r in rows)
legend=''.join(f'<span class="lg"><span class="sr" style="background:{LAB[k][1]}">{LAB[k][0]}</span>{e(d["series"][k])} · {c[k]}편</span>' for k in ORDER)
head=f'''    <div class="tip"><b>목표 · 3개월 안에 캐러셀 조회 100만</b><br>
      10월 지금까지 124,760회. 남은 87.5만 ÷ 180편 = <b>편당 평균 4,900회</b>면 누적 100만입니다.<br>
      남자 해독형 평균이 2.8만이라 이 페이스면 누적 100만은 11월 안에 넘습니다. 그래서 진짜 목표는 <b>월간 100만</b> = 60편 × <b>편당 1.7만</b>.</div>
    <div class="rules" style="margin-top:12px">
      <div><b>11~12시</b> 저장형: 신호 · 진심 · 비교 · 반어(화·금) · 합본 &nbsp; <b>18~19시</b> 감정형: 번역 · 이별 · 그녀의 말 · 3권 · 사연</div>
      <div><b>반어(C형)</b> · #06 「버림받는 법」 1시간 반 만에 7,471회, 비팔로워 노출이 평소의 약 3배, 저장이 좋아요의 2배. 공유는 0이라 마지막 장 문구를 "생각난 사람 있으면 보내주세요"로 바꿉니다.</div>
      <div><b>릴스</b> · 팔로우 담당. 화·목·일 21시, 남자 해독형만. 핵심 3개만 말하고 "나머지는 ○요일 캐러셀에"로 2~3일 뒤 캐러셀 완전판을 예고합니다.</div>
      <div><b>고정 리듬</b> · 화·금 낮 = 반어, 일요일 밤 = 그녀의 말 번역, 수요일 밤 = 댓글 사연 답변(10/28~), 격주 토요일 낮 = 합본</div>
      <div><b>점검</b> · 매주 일요일, 편당 평균 1만 이상이면 그대로. 5천 아래로 2주 연속이면 하루 1편으로 되돌리고 약한 시리즈를 뺍니다.</div>
      <div><b>위험</b> · 하루 2편이면 팔로워 피드 노출이 나뉘어 편당 조회가 줄 수 있어요. 첫 2주는 "2편 합계 > 예전 1편"인지 꼭 확인.</div>
    </div>
    <div class="legend">{legend}<span class="lg"><span class="sr" style="background:#ff5c8a;color:#fff">릴스</span>화·목 21시 · 캐러셀 예고</span><span class="lg"><span class="sr" style="background:#c86bff;color:#fff">릴스</span>일 21시 · 그녀의 진짜 이유</span></div>
    <div class="flt" role="group" aria-label="보기"><button class="btn gold" data-f="all">전체 <b>{180+len(R)}</b></button><button class="btn" data-f="cr">캐러셀 <b>180</b></button><button class="btn" data-f="rl">릴스 <b>{len(R)}</b></button></div>
'''
md.insert(1,'목표: 10월 124,760회 → 3개월 안에 100만. 누적 기준 편당 평균 4,900회, 월간 100만 기준 편당 1.7만.\n\n시리즈별 편수: '+', '.join(f'{d["series"][k]} {c[k]}' for k in ORDER)+'\n')
open('plan90.md','w',encoding='utf-8').write('\n'.join(md))
P=sys.argv[1]
t=open(P,encoding='utf-8').read()
a=t.index('<section class="panel" id="p-plan"'); a2=t.index('>',a)+1; b=t.index('</section>',a)
sec=t[a2:b]
old=sec[sec.index('<details class="old">'):]
t=t[:a2]+'\n'+head+'\n'.join(parts)+'\n    '+old+'\n  '+t[b:]
t=t.replace('ol.topics .n {','ol.topics .n .sr { width: 30px; }\n  ol.topics .n {',1) if 'ol.topics .n .sr' not in t else t
# ---- reels tab
a=t.index('<section class="panel" id="p-reels"'); b=t.index('</section>',a)
sec=t[a:b]
h0=(sec.index('<h2>일요일 · 그녀의 진짜 이유') if '<h2>일요일 · 그녀의 진짜 이유' in sec else sec.index('<h2>90일 릴스 목록') if '<h2>90일 릴스 목록' in sec else sec.index('<h2>1주차')); h1=sec.index('<h2>예비 소재')
items=[]
for x in R:
    dd=dt.date.fromisoformat(x['date'])
    lk=(f'캐러셀 #{x["link_no"]:02d} 「{e(x["link_t"])}」 {int(x["link_date"][5:7])}/{int(x["link_date"][8:])} 예고' if x['link_no'] else '')
    extra=reeldet(x['no'])
    st=f'<span class="k3" style="background:#b9d38f">{e(x["done"])}</span> ' if x['done'] else ''
    if x.get('kind')=='W':
        items.append(f'<li><span class="d">{dd.month}/{dd.day}<i>{DOW[dd.weekday()]}</i></span><span class="ty" style="background:#c86bff;color:#fff">그</span><span class="m"><b>{e(x["title"])}</b><em class="hk"><span class="k3">첫 3초</span> {e(x["hook"])}</em><em class="em2"><span class="k3">뒤집기</span> {e(x["flip"])}</em><em>{st}R{x["no"]} · 21시 · 그녀의 진짜 이유</em></span>{extra}</li>')
        continue
    items.append(f'<li><span class="d">{dd.month}/{dd.day}<i>{DOW[dd.weekday()]}</i></span><span class="ty" style="background:#ff5c8a;color:#fff">R</span><span class="m"><b>{e(x["title"])}</b><em>{st}R{x["no"]} · 21시{" · "+lk if lk else ""}</em></span>{extra}</li>')
spec=importlib.util.spec_from_file_location('her','/home/user/-/reels/her_reasons.py'); HM=importlib.util.module_from_spec(spec); spec.loader.exec_module(HM)
nW=sum(1 for x in R if x.get('kind')=='W')
herbox=('<h2>일요일 · 그녀의 진짜 이유<small>잔소리 릴스 공식 · '+str(nW)+'편</small></h2>'
  '<div class="tip">잔소리 릴스에 "전생에 여자 아니냐"는 댓글이 쏟아진 이유: <b>여자가 미안해하던 행동을, 남자가 "그게 사랑이야"라고 대신 말해줬기 때문</b>이에요. 위로가 아니라 인정. 얼굴 보고 남자 목소리로 들어야 힘이 나는 소재라 캐러셀보다 릴스로 먼저 올립니다.</div>'
  '<ol class="topics">'+''.join(f'<li><span class="n">{i}</span><span class="t">{e(s)}</span><span></span></li>' for i,s in enumerate(HM.FORMULA,1))+'</ol>'
  '<div class="note"><div><b>예비:</b> '+' / '.join(e(s[1]) for s in HM.SPARE)+'</div><div><b>끝 멘트 고정:</b> "안 해도 되는데, 이 남자랑 오래 가고 싶어서 굳이 하는 거예요. 그러니까 귀찮아하지 마세요."</div></div>')
lst=herbox+'<h2>90일 릴스 목록<small>화·목·일 21시 · '+str(len(R))+'편</small></h2><p class="lead"><b style="color:#ff5c8a">화·목</b> = 2~3일 뒤 캐러셀의 핵심 3개만 말하는 예고편(남자 해독). <b style="color:#c86bff">일요일</b> = 그녀의 진짜 이유(인정형). 대본은 후보 훅을 먼저 보여드리고, 고르시면 씁니다.</p><ol class="plan">'+''.join(items)+'</ol>\n    '
sec=sec[:h0]+lst+sec[h1:]
t=t[:a]+sec+t[b:]
open(P,'w',encoding='utf-8').write(t)
print(c, len(spare))
