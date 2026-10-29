# 관문 점수 자료(사용자 2026-10-29) — '내 종목 점검'·'반도체 온도판' 탭용 d/ideas/gates.json
#  1관문 사슬(AI 확인) → 2관문 재무(시장가치) → 3관문 자리(지금 살 때인가) + 보조 바람(수급·층 흐름)
#  자리 규칙은 10년치 월별 주가로 거꾸로 채점해 함께 실음(bt). 새 수집 없이 사이트 자료 + d/ideas/fin.json(SEC)만 씀
# 사용: python3 -I _tools/build_gates.py <사이트 폴더>
import json, os, re, sys, html, statistics as st, datetime as dt, collections as C
R = sys.argv[1] if len(sys.argv) > 1 else '.'
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
px = {p['ticker']: p for p in J('d/prices/prices.json')}
TK = {t['ticker']: t for t in J('d/targets/tickers.json')}
ev = J('d/targets/events.json'); q = J('d/qtr/earnings.json'); si = J('d/short/si.json'); ins = J('d/insider/insider_tx.json')
fin = J('d/ideas/fin.json').get('items', {}) if os.path.exists(os.path.join(R, 'd/ideas/fin.json')) else {}
H = C.defaultdict(list)
for r in J('d/prices/history.json'):
    if r['kind'] == 'd': H[r['ticker']].append((r['date'], r['close']))
for k in H: H[k].sort()
LAST = max(d for v in H.values() for d, _ in v)

def ma(t, n):
    s = [c for _, c in H[t]]
    return st.mean(s[-n:]) if len(s) >= n else None
def rsi(t, n=14):
    s = [c for _, c in H[t]][-(n + 1):]
    if len(s) < n + 1: return None
    g = sum(max(s[i] - s[i - 1], 0) for i in range(1, len(s))); l = sum(max(s[i - 1] - s[i], 0) for i in range(1, len(s)))
    return 100.0 if l == 0 else 100 - 100 / (1 + g / l)
pc = lambda a, b: (a / b - 1) * 100 if a and b else None

# 실적: 종목별 최근 분기, 실적 결과 페이지의 'AI 관점' 판정
last = {}
for r in q:
    if r.get('rev') is None: continue
    if r['ticker'] not in last or r['cq'] > last[r['ticker']]['cq']: last[r['ticker']] = r
AI = {}
s = open(os.path.join(R, 'p-earn.html'), encoding='utf-8').read().replace('\\"', '"')
for m in re.finditer(r'<article\b([^>]*)>', s):
    a = dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
    if not a.get('name'): continue
    t = html.unescape(a['name']).split()[-1]; v = re.search(r'AI 관점 (호재|중립|경고)', html.unescape(a.get('sum', '')))
    if v and (t not in AI or a.get('ts', '') > AI[t][1]): AI[t] = (v.group(1), a.get('ts', ''))
beat = lambda e: bool(e and (e.get('rev_vs') == '상회' or (e.get('rev') and e.get('rev_est') and e['rev'] > e['rev_est'])))

# 층(카테고리)
UNI = [t for t, p in px.items() if t in TK and p.get('price') and 'ETF' not in (p.get('category') or '')]
LAY = C.defaultdict(list)
for t in UNI: LAY[px[t]['category']].append(t)
def above50(t):
    m = ma(t, 50); return m is not None and px[t]['price'] > m
lay = {}
for c, ts in LAY.items():
    lq = [last[t] for t in ts if t in last]; yy = [e['rev_yoy'] for e in lq if e.get('rev_yoy') is not None]
    r3 = [pc(px[t]['price'], px[t].get('m3_close')) for t in ts if px[t].get('m3_close')]
    fp = [px[t]['fwd_pe_snap'] for t in ts if (px[t].get('fwd_pe_snap') or 0) > 0]
    av = C.Counter(AI[t][0] for t in ts if t in AI)
    lay[c] = {'n': len(ts), 'beat': sum(beat(e) for e in lq), 'rep': len(lq), 'yoy': round(st.median(yy)) if yy else None,
              'm3': round(st.mean(r3), 1) if r3 else None, 'a50': sum(above50(t) for t in ts), 'fpe': round(st.median(fp), 1) if len(fp) >= 3 else None,
              'ai': dict(av)}
