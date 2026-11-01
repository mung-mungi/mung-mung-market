# 시장 경고등 자동 갱신(사용자 2026-10-29) — 6시간마다 GitHub이 공식 출처에서 마감 숫자를 받아 불 10개를 다시 켜고 끔. 크레딧 없음
# 출처: 미 재무부(2·10·30년물·3개월), CBOE(VIX·VIX3M·풋콜), FRED(하이일드 스프레드), 야후(WTI·QQQ 종가)
# 받지 못한 숫자는 직전 값을 그대로 이어 씀(빈칸으로 불이 꺼지지 않게). 국채 입찰(auc)은 허브 동기화 값을 이어 씀
# 사용: python3 -I _tools/build_lights.py <사이트 폴더>
import csv, io, json, os, sys, subprocess, datetime as dt
R = sys.argv[1] if len(sys.argv) > 1 else '.'
P = lambda *a: os.path.join(R, *a)
def get(u):
    o = subprocess.run(['curl', '-sSL', '-m', '25', '-A', 'Mozilla/5.0', u], capture_output=True, text=True)
    if o.returncode or not o.stdout: raise RuntimeError('fail ' + u[:60])
    return o.stdout
def load(p, d):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return d
def iso(md): m, d, y = md.split('/'); return '%s-%s-%s' % (y, m.zfill(2), d.zfill(2))
log = load(P('d/lights/lights_log.json'), []); TH = {t['id']: t for t in load(P('d/lights/thresholds.json'), [])}
# 반도체·AI 영역(사용자 2026-11-01) — 시장 전체는 버텨도 반도체에 공포가 몰리는 날을 잡음. 허브 동기화로 기준표가 덮여도 다시 넣음
SOX_TH = [
    {'id': 'soxdd', 'board': '반도체·AI', 'name': '반도체 고점 대비 낙폭', 'rule': '필라델피아 반도체 지수가 최근 1년 고점보다 15% 이상 낮음', 'op': '>=', 'value': 15, 'unit': '%',
     'why': '반도체가 고점에서 15% 넘게 빠지면 조정을 넘어 AI 투자 기대 자체를 다시 따지는 구간입니다.', 'since': '2026-11-01', 'history': [], 'weight': 0.5},
    {'id': 'soxday', 'board': '반도체·AI', 'name': '반도체 하루 급락(최근 5일)', 'rule': '최근 5거래일 중 반도체 지수가 하루 5% 이상 빠진 날이 있음', 'op': '>=', 'value': 5, 'unit': '%',
     'why': '하루 -5%는 흔치 않은 투매입니다. 레버리지 청산이 몰리면 나타나고, 며칠 동안 여진이 이어지기 쉽습니다.', 'since': '2026-11-01', 'history': [], 'weight': 0.5,
     'weight_why': '반도체·AI 영역은 둘이 함께 켜져도 1개 몫(각 0.5)으로 셉니다 — 반도체 쏠림은 업종 신호가 따로 잡고, 기본 경고등은 시장 전체 온도를 차분하게 유지(사용자 2026-11-01).'}]
_tl = load(P('d/lights/thresholds.json'), [])
_tl = SOX_TH + [t for t in _tl if t.get('id') not in ('soxdd', 'soxday')]
json.dump(_tl, open(P('d/lights/thresholds.json'), 'w', encoding='utf-8'), ensure_ascii=False)
TH = {t['id']: t for t in _tl}
yd = load(P('d/bond/yields_daily.json'), []); hy = load(P('d/bond/hy_spread.json'), [])
oil = load(P('d/lights/oil.json'), []); qqq = load(P('d/lights/qqq_px.json'), [])
got = []
# ① 재무부 금리(올해 전체 CSV)
try:
    Y = {r['date']: r for r in yd}
    for yr in sorted({dt.date.today().year - 1, dt.date.today().year}):
        t = get('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/%d/all?type=daily_treasury_yield_curve&field_tdr_date_value=%d&page&_format=csv' % (yr, yr))
        for r in csv.DictReader(io.StringIO(t)):
            try: Y[iso(r['Date'])] = {'date': iso(r['Date']), 'us3m': float(r['3 Mo']), 'us2y': float(r['2 Yr']), 'us10y': float(r['10 Yr']), 'us30y': float(r['30 Yr'])}
            except Exception: pass
    yd = [Y[k] for k in sorted(Y)]; got.append('금리')
