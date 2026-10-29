# 아이디어 페이지 2종 자료 만들기(사용자 2026-10-29) — 새 수집 없이 사이트에 이미 있는 자료만으로 계산
#  ① d/ideas/value.json : 저평가 서치(불 7개 점수)
#  ② d/ideas/pros.json  : 증권사 적중률 성적표 + 잘 맞히는 곳의 최근 상향 + 큰손 포트폴리오
# 사용: python3 -I _tools/build_ideas.py <사이트 폴더>
import json, os, sys, bisect, statistics as st, datetime as dt
R = sys.argv[1] if len(sys.argv) > 1 else '.'
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
ev = J('d/targets/events.json'); tks = J('d/targets/tickers.json'); px = J('d/prices/prices.json')
hist = J('d/prices/history.json'); q = J('d/qtr/earnings.json'); si = J('d/short/si.json')
ins = J('d/insider/insider_tx.json'); f13 = J('d/insider/inst_13f.json'); leo = J('d/short/leopold.json')

# 일별 종가
S = {}
for r in hist:
    if r['kind'] == 'd': S.setdefault(r['ticker'], []).append((r['date'], r['close']))
for k in S: S[k].sort()
LAST = max(d for v in S.values() for d, _ in v)
def at(t, d, off=0):
    s = S.get(t)
    if not s: return None
    i = bisect.bisect_left(s, (d, -1))
    j = i + off
    return s[j] if 0 <= j < len(s) and i < len(s) else None

TK = {t['ticker']: t for t in tks}
PX = {p['ticker']: p for p in px}
BULL_T, BEAR_T = {'상향', '의견상향'}, {'하향', '의견하향'}
def direc(e):
    if e['type'] in BULL_T: return 1
    if e['type'] in BEAR_T: return -1
    if e['type'] == '신규':
        if e['rating_to'] in ('매수', '비중확대'): return 1
        if e['rating_to'] in ('비중축소', '매도'): return -1
    return 0

# ── ② 증권사 성적표: 의견 낸 날 종가 → 63거래일(약 3개월) 뒤, 나스닥100(QQQ) 대비 초과수익이 의견 방향과 맞았나
H = 63; H1 = 21
firms = {}
scored = 0
for e in ev:
    d = direc(e)
    if not d or TK.get(e['ticker'], {}).get('currency') != 'USD': continue
    a, b = at(e['ticker'], e['date']), at(e['ticker'], e['date'], H)
    qa, qb = at('QQQ', e['date']), at('QQQ', e['date'], H)
    f = firms.setdefault(e['firm'], {'firm': e['firm'], 'firm_en': e['firm_en'], 'calls': 0, 'n': 0, 'hit': 0, 'ex': [], 'n1': 0, 'hit1': 0, 'best': None, 'tickers': set()})
    f['calls'] += 1; f['tickers'].add(e['ticker'])
    a1, b1, qa1, qb1 = a, at(e['ticker'], e['date'], H1), qa, at('QQQ', e['date'], H1)
    if a and b1 and qa1 and qb1 and b1[0] > a[0]:
        x1 = (b1[1] / a[1] - qb1[1] / qa1[1]) * 100 * d
        f['n1'] += 1; f['hit1'] += x1 > 0
    if not (a and b and qa and qb) or b[0] <= a[0]: continue
    x = (b[1] / a[1] - qb[1] / qa[1]) * 100 * d   # 의견 방향으로 본 초과수익(%p)
    f['n'] += 1; f['hit'] += x > 0; f['ex'].append(x); scored += 1
    if not f['best'] or x > f['best']['x']:
        f['best'] = {'ticker': e['ticker'], 'name': TK[e['ticker']]['name'], 'date': e['date'], 'type': e['type'], 'x': round(x, 1)}
MINN = 8
rows = []
for f in firms.values():
    if f['n'] < MINN: continue
    sr = f['hit'] / f['n']; avg = st.mean(f['ex'])
    shr = (f['hit'] + 5) / (f['n'] + 10)          # 건수 적은 곳 운빨 보정(가운데로 당김)
    rows.append({'firm': f['firm'], 'firm_en': f['firm_en'], 'n': f['n'], 'calls': f['calls'], 'hit': round(sr * 100), 'avg': round(avg, 1),
                 'med': round(st.median(f['ex']), 1), 'hit1': round(f['hit1'] / f['n1'] * 100) if f['n1'] else None, 'n1': f['n1'],
                 'score': shr * 100 + max(min(avg, 20), -20) * 0.8, 'cover': len(f['tickers']), 'best': f['best']})
