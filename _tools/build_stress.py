# 공식 금융 스트레스 지수·투자 심리 묶음(사용자 2026-11-01) — 기관마다 눈금이 달라 '최근 10년 중 몇 % 자리'(백분위)로 맞춰 평균을 냄
# 출처: OFR 금융 스트레스 지수(매일), FRED: 시카고 연은 NFCI·ANFCI·하위지수(매주), 세인트루이스 연은 STLFSI4(매주), 캔자스시티 연은 KCFSI(매월)
#       CBOE VIX, 야후 ^MOVE, CNN 공포·탐욕(d/fng.json), BofA·AAII는 d/stress/manual.json(브리핑이 기사에서 기록)
# 백분위는 '스트레스 쪽'으로 통일: 높을수록 불안. 공포·탐욕은 100-점수로 뒤집음. 못 받은 값은 직전 값 유지
# 사용: python3 -I _tools/build_stress.py <사이트 폴더>
import csv, io, json, os, subprocess, sys, datetime as dt, bisect
R = sys.argv[1] if len(sys.argv) > 1 else '.'
P = lambda *a: os.path.join(R, *a)
OUT = P('d/stress/stress.json')
def get(u):
    o = subprocess.run(['curl', '-sSL', '-m', '40', '-A', 'Mozilla/5.0', u], capture_output=True, text=True)
    if o.returncode or not o.stdout: raise RuntimeError('fail ' + u[:70])
    return o.stdout
def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d
old = load(OUT, {}); oldi = {x['id']: x for x in old.get('items', [])}
TODAY = dt.date.today(); START = (TODAY - dt.timedelta(days=3653)).isoformat()
def pct(series, v):
    xs = sorted(x for _, x in series)
    return round(bisect.bisect_left(xs, v) / max(1, len(xs)) * 100) if xs else None
def pack(id_, name, org, kind, freq, ser, unit, read, invert=False, nd=2):
    ser = [(d, v) for d, v in ser if d >= START and v is not None]
    if not ser: raise RuntimeError('empty ' + id_)
    d, v = ser[-1]; pv = ser[-2][1] if len(ser) > 1 else None
    p = pct(ser, v); p = 100 - p if invert else p
    hist = ser[-260:] if freq == '매일' else ser[-104:] if freq == '매주' else ser[-36:]
    return {'id': id_, 'name': name, 'org': org, 'kind': kind, 'freq': freq, 'date': d, 'value': round(v, nd), 'prev': None if pv is None else round(pv, nd),
            'pct': p, 'unit': unit, 'read': read(v), 'hist': [[a, round(b, nd)] for a, b in hist]}
items = []; errs = []
def tryit(fn, id_):
    try: items.append(fn())
    except Exception as e:
        errs.append(id_ + ': ' + str(e)[:80])
        if id_ in oldi: items.append(oldi[id_])
# FRED 묶음
def equi(i):
    # FRED 거울 사이트(equibles) — GitHub에서 FRED가 막힐 때 예비. 최신이 맨 위
    t = get('https://equibles.com/economicdata/%s.csv' % i.lower()); out = []
    for r in csv.DictReader(io.StringIO(t)):
        try: out.append((r['Date'][:10], float(r['Value'])))
        except Exception: pass
    if not out: raise RuntimeError('equibles %s 빈 자료' % i)
    return sorted(out)
