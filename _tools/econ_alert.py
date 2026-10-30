# 주요 경제지표 발표 알림(사용자 2026-10-30) — 별 3개 + 졸트 + 시간당 임금(고용과 같이)
# 발표 1시간 전쯤 깨어나 기다렸다가 발표 1분 뒤 공식 숫자(노동통계국·연준, 안 되면 FRED)를 읽어 원시그널 알림 한 번.
# 같은 시각 지표는 한 알림으로 묶음. 숫자는 경제지표 일정(d/econ/calendar.json)의 '실제' 칸에도 채움. 보낸 것은 d/econ/alert_state.json
# Claude 크레딧 없음(GitHub 자동 작업 econ-alert). 사용: python3 -I _tools/econ_alert.py <사이트 폴더>
#   DRY=1      알림은 안 보내고 무엇을 보낼지만 출력(시험용)
#   ONLY=<id>  그 묶음(지표 id 하나)만 시간과 상관없이 바로 처리(시험용, DRY와 같이)
import json, os, sys, re, time, urllib.request, datetime as dt
from zoneinfo import ZoneInfo

R = sys.argv[1] if len(sys.argv) > 1 else '.'
CAL = os.path.join(R, 'd/econ/calendar.json')
SP = os.path.join(R, 'd/econ/alert_state.json')
APP = os.environ.get('ONESIGNAL_APP_ID', '').strip() or 'b81f8268-5aef-4a29-b2b8-2173248136a3'
KEY = os.environ.get('ONESIGNAL_API_KEY', '').strip()
DRY = os.environ.get('DRY', '').strip() == '1'
ONLY = os.environ.get('ONLY', '').strip()
SITE = 'https://mung-mungi.github.io/mung-mung-market/'
NY = ZoneInfo('America/New_York')
UA = {'User-Agent': 'Mozilla/5.0 (mung-terminal econ alert; contact mung-mungi@users.noreply.github.com)'}
AHEAD_MIN, LATE_MIN, POLL_MIN = 75, 120, 15   # 몇 분 앞까지 기다리나 / 몇 분 늦어도 보내나 / 숫자 기다리는 최대 시간


def want(x):
    i = x.get('id', '')
    return x.get('stars') == 3 or i.startswith('jolts-') or i.startswith('ahe-')


def when_utc(x):
    t = dt.datetime.strptime(x['date_et'] + ' ' + x['time_et'], '%Y-%m-%d %H:%M').replace(tzinfo=NY)
    return t.astimezone(dt.timezone.utc)


def get(url, data=None, timeout=20):
    h = dict(UA)
    if data is not None:
        h['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=h)
    return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', 'replace')


# ── 지표별 계산 방법: (노동통계국 시리즈, FRED 시리즈, 계산) ──────────────────────────
# 계산: 'level' 최신값 / 'diff' 전월 대비 증감 / 'yoy' 12개월 전 대비 % / 'jolts' 천→백만
SPEC = {
    'cpi': ('CUUR0000SA0', 'CPIAUCNS', 'yoy'),
    'core-cpi': ('CUUR0000SA0L1E', 'CPILFENS', 'yoy'),
    'nfp': ('CES0000000001', 'PAYEMS', 'diff'),
    'ur': ('LNS14000000', 'UNRATE', 'level'),
    'ahe': ('CES0500000003', 'CES0500000003', 'yoy'),
    'jolts': ('JTS000000000000000JOL', 'JTSJOL', 'jolts'),
    'gdp': (None, 'A191RL1Q225SBEA', 'level'),
    'core-pce': (None, 'PCEPILFE', 'yoy'),
}
MON = {'1월': 1, '2월': 2, '3월': 3, '4월': 4, '5월': 5, '6월': 6, '7월': 7, '8월': 8, '9월': 9, '10월': 10, '11월': 11, '12월': 12}


def kind(x):
    i = x['id']
    for k in sorted(SPEC, key=len, reverse=True):
        if i.startswith(k + '-'):
            return k
    return 'fomc' if i.startswith('fomc-2') else ('fomc-pc' if i.startswith('fomc-pc') else None)


def target_period(x):
    # 이 발표가 다루는 달(또는 분기 끝 달) — 옛 숫자를 새 숫자로 착각하지 않게
    p = x.get('period', '')
    m = re.search(r'(\d{4})년\s*(\d+)분기', p)
    if m:
        return int(m.group(1)), int(m.group(2)) * 3 - 2   # FRED 분기 자료는 분기 첫 달 날짜
    m = re.search(r'(\d{4})년\s*(\d+)월', p)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def series_bls(sid):
    y = dt.date.today().year
    j = json.loads(get('https://api.bls.gov/publicAPI/v2/timeseries/data/', {'seriesid': [sid], 'startyear': str(y - 2), 'endyear': str(y)}))
    out = {}
    for d in (j.get('Results', {}).get('series') or [{}])[0].get('data', []):
        if not re.match(r'M\d\d$', d.get('period', '')) or d['period'] == 'M13':
            continue
        try:
            out[(int(d['year']), int(d['period'][1:]))] = float(d['value'])
        except Exception:
            pass
    return out


def series_fred(sid):
    t = get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + sid)
    out = {}
    for line in t.splitlines()[1:]:
        a = line.split(',')
        try:
            y, m, _ = a[0].split('-'); out[(int(y), int(m))] = float(a[1])
        except Exception:
            pass
    return out