rows.sort(key=lambda r: -r['score'])
for i, r in enumerate(rows):
    p = 1 - i / max(len(rows) - 1, 1)
    r['rank'] = i + 1; r['stars'] = 5 if p >= .8 else 4 if p >= .6 else 3 if p >= .4 else 2 if p >= .2 else 1; r['score'] = round(r['score'], 1)
TOP = [r['firm'] for r in rows[:10]]
d45 = (dt.date.fromisoformat(LAST) - dt.timedelta(days=45)).isoformat()
recent = []
for e in sorted(ev, key=lambda e: e['date'], reverse=True):
    if e['date'] < d45 or e['firm'] not in TOP or direc(e) != 1: continue
    t = TK.get(e['ticker']); p = PX.get(e['ticker'])
    since = None
    if p and at(e['ticker'], e['date']): since = round((p['price'] / at(e['ticker'], e['date'])[1] - 1) * 100, 1)
    recent.append({'date': e['date'], 'firm': e['firm'], 'rank': TOP.index(e['firm']) + 1, 'ticker': e['ticker'], 'name': t['name'] if t else e['ticker'],
                   'type': e['type'], 'rating': e['rating_to'], 'pt_from': e['pt_from'], 'pt_to': e['pt_to'], 'since': since})
# 큰손: 상황인식(레오폴드) 2분기말 보유 + 13F 기관 보유 변화 + 내부자 순매수
leo_rows = sorted([l for l in leo if l.get('type') == '주식'], key=lambda l: -(l.get('pct_portfolio') or 0))[:12]
inst = sorted([{'ticker': x['ticker'], 'name': x['company'], 'cat': x['category'], 'holders': x['holders'], 'chg': x['holders_change_qoq'],
                'own': x['inst_own_pct'], 'own_chg': x['own_pct_chg_pp'], 'q': x['quarter']} for x in f13 if x.get('holders_change_qoq') is not None],
              key=lambda x: -(x['own_chg'] or 0))
insd = {}
for t in ins:
    v = t.get('value_usd') or 0
    o = insd.setdefault(t['ticker'], {'ticker': t['ticker'], 'name': t['company'], 'buy': 0, 'sell': 0, 'nb': 0, 'ns': 0})
    if t['side'] == '매수': o['buy'] += v; o['nb'] += 1
    elif t['side'] == '매도': o['sell'] += v; o['ns'] += 1
pros = {'asof': LAST, 'horizon_days': H, 'min_calls': MINN, 'scored': scored, 'firms_total': len(firms), 'rank': rows, 'recent': recent[:40],
        'leopold': [{'ticker': l['ticker'], 'name': l['name'], 'pct': l['pct_portfolio'], 'value_bn': round(l['value_usd'] / 1e9, 2), 'change': l['change'], 'q': l['q']} for l in leo_rows],
        'inst': inst, 'insider': sorted(insd.values(), key=lambda o: -(o['buy'] - o['sell']))}

# ── ① 저평가 서치: 불 7개
d60 = (dt.date.fromisoformat(LAST) - dt.timedelta(days=60)).isoformat()
lastq = {}
for r in q:
    if r.get('rev') is None: continue
    if r['ticker'] not in lastq or r['cq'] > lastq[r['ticker']]['cq']: lastq[r['ticker']] = r
silast = {}
for r in sorted(si, key=lambda r: r['date']): silast.setdefault(r['ticker'], []).append(r)
f13m = {x['ticker']: x for x in f13}
uni = [p for p in px if p['ticker'] in TK and p.get('price') and 'ETF' not in (p.get('category') or '') and 'REIT' not in p['ticker']]
cat_pe = {}
for p in uni:
    if p.get('fwd_pe_snap') and p['fwd_pe_snap'] > 0: cat_pe.setdefault(p['category'], []).append(p['fwd_pe_snap'])
