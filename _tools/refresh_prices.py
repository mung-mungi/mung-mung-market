# 멍뭉 터미널 시세 새로고침 — 야후 차트 API에서 숫자만 받아 prices.json·history.json을 고친다(검색 없음)
# 사용:
#   python3 -I refresh_prices.py update  <prices.json> <history.json>      → 현재가(프리마켓·장중·종가) + 일별 종가 기록
#   python3 -I refresh_prices.py trend   <p-trend.html> <prices.json> <history.json>  → 차트 길잡이 페이지의 const DATA 한 줄만 교체
#   python3 -I refresh_prices.py unwrap  <page.html>   → Artifact read로 받은 파일 앞뒤의 게시용 바깥 틀 제거
import json, sys, time, subprocess, datetime as dt, concurrent.futures as cf, re

UA = 'Mozilla/5.0'
KST = dt.timezone(dt.timedelta(hours=9))


def get(url, tries=3):
    for k in range(tries):
        try:
            o = subprocess.run(['curl', '-sS', '-m', '20', '-A', UA, url], capture_output=True, text=True).stdout
            r = json.loads(o)['chart']['result'][0]
            if r and r.get('meta'):
                return r
        except Exception:
            pass
        time.sleep(1.5 * (k + 1))
    return None


def fetch(sym):
    base = 'https://query1.finance.yahoo.com/v8/finance/chart/' + sym
    return sym, get(base + '?range=1d&interval=5m&includePrePost=true'), get(base + '?range=3mo&interval=1d')


def ldate(ts, off):
    return dt.datetime.fromtimestamp(ts + off, dt.timezone.utc).strftime('%Y-%m-%d')


def month_back(d, n):
    y, m = d.year, d.month - n
    while m <= 0:
        m += 12; y -= 1
    import calendar
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


INTRA = {}