def calc(k, s, tp):
    if tp not in s:
        return None
    y, m = tp
    if k in ('cpi', 'core-cpi', 'ahe', 'core-pce'):
        prev = s.get((y - 1, m))
        return round((s[tp] / prev - 1) * 100, 1) if prev else None
    if k == 'nfp':
        pm = (y, m - 1) if m > 1 else (y - 1, 12)
        return round(s[tp] - s[pm]) if pm in s else None
    if k == 'jolts':
        return round(s[tp] / 1000, 3)
    return round(s[tp], 1)


def value(x):
    k = kind(x); tp = target_period(x)
    if k not in SPEC or not tp:
        return None
    bls, fred, _ = SPEC[k]
    for src, sid in (('bls', bls), ('fred', fred)):
        if not sid:
            continue
        try:
            s = series_bls(sid) if src == 'bls' else series_fred(sid)
            v = calc(k, s, tp)
            if v is not None:
                return v, src
        except Exception as e:
            print('  읽기 실패', src, sid, str(e)[:120])
    return None


def fomc(x):
    d = x['date_et'].replace('-', '')
    t = get('https://www.federalreserve.gov/newsevents/pressreleases/monetary%sa.htm' % d)
    t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'\s+', ' ', t)
    m = re.search(r'target range for the federal funds rate (?:at|to) ([\d\-/ ]+?) to ([\d\-/ ]+?) percent', t)
    if not m:
        return None
    def num(s):
        s = s.strip(); w, _, f = s.partition('-')
        if '/' in f:
            a, b = f.split('/'); return float(w) + float(a) / float(b)
        return float(w)
    lo, hi = num(m.group(1)), num(m.group(2))
    dis = len(re.findall(r'[Vv]oting against', t)) > 0
    return (lo, hi, dis)


# ── 글자 만들기 ─────────────────────────────────────────────────────────
def fmt(x, v):
    u = x.get('unit') or ''
    if u == '천 명':
        return ('%+.1f만 명' % (v / 10)).replace('+-', '-')
    if u == '백만 건':
        return '%d만 건' % round(v * 100)
    if u.startswith('%'):
        return '%.1f%%' % v
    return '%s' % v


def cmp(x, v):
    c = x.get('consensus')
    if c is None:
        p = x.get('previous')
        return ' (직전 %s)' % fmt(x, p) if p is not None else ''
    sign = '▲ 예상 상회' if v > c + 1e-9 else ('▼ 예상 하회' if v < c - 1e-9 else '＝ 예상 부합')
    return ' (예상 %s) %s' % (fmt(x, c), sign)


SHORT = {'cpi': '소비자물가(CPI) 전년비', 'core-cpi': '근원 CPI 전년비', 'nfp': '비농업 고용', 'ur': '실업률', 'ahe': '시간당 임금 전년비',
         'jolts': '졸트 구인 건수', 'gdp': 'GDP 속보치(연율)', 'core-pce': '근원 PCE 전년비'}
ORDER = ['nfp', 'ur', 'ahe', 'cpi', 'core-cpi', 'gdp', 'core-pce', 'jolts']


def build(group):
    lines, got, miss = [], {}, []
    group = sorted(group, key=lambda x: ORDER.index(kind(x)) if kind(x) in ORDER else 9)
    for x in group:
        k = kind(x)
        if k == 'fomc-pc':
            got[x['id']] = ('start', None); continue
        if k == 'fomc':
            try:
                r = fomc(x)
            except Exception as e:
                r = None; print('  연준 읽기 실패', str(e)[:120])
            if not r:
                miss.append(x); continue
            lo, hi, dis = r; prev = x.get('previous')
            act = '동결' if prev is None or abs(hi - prev) < 1e-9 else ('인상' if hi > prev else '인하')
            lines.append('금리 %s · %.2f~%.2f%%%s' % (act, lo, hi, ' · 반대표 있음' if dis else ''))
            got[x['id']] = ('val', hi); continue
        r = value(x)
        if r is None:
            miss.append(x); continue
        v, src = r
        lines.append('%s %s%s' % (SHORT.get(k, x['event']), fmt(x, v), cmp(x, v)))
        got[x['id']] = ('val', v)
    return lines, got, miss


