# VIX 선물 정산값 매일 받기(사용자 2026-11-02) — 옵션 온도계 기간구조 오른쪽 그림(d/opt/vix_futures.json)
# 자료: CBOE 공식 계약별 기록 CSV(cdn.cboe.com/.../historical_data/VX/VX_<만기>.csv)의 Settle 열. 크레딧 없음(GitHub Actions)
# 만기 = 다음 달 셋째 금요일 30일 전(수요일). 휴일로 밀리는 달은 하루 앞(화요일)도 시도.
import csv, io, json, os, sys, datetime as dt, urllib.request
R = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = os.path.join(R, 'd/opt/vix_futures.json')
MC = 'FGHJKMNQUVXZ'
def third_fri(y, m):
    d = dt.date(y, m, 15)
    return d + dt.timedelta(days=(4 - d.weekday()) % 7)
def expiry(y, m):
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    return third_fri(ny, nm) - dt.timedelta(days=30)
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (mung-mung-market vix futures)'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode('utf-8', 'replace')
def rows_for(e):
    for d in (e, e - dt.timedelta(days=1)):
        u = f'https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/VX_{d.isoformat()}.csv'
        try:
            t = get(u)
        except Exception as ex:
            print('miss', u, ex); continue
        rd = [r for r in csv.DictReader(io.StringIO(t)) if r.get('Trade Date')]
        out = []
        for r in rd:
            try:
                s = float(r.get('Settle') or 0)
            except ValueError:
                continue
            if s > 0:
                out.append((r['Trade Date'][:10], s))
        if out:
            return d, sorted(out), u
    return None, [], None
today = dt.date.today()
y, m = today.year, today.month
res = []
for k in range(10):
    yy, mm = y + (m - 1 + k) // 12, (m - 1 + k) % 12 + 1
    e = expiry(yy, mm)
    if e < today:
        continue
    d, rs, u = rows_for(e)
    if rs:
        res.append({'contract': f'VX/{MC[mm-1]}{yy % 10}', 'month': f'{yy}-{mm:02d}', 'expiry': d.isoformat(), 'rows': rs, 'u': u})
    if len(res) >= 8:
        break
if len(res) < 4:
    print('too few contracts', len(res)); sys.exit(0)  # 자료를 못 받으면 기존 파일 그대로
dates = sorted(set(res[0]['rows'][i][0] for i in range(len(res[0]['rows']))))
last2 = dates[-2:]
F = []
for c in res:
    m_ = dict(c['rows'])
    row = {'contract': c['contract'], 'month': c['month'], 'expiry': c['expiry']}
    for d in reversed(last2):
        if d in m_:
            row['settle_' + d] = round(m_[d], 4)
    if 'settle_' + last2[-1] not in row:
        continue
    row['source'] = 'CBOE 공식 정산(cdn.cboe.com VX 계약별 기록)'
    F.append(row)
old = None
try:
    old = json.load(open(OUT, encoding='utf-8'))
except Exception:
    pass
if old == F:
    print('no change'); sys.exit(0)
json.dump(F, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', len(F), 'contracts, last', last2)