allfpe = st.median([px[t]['fwd_pe_snap'] for t in UNI if (px[t].get('fwd_pe_snap') or 0) > 0])
for c, L in lay.items():
    good = L['rep'] and L['beat'] / L['rep'] >= .7 and (L['yoy'] or 0) >= 25
    hot = (L['m3'] or 0) >= 10 and L['a50'] / L['n'] >= .5
    L['temp'] = '뜨거움' if good and hot else '실적 좋음·주가 쉼' if good else '주가만 뜨거움' if hot else '식음' if (L['m3'] or 0) < 0 else '미지근'
    L['lv'] = {'뜨거움': 4, '실적 좋음·주가 쉼': 3, '주가만 뜨거움': 2, '미지근': 2, '식음': 1}[L['temp']]

# 목표가 흐름(60일)
d60 = (dt.date.fromisoformat(LAST) - dt.timedelta(days=60)).isoformat()
ptf = C.Counter(); ptd = C.Counter()
for e in ev:
    if e['date'] < d60: continue
    if e['type'] in ('상향', '의견상향'): ptf[e['ticker']] += 1
    elif e['type'] in ('하향', '의견하향'): ptd[e['ticker']] += 1
silast = C.defaultdict(list)
for r in sorted(si, key=lambda r: r['date']): silast[r['ticker']].append(r)
insd = C.defaultdict(float)
for x in ins:
    insd[x['ticker']] += (x.get('value_usd') or 0) * (1 if x['side'] == '매수' else -1 if x['side'] == '매도' else 0)

def spot_label(v200, dd, rsi_, v50):
    # 자리 규칙(월별 거꾸로 채점과 같은 규칙: 200일선·고점 대비가 뼈대, RSI·50일선은 보조)
    if v200 is not None and v200 < 0: return '추세 아래', 1
    if (dd is not None and dd > -5) or (rsi_ is not None and rsi_ >= 70): return '고점 근처', 2
    if (dd is not None and dd <= -15) or (rsi_ is not None and rsi_ <= 40) or (v50 is not None and abs(v50) <= 3): return '눌림 자리', 4
    return '보통', 3