except Exception as e: print('금리 실패', e)
# ② CBOE VIX·VIX3M
def cboe(sym):
    t = get('https://cdn.cboe.com/api/global/us_indices/daily_prices/%s_History.csv' % sym)
    return {iso(r['DATE']): float(r['CLOSE']) for r in csv.DictReader(io.StringIO(t)) if r.get('CLOSE')}
try: VIX = cboe('VIX'); V3 = cboe('VIX3M'); got.append('VIX')
except Exception as e: VIX, V3 = {}, {}; print('VIX 실패', e)
# ③ 하이일드 스프레드(FRED, 하루 늦게 나옴)
try:
    H = {r['date']: r for r in hy}
    # 한 번 더 시도(사용자 2026-10-31 — 하이일드가 10/28 값에 사흘 멈춘 일이 있었음)
    try: _t = get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2&cosd=' + (dt.date.today() - dt.timedelta(days=60)).isoformat())
    except Exception: _t = get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2')
    for r in csv.DictReader(io.StringIO(_t)):
        k = r.get('observation_date') or r.get('DATE'); v = r.get('BAMLH0A0HYM2')
        if k and v not in (None, '', '.'): H[k] = {'date': k, 'hy': float(v)}
    hy = [H[k] for k in sorted(H)]; got.append('하이일드')
except Exception as e: print('하이일드 실패', e)
# ④ 야후 일봉(WTI·QQQ) — 마감된 날만(오늘 장중 값은 빼기)
def yh(sym):
    j = json.loads(get('https://query1.finance.yahoo.com/v8/finance/chart/%s?range=3mo&interval=1d' % sym))['chart']['result'][0]
    tz = j['meta'].get('exchangeTimezoneName', 'America/New_York'); import zoneinfo
    z = zoneinfo.ZoneInfo(tz); now = dt.datetime.now(z); out = {}
    for ts, c in zip(j['timestamp'], j['indicators']['quote'][0]['close']):
        if c is None: continue
        d = dt.datetime.fromtimestamp(ts, z).date()
        if d == now.date() and now.hour < 17: continue
        out[d.isoformat()] = round(c, 2)
    return out
try:
    O = {r['date']: r for r in oil}
    for d, c in yh('CL%3DF').items():
        if d > (oil[-1]['date'] if oil else ''): O[d] = {'date': d, 'wti': c}
    oil = [O[k] for k in sorted(O)]; got.append('유가')
except Exception as e: print('유가 실패', e)
try:
    Q = {r['date']: r for r in qqq}
    for d, c in yh('QQQ').items(): Q[d] = {'date': d, 'close': c}
    qqq = [Q[k] for k in sorted(Q)][-260:]; got.append('QQQ')
except Exception as e: print('QQQ 실패', e)
# ④-2 필라델피아 반도체 지수(야후 1년 일봉, 마감된 날만)
SOXP = {}
try:
    _j = json.loads(get('https://query1.finance.yahoo.com/v8/finance/chart/%5ESOX?range=2y&interval=1d'))['chart']['result'][0]
    import zoneinfo; _z = zoneinfo.ZoneInfo('America/New_York'); _now = dt.datetime.now(_z)
    for ts, c in zip(_j['timestamp'], _j['indicators']['quote'][0]['close']):
        if c is None: continue
        d0 = dt.datetime.fromtimestamp(ts, _z).date()
        if d0 == _now.date() and _now.hour < 17: continue
        SOXP[d0.isoformat()] = c
    got.append('반도체')
except Exception as e: print('반도체 실패', e)
_sk = sorted(SOXP)
def soxdd(d):
    ks = [k for k in _sk if k <= d][-252:]
    if len(ks) < 20: return None
    return round((1 - SOXP[ks[-1]] / max(SOXP[k] for k in ks)) * 100, 2)
def soxday(d):
    ks = [k for k in _sk if k <= d][-6:]
    if len(ks) < 6: return None
    return round(max(0.0, max((1 - SOXP[ks[i]] / SOXP[ks[i - 1]]) * 100 for i in range(1, 6))), 2)