all_pe = st.median([v for l in cat_pe.values() for v in l])
out = []
for p in uni:
    t = p['ticker']; tk = TK[t]; L = []
    pt = tk.get('cons_avg_pt') or p.get('cons_avg_pt'); up = (pt / p['price'] - 1) * 100 if pt else None
    L.append({'k': '목표가 여력', 'on': up is not None and up >= 20, 'v': f'평균 목표가까지 {up:+.0f}%' if up is not None else '목표가 자료 없음'})
    fpe = p.get('fwd_pe_snap'); peers = cat_pe.get(p['category'], []); med = st.median(peers) if len(peers) >= 3 else all_pe
    L.append({'k': '같은 층 대비 싸다', 'on': bool(fpe and fpe > 0 and fpe < med * 0.9),
              'v': f'선행 PER {fpe:.1f}배 · {"같은 층" if len(peers) >= 3 else "전체"} 가운데값 {med:.1f}배' if fpe and fpe > 0 else '선행 PER 자료 없음'})
    e = lastq.get(t)
    ok = bool(e and (e.get('rev_vs') == '상회' or (e.get('rev') and e.get('rev_est') and e['rev'] > e['rev_est'])) and (e.get('rev_yoy') or 0) >= 15)
    L.append({'k': '실적 탄력', 'on': ok, 'v': (f"{e['fq']} 매출 {'예상 상회' if e.get('rev_vs') == '상회' else '예상 하회' if e.get('rev_vs') == '하회' else '예상 부합'} · 전년비 {e['rev_yoy']:+.0f}%" if e and e.get('rev_yoy') is not None else (f"{e['fq']} 매출 발표" if e else '분기 실적 자료 없음'))})
    hi = p.get('hi_52w'); dd = (p['price'] / hi - 1) * 100 if hi else None
    L.append({'k': '고점 대비 눌림', 'on': dd is not None and dd <= -15, 'v': f'1년 고점 대비 {dd:.0f}%' if dd is not None else '고점 자료 없음'})
    re_ = [x for x in ev if x['ticker'] == t and x['date'] >= d60]
    upc = sum(1 for x in re_ if x['type'] in ('상향', '의견상향')); dnc = sum(1 for x in re_ if x['type'] in ('하향', '의견하향'))
    L.append({'k': '목표가 오름세', 'on': upc >= 2 and upc > dnc * 2, 'v': f'최근 60일 상향 {upc} · 하향 {dnc}'})
    tp = [x for x in re_ if x['firm'] in TOP and direc(x) == 1]
    L.append({'k': '고수 상향', 'on': bool(tp), 'v': ('적중률 상위 ' + ', '.join(sorted({f"{x['firm']}({TOP.index(x['firm']) + 1}위)" for x in tp})) + ' 상향') if tp else '최근 60일 상위 10곳 상향 없음'})
    sl = silast.get(t, []); f = f13m.get(t); io = insd.get(t)
    sig = []
    if len(sl) >= 2 and sl[-1]['shares'] < sl[-2]['shares']: sig.append(f"공매도 잔고 감소({int(sl[-1]['date'][5:7])}.{int(sl[-1]['date'][8:10])} {sl[-1]['chg_pct']:+.1f}%)")
    if f and (f.get('own_pct_chg_pp') or 0) > 0: sig.append(f"기관 보유 +{f['own_pct_chg_pp']}%p")
    if io and io['buy'] > io['sell']: sig.append('내부자 순매수')
    L.append({'k': '수급 개선', 'on': len(sig) >= 1, 'v': ' · '.join(sig) if sig else '뚜렷한 개선 없음'})
    n = sum(1 for x in L if x['on'])
    out.append({'ticker': t, 'name': tk['name'], 'cat': p['category'], 'price': p['price'], 'cur': p['currency'], 'up': round(up, 1) if up is not None else None,
                'fpe': fpe, 'dd': round(dd, 1) if dd is not None else None, 'm3': round((p['price'] / p['m3_close'] - 1) * 100, 1) if p.get('m3_close') else None,
                'n_buy': tk.get('n_buy'), 'n_hold': tk.get('n_hold'), 'n_sell': tk.get('n_sell'), 'lights': n, 'L': L})
out.sort(key=lambda o: (-o['lights'], -(o['up'] or -999)))
os.makedirs(os.path.join(R, 'd/ideas'), exist_ok=True)
json.dump({'asof': LAST, 'n': len(out), 'items': out}, open(os.path.join(R, 'd/ideas/value.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for r in rows: r['best'] = r['best']
json.dump(pros, open(os.path.join(R, 'd/ideas/pros.json'), 'w', encoding='utf-8'), ensure_ascii=False, default=list)
print('asof', LAST, '| 성적 채점', scored, '건, 순위', len(rows), '곳 | 저평가 후보', len(out), '| 불5+', sum(o['lights'] >= 5 for o in out))