items = {}
for t in UNI:
    p = px[t]; c = p['category']; L = lay[c]; e = last.get(t)
    # ① 사슬
    peers = [u for u in LAY[c] if u != t]; pq = [last[u] for u in peers if u in last]
    pb = sum(beat(x) for x in pq); pyy = [x['rev_yoy'] for x in pq if x.get('rev_yoy') is not None]
    own_ai = AI.get(t, (None,))[0]; own_yoy = e.get('rev_yoy') if e else None
    # 층(동료)이 AI 돈을 받고 있나 + 이 종목 자신도 받고 있나 — 둘 다여야 'AI 확인'(사용자 2026-10-29: 사슬에서 AI가 확인돼야 출발)
    # 예상치 자료가 없는 분기는 '미달'로 치지 않고 빼고 셈. 실적 결과 페이지의 'AI 관점 호재'가 있으면 그게 우선(예: 앰코 — 스마트폰 약세는 따로 봄)
    kn = [x for x in pq if x.get('rev_vs') or (x.get('rev') and x.get('rev_est'))]; pb = sum(beat(x) for x in kn)
    lay_ok = bool(pyy) and st.median(pyy) >= 15 and (not kn or pb / len(kn) >= .6)
    own_known = bool(e and (e.get('rev_vs') or e.get('rev_est')))
    own_ok = own_ai == '호재' or ((beat(e) if own_known else True) and (own_yoy or 0) >= (20 if own_known else 30))
    if own_ai == '경고' or (own_ai != '호재' and e and e.get('rev_vs') == '하회' and (own_yoy or 0) < 10): ch = ('AI 경고', 1)
    elif lay_ok and own_ok: ch = ('AI 확인', 3)
    elif own_ok or lay_ok: ch = ('확인 중', 2)
    else: ch = ('미확인', 1)
    chain = {'v': ch[0], 'lv': ch[1], 'peers': len(kn), 'pbeat': pb, 'pyoy': round(st.median(pyy)) if pyy else None, 'ai': own_ai, 'yoy': own_yoy,
             'lay_ai': L['ai']}
    # ② 재무
    fpe = p.get('fwd_pe_snap') if (p.get('fwd_pe_snap') or 0) > 0 else None; lfpe = L['fpe'] or allfpe
    peg = round(fpe / own_yoy, 2) if fpe and own_yoy and own_yoy > 0 else None
    F = fin.get(t, {}); pts = []; why = []
    if fpe: pts.append(fpe < lfpe * .95); why.append(f'선행 PER {fpe:.1f}배(층 가운데값 {lfpe:.1f}배)')
    if peg is not None: pts.append(peg < 1); why.append(f'성장 대비 PER {peg}')
    if e and e.get('eps_surp') is not None: pts.append(e['eps_surp'] > 0); why.append(f"EPS 예상 대비 {e['eps_surp']:+.1f}%")
    if own_yoy is not None: pts.append(own_yoy >= 20); why.append(f'매출 전년비 {own_yoy:+.0f}%')
    if F.get('opm') is not None: pts.append(F['opm'] >= 15); why.append(f"영업이익률 {F['opm']:.0f}%")
    if F.get('fcfm') is not None: pts.append(F['fcfm'] > 0); why.append(f"잉여현금흐름률 {F['fcfm']:+.0f}%")
    if F.get('nd_rev') is not None: pts.append(F['nd_rev'] <= 1); why.append('순현금' if F['nd_rev'] <= 0 else f"순부채 매출의 {F['nd_rev']:.1f}배")
    r_ = sum(pts) / len(pts) if pts else None
    gr = None if r_ is None else 'A' if r_ >= .8 else 'B' if r_ >= .6 else 'C' if r_ >= .4 else 'D'
    finx = {'v': gr or '—', 'lv': {'A': 3, 'B': 3, 'C': 2, 'D': 1}.get(gr, 0), 'why': why, 'n': len(pts), 'health': bool(F)}
    # ③ 자리
    m50, m200 = ma(t, 50), ma(t, 200); r14 = rsi(t)
    v50, v200 = pc(p['price'], m50), pc(p['price'], m200); dd = pc(p['price'], p.get('hi_52w'))
    sl = spot_label(v200, dd, r14, v50)
    spot = {'v': sl[0], 'lv': sl[1], 'dd': round(dd, 1) if dd is not None else None, 'v50': round(v50, 1) if v50 is not None else None,
            'v200': round(v200, 1) if v200 is not None else None, 'm50': round(m50, 2) if m50 else None, 'm200': round(m200, 2) if m200 else None, 'rsi': round(r14) if r14 is not None else None}
    # 바람
    br = L['a50'] / L['n']; me50 = above50(t)
    wv = '층째 조정' if br <= .25 and not me50 else '나 홀로 약세' if br >= .5 and not me50 else '순풍' if br >= .5 and me50 else '약함'
    s2 = silast.get(t, [])
    wind = {'v': wv, 'lv': {'순풍': 3, '약함': 2, '층째 조정': 2, '나 홀로 약세': 1}[wv], 'a50': L['a50'], 'ln': L['n'], 'me50': me50,
            'si': s2[-1]['chg_pct'] if s2 else None, 'ins': round(insd[t]) if t in insd else None, 'up60': ptf[t], 'dn60': ptd[t]}
    # 판정 문장
    stop = ch[0] in ('AI 경고', '미확인') or (gr == 'D') or (e and e.get('rev_vs') == '하회' and ptd[t] > ptf[t])
    if stop: vd = '물타기 멈춤 신호 — ' + ('산 이유(사슬)부터 다시 확인할 때입니다.' if ch[0] in ('AI 경고', '미확인') else '실적·목표가 흐름이 꺾여, 싸 보여도 이유부터 확인할 때입니다.')
    elif sl[0] == '추세 아래': vd = '사슬·재무는 그대로인데 200일선 아래로 내려온 자리입니다. 싸 보여도 추세가 꺾여 있어, 반등 확인 전 나눠 담기 여부를 따져 볼 구간입니다.'
    elif sl[0] == '고점 근처': vd = '사슬·재무는 그대로이고 주가가 고점 근처입니다. 추가매수라면 서두를 자리는 아닙니다.'
    elif sl[0] == '눌림 자리': vd = '물타기 멈춤 신호 없음. 사슬·재무는 그대로이고, 큰 추세 안에서 쉬어 가는 눌림 자리입니다.'
    else: vd = '물타기 멈춤 신호 없음. 사슬·재무는 그대로이고, 자리는 중간입니다.'
    if not stop and wv == '나 홀로 약세': vd += ' 다만 층은 괜찮은데 이 종목만 약해, 종목 쪽 이유를 확인해 볼 만합니다.'
    items[t] = {'name': TK[t]['name'], 'cat': c, 'price': p['price'], 'cur': p['currency'], 'chain': chain, 'fin': finx, 'spot': spot, 'wind': wind, 'stop': bool(stop), 'vd': vd}

