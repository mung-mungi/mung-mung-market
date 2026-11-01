# 옵션 온도계 자료 자동 갱신(사용자 2026-11-02 '오래된 자료 칩이 뜨면 자체적으로 최신화') — Claude 크레딧 없음
# 10.23에서 멈춘 원인: VIX 종가·VIX9D·VIX3M·VVIX·풋콜을 사람이(Claude 대화) 손으로 넣어 왔고, 그 갱신이 끊김.
# 이제 CBOE 공식 자료로 매일 채움: VIX·VIX9D·VIX3M·VVIX 일별 종가 CSV, 일별 옵션 통계(풋콜). 이미 있는 날은 건드리지 않고 빠진 날만 붙임.
# 사용: python3 -I _tools/build_opt.py <사이트 폴더>   (lights.yml에서 경고등 다음에 실행)
import csv, io, json, os, sys, subprocess
R = sys.argv[1] if len(sys.argv) > 1 else '.'
D = os.path.join(R, 'd', 'opt')
SRC_IDX = 'https://www.cboe.com/us/indices/ (CBOE 공식 종가)'
SRC_PC = 'https://www.cboe.com/us/options/market_statistics/daily/'
def get(u):
    o = subprocess.run(['curl', '-sSL', '-m', '25', '-A', 'Mozilla/5.0', u], capture_output=True, text=True)
    if o.returncode or not o.stdout: raise RuntimeError('fail ' + u[:70])
    return o.stdout
def load(n):
    try: return json.load(open(os.path.join(D, n + '.json'), encoding='utf-8'))
    except Exception: return []
def dump(n, o):
    p = os.path.join(D, n + '.json'); s = json.dumps(o, ensure_ascii=False)
    try:
        if json.dumps(json.load(open(p, encoding='utf-8')), ensure_ascii=False) == s: return False
    except Exception: pass
    open(p, 'w', encoding='utf-8').write(s); return True
def iso(md): m, d, y = md.split('/'); return '%s-%s-%s' % (y, m.zfill(2), d.zfill(2))
def cboe(sym):
    t = get('https://cdn.cboe.com/api/global/us_indices/daily_prices/%s_History.csv' % sym)
    out = {}
    for r in csv.DictReader(io.StringIO(t)):
        k = r.get('DATE') or r.get('Date')
        v = r.get('CLOSE') or r.get(sym) or list(r.values())[-1]
        try: out[iso(k)] = round(float(v), 2)
        except Exception: pass
    return out
if not os.path.isdir(D): print('d/opt 없음'); sys.exit(0)
ch = []
try:
    VIX = cboe('VIX')
except Exception as e:
    print('VIX 실패', e); VIX = {}
days = sorted(VIX)
# ① VIX 일별 종가: 마지막 확정일 이후 빠진 날 + 장중 행은 확정 종가가 나오면 교체
vd = load('vix_daily')
if days and vd:
    fin = {r['date'] for r in vd if r.get('status') == 'final'}
    last_fin = max(fin) if fin else days[0]
    keep = [r for r in vd if not (r.get('status') != 'final' and r['date'] in VIX)]
    have = {r['date'] for r in keep}
    for d in days:
        if d > last_fin and d not in have:
            keep.append({'date': d, 'close': VIX[d], 'status': 'final', 'source': SRC_IDX})
    keep.sort(key=lambda r: r['date']); keep = keep[-130:]
    if dump('vix_daily', keep): ch.append('VIX')
# ② 기간구조: VIX9D·VIX3M·VVIX — 마지막 날 이후 + 최근 15일 빈칸 채우기
tm = load('term')
if days:
    S = {}
    for sym, key in (('VIX9D', 'vix9d'), ('VIX3M', 'vix3m'), ('VVIX', 'vvix')):
        try: S[key] = cboe(sym)
        except Exception as e: print(sym, '실패', e); S[key] = {}
    by = {r['date']: r for r in tm}
    last = max(by) if by else days[-30]
    recent = set(sorted(by)[-15:])
    for d in days:
        if d <= last and d not in recent: continue
        r = by.get(d) or {'date': d, 'vix9d': None, 'vix3m': None, 'vvix': None, 'source': SRC_IDX}
        for key in ('vix9d', 'vix3m', 'vvix'):
            if r.get(key) is None and d in S[key]: r[key] = S[key][d]
        if any(r.get(k) is not None for k in ('vix9d', 'vix3m', 'vvix')): by[d] = r
    nt = [by[k] for k in sorted(by)][-130:]
    if dump('term', nt): ch.append('기간구조')
    # ③ VIX ÷ VIX3M
    vr = load('vix_ratio'); vb = {r['date']: r for r in vr}
    for d in days[-15:]:
        if d in VIX and d in S['vix3m'] and d not in vb:
            vb[d] = {'date': d, 'vix': VIX[d], 'vix3m': S['vix3m'][d], 'ratio': round(VIX[d] / S['vix3m'][d], 3)}
    nv = [vb[k] for k in sorted(vb)][-260:]
    if vr and dump('vix_ratio', nv): ch.append('VIX÷VIX3M')
# ④ 풋콜(일별 옵션 통계) — 마지막 날 이후 빠진 날만, 9일 지수이동평균 이어 계산
pc = load('putcall')
if pc and days:
    last = pc[-1]['date']; ema = pc[-1].get('total_ema9')
    for d in [x for x in days if x > last][-10:]:
        try:
            j = json.loads(get('https://cdn.cboe.com/data/us/options/market_statistics/daily/%s_daily_options' % d))
            R_ = {x['name'].upper(): float(x['value']) for x in j.get('ratios', []) if x.get('value') not in (None, '')}
            tot = R_.get('TOTAL PUT/CALL RATIO')
            if tot is None: continue
            ema = round(tot if ema is None else ema + 0.2 * (tot - ema), 3)
            pc.append({'date': d, 'total': round(tot, 2), 'equity': R_.get('EQUITY PUT/CALL RATIO'), 'index': R_.get('INDEX PUT/CALL RATIO'),
                       'total_ema9': ema, 'note': '', 'source': SRC_PC})
        except Exception as e:
            print('풋콜', d, e)
    if dump('putcall', pc[-260:]): ch.append('풋콜')
print('옵션 온도계:', ' · '.join(ch) if ch else '변화 없음', '(마지막 VIX', days[-1] if days else '-', ')')
