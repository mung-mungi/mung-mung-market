import json,urllib.request,urllib.parse
B='https://api.elections.kalshi.com/trade-api/v2'
def get(p,**q):
    u=B+p+('?'+urllib.parse.urlencode(q) if q else '')
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'mung'}),timeout=30) as r: return json.load(r)
    except Exception as e: print('ERR',u,e); return {}
for cat in ('Elections','Politics'):
    d=get('/series',category=cat); ss=d.get('series',[])
    print(cat,len(ss))
    for s in ss:
        t=s.get('ticker','')
        if any(k in t for k in ('HOUSE','SENATEOH','SENATEFL','SENATEKY','SENATELA','CONTROL')): print('S',t,'|',s.get('title'))
for t in ('HOUSETX28','HOUSEOH9','HOUSEOH09','HOUSEWI3','HOUSEWI03','CONTROLH','CONTROLS','SENATEOHS','SENATEFLS'):
    e=get('/events',series_ticker=t,limit=2); print('E',t,[x.get('event_ticker') for x in e.get('events',[])])