def fred1(i):
    last = None
    try: return equi(i)
    except Exception as e: last = e
    for u in ('https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s' % i, 'https://fred.stlouisfed.org/data/%s.txt' % i, 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=%s' % (i, START)):
        for _ in range(2):
            try:
                t = get(u); out = []
                if u.endswith('.txt'):
                    for ln in t.splitlines():
                        a = ln.split()
                        if len(a) == 2 and a[0][:2] in ('19', '20') and a[1] not in ('.',):
                            try: out.append((a[0], float(a[1])))
                            except Exception: pass
                else:
                    for r in csv.DictReader(io.StringIO(t)):
                        d = r.get('observation_date') or r.get('DATE'); v = r.get(i)
                        if d and v not in (None, '', '.'): out.append((d, float(v)))
                if out: return out
            except Exception as e: last = e
            subprocess.run(['sleep', '3'])
    raise RuntimeError('FRED %s 실패 %s' % (i, str(last)[:40]))
def chifed():
    t = get('https://www.chicagofed.org/-/media/publications/nfci/nfci-data-series-csv.csv'); rows = list(csv.DictReader(io.StringIO(t))); out = {}
    for r in rows:
        ks = {k.strip().upper(): v for k, v in r.items() if k}
        d = ks.get('FRIDAY_OF_WEEK') or ks.get('DATE') or ''
        try: m, dd, y = d.split('/'); d = '%s-%s-%s' % (y, m.zfill(2), dd.zfill(2))
        except Exception: pass
        for k in ('NFCI', 'ANFCI', 'RISK', 'CREDIT', 'LEVERAGE'):
            v = ks.get(k)
            if v not in (None, ''):
                try: out.setdefault({'RISK': 'NFCIRISK', 'CREDIT': 'NFCICREDIT', 'LEVERAGE': 'NFCILEVERAGE'}.get(k, k), []).append((d, float(v)))
                except Exception: pass
    return out
F = {}
for _i in ['NFCI', 'ANFCI', 'NFCIRISK', 'NFCICREDIT', 'NFCILEVERAGE', 'STLFSI4', 'KCFSI']:
    try: F[_i] = fred1(_i)
    except Exception as e: errs.append(str(e)[:90])
if any(k not in F for k in ('NFCI', 'ANFCI', 'NFCIRISK', 'NFCICREDIT', 'NFCILEVERAGE')):
    try:
        for k, v in chifed().items(): F.setdefault(k, sorted(v))
    except Exception as e: errs.append('시카고 연은 직접: ' + str(e)[:60])
z = lambda v: '평균보다 긴장' if v > 0.5 else '평균보다 약간 긴장' if v > 0 else '평균보다 느슨' if v > -0.5 else '평균보다 많이 느슨'
tryit(lambda: pack('nfci', '금융여건지수(NFCI)', '시카고 연은', 'official', '매주', F['NFCI'], '', z), 'nfci')
tryit(lambda: pack('anfci', '조정 금융여건지수(ANFCI)', '시카고 연은', 'official', '매주', F['ANFCI'], '', z), 'anfci')
for k, nm in (('NFCIRISK', '위험'), ('NFCICREDIT', '신용'), ('NFCILEVERAGE', '레버리지')):
    tryit(lambda k=k, nm=nm: dict(pack('nfci_' + k[4:].lower(), 'NFCI ' + nm + ' 하위지수', '시카고 연은', 'sub', '매주', F[k], '', z)), 'nfci_' + k[4:].lower())
tryit(lambda: pack('stlfsi', '금융 스트레스 지수(STLFSI4)', '세인트루이스 연은', 'official', '매주', F['STLFSI4'], '', lambda v: '평균보다 스트레스 높음' if v > 0 else '평균보다 낮음'), 'stlfsi')
tryit(lambda: pack('kcfsi', '금융 스트레스 지수(KCFSI)', '캔자스시티 연은', 'official', '매월', F['KCFSI'], '', lambda v: '평균보다 스트레스 높음' if v > 0 else '평균보다 낮음'), 'kcfsi')
# OFR(매일, 하위 5개 영역 기여도 포함)
def ofr():
    t = get('https://www.financialresearch.gov/financial-stress-index/data/fsi.csv')
    rows = list(csv.DictReader(io.StringIO(t))); ser = []; last = rows[-1]
    for r in rows:
        try: ser.append((r['Date'][:10], float(r['OFR FSI'])))
        except Exception: pass
    it = pack('ofr', '금융 스트레스 지수(OFR FSI)', 'OFR(미 재무부 금융연구소)', 'official', '매일', ser, '', lambda v: '평균보다 스트레스 높음' if v > 0 else '평균보다 낮음')
    sub = {}
    for k, nm in (('Credit', '신용'), ('Equity valuation', '주식 밸류에이션'), ('Funding', '자금조달'), ('Safe assets', '안전자산'), ('Volatility', '변동성')):
        try: sub[nm] = round(float(last[k]), 2)
        except Exception: pass
    it['parts'] = sub; return it
tryit(ofr, 'ofr')
# 심리·변동성
def vix():
    t = get('https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv'); ser = []
    for r in csv.DictReader(io.StringIO(t)):
        m, d, y = r['DATE'].split('/'); ser.append(('%s-%s-%s' % (y, m.zfill(2), d.zfill(2)), float(r['CLOSE'])))
    return pack('vix', 'VIX(주식 변동성)', 'CBOE', 'sentiment', '매일', ser, '', lambda v: '불안 큼' if v >= 25 else '불안 커짐' if v >= 20 else '보통' if v >= 15 else '차분')
tryit(vix, 'vix')
def move():
    j = None
    for rg in ('10y', '5y', '2y'):
        for host in ('query1', 'query2'):
            try: j = json.loads(get('https://%s.finance.yahoo.com/v8/finance/chart/%%5EMOVE?range=%s&interval=1d' % (host, rg)))['chart']['result'][0]; break
            except Exception: subprocess.run(['sleep', '2'])
        if j: break
    if not j: raise RuntimeError('MOVE 실패')
    ser = [(dt.datetime.fromtimestamp(a, dt.timezone.utc).date().isoformat(), c) for a, c in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if c]
    return pack('move', 'MOVE(채권 변동성)', 'ICE BofA', 'sentiment', '매일', ser, '', lambda v: '불안 큼' if v >= 120 else '불안 커짐' if v >= 100 else '보통' if v >= 80 else '차분', nd=1)
tryit(move, 'move')
def cnn():
    f = load(P('d/fng.json'), {}).get('fng')
    if not f: raise RuntimeError('no fng')
    ser = [(h['date'], h['score']) for h in f.get('hist', [])]
    it = pack('cnn', '공포·탐욕 지수', 'CNN', 'sentiment', '매일', ser or [(f['date'], f['score'])], '점', lambda v: '극단적 공포' if v < 25 else '공포' if v < 45 else '중립' if v < 55 else '탐욕' if v < 75 else '극단적 탐욕', invert=True, nd=0)
    it['pct'] = round(100 - f['score']); it['note'] = '점수 자체가 0~100 눈금이라 100−점수를 불안 온도로 씀'; return it
tryit(cnn, 'cnn')
# 수기 기록(BofA·AAII) — d/stress/manual.json: [{id,name,org,kind,date,value,unit,read,pct,src}]
for m in load(P('d/stress/manual.json'), []): items.append(dict(m, kind=m.get('kind', 'sentiment'), freq=m.get('freq', '기사'), manual=True))
# ── 업종 회전 지도·관련 기업(사용자 2026-11-01) — 야후 spark 묶음 받기(20개씩)
SECT = [('SOXX', '반도체', 'atk'), ('XLK', '기술', 'atk'), ('XLC', '통신', 'atk'), ('XLY', '경기소비재', 'atk'), ('XLI', '산업재', 'cyc'), ('XLF', '금융', 'cyc'),
        ('XLE', '에너지', 'cyc'), ('XLV', '헬스케어', 'def'), ('XLP', '필수소비재', 'def'), ('XLU', '유틸리티', 'def')]
COMP = {
 'SOXX': [('NVDA', '엔비디아', 'GPU'), ('AVGO', '브로드컴', '맞춤칩·네트워크'), ('AMD', 'AMD', 'GPU·CPU'), ('TSM', 'TSMC', '파운드리'), ('MU', '마이크론', '메모리'), ('INTC', '인텔', 'CPU'), ('MRVL', '마벨', '광·맞춤칩'), ('LRCX', '램리서치', '장비'), ('AMAT', '어플라이드', '장비'), ('QCOM', '퀄컴', '모바일')],
 'XLK': [('MSFT', '마이크로소프트', '빅테크·클라우드'), ('AAPL', '애플', '빅테크'), ('ORCL', '오라클', '클라우드'), ('PLTR', '팔란티어', 'AI 소프트웨어'), ('CRM', '세일즈포스', '소프트웨어'), ('NOW', '서비스나우', '소프트웨어'), ('ADBE', '어도비', '소프트웨어'), ('IBM', 'IBM', '소프트웨어')],
 'XLC': [('META', '메타', '빅테크'), ('GOOGL', '알파벳', '빅테크·클라우드'), ('NFLX', '넷플릭스', '미디어'), ('TMUS', 'T모바일', '통신'), ('DIS', '디즈니', '미디어'), ('RDDT', '레딧', '플랫폼')],
 'XLY': [('AMZN', '아마존', '빅테크·클라우드'), ('TSLA', '테슬라', '전기차·로봇'), ('HD', '홈디포', '소매'), ('MCD', '맥도날드', '외식'), ('BKNG', '부킹', '여행'), ('NKE', '나이키', '의류')],
 'XLI': [('GEV', 'GE버노바', '전력 장비'), ('ETN', '이튼', '전력 장비'), ('VRT', '버티브', '냉각·전력'), ('PWR', '콴타', '전력망 공사'), ('CAT', '캐터필러', '발전기·건설'), ('GE', 'GE에어로', '항공'), ('BA', '보잉', '항공')],
 'XLF': [('JPM', 'JP모건', '은행'), ('BRK-B', '버크셔', '지주'), ('V', '비자', '결제'), ('GS', '골드만삭스', '투자은행'), ('BX', '블랙스톤', '사모·데이터센터 투자'), ('APO', '아폴로', '사모신용')],
 'XLE': [('XOM', '엑손모빌', '석유'), ('CVX', '셰브론', '석유'), ('COP', '코노코필립스', '석유'), ('SLB', 'SLB', '유전 서비스'), ('EQT', 'EQT', '천연가스')],
 'XLV': [('LLY', '일라이릴리', '제약'), ('UNH', '유나이티드헬스', '보험'), ('JNJ', '존슨앤존슨', '제약'), ('ABBV', '애브비', '제약'), ('ISRG', '인튜이티브', '의료기기')],
 'XLP': [('COST', '코스트코', '유통'), ('WMT', '월마트', '유통'), ('PG', 'P&G', '생활용품'), ('KO', '코카콜라', '음료'), ('PM', '필립모리스', '담배')],
 'XLU': [('CEG', '컨스텔레이션', '원전 전력'), ('VST', '비스트라', '전력'), ('TLN', '탈렌', '원전 전력'), ('NEE', '넥스트에라', '재생에너지'), ('SO', '서던', '전력')]}
def spark(syms):
    out = {}
    for i in range(0, len(syms), 20):
        part = syms[i:i + 20]
        for host in ('query1', 'query2', 'query1'):
            try:
                j = json.loads(get('https://%s.finance.yahoo.com/v7/finance/spark?symbols=%s&range=1y&interval=1d' % (host, ','.join(part))))
                for r in j['spark']['result']:
                    q = r['response'][0]; out[r['symbol']] = [c for c in q['indicators']['quote'][0]['close'] if c]
                break
            except Exception: subprocess.run(['sleep', '3'])
    return out
sectors = []; comps = {}; atkdef = {}
try:
    syms = ['SPY'] + [t for t, _, _ in SECT] + [c for v in COMP.values() for c, _, _ in v]
    PX = spark(syms); spy = PX['SPY']
    for t, n, g in SECT:
        c = PX.get(t)
        if not c or len(c) < 90: continue
        L = min(len(c), len(spy)); c2, s2 = c[-L:], spy[-L:]; trail = []
        for back in (20, 15, 10, 5, 0):
            e = L - 1 - back
            trail.append([round((c2[e] / c2[e - 63] - 1 - (s2[e] / s2[e - 63] - 1)) * 100, 1), round((c2[e] / c2[e - 21] - 1 - (s2[e] / s2[e - 21] - 1)) * 100, 1)])
        m1 = round((c[-1] / c[-22] - 1) * 100, 1)
        sectors.append({'t': t, 'n': n, 'g': g, 'm1': m1, 'd1': round((c[-1] / c[-2] - 1) * 100, 1), 'dd': round((c[-1] / max(c) - 1) * 100, 1), 'trail': trail})
        atkdef.setdefault(g, []).append(m1)
        cl = []
        for ct, cn, cr in COMP.get(t, []):
            p = PX.get(ct)
            if not p or len(p) < 23: continue
            cl.append({'t': ct, 'n': cn, 'r': cr, 'm1': round((p[-1] / p[-22] - 1) * 100, 1), 'd1': round((p[-1] / p[-2] - 1) * 100, 1), 'dd': round((p[-1] / max(p) - 1) * 100, 1)})
        comps[t] = sorted(cl, key=lambda x: x['m1'])
    spy_m1 = round((spy[-1] / spy[-22] - 1) * 100, 1); spy_d1 = round((spy[-1] / spy[-2] - 1) * 100, 2)
except Exception as e:
    errs.append('업종: ' + str(e)[:80]); spy_m1 = None; spy_d1 = None
    sectors = old.get('sectors', []); comps = old.get('comps', {})
    for x in sectors: atkdef.setdefault(x['g'], []).append(x['m1'])
mean = lambda xs: round(sum(xs) / len(xs), 1) if xs else None
def avg(kind):
    xs = [x['pct'] for x in items if x.get('kind') == kind and x.get('pct') is not None]
    return round(sum(xs) / len(xs)) if xs else None
# 층위 점수 — 위험 쪽(0 평온~100 불안)과 심리 쪽(0 공포~100 환희)을 따로
it = {x['id']: x for x in items}
def emo(x):
    i = x['id']; v = x['value']
    if i == 'cnn': return v
    if i == 'aaii': return max(0, min(100, 50 + (x.get('bull', 50 - v) - v) * 1.25))
    if i == 'bofa_bb': return v * 10
    if i == 'bofa_fms': return max(0, min(100, 50 + (4.5 - v) * 40))
    return None
for x in items:
    e = emo(x)
    if e is not None: x['emo'] = round(e)
ret = [it[k]['emo'] for k in ('cnn', 'aaii') if k in it and 'emo' in it[k]]
ins = [it[k]['emo'] for k in ('bofa_bb', 'bofa_fms') if k in it and 'emo' in it[k]]
prc = [it[k]['pct'] for k in ('vix', 'move') if k in it and it[k].get('pct') is not None]
scores = {'system': avg('official'), 'price': round(sum(prc) / len(prc)) if prc else None,
          'retail': round(sum(ret) / len(ret)) if ret else None, 'inst': round(sum(ins) / len(ins)) if ins else None,
          'atk': mean(atkdef.get('atk', [])), 'def': mean(atkdef.get('def', [])), 'cyc': mean(atkdef.get('cyc', [])), 'spy_m1': spy_m1, 'spy_d1': spy_d1, 'y10': (load(P('d/bond/yields_daily.json'), [{}]) or [{}])[-1].get('us10y')}
out = {'updated': dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M KST'), 'window': '최근 10년',
       'avg_official': avg('official'), 'avg_sentiment': avg('sentiment'), 'scores': scores, 'sectors': sectors, 'comps': comps, 'items': items, 'errors': errs}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('점수', scores, '| 업종', len(sectors), '| 실패', errs)
for x in items: print(x['id'], x['date'], x['value'], 'pct', x['pct'], x.get('read'))