def update(pp, hp):
    P = json.load(open(pp, encoding='utf-8'))
    H = json.load(open(hp, encoding='utf-8'))
    hist = {}
    for r in H:
        hist.setdefault(r['ticker'], {})[(r['date'], r['kind'])] = r['close']
    now = time.time()
    syms = [r['ticker'] for r in P]
    with cf.ThreadPoolExecutor(6) as ex:
        res = {s: (a, b) for s, a, b in ex.map(fetch, syms)}
    out = {'ok': 0, 'fail': [], 'split': [], 'kinds': {}, 'new_closes': 0, 'changed': 0}
    before = {r['ticker']: (r.get('price'), r.get('price_kind'), r.get('price_date')) for r in P}
    for r in P:
        t = r['ticker']; a, b = res.get(t, (None, None))
        if not a or not b:
            out['fail'].append(t); continue
        m = a['meta']; off = m.get('gmtoffset', 0); tp = m.get('currentTradingPeriod', {})
        try:  # 당일 5분 흐름(토스식 1일 차트용, 사용자 2026-10-29) — MM_INTRA 환경변수가 있을 때만 파일로
            q5 = a.get('indicators', {}).get('quote', [{}])[0].get('close', []); ts5 = a.get('timestamp', []) or []
            pts = [(x, round(float(c), 4)) for x, c in zip(ts5, q5) if c is not None]
            if pts:
                s0 = pts[0][0]
                INTRA[t] = {'pc': m.get('chartPreviousClose') or m.get('previousClose'), 'cur': m.get('currency'), 'off': off, 's': s0,
                            'p': [[(x - s0) // 60, c] for x, c in pts],
                            'reg': [tp.get('regular', {}).get('start'), tp.get('regular', {}).get('end')]}
        except Exception:
            pass
        reg = tp.get('regular', {}); pre = tp.get('pre', {})
        in_reg = reg and reg['start'] <= now < reg['end']
        today = ldate(now, off)
        # 일별 종가(끝난 거래일만)
        days = []
        q = b.get('indicators', {}).get('quote', [{}])[0].get('close', [])
        for ts, c in zip(b.get('timestamp', []), q):
            if c is None: continue
            d = ldate(ts, off)
            if d == today and (in_reg or (reg and now < reg['start'])): continue  # 아직 안 끝난 오늘
            days.append((d, round(float(c), 4)))
        days = sorted(dict(days).items())
        if not days:
            out['fail'].append(t); continue
        th = hist.setdefault(t, {})
        old = th.get((days[-1][0], 'd'))
        if old and abs(days[-1][1] / old - 1) > 0.25:  # 액면분할 의심 → 이 종목은 건너뜀
            out['split'].append(t); continue
        for d, c in days:
            if th.get((d, 'd')) != c:
                if (d, 'd') not in th: out['new_closes'] += 1
                th[(d, 'd')] = c
        last_d, last_c = days[-1]
        prev_d, prev_c = days[-2] if len(days) > 1 else (r.get('prev_date'), r.get('prev_close'))
        kind, price, pdate = 'close', last_c, last_d
        if in_reg and m.get('regularMarketPrice') is not None:
            kind, price, pdate = 'intraday', float(m['regularMarketPrice']), today
            prev_d, prev_c = last_d, last_c
        elif pre and pre.get('start', 0) <= now < pre.get('end', 0):
            q5 = a.get('indicators', {}).get('quote', [{}])[0].get('close', [])
            pts = [(ts, c) for ts, c in zip(a.get('timestamp', []), q5) if c is not None and ts >= pre['start']]
            if pts:
                kind, price, pdate = 'premarket', float(pts[-1][1]), today
                prev_d, prev_c = last_d, last_c
        elif reg and now >= reg.get('end', 1 << 62) and last_d == ldate(reg['start'], off):
            # 애프터(시간외, 사용자 2026-10-29): 정규장이 끝난 뒤 거래가 있으면 그 값을 보여 줌 — 다음 프리마켓 전까지 유지, 등락은 그날 종가 대비
            q5 = a.get('indicators', {}).get('quote', [{}])[0].get('close', [])
            pts = [(ts, c) for ts, c in zip(a.get('timestamp', []), q5) if c is not None and ts >= reg['end']]
            if pts:
                kind, price, pdate = 'aftermarket', float(pts[-1][1]), last_d
                prev_d, prev_c = last_d, last_c
        r['price'] = round(price, 4); r['price_date'] = pdate; r['price_kind'] = kind
        r['prev_close'] = prev_c; r['prev_date'] = prev_d
        r['price_time_kst'] = dt.datetime.now(KST).strftime('%m.%d %H:%M')
        # 1·3·6·12개월 전, 연초 대비, 52주 고저(일별 종가 기준)
        dd = sorted((d, c) for (d, k), c in th.items() if k == 'd')
        mm = sorted((d, c) for (d, k), c in th.items() if k == 'm')
        base = dt.date.fromisoformat(pdate)
        for n, key in ((1, 'm1'), (3, 'm3'), (6, 'm6'), (12, 'm12')):
            tgt = month_back(base, n).isoformat()
            cand = [x for x in dd if x[0] <= tgt] or [x for x in mm if x[0] <= tgt]
            if cand:
                r[key + '_close'], r[key + '_date'] = cand[-1][1], cand[-1][0]
        ye = f'{base.year - 1}-12-31'
        yc = [x for x in dd + mm if x[0] <= ye]
        if yc:
            yc.sort(); r['ytd_pct'] = round((price / yc[-1][1] - 1) * 100, 2)
        yr = (base - dt.timedelta(days=365)).isoformat()
        win = [c for d, c in dd if d >= yr]
        if win:
            r['hi_52w'] = max(win); r['lo_52w'] = min(win)
        if before.get(t) != (r['price'], r['price_kind'], r['price_date']): out['changed'] += 1
        out['ok'] += 1; out['kinds'][kind] = out['kinds'].get(kind, 0) + 1
    H2 = []
    for t, th in hist.items():
        for (d, k), c in th.items():
            H2.append({'ticker': t, 'date': d, 'close': c, 'kind': k})
    H2.sort(key=lambda x: (x['ticker'], x['date'], x['kind']))
    import os as _os
    if _os.environ.get('MM_INTRA') and INTRA:
        json.dump({'at': dt.datetime.now(KST).isoformat(timespec='seconds'), 'd': INTRA}, open(_os.environ['MM_INTRA'], 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump(P, open(pp, 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(H2, open(hp, 'w', encoding='utf-8'), ensure_ascii=False)
    out['total'] = len(P)
    print(json.dumps(out, ensure_ascii=False))


KEYS = ['ticker', 'name', 'category', 'order', 'currency', 'cons_avg_pt', 'price', 'price_date', 'price_kind', 'prev_close',
        'm1_close', 'm1_date', 'm3_close', 'm3_date', 'm6_close', 'm6_date', 'm12_close', 'm12_date', 'hi_52w', 'lo_52w', 'ytd_pct']


def trend(page, pp, hp):
    P = json.load(open(pp, encoding='utf-8')); H = json.load(open(hp, encoding='utf-8'))
    P = sorted(P, key=lambda r: r.get('order', 0))
    from collections import Counter
    asof = Counter(r.get('price_date') for r in P).most_common(1)[0][0]
    live = [r for r in P if r.get('price_kind') in ('premarket', 'intraday', 'aftermarket')]
    stamp = dt.datetime.now(KST).strftime('%m.%d %H:%M')
    label = f'{stamp} 기준 · ' + ('프리마켓·장중·애프터 가격 포함' if live else '종가 기준')
    hh = {}
    for r in H:
        hh.setdefault(r['ticker'], {})
        cur = hh[r['ticker']].get(r['date'])
        if cur is None or (cur[1] == 1 and r['kind'] == 'd'):
            hh[r['ticker']][r['date']] = (r['close'], 1 if r['kind'] == 'm' else 0)
    Hd = {t: [[d, v[0], v[1]] for d, v in sorted(x.items())] for t, x in hh.items()}
    D = {'asof': asof, 'label': label, 'P': [{k: r.get(k) for k in KEYS} for r in P], 'H': Hd}
    if page.endswith('.json'):  # trendjson: 차트 길잡이용 자료만 따로 파일로(5분 갱신이 씀)
        json.dump(D, open(page, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        print(json.dumps({'trendjson': 'ok', 'asof': asof, 'label': label}, ensure_ascii=False)); return
    line = 'const DATA = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    s = open(page, encoding='utf-8').read()
    had_live = 'live/trend.json' in s
    i = s.index('const DATA = '); j = s.index('\n', i)
    s = s[:i] + line + s[j:]
    if had_live:  # 사이트용 실시간 자료 읽기(site_live.py)를 지우지 않게 다시 감쌈
        import os as _o
        sys.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import site_live as _sl
        k = s.index('const DATA = ') + len('const DATA = '); e = s.index('\n', k); ln = s[k:e].rstrip()
        s = s[:k] + _sl.TREND_LOADER + ln[:-1] + ');' + s[e:]
    s = s.replace("document.getElementById('asof').textContent = '대부분 ' + fmtDate(DATA.asof) + ' 종가 기준';",
                  "document.getElementById('asof').textContent = DATA.label || ('대부분 ' + fmtDate(DATA.asof) + ' 종가 기준');")
    open(page, 'w', encoding='utf-8').write(s)
    print(json.dumps({'trend': 'ok', 'asof': asof, 'label': label}, ensure_ascii=False))


def unwrap(page):
    s = open(page, encoding='utf-8').read()
    if re.match(r'\s*<!doctype html><html><head><meta charset=utf8>', s, re.I) and '<title>' in s:
        s = s[s.index('<title>'):]
        while s.rstrip().endswith('</body></html>'):
            s = s.rstrip()[:-len('</body></html>')]
        open(page, 'w', encoding='utf-8').write(s)
        print('unwrapped')
    else:
        print('no-wrapper')


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'update': update(sys.argv[2], sys.argv[3])
    elif c in ('trend', 'trendjson'): trend(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'unwrap': unwrap(sys.argv[2])
