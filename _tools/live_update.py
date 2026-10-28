# GitHub Actions 5분 시세 갱신(사용자 2026-10-29 지시) — 시세 보드·차트 길잡이·한국 종목
# 장 시간에만: 미국 프리(04:00)~애프터(20:00) 뉴욕 평일, 한국 09:00~15:40 평일. 그 외·주말은 쉼.
# Claude 우선: 최근 1시간 사이트 게시(커밋) 7번 이상이면 건너뜀, Claude(봇 아닌 커밋)가 10분 안에 올렸으면 쉼.
# 실적 시간대(뉴욕 06:00~09:30, 16:00~19:30)는 15분 간격.
# 결과는 live/ 에만 씀(통합본 동기화가 덮어쓰는 d/prices 와 분리). 충돌 시 최신본 받고 다시 계산.
import urllib.parse, re
import datetime as dt, json, os, shutil, subprocess, sys
from zoneinfo import ZoneInfo

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(R, '_tools')
BOT = 'mung-bot'
FORCE = os.environ.get('FORCE') == '1'


def sh(*a, check=True):
    return subprocess.run(a, cwd=R, capture_output=True, text=True, check=check).stdout.strip()


def window(now):
    ny = now.astimezone(ZoneInfo('America/New_York')); kr = now.astimezone(ZoneInfo('Asia/Seoul'))
    m_ny = ny.hour * 60 + ny.minute; m_kr = kr.hour * 60 + kr.minute
    us = ny.weekday() < 5 and 4 * 60 <= m_ny < 20 * 60
    ko = kr.weekday() < 5 and 9 * 60 <= m_kr < 15 * 60 + 40
    earn = ny.weekday() < 5 and (6 * 60 <= m_ny < 9 * 60 + 30 or 16 * 60 <= m_ny < 19 * 60 + 30)
    return us, ko, earn


def gate(now):
    us, ko, earn = window(now)
    if not (us or ko):
        # 장 밖이라도 통합본 동기화로 바탕이 바뀌었으면 한 번만 다시 맞춤(주말에 옛 가격으로 돌아가지 않게)
        try:
            meta = json.load(open(os.path.join(R, 'd', 'meta.json'), encoding='utf-8'))
            base = dt.datetime.fromisoformat(meta['synced']).strftime('%Y%m%d%H%M')
            st = json.load(open(os.path.join(R, 'live', 'stamp.json'), encoding='utf-8'))
            if st.get('base') == base: return 'rest: 장 시간 아님'
        except Exception:
            return 'rest: 장 시간 아님'
        earn = False
    if FORCE: return None
    # 자료(d/, 통합본 동기화) 올림만 셈 — 화면 다듬기(_tools/·CSS) 커밋 때문에 시세가 멈추지 않게(사용자 2026-10-29)
    log = sh('git', 'log', '-40', '--format=%ct|%an', 'origin/main', '--', 'd/').splitlines()
    ts = [(int(x.split('|')[0]), x.split('|', 1)[1]) for x in log if '|' in x]
    t0 = now.timestamp()
    if sum(1 for t, _ in ts if t0 - t < 3600) >= 7: return 'skip: 최근 1시간 게시 7번'
    human = [t for t, a in ts if a != BOT]
    if human and t0 - human[0] < 600: return 'skip: Claude가 10분 안에 올림'
    if earn:
        mine = [t for t, a in ts if a == BOT]
        if mine and t0 - mine[0] < 14 * 60: return 'skip: 실적 시간대 15분 간격'
    return None


MKT = [('nasdaq', '^IXIC', 'pct'), ('sox', '^SOX', 'pct'), ('us10y', '^TNX', 'lvl'), ('wti', 'CL=F', 'usd')]


