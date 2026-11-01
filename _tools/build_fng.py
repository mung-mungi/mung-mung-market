# 공포·탐욕 지수·VIX 공식값 자동 갱신(사용자 2026-11-01)
# 시황 브리핑이 기사에서 옮겨 적던 공포·탐욕 지수가 하루~이틀 밀리는 일이 있어(10/30 금요일 26인데 화면은 수요일 36),
# CNN 원본 데이터를 직접 받아 d/fng.json에 씀. VIX도 CBOE 공식 종가(전날 대비)를 함께 씀.
# 화면(p-brief)의 공포·탐욕 칸과 VIX 칸은 이 파일이 더 최신이면 이 값을 씀. 못 받으면 직전 값 유지.
# 사용: python3 -I _tools/build_fng.py <사이트 폴더>
import csv, io, json, os, subprocess, sys, datetime as dt, zoneinfo
R = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = os.path.join(R, 'd/fng.json')
NY = zoneinfo.ZoneInfo('America/New_York')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/124.0 Safari/537.36')


def get(u, extra=()):
    cmd = ['curl', '-sSL', '-m', '25', '-A', UA, '-H', 'Accept: application/json, text/plain, */*']
    for h in extra:
        cmd += ['-H', h]
    o = subprocess.run(cmd + [u], capture_output=True, text=True)
    if o.returncode or not o.stdout:
        raise RuntimeError('fail ' + u[:70])
    return o.stdout


try:
    old = json.load(open(OUT, encoding='utf-8'))
except Exception:
    old = {}
out = dict(old)

# ① CNN 공포·탐욕 지수(원본 그래프 데이터)
try:
    j = json.loads(get('https://production.dataviz.cnn.io/index/fearandgreed/graphdata/',
                       ['Referer: https://edition.cnn.com/', 'Origin: https://edition.cnn.com']))
    fg = j['fear_and_greed']
    ts = dt.datetime.fromisoformat(str(fg['timestamp']).replace('Z', '+00:00')).astimezone(NY)
    # 지난 거래일별 마감 값(그래프 데이터) — 최근 10개만
    hist = []
    for p in (j.get('fear_and_greed_historical') or {}).get('data', [])[-12:]:
        d = dt.datetime.fromtimestamp(p['x'] / 1000, dt.timezone.utc).date().isoformat()  # 그래프 점은 UTC 자정 기준
        hist = [h for h in hist if h['date'] != d] + [{'date': d, 'score': round(float(p['y']), 1)}]
    # 장이 닫힌 주말·새벽에 받으면 timestamp가 마지막 거래일 마감 시각이 됨
    out['fng'] = {
        'score': round(float(fg['score']), 1),
        'rating': fg.get('rating'),
        'date': ts.date().isoformat(),
        'asof': ts.strftime('%Y-%m-%d %H:%M ET'),
        'prev_close': round(float(fg['previous_close']), 1) if fg.get('previous_close') is not None else None,
        'prev_week': round(float(fg['previous_1_week']), 1) if fg.get('previous_1_week') is not None else None,
        'prev_month': round(float(fg['previous_1_month']), 1) if fg.get('previous_1_month') is not None else None,
        'hist': hist,
        'src': 'https://edition.cnn.com/markets/fear-and-greed',
    }
    print('CNN 공포·탐욕', out['fng']['score'], out['fng']['date'])
except Exception as e:
    print('CNN 실패', e)

# ② CBOE VIX 공식 종가(전날 대비)
try:
    t = get('https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv')
    rows = [r for r in csv.DictReader(io.StringIO(t)) if r.get('CLOSE')]
    def iso(md):
        m, d, y = md.split('/')
        return '%s-%s-%s' % (y, m.zfill(2), d.zfill(2))
    a, b = rows[-1], rows[-2]
    c, p = float(a['CLOSE']), float(b['CLOSE'])
    out['vix'] = {'date': iso(a['DATE']), 'close': round(c, 2), 'prev': round(p, 2),
                  'chg': round((c / p - 1) * 100, 2), 'src': 'https://www.cboe.com/tradable_products/vix/'}
    print('VIX', out['vix'])
except Exception as e:
    print('VIX 실패', e)

if out != old:
    out['updated'] = dt.datetime.now(zoneinfo.ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('written')
else:
    print('no change')