# 반도체 지수(SOXX)
x = 'SOXX'; sp = px[x]; hs = H[x]; pk = 0; worst = (0, '')
for d, c_ in hs:
    pk = max(pk, c_); w = c_ / pk - 1
    if w < worst[0]: worst = (w, d)
xv200, xv50, xdd, xr = pc(sp['price'], ma(x, 200)), pc(sp['price'], ma(x, 50)), pc(sp['price'], sp.get('hi_52w')), rsi(x)
xl = spot_label(xv200, xdd, xr, xv50)
on = [xv200 is not None and xv200 > 0, (ma(x, 50) or 0) > (st.mean([c_ for _, c_ in hs[-70:-20]]) if len(hs) > 70 else 0), xdd is not None and -25 <= xdd <= -8, xr is not None and xr <= 45]
soxx = {'price': sp['price'], 'v200': round(xv200, 1), 'v50': round(xv50, 1), 'dd': round(xdd, 1), 'rsi': round(xr), 'm3': round(pc(sp['price'], sp.get('m3_close')), 1),
        'worst': round(worst[0] * 100, 1), 'worst_d': worst[1], 'spot': xl[0], 'lights': sum(on), 'L': ['200일선 위', '50일선 오름세', '고점 대비 −8~−25% 눌림', 'RSI 45 이하'], 'on': on,
        'breadth': sum(above50(t) for t in UNI), 'bn': len(UNI)}

# 자리 규칙 거꾸로 채점: 10년치 월말 주가(live/long.json), 3개월 뒤 나스닥100(QQQ) 대비 초과수익
LG = J('live/long.json')['d']
def month_end(rows):
    m = {}
    for d, c_ in rows: m[d[:7]] = c_
    return sorted(m.items())
QQ = dict(month_end(LG['QQQ']))
agg = C.defaultdict(list); aggx = C.defaultdict(list)
for t, rows in LG.items():
    if t in ('QQQ', 'SOXL') or (t not in TK and t != 'SOXX'): continue
    me = month_end(rows)
    for i in range(12, len(me) - 3):
        k, c_ = me[i]; k3, c3 = me[i + 3]
        if k not in QQ or k3 not in QQ: continue
        v10 = pc(c_, st.mean([v for _, v in me[i - 9:i + 1]])); hi = max(v for _, v in me[i - 11:i + 1]); dd_ = pc(c_, hi)
        lab = spot_label(v10, dd_, None, None)[0]
        ex = (c3 / c_ - QQ[k3] / QQ[k]) * 100
        (aggx if t == 'SOXX' else agg)[lab].append(ex)
def summ(a):
    return {k: {'n': len(v), 'avg': round(st.mean(v), 1), 'med': round(st.median(v), 1), 'hit': round(sum(x > 0 for x in v) / len(v) * 100)} for k, v in a.items() if v}
bt = {'stocks': summ(agg), 'soxx': summ(aggx), 'note': '월말 종가 기준 · 200일선 대신 10개월 평균 · RSI·50일선 제외 · 3개월 뒤 나스닥100 대비 초과수익'}

json.dump({'asof': LAST, 'items': items, 'layers': lay, 'soxx': soxx, 'bt': bt, 'fin_asof': (J('d/ideas/fin.json').get('asof') if fin else None)},
          open(os.path.join(R, 'd/ideas/gates.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('gates', len(items), '| SEC 재무', len(fin), '| 층', len(lay), '| SOXX', soxx['spot'], soxx['lights'], '/4')
print('채점(종목):', bt['stocks']); print('채점(SOXX):', bt['soxx'])