def market():
    # 홈 '오늘 한눈에' 숫자 4개(나스닥·반도체·10년물·WTI) — 사용자 2026-10-29 지시
    sys.path.insert(0, T); import refresh_prices as rp
    out = {}
    for k, sym, kind in MKT:
        r = rp.get('https://query1.finance.yahoo.com/v8/finance/chart/' + sym.replace('^', '%5E').replace('=', '%3D') + '?range=1d&interval=5m&includePrePost=true')
        if not r: continue
        m = r['meta']; v = m.get('regularMarketPrice'); pc = m.get('chartPreviousClose') or m.get('previousClose')
        try:
            q = r['indicators']['quote'][0]['close']; ts = r['timestamp']
            last = [(t, c) for t, c in zip(ts, q) if c is not None]
            if last: v = last[-1][1]; tt = last[-1][0]
            else: tt = m.get('regularMarketTime')
        except Exception: tt = m.get('regularMarketTime')
        if v is None: continue
        out[k] = {'v': round(v, 3), 'pc': pc, 'chg': round((v / pc - 1) * 100, 2) if pc else None, 'kind': kind, 't': tt}
    return out


# 데일리 시황 '일별 지수 등락' 3개월 차트용 지수 일별 등락(사용자 2026-10-29) — 6시간에 한 번만 받음(요청 4개)
IDX = [('^GSPC', 'spx_chg'), ('^IXIC', 'ndx_chg'), ('^SOX', 'sox_chg'), ('^DJI', 'dji_chg')]


