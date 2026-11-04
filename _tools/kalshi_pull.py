# 칼시(예측시장) 주별 상원·주지사 '당 승리 확률'을 d/election/kalshi.json으로 (선거 지도 보조 표시, 결과 아님)
import json, urllib.request, urllib.parse, re, sys, time, datetime
B='https://api.elections.kalshi.com/trade-api/v2'
def get(path, **q):
    u=B+path+('?'+urllib.parse.urlencode(q) if q else '')
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'mung-market/1.0'}),timeout=20) as r: return json.load(r)
        except Exception as e: err=e; time.sleep(1.5)
    print('fail',u,err); return {}
ST="AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
def party(m):
    t=' '.join(str(m.get(k) or '') for k in ('yes_sub_title','subtitle','title','ticker')).lower()
    if re.search(r'democrat|\b-d\b|dem\b',t): return 'D'
    if re.search(r'republican|\b-r\b|gop|rep\b',t): return 'R'
    return None
def price(m):
    for k in ('last_price','yes_bid','yes_ask'):
        v=m.get(k)
        if isinstance(v,(int,float)) and v>0: return v
    return None
out={'src':'Kalshi 예측시장(베팅 가격 = 시장이 매긴 확률, 실제 개표 결과 아님)','updated_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec='minutes'),'senate':{},'gov':{}}
for kind,pre in (('senate',['SENATE']),('gov',['GOVPARTY','GOV'])):
    for s in ST:
        for p in pre:
            ev=get('/events',series_ticker=p+s,with_nested_markets='true',limit=5)
            evs=[e for e in ev.get('events',[]) if '26' in e.get('event_ticker','') or '2026' in (e.get('title') or '')]
            if not evs: continue
            ms=evs[0].get('markets') or []
            res={}
            for m in ms:
                pp=party(m); pr=price(m)
                if pp and pr is not None: res[pp]=max(res.get(pp,0),pr)
                if m.get('result') in ('yes',) and pp: res['won']=pp
            if res:
                out[kind][s]=res; print(kind,s,p,evs[0].get('event_ticker'),res)
            break
json.dump(out,open('d/election/kalshi.json','w'),ensure_ascii=False,indent=0)
print('senate',len(out['senate']),'gov',len(out['gov']))
