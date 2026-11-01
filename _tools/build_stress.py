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
    o = subprocess.run(['curl', '-sSL', '-m', '40', '-A', 'Mozilla/5.0 (Macintosh) Chrome/124', u], capture_output=True, text=True)
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
def fred(ids):
    t = get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + ','.join(ids) + '&cosd=' + START)
    rows = list(csv.DictReader(io.StringIO(t))); out = {i: [] for i in ids}
    for r in rows:
        d = r.get('observation_date') or r.get('DATE')
        for i in ids:
            v = r.get(i)
            if v not in (None, '', '.'): out[i].append((d, float(v)))
    return out
F = {}
try: F = fred(['NFCI', 'ANFCI', 'NFCIRISK', 'NFCICREDIT', 'NFCILEVERAGE', 'STLFSI4', 'KCFSI'])
except Exception as e: errs.append('FRED: ' + str(e)[:80])
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
    j = json.loads(get('https://query1.finance.yahoo.com/v8/finance/chart/%5EMOVE?range=10y&interval=1d'))['chart']['result'][0]
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
def avg(kind):
    xs = [x['pct'] for x in items if x.get('kind') == kind and x.get('pct') is not None]
    return round(sum(xs) / len(xs)) if xs else None
out = {'updated': dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M KST'), 'window': '최근 10년',
       'avg_official': avg('official'), 'avg_sentiment': avg('sentiment'), 'items': items, 'errors': errs}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('공식 평균', out['avg_official'], '심리 평균', out['avg_sentiment'], '| 실패', errs)
for x in items: print(x['id'], x['date'], x['value'], 'pct', x['pct'], x.get('read'))
