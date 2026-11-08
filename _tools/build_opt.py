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
# ①-2 VIX 10년 일별 종가(사용자 2026-11-09 '기간 설정 — 5년·10년까지, 역사적 사건과 지금 비교') — 화면 _tools/vixlong.js
if days:
    import datetime as _dt
    cut = (_dt.date.fromisoformat(days[-1]) - _dt.timedelta(days=3653)).isoformat()
    ks = [d for d in days if d >= cut]
    if dump('vix_long', {'src': SRC_IDX, 'd': ks, 'c': [VIX[d] for d in ks]}): ch.append('VIX 10년')
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
# ⑤ 실적 '옵션 예상 vs 실제' — 발표일이 지난 '발표 예정' 행의 실제 등락을 야후 종가로 채움(사용자 2026-11-09 '최신화가 안 됨')
#    장 마감 후 발표 = 발표일 종가 → 다음 거래일 종가, 장 시작 전 = 전 거래일 종가 → 발표일 종가
em = load('earnings_moves')
if em:
    import datetime as _dt
    _today = _dt.date.today().isoformat(); _n = 0
    for r in em:
        if r.get('status') == 'reported' or not r.get('report_date') or r['report_date'] >= _today: continue
        try:
            j = json.loads(get('https://query1.finance.yahoo.com/v8/finance/chart/%s?range=3mo&interval=1d' % r['ticker']))['chart']['result'][0]
            import zoneinfo; z = zoneinfo.ZoneInfo('America/New_York')
            px = [(_dt.datetime.fromtimestamp(t, z).date().isoformat(), c) for t, c in zip(j['timestamp'], j['indicators']['quote'][0]['close']) if c]
            ks = [d for d, _ in px]; rd = r['report_date']
            if '전' in (r.get('timing') or ''):
                i = next((k for k, d in enumerate(ks) if d >= rd), None); a, b = (i - 1, i) if i else (None, None)
            else:
                i = max((k for k, d in enumerate(ks) if d <= rd), default=None); a, b = (i, i + 1) if i is not None else (None, None)
            if a is None or b is None or b >= len(px) or a < 0: continue
            if px[b][0] >= _today: continue   # 다음 날 장이 아직 안 끝남
            r['actual_pct'] = round((px[b][1] / px[a][1] - 1) * 100, 2); r['actual_date'] = px[b][0]
            r['actual_source'] = 'https://finance.yahoo.com/quote/%s/history/ (야후 종가)' % r['ticker']; r['status'] = 'reported'; _n += 1
        except Exception as e: print('실적 변동', r.get('ticker'), e)
    if _n and dump('earnings_moves', em): ch.append('실적 실제 변동 %d' % _n)
# ⑥ 다가오는 실적(실적 일정 페이지의 이번 주·다음 주) → '발표 예정' 행 + 옵션 예상 변동폭(CBOE 지연 시세, 등가격 스트래들 ÷ 주가)
#    (사용자 2026-11-09 '최신화가 안 됨 · 실적 가까운 순') — 미국 상장 추적 종목만, 발표 전까지 매일 다시 계산
US = {'엔비디아': 'NVDA', '코어위브': 'CRWV', '네비우스': 'NBIS', '어플라이드머티리얼즈': 'AMAT', '시스코': 'CSCO', '세레브라스': 'CBRS',
      'AMD': 'AMD', '마이크론': 'MU', '브로드컴': 'AVGO', '오라클': 'ORCL', '마벨': 'MRVL', '델': 'DELL', 'HP엔터프라이즈': 'HPE', '슈퍼마이크로': 'SMCI',
      '아리스타': 'ANET', '코히어런트': 'COHR', '버티브': 'VRT', '램리서치': 'LRCX', 'KLA': 'KLAC', '세일즈포스': 'CRM', '스노우플레이크': 'SNOW',
      '팔란티어': 'PLTR', '아이렌': 'IREN', '클라우드플레어': 'NET', '어플라이드 옵토': 'AAOI', '시게이트': 'STX', '웨스턴디지털': 'WDC', '샌디스크': 'SNDK',
      '퀄컴': 'QCOM', '애플': 'AAPL', '마이크로소프트': 'MSFT', '구글': 'GOOGL', '아마존': 'AMZN', '메타': 'META', '테슬라': 'TSLA', '인텔': 'INTC'}
