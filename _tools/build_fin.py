# 재무 체력(사용자 2026-10-29) — 미국 증권거래위원회(SEC) 공식 XBRL 재무 자료로 영업이익률·잉여현금흐름률·순부채를 계산해 d/ideas/fin.json
# 최근 회계연도(10-K) 기준 · 미국 공시(us-gaap) 회사만(대만·한국·일본 상장사, IFRS 20-F 회사는 비움) · GitHub이 분기에 한 번 돌림
# 사용: python3 -I _tools/build_fin.py <사이트 폴더>
import json, os, sys, time, urllib.request, datetime as dt
R = sys.argv[1] if len(sys.argv) > 1 else '.'
UA = {'User-Agent': 'mung-mungi research mung-mungi@users.noreply.github.com'}  # SEC 규칙: '이름 이메일' 형식
def get(u):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r: return json.load(r)
        except Exception as e:
            err = e; time.sleep(1.5 * (i + 1))
    raise err
tks = [t['ticker'] for t in json.load(open(os.path.join(R, 'd/targets/tickers.json'), encoding='utf-8')) if t.get('currency') == 'USD' and '.' not in t['ticker']]
cik = {v['ticker'].upper(): str(v['cik_str']).zfill(10) for v in get('https://www.sec.gov/files/company_tickers.json').values()}
REV = ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet', 'RevenueFromContractWithCustomerIncludingAssessedTax']
def annual(g, names):
    # 최근 회계연도 10-K 값(기간 약 1년)
    best = None
    for n in names:
        for u, rows in (g.get(n, {}).get('units') or {}).items():
            if u != 'USD': continue
            for r in rows:
                if r.get('form') not in ('10-K', '10-K/A') or not r.get('start'): continue
                d = (dt.date.fromisoformat(r['end']) - dt.date.fromisoformat(r['start'])).days
                if not 340 <= d <= 380: continue
                if not best or r['end'] > best['end'] or (r['end'] == best['end'] and r.get('filed', '') > best.get('filed', '')): best = r
        if best: break
    return best
def instant(g, names):
    best = None
    for n in names:
        for u, rows in (g.get(n, {}).get('units') or {}).items():
            if u != 'USD': continue
            for r in rows:
                if r.get('start') or r.get('form') not in ('10-K', '10-Q', '10-K/A', '10-Q/A'): continue
                if not best or r['end'] > best['end'] or (r['end'] == best['end'] and r.get('filed', '') > best.get('filed', '')): best = r
        if best: break
    return best
out, miss = {}, []
for t in tks:
    c = cik.get(t)
    if not c: miss.append(t); continue
    try: g = get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{c}.json').get('facts', {}).get('us-gaap', {})
    except Exception: miss.append(t); continue
    time.sleep(0.15)  # SEC 요청 예절(초당 10회 이하)
    rv = annual(g, REV)
    if not rv or not rv['val']: miss.append(t); continue
    op = annual(g, ['OperatingIncomeLoss']); cfo = annual(g, ['NetCashProvidedByUsedInOperatingActivities'])
    cap = annual(g, ['PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets'])
    cash = instant(g, ['CashAndCashEquivalentsAtCarryingValue', 'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents'])
    sti = instant(g, ['ShortTermInvestments', 'MarketableSecuritiesCurrent', 'AvailableForSaleSecuritiesDebtSecuritiesCurrent'])
    debt = instant(g, ['LongTermDebt', 'LongTermDebtNoncurrent', 'DebtInstrumentCarryingAmount'])
    dcur = instant(g, ['LongTermDebtCurrent', 'DebtCurrent'])
    R_ = rv['val']; o = {'fy_end': rv['end'], 'rev_bn': round(R_ / 1e9, 2)}
    if op: o['opm'] = round(op['val'] / R_ * 100, 1)
    if cfo and cap: o['fcfm'] = round((cfo['val'] - cap['val']) / R_ * 100, 1)
    if cash:
        d_ = (debt['val'] if debt else 0) + (dcur['val'] if dcur and (not debt or dcur['end'] == debt['end']) else 0)
        o['nd_rev'] = round((d_ - cash['val'] - (sti['val'] if sti else 0)) / R_, 2); o['bs_end'] = cash['end']
    out[t] = o
json.dump({'asof': dt.date.today().isoformat(), 'basis': '최근 회계연도 10-K · 순부채는 최근 분기말', 'items': out, 'missing': miss},
          open(os.path.join(R, 'd/ideas/fin.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('fin', len(out), '/', len(tks), '| 빈 곳', miss)