def title(group):
    ks = {kind(x) for x in group}
    p = group[0].get('period', '')
    m = re.search(r'(\d+)월', p); mm = (m.group(1) + '월 ') if m else ''
    if 'fomc' in ks:
        return '🏦 FOMC 금리 결정'
    if ks == {'fomc-pc'}:
        return '🎤 연준 의장 기자회견 시작'
    if 'nfp' in ks or 'ur' in ks:
        return '🔔 %s고용 보고서' % mm
    if 'cpi' in ks or 'core-cpi' in ks:
        return '🔔 %s소비자물가' % mm
    if 'gdp' in ks:
        return '🔔 GDP·PCE 발표' if 'core-pce' in ks else '🔔 GDP 발표'
    if 'core-pce' in ks:
        return '🔔 %sPCE 물가' % mm
    if 'jolts' in ks:
        return '🔔 %s졸트(구인)' % mm
    return '🔔 경제지표 발표'


def push(head, body):
    if DRY:
        print('[DRY] 알림 →', head, '|', body.replace('\n', ' / ')); return True
    if not KEY:
        print('원시그널 키 없음 — 건너뜀'); return False
    req = urllib.request.Request('https://api.onesignal.com/notifications', method='POST',
        headers={'Content-Type': 'application/json', 'Authorization': 'Key ' + KEY},
        data=json.dumps({'app_id': APP, 'included_segments': ['Total Subscriptions'], 'target_channel': 'push',
                         'headings': {'en': head, 'ko': head}, 'contents': {'en': body, 'ko': body}, 'url': SITE + 'p-econ.html'}).encode())
    try:
        r = json.load(urllib.request.urlopen(req, timeout=20)); print('알림 보냄', head, r.get('id'), r.get('errors')); return True
    except Exception as e:
        print('알림 실패', e); return False


def main():
    cal = json.load(open(CAL, encoding='utf-8'))
    try:
        st = json.load(open(SP, encoding='utf-8'))
    except Exception:
        st = {'sent': []}
    sent = set(st.get('sent', []))
    now = dt.datetime.now(dt.timezone.utc)
    groups = {}
    for x in cal:
        if not want(x) or x['id'] in sent or kind(x) is None:
            continue
        if ONLY and x['id'] != ONLY and not any(y['id'] == ONLY and y['date_et'] == x['date_et'] and y['time_et'] == x['time_et'] for y in cal):
            continue
        t = when_utc(x)
        if not ONLY and not (-LATE_MIN <= (t - now).total_seconds() / 60 <= AHEAD_MIN):
            continue
        groups.setdefault(t, []).append(x)
    if not groups:
        print('가까운 발표 없음'); return
    changed = False
    for t in sorted(groups):
        g = groups[t]
        wait = (t + dt.timedelta(seconds=60) - dt.datetime.now(dt.timezone.utc)).total_seconds()
        if wait > 0 and not ONLY:
            print('기다림 %.0f초 →' % wait, [x['id'] for x in g]); time.sleep(wait)
        if {kind(x) for x in g} == {'fomc-pc'}:
            lines, got, miss = [], {g[0]['id']: ('start', None)}, []
        else:
            end = time.time() + POLL_MIN * 60
            while True:
                lines, got, miss = build(g)
                if not miss or time.time() > end:
                    break
                print('  아직 안 나온 숫자', [x['id'] for x in miss], '— 20초 뒤 다시'); time.sleep(20)
        late = (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 60
        if lines or got:
            body = '\n'.join(lines) if lines else ('지금 시작합니다 · 실시간 해석은 경제지표 페이지에서' if 'fomc-pc' in {kind(x) for x in g} else '')
            if miss:
                body += ('\n' if body else '') + '나머지(%s)는 확인되는 대로 페이지에 반영합니다' % ', '.join(SHORT.get(kind(x), x['event']) for x in miss)
            if late > 20:
                body += '\n(발표 %d분 뒤 확인)' % late
            if push(title(g), body):
                ids = [x['id'] for x in g] if not miss else list(got)
                sent |= set(ids)
                for x in cal:
                    if x['id'] in got and got[x['id']][0] == 'val' and x.get('actual') is None:
                        x['actual'] = got[x['id']][1]; x['status'] = '발표'; changed = True
        else:
            print('숫자를 못 읽음 — 다음 실행에서 다시', [x['id'] for x in g])
    if not DRY:
        st['sent'] = sorted(sent)[-400:]; st['last'] = now.isoformat(timespec='minutes')
        json.dump(st, open(SP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if changed:
            json.dump(cal, open(CAL, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


main()