def _cal_events():
    import re, datetime as _dt
    try: h = open(os.path.join(R, 'p-cal.html'), encoding='utf-8').read()
    except Exception: return []
    ev = []
    for key in ('const DAYS = ', 'const NEXT = '):
        i = h.find(key)
        if i < 0: continue
        j = h.find(';\n', i)
        try: arr = json.loads(h[i + len(key):j].strip().rstrip(';'))
        except Exception: continue
        y = _dt.date.today().year
        for d in arr:
            if 'blocks' in d:
                lab = d['d']; rows = [(e.get('t', ''), e) for b in d['blocks'] for e in b['ev']]
            else:
                m = re.match(r'(\d+)/(\d+)', d.get('h', ''))
                if not m: continue
                lab = m.group(0); t0 = '장후' if '장후' in d['h'] else '장전' if '장전' in d['h'] else ''
                rows = [(t0, e) for e in d['ev']]
            mo, da = map(int, lab.split('/')[:2]); kd = _dt.date(y + (1 if mo < _dt.date.today().month - 6 else 0), mo, da)
            for t, e in rows:
                tk = US.get(e['n'])
                if not tk: continue
                hh = re.match(r'(\d+):', t or '')
                if t == '장후' or (hh and int(hh.group(1)) < 12):     # 한국 새벽 = 뉴욕 전날 장 마감 후
                    ev.append((tk, e['n'], (kd - _dt.timedelta(days=1)).isoformat(), '장 마감 후'))
                elif t == '장전' or (hh and int(hh.group(1)) >= 18):
                    ev.append((tk, e['n'], kd.isoformat(), '장 시작 전'))
    return ev
def _implied(tk, rd, after):
    j = json.loads(get('https://cdn.cboe.com/api/global/delayed_quotes/options/%s.json' % tk))['data']
    px = j.get('current_price') or j.get('close'); ops = j.get('options') or []
    if not px or not ops: return None
    import re
    by = {}
    for o in ops:
        m = re.match(r'^[A-Z]+(\d{6})([CP])(\d{8})$', o['option'])
        if not m: continue
        exp = '20%s-%s-%s' % (m.group(1)[:2], m.group(1)[2:4], m.group(1)[4:]); k = int(m.group(3)) / 1000
        mid = (o.get('bid', 0) + o.get('ask', 0)) / 2 if o.get('bid') and o.get('ask') else None
        if mid: by.setdefault(exp, {}).setdefault(k, {})[m.group(2)] = mid
    exps = sorted(e for e in by if (e > rd if after else e >= rd))
    for e in exps[:2]:
        ks = [k for k in by[e] if 'C' in by[e][k] and 'P' in by[e][k]]
        if not ks: continue
        k = min(ks, key=lambda x: abs(x - px))
        return round((by[e][k]['C'] + by[e][k]['P']) / px * 100, 2), e
    return None
try:
    import datetime as _dt
    em = load('earnings_moves'); have = {(r['ticker'], r['report_date']) for r in em}; _today = _dt.date.today().isoformat(); _u = 0
    for tk, nm, rd, tm in _cal_events():
        if rd < _today: continue
        row = next((r for r in em if r['ticker'] == tk and r['report_date'] == rd), None)
        if not row:
            row = {'ticker': tk, 'name_ko': nm, 'report_date': rd, 'timing': tm, 'implied_pct': None, 'implied_source': None, 'implied_alt_pct': None,
                   'implied_alt_source': None, 'actual_pct': None, 'actual_date': None, 'actual_source': None, 'status': 'upcoming'}
            em.append(row)
        try:
            iv = _implied(tk, rd, tm == '장 마감 후')
            if iv: row['implied_pct'] = iv[0]; row['implied_source'] = 'https://www.cboe.com/delayed_quotes/%s/quote_table (등가격 스트래들 %s 만기 ÷ 주가, 자동 계산)' % (tk.lower(), iv[1]); _u += 1
        except Exception as e: print('예상 변동', tk, e)
    em.sort(key=lambda r: r['report_date'])
    if dump('earnings_moves', em[-40:]): ch.append('실적 예정 %d' % _u)
except Exception as e: print('실적 예정 실패', e)
print('옵션 온도계:', ' · '.join(ch) if ch else '변화 없음', '(마지막 VIX', days[-1] if days else '-', ')')
