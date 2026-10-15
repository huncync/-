import json, datetime as dt
d=json.load(open('plan90.json')); rows=d['rows']
car=[]; n=7
for r in rows: car.append(dict(date=dt.date.fromisoformat(r[0]),slot=r[1],s=r[2],t=r[3],note=r[4],no=n)); n+=1
OK={'S1','S2','S3','S4','S5','S7'}
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
json.dump(reels,open('reels90.json','w'),ensure_ascii=False,indent=0)
print(len(reels)); [print(r['date'],'R%d'%r['no'],r['title'],'→',r['link_date'],'#%s'%r['link_no']) for r in reels]
