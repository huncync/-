import json, datetime as dt
d=json.load(open('plan90.json')); rows=d['rows']
car=[]; n=7
for r in rows: car.append(dict(date=dt.date.fromisoformat(r[0]),slot=r[1],s=r[2],t=r[3],note=r[4],no=n)); n+=1
OK={'S1','S2','S3','S4','S5','S7','M','D','E'}
used=set(); reels=[]
day=dt.date(2026,10,18); k=1
while day<=dt.date(2027,1,13):
    if day.weekday() in (1,3,6):
        if k==1:
            tgt=next(c for c in car if c['t']=='다시 좋아진 걸까, 정리하는 걸까')
            title='헤어지기 전 남자가 갑자기 잘해주는 이유'; done='대본 완성'
        else:
            tgt=None
            for lo,hi in ((2,4),(1,6)):
                cands=[c for c in car if c['s'] in OK and c['no'] not in used and lo<=(c['date']-day).days<=hi]
                if cands: tgt=sorted(cands,key=lambda c:((c['date']-day).days, c['slot']))[0]; break
            title=tgt['t'] if tgt else '(소재 미정)'; done=''
        if tgt: used.add(tgt['no'])
        reels.append(dict(date=day.isoformat(),no=k,title=title,s=tgt['s'] if tgt else None,link_no=tgt['no'] if tgt else None,link_date=tgt['date'].isoformat() if tgt else None,link_t=tgt['t'] if tgt else None,done=done))
        k+=1
    day+=dt.timedelta(1)
# --- manual overrides (keep on rerun)
import importlib.util
by={x['date']:x for x in reels}
by['2026-11-15'].update(title='남자의 말이 줄어들 때, 여자가 꼭 알아야 할 것',s='S7',link_no=None,link_date=None,link_t=None,done='3권 예약 마감(11/17) 홍보')
by['2026-10-18']['done']='업로드 완료'; by['2026-10-20']['done']='대본 완성 · 10/22 업로드 (캐러셀 #19 다음에)'
by['2026-10-22']['done']='건너뜀 · R2가 10/22로 밀림'
spec=importlib.util.spec_from_file_location('h','/home/user/-/reels/her_reasons.py'); h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
for rank,title,hook,flip,date in h.HER:
    by[date].update(title=title,s='W',link_no=None,link_date=None,link_t=None,kind='W',hook=hook,flip=flip,rank=rank)
json.dump(reels,open('reels90.json','w'),ensure_ascii=False,indent=0)
print(len(reels)); [print(r['date'],'R%d'%r['no'],r['title'],'→',r['link_date'],'#%s'%r['link_no']) for r in reels]