def idx_update(L, now):
    fp = os.path.join(L, 'idx.json')
    try:
        old = json.load(open(fp, encoding='utf-8'))
        if (now - dt.datetime.fromisoformat(old['at'])).total_seconds() < 6 * 3600: return False
    except Exception: old = None
    sys.path.insert(0, T); import refresh_prices as rp
    ny = now.astimezone(ZoneInfo('America/New_York')); today = ny.strftime('%Y-%m-%d')
    closed = ny.weekday() >= 5 or ny.hour * 60 + ny.minute >= 16 * 60 + 15
    rows = {}
    for sym, key in IDX:
        r = rp.get('https://query1.finance.yahoo.com/v8/finance/chart/' + sym.replace('^', '%5E') + '?range=6mo&interval=1d')
        if not r: continue
        off = r['meta'].get('gmtoffset', -14400); ts = r.get('timestamp') or []; cl = r['indicators']['quote'][0].get('close') or []
        prev = None
        for t, c in zip(ts, cl):
            if c is None: continue
            d = rp.ldate(t, off)
            if prev and not (d == today and not closed):
                rows.setdefault(d, {'date': d})[key] = round((c / prev - 1) * 100, 2)
            prev = c
    if not rows: return False
    out = {'at': now.isoformat(timespec='seconds'), 'rows': [rows[d] for d in sorted(rows)]}
    if old and old.get('rows') == out['rows']:
        old['at'] = out['at']; out = old
    json.dump(out, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return True


# 차트에만 보이는 거시 지표(사용자 2026-10-29): 시세 보드·관심종목에는 안 올리고 종목 차트 층위로만
MACRO = [('2YY=F', '미국 2년물 금리', '미국채 금리', '%'), ('^TNX', '미국 10년물 금리', '미국채 금리', '%'), ('^TYX', '미국 30년물 금리', '미국채 금리', '%'),
         ('CL=F', 'WTI 원유', '유가', 'USD'), ('BZ=F', '브렌트유', '유가', 'USD'),
         # 레버리지·테마 ETF(2026-10-29) — 차트에만
         ('USD', '반도체 2배 레버리지(USD)', '레버리지·테마 ETF', 'USD'), ('DISK', '메모리 ETF(DISK)', '레버리지·테마 ETF', 'USD'), ('LAZR', '광학·포토닉스 ETF(LAZR)', '레버리지·테마 ETF', 'USD')]


def macro_files(W, L):
    """live/macro_*.json을 작업 폴더로 — 없으면 2년치 일별 종가로 처음 채움"""
    mp, mh = os.path.join(W, 'mprices.json'), os.path.join(W, 'mhistory.json')
    try:
        P = json.load(open(os.path.join(L, 'macro_prices.json'), encoding='utf-8')); H = json.load(open(os.path.join(L, 'macro_history.json'), encoding='utf-8'))
    except Exception:
        P, H = [], []
    have = {r['ticker'] for r in P}
    for i, (t, n, c, cur) in enumerate(MACRO):
        if t in have: continue
        P.append({'ticker': t, 'name': n, 'category': c, 'order': 900 + i, 'currency': cur})
        try:
            o = subprocess.run(['curl', '-sS', '-m', '25', '-A', 'Mozilla/5.0', 'https://query1.finance.yahoo.com/v8/finance/chart/' + urllib.parse.quote(t) + '?range=2y&interval=1d'], capture_output=True, text=True).stdout
            r = json.loads(o)['chart']['result'][0]; off = r['meta'].get('gmtoffset', 0)
            for ts, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
                if v is not None: H.append({'ticker': t, 'date': dt.datetime.fromtimestamp(ts + off, dt.timezone.utc).strftime('%Y-%m-%d'), 'close': round(float(v), 4), 'kind': 'd'})
        except Exception as e:
            print('macro seed fail', t, e)
    for r in P:  # 이름·층위는 여기 목록을 따름
        for t, n, c, cur in MACRO:
            if r['ticker'] == t: r.update(name=n, category=c, currency=cur)
    P = [r for r in P if r['ticker'] in {m[0] for m in MACRO}]
    json.dump(P, open(mp, 'w', encoding='utf-8'), ensure_ascii=False); json.dump(H, open(mh, 'w', encoding='utf-8'), ensure_ascii=False)
    return mp, mh


def long_update(L, tickers):
    """5년치 주간 종가(토스식 5년 차트용, 사용자 2026-10-29) — 하루 한 번만 받음(5분마다 받을 필요 없음)"""
    fp = os.path.join(L, 'long.json')
    try: old = json.load(open(fp, encoding='utf-8'))
    except Exception: old = {}
    now = dt.datetime.now(ZoneInfo('Asia/Seoul'))
    fresh = old.get('at') and (now - dt.datetime.fromisoformat(old['at'])).total_seconds() < 20 * 3600
    if old.get('v') != 2: old = {}  # 10년판(주간 5년 + 그 앞은 월간)으로 바뀜
    need = [t for t in tickers if t not in old.get('d', {})]
    if fresh and not need: return False
    todo = tickers if not fresh else need
    def get(t, rg, iv):
        o = subprocess.run(['curl', '-sS', '-m', '25', '-A', 'Mozilla/5.0', 'https://query1.finance.yahoo.com/v8/finance/chart/' + urllib.parse.quote(t) + '?range=' + rg + '&interval=' + iv], capture_output=True, text=True).stdout
        r = json.loads(o)['chart']['result'][0]; off = r['meta'].get('gmtoffset', 0)
        return [[dt.datetime.fromtimestamp(ts + off, dt.timezone.utc).strftime('%Y-%m-%d'), round(float(v), 4)] for ts, v in zip(r.get('timestamp') or [], r['indicators']['quote'][0]['close']) if v is not None]
    def one(t):
        try:
            wk = get(t, '5y', '1wk')
            try: mo = get(t, '10y', '1mo')
            except Exception: mo = []
            first = wk[0][0] if wk else '9999'
            return t, [x for x in mo if x[0] < first] + wk
        except Exception:
            return t, None
    import concurrent.futures as cf
    D = dict(old.get('d', {}))
    with cf.ThreadPoolExecutor(6) as ex:
        for t, v in ex.map(one, todo):
            if v: D[t] = v
    D = {t: D[t] for t in tickers if t in D}
    json.dump({'v': 2, 'at': now.isoformat(timespec='seconds'), 'd': D}, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return True


def ohlc_update(L, tickers):
    """캔들 자료(사용자 2026-10-29): 종목별 일봉 1년 + 주봉 10년 → live/ohlc/<slug>.json, 하루 한 번"""
    D = os.path.join(L, 'ohlc'); os.makedirs(D, exist_ok=True)
    ip = os.path.join(D, '_index.json')
    try: idx = json.load(open(ip, encoding='utf-8'))
    except Exception: idx = {}
    now = dt.datetime.now(ZoneInfo('Asia/Seoul'))
    fresh = idx.get('at') and (now - dt.datetime.fromisoformat(idx['at'])).total_seconds() < 20 * 3600
    slug = lambda t: re.sub(r'[^A-Za-z0-9]', '-', t)
    todo = [t for t in tickers if not fresh or not os.path.exists(os.path.join(D, slug(t) + '.json'))]
    if not todo: return False
    def get(t, rg, iv):
        o = subprocess.run(['curl', '-sS', '-m', '25', '-A', 'Mozilla/5.0', 'https://query1.finance.yahoo.com/v8/finance/chart/' + urllib.parse.quote(t) + '?range=' + rg + '&interval=' + iv], capture_output=True, text=True).stdout
        r = json.loads(o)['chart']['result'][0]; off = r['meta'].get('gmtoffset', 0); q = r['indicators']['quote'][0]
        sig = lambda v: float('%.5g' % v)
        out = []
        for i, ts in enumerate(r.get('timestamp') or []):
            o_, h_, l_, c_ = q['open'][i], q['high'][i], q['low'][i], q['close'][i]
            if None in (o_, h_, l_, c_): continue
            out.append([dt.datetime.fromtimestamp(ts + off, dt.timezone.utc).strftime('%Y-%m-%d'), sig(o_), sig(h_), sig(l_), sig(c_)])
        return out
    def one(t):
        try: return t, {'d': get(t, '1y', '1d'), 'w': get(t, '10y', '1wk')}
        except Exception: return t, None
    import concurrent.futures as cf
    n = 0
    with cf.ThreadPoolExecutor(6) as ex:
        for t, v in ex.map(one, todo):
            if v and v['d']:
                json.dump(v, open(os.path.join(D, slug(t) + '.json'), 'w', encoding='utf-8'), separators=(',', ':')); n += 1
    json.dump({'at': now.isoformat(timespec='seconds'), 'n': n}, open(ip, 'w', encoding='utf-8'))
    return n > 0


def build():
    W = os.path.join(R, '.live_tmp'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
    for f in ('prices.json', 'history.json'):
        shutil.copy(os.path.join(R, 'd', 'prices', f), os.path.join(W, f))
    os.environ['MM_INTRA'] = os.path.join(W, 'intraday.json')
    out = sh(sys.executable, '-I', os.path.join(T, 'refresh_prices.py'), 'update', os.path.join(W, 'prices.json'), os.path.join(W, 'history.json'))
    res = json.loads(out.splitlines()[-1])
    if not res.get('ok'): print('fail: 시세 받기 실패', res); return None
    L = os.path.join(R, 'live'); os.makedirs(L, exist_ok=True)
    mp = mh = None
    try:  # 거시 지표(채권 금리·유가)는 따로 받아 차트 자료에만 합침
        mp, mh = macro_files(W, L)
        os.environ['MM_INTRA'] = os.path.join(W, 'intra_m.json')
        sh(sys.executable, '-I', os.path.join(T, 'refresh_prices.py'), 'update', mp, mh)
        os.environ['MM_INTRA'] = os.path.join(W, 'intraday.json')
        try:
            I = json.load(open(os.path.join(W, 'intraday.json'), encoding='utf-8')); Im = json.load(open(os.path.join(W, 'intra_m.json'), encoding='utf-8'))
            I['d'].update(Im['d']); json.dump(I, open(os.path.join(W, 'intraday.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        except Exception as e: print('macro intra merge', e)
        ap, ah = os.path.join(W, 'all_p.json'), os.path.join(W, 'all_h.json')
        json.dump(json.load(open(os.path.join(W, 'prices.json'), encoding='utf-8')) + json.load(open(mp, encoding='utf-8')), open(ap, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump(json.load(open(os.path.join(W, 'history.json'), encoding='utf-8')) + json.load(open(mh, encoding='utf-8')), open(ah, 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception as e:
        print('macro fail', e); mp = None; ap, ah = os.path.join(W, 'prices.json'), os.path.join(W, 'history.json')
    sh(sys.executable, '-I', os.path.join(T, 'refresh_prices.py'), 'trendjson', os.path.join(W, 'trend.json'), ap, ah)
    mch = False
    if mp:
        try: mch = json.load(open(mp, encoding='utf-8')) != json.load(open(os.path.join(L, 'macro_prices.json'), encoding='utf-8'))
        except Exception: mch = True
    old = None
    try: old = json.load(open(os.path.join(L, 'prices.json'), encoding='utf-8'))
    except Exception: pass
    new = json.load(open(os.path.join(W, 'prices.json'), encoding='utf-8'))
    try: meta = json.load(open(os.path.join(R, 'd', 'meta.json'), encoding='utf-8'))
    except Exception: meta = {}
    base = dt.datetime.fromisoformat(meta['synced']).strftime('%Y%m%d%H%M') if meta.get('synced') else ''
    oldst = {}
    try: oldst = json.load(open(os.path.join(L, 'stamp.json'), encoding='utf-8'))
    except Exception: pass
    try: idxch = idx_update(L, dt.datetime.now(ZoneInfo('Asia/Seoul')))
    except Exception as e: idxch = False; print('idx fail', e)
    lch = False
    try: lch = long_update(L, [r['ticker'] for r in json.load(open(ap, encoding='utf-8'))])
    except Exception as e: print('long fail', e)
    try: lch = ohlc_update(L, [r['ticker'] for r in json.load(open(ap, encoding='utf-8'))]) or lch
    except Exception as e: print('ohlc fail', e)
    if old == new and oldst.get('base') == base and not idxch and not mch and not lch:
        print('same: 시세 변화 없음', res); shutil.rmtree(W, ignore_errors=True); return None
    now = dt.datetime.now(ZoneInfo('Asia/Seoul'))
    tr = json.load(open(os.path.join(W, 'trend.json'), encoding='utf-8')); tr['at'] = now.isoformat(timespec='seconds')
    json.dump(tr, open(os.path.join(L, 'trend.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    for f in ('prices.json', 'history.json'):
        shutil.copy(os.path.join(W, f), os.path.join(L, f))
    if mp:
        shutil.copy(mp, os.path.join(L, 'macro_prices.json')); shutil.copy(mh, os.path.join(L, 'macro_history.json'))
    if os.path.exists(os.path.join(W, 'intraday.json')): shutil.copy(os.path.join(W, 'intraday.json'), os.path.join(L, 'intraday.json'))
    kinds = res.get('kinds', {})
    st = {'at': now.isoformat(timespec='seconds'), 'key': now.strftime('%Y%m%d%H%M'), 'label': now.strftime('%m.%d %H:%M') + ' 기준(5분 갱신)',
          'base': base, 'files': ['prices', 'history'], 'ok': res.get('ok'), 'fail': res.get('fail', []), 'kinds': kinds}
    json.dump(st, open(os.path.join(L, 'stamp.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    mk = market()
    if mk: json.dump({'at': st['at'], 'label': now.strftime('%H:%M'), 'items': mk}, open(os.path.join(L, 'market.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    shutil.rmtree(W, ignore_errors=True)
    return st


def main():
    now = dt.datetime.now(dt.timezone.utc)
    g = gate(now)
    if g: print(g); return
    for k in range(4):
        st = build()
        if not st: return
        sh('git', 'add', 'live')
        if not sh('git', 'status', '--porcelain', 'live'): print('same'); return
        sh('git', '-c', f'user.name={BOT}', '-c', 'user.email=mung-bot@users.noreply.github.com', 'commit', '-q', '-m', '시세 5분 갱신 ' + st['label'])
        if subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:main'], cwd=R).returncode == 0:
            print('pushed', st['label'], st['kinds']); return
        # 충돌: 최신본 받고 다시 계산
        sh('git', 'fetch', '-q', 'origin', 'main'); sh('git', 'reset', '-q', '--hard', 'origin/main')
        g = gate(dt.datetime.now(dt.timezone.utc))
        if g: print('retry stop:', g); return
    print('push failed 4x')


if __name__ == '__main__':
    main()