# ⑤ 풋콜(CBOE 일별 통계) — 로그에 없는 최근 날짜만
pcv = {r['date']: r['val'] for r in log if r['id'] == 'pc'}
days = [r['date'] for r in yd if r['date'] >= '2026-01-01']
for d in days[-8:]:
    if d in pcv and d < days[-3]: continue
    try:
        j = json.loads(get('https://cdn.cboe.com/data/us/options/market_statistics/daily/%s_daily_options' % d))
        pcv[d] = float([x for x in j['ratios'] if x['name'] == 'TOTAL PUT/CALL RATIO'][0]['value'])
    except Exception: pass
# ⑥ 불 계산 — 금리 날짜(미국 거래일)마다, 로그 마지막 날 이후(+최근 3일 다시)
ymap = {r['date']: r for r in yd}; idx = {r['date']: i for i, r in enumerate(yd)}
hmap = {r['date']: r['hy'] for r in hy}; omap = [(r['date'], r['wti']) for r in oil]
prev = {}
for r in log: prev[r['id']] = r['val']
lastlog = max([r['date'] for r in log] or ['2000-01-01'])
redo = [d for d in days if d > lastlog] + [d for d in days if d <= lastlog][-3:]
def carry(mp, d):
    ks = [k for k in mp if k <= d]; return mp[max(ks)] if ks else None
def oilchg(d):
    s = [x for x in omap if x[0] <= d]
    return round((s[-1][1] / s[-22][1] - 1) * 100, 3) if len(s) >= 22 else None
OP = {'<': lambda a, b: a < b, '>=': lambda a, b: a >= b, '>': lambda a, b: a > b, '<=': lambda a, b: a <= b}
keep = [r for r in log if r['date'] not in set(redo)]
old = {(r['date'], r['id']): r['val'] for r in log}
new = []
for d in sorted(set(redo)):
    y = ymap[d]; i = idx[d]
    vals = {'inv': round(y['us10y'] - y['us2y'], 2), 'y10': y['us10y'], 'y30': y['us30y'],
            'jump': round(y['us10y'] - yd[i - 10]['us10y'], 2) if i >= 10 else None,
            'hy': carry(hmap, d), 'vix': VIX.get(d), 'term': round(VIX[d] / V3[d], 2) if d in VIX and d in V3 else None,
            'pc': pcv.get(d), 'oil': oilchg(d), 'auc': None,
            'soxdd': soxdd(d) if SOXP else None, 'soxday': soxday(d) if SOXP else None}
    for k in TH:
        v = vals.get(k)
        if v is None: v = old.get((d, k), prev.get(k))
        if v is None: continue
        t = TH[k]; prev[k] = v
        new.append({'date': d, 'board': t['board'], 'id': k, 'val': v, 'on': int(OP[t['op']](v, t['value'])), 'w': t.get('weight', 1)})
# 반도체 불이 없던 지난 날짜도 채움(1년 기록 그래프가 끊기지 않게)
if SOXP:
    _have = {(r['date'], r['id']) for r in keep + new}
    for d in sorted({r['date'] for r in keep}):
        for k, fn in (('soxdd', soxdd), ('soxday', soxday)):
            if (d, k) in _have or k not in TH: continue
            v = fn(d)
            if v is None: continue
            t = TH[k]; keep.append({'date': d, 'board': t['board'], 'id': k, 'val': v, 'on': int(OP[t['op']](v, t['value'])), 'w': t.get('weight', 1)})
for r in keep:
    if r['id'] in ('soxdd', 'soxday'): r['w'] = TH[r['id']].get('weight', 1)
log = sorted(keep + new, key=lambda r: (r['date'], list(TH).index(r['id']) if r['id'] in TH else 99))
def dump(p, o): json.dump(o, open(P(p), 'w', encoding='utf-8'), ensure_ascii=False)
dump('d/lights/lights_log.json', log); dump('d/bond/yields_daily.json', yd); dump('d/bond/hy_spread.json', hy)
dump('d/lights/oil.json', oil); dump('d/lights/qqq_px.json', qqq)
L = log[-len(TH):]
print('경고등', L[-1]['date'], '| 받은 것', got, '| 켜진 불', [r['id'] for r in L if r['on']])
# 멈춘 값 표시·자동 한 줄(사용자 2026-10-31) — 실패해도 경고등 계산에는 영향 없음
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lights_fresh
    _D = L[-1]['date']; _ld = lambda m: max([k for k in m if k <= _D] or [None], key=lambda x: x or '')
    lights_fresh.run(R, {'vix': _ld(VIX), 'term': _ld(VIX), 'pc': _ld(pcv)})
except Exception as e: print('fresh 실패', e)
