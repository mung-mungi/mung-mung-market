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
    r=(m.get('rules_primary') or '').lower()
    if 'democratic party' in r or 'democrat' in r[:120]: return 'D'
    if 'republican party' in r or 'republican' in r[:120]: return 'R'
    t=' '.join(str(m.get(k) or '') for k in ('yes_sub_title','subtitle','title','ticker')).lower()
    if re.search(r'democrat|\b-d\b|dem\b',t): return 'D'
    if re.search(r'republican|\b-r\b|gop|rep\b',t): return 'R'
    return None
def price(m):
    for k in ('last_price_dollars','yes_bid_dollars','yes_ask_dollars'):
        try:
            v=float(m.get(k) or 0)
            if v>0: return round(v*100)
        except: pass
    for k in ('last_price','yes_bid'):
        v=m.get(k)
        if isinstance(v,(int,float)) and v>0: return v
    return None
out={'src':'Kalshi 예측시장(베팅 가격 = 시장이 매긴 확률, 실제 개표 결과 아님)','updated_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec='minutes'),'senate':{},'gov':{}}
for kind,pre in (('senate',['SENATE']),('gov',['GOVPARTY','GOV'])):
    for s in ST:
        for p in (pre+([p2+s+'S' for p2 in pre] if kind=='senate' else [])) if not (kind=='senate' and s in ('OH','FL')) else ['SENATE'+s+'S']:
            p,s0=(p[:-len(s)-1],None) if p.endswith(s+'S') else (p,None)
            tick=p+s+('S' if (kind=='senate' and s in ('OH','FL')) else '')
            ev=get('/events',series_ticker=tick,with_nested_markets='true',limit=5)
            evs=[e for e in ev.get('events',[]) if '26' in e.get('event_ticker','') or '2026' in (e.get('title') or '')]
            if not evs: continue
            ms=evs[0].get('markets') or []
            res={}
            for m in ms:
                pp=party(m); pr=price(m)
                if pp and pr is not None and pr>res.get(pp,-1): res[pp]=pr; res['n'+pp]=m.get('yes_sub_title') or ''
                if m.get('result') in ('yes',) and pp: res['won']=pp
            if kind=='senate' and s=='LA' and 'Barr' in str(res.get('nR','')): s2='KY'
            else: s2=s
            if res:
                out[kind][s2]=res; print(kind,s2,p,evs[0].get('event_ticker'),res)
            break
# 하원: 선거구별 시장(KXHOUSERACE) → 주별로 묶기
out['house']={};cur=None;n=0;sample=0
while True:
    q=dict(series_ticker='KXHOUSERACE',with_nested_markets='true',limit=200)
    if cur:q['cursor']=cur
    d=get('/events',**q);evs=d.get('events',[])
    for e in evs:
        t=e.get('event_ticker','');m_=re.search(r'-26([A-Z]{2})(\d+|AL)',t)
        if sample<3: print('HS',t,e.get('title'));sample+=1
        if not m_: continue
        st=m_.group(1);h=out['house'].setdefault(st,{'D':0,'R':0,'wD':0,'wR':0,'n':0});h['n']+=1;n+=1
        best=None;bp=-1;won=None
        for m in e.get('markets') or []:
            pp=party(m);pr=price(m)
            if m.get('result')=='yes' and pp: won=pp
            if pp and pr is not None and pr>bp: bp=pr;best=pp
        if won: h['w'+won]+=1
        if best: h[best]+=1
    cur=d.get('cursor')
    if not cur or not evs: break
print('house districts',n,'states',len(out['house']))
json.dump(out,open('d/election/kalshi.json','w'),ensure_ascii=False,indent=0)
print('senate',len(out['senate']),'gov',len(out['gov']))
