# 매일 점검(사용자 2026-11-01) — GitHub 서버에서 무료로 측정만 함. 결과는 'health' 가지에 올리고 사이트 본문(main)에는 안 섞음.
# 재는 것: ① 페이지 오류·가로 넘침·무게·통째 부품 수  ② 자료별 마지막 갱신 시각과 늦음 여부  ③ 봇 게시 간격(헛걸음)  ④ 공용 부품 참조 누락
# Claude는 아침에 health.json 한 장만 읽고 이 대화에 요약을 올림(크레딧 최소).
import os, sys, re, json, glob, subprocess, datetime as dt, asyncio, http.server, threading, functools
from zoneinfo import ZoneInfo

R = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(R, '_health')
os.makedirs(OUT, exist_ok=True)
KST = ZoneInfo('Asia/Seoul'); NY = ZoneInfo('America/New_York')
now = dt.datetime.now(dt.timezone.utc)

def git(*a):
    return subprocess.run(['git', *a], cwd=R, capture_output=True, text=True).stdout.strip()

# ② 자료 신선도 — 허용 시간(시간 단위). 주말·휴장 때 늦는 건 '쉬는 날'로 따로 표시
FRESH = [
    ('시세(5분)', 'live/stamp.json', 2, True),
    ('시장 경고등', 'd/lights', 30, True),
    ('옵션 온도계', 'd/opt', 30, True),
    ('주요 뉴스', 'd/policy', 30, False),
    ('AI·테크 뉴스', 'd/tech', 36, False),
    ('유튜브 영상', 'd/yt.json', 9999, False),
    ('공포·탐욕', 'd/fng.json', 30, True),
    ('금융 스트레스', 'd/stress', 30, True),
    ('시황 브리핑', 'd/brief', 30, True),
    ('목표주가', 'd/targets', 26, False),
    ('실적 노트', 'd/notes.json', 72, True),
    ('공매도', 'd/short', 72, True),
    ('경제지표', 'd/econ', 72, False),
    ('아이디어(저평가·고수)', 'd/ideas', 30, True),
    ('IR 서재', 'd/ir', 96, False),
]
ny = now.astimezone(NY)
weekend = ny.weekday() >= 5 or (ny.weekday() == 0 and ny.hour < 4)
fresh = []
for name, path, lim, mkt in FRESH:
    ts = git('log', '-1', '--format=%ct', 'origin/main', '--', path) or git('log', '-1', '--format=%ct', '--', path)
    if not ts:
        fresh.append({'name': name, 'path': path, 'state': 'none'}); continue
    age = (now.timestamp() - int(ts)) / 3600
    lim2 = lim + (60 if (mkt and weekend) else 0)
    st = 'ok' if age <= lim2 else 'late'
    fresh.append({'name': name, 'path': path, 'age_h': round(age, 1), 'limit_h': lim2, 'state': st,
                  'last': dt.datetime.fromtimestamp(int(ts), KST).strftime('%m.%d %H:%M')})

# ③ 봇 게시 간격(최근 24시간)
log = git('log', '--since=24 hours ago', '--format=%ct|%an', 'origin/main') or git('log', '--since=24 hours ago', '--format=%ct|%an')
rows = [x.split('|', 1) for x in log.splitlines() if '|' in x]
by = {}
for t, a in rows: by.setdefault(a, []).append(int(t))
bot = sorted(by.get('mung-bot', []))
gaps = [b - a for a, b in zip(bot, bot[1:])]
posts = {'total_24h': len(rows), 'by_author': {k: len(v) for k, v in by.items()},
         'bot_under_5min': sum(1 for g in gaps if g < 300)}
hours = {}
for t, _ in rows:
    h = dt.datetime.fromtimestamp(int(t), dt.timezone.utc).strftime('%Y%m%d%H'); hours[h] = hours.get(h, 0) + 1
posts['busiest_hour_posts'] = max(hours.values()) if hours else 0
posts['hours_over_10'] = sum(1 for v in hours.values() if v > 10)

# ⑤ 되돌림 감지(2026-11-01) — 복사본에 '화면 정리 다시 입히기'를 돌려 바뀌는 페이지가 있으면, 누군가 옛 코드로 페이지를 덮어쓴 것
import shutil, tempfile
drift = []
try:
    tmp = tempfile.mkdtemp(); cp = os.path.join(tmp, 'site')
    shutil.copytree(R, cp, ignore=shutil.ignore_patterns('.git', '_health', 'node_modules'))
    subprocess.run([sys.executable, '-I', os.path.join(cp, '_tools', 'reapply_tidy.py'), cp], capture_output=True, timeout=300)
    for f in sorted(glob.glob(os.path.join(R, '*.html'))):
        a = open(f, encoding='utf-8').read(); b = open(os.path.join(cp, os.path.basename(f)), encoding='utf-8').read()
        if a != b: drift.append(os.path.basename(f))
    shutil.rmtree(tmp, ignore_errors=True)
except Exception as e:
    drift = ['검사 실패: ' + str(e)[:80]]

# ⑥ 사이트 내보내기 막힘(2026-11-01) — 실제 사이트의 판 번호가 저장소보다 30분 넘게 뒤처져 있으면 알림(11.01 17:13~18:2x 내보내기가 멈춰 있었음)
live_lag = None
try:
    import urllib.request
    repo_v = json.load(open(os.path.join(R, 'version.json'), encoding='utf-8')).get('v')
    with urllib.request.urlopen('https://mung-mungi.github.io/mung-mung-market/version.json?t=' + str(int(now.timestamp())), timeout=20) as r:
        site_v = json.loads(r.read().decode()).get('v')
    vt = git('log', '-1', '--format=%ct', '--', 'version.json')
    if site_v != repo_v and vt and now.timestamp() - int(vt) > 1800:
        live_lag = {'site': site_v, 'repo': repo_v}
except Exception as e:
    live_lag = None

# ⑦ 기능 되돌림 감지(2026-11-01) — 다른 세션이 옛 복사본으로 공용 부품을 덮어쓰면 오늘 넣은 기능이 조용히 사라짐(19:16 navfab.js 사례). 꼭 있어야 할 표시를 확인
try: MUST = {k: v for k, v in json.load(open(os.path.join(R, '_tools', 'guard.json'), encoding='utf-8')).items() if '/' in k}
except Exception: MUST = {}
lost = []
for f, keys in MUST.items():
    try: t = open(os.path.join(R, f), encoding='utf-8').read()
    except Exception: lost.append(f + ' 없음'); continue
    lost += [f'{os.path.basename(f)}: {k}' for k in keys if k not in t]

# ① 페이지 — 무게·통째 부품·공용 참조
CORE = ['perf', 'hshome', 'wrapfix', 'splash', 'vt', 'tick']
pages = {}
for f in sorted(glob.glob(os.path.join(R, '*.html'))):
    s = open(f, encoding='utf-8').read(); n = os.path.basename(f)
    miss = [m for m in CORE if not re.search(r'<(?:script|link) data-%s (?:src|rel)=' % m, s)]
    if n == 'index.html': miss = [m for m in miss if m != 'perf']  # 메인은 버벅임 부품이 아직 통째(정리 마지막 순서)
    pages[n] = {'kb': round(len(s.encode()) / 1024), 'inline': len(re.findall(r'<(?:script|style)(?![^>]*\bsrc=)[^>]*>', s)),
                'missing_core': miss, 'doctype_first': s.lstrip().lower().startswith('<!doctype')}

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), functools.partial(Q, directory=R))
threading.Thread(target=srv.serve_forever, daemon=True).start()

async def run_pages():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        await ctx.add_init_script("try{sessionStorage.setItem('mmSplash','1')}catch(e){};window.__NMO=window.MutationObserver;")
        for n in pages:
            pg = await ctx.new_page(); errs = []; bad = []
            pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)[:120]))
            pg.on('response', lambda r, bad=bad: (r.status >= 400 and '127.0.0.1' in r.url) and bad.append(f'{r.status} {r.url[22:100]}'))
            try:
                await pg.goto(f'http://127.0.0.1:8765/{n}', wait_until='load', timeout=30000); await pg.wait_for_timeout(2000)
                m = await pg.evaluate('({sw:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight,n:document.getElementsByTagName("*").length})')
                # ⑧ 쉬는 동안 일하는 페이지(2026-11-02) — 다 뜬 뒤(9초) 가만히 둔 3초 동안 화면이 바뀐 횟수. 부품끼리 서로 깨우는 반복 고리를 잡음
                #    (11.01 주요 뉴스가 1초에 50번 넘게 'n건'을 다시 써서 폰이 쉬지 못했음)
                await pg.wait_for_timeout(7000)
                churn = await pg.evaluate('''new Promise(function(res){var o={},n=0;function d(e){return !e||!e.tagName?(e&&e.nodeName):e.tagName+(e.id?'#'+e.id:'')+(typeof e.className=='string'&&e.className?'.'+e.className.trim().split(/\\s+/)[0]:'')}
                  var mo=new window.__NMO(function(ms){ms.forEach(function(m){n++;var k=m.type+' @'+d(m.target);o[k]=(o[k]||0)+1})});
                  mo.observe(document.documentElement,{subtree:true,childList:true,attributes:true,characterData:true});
                  setTimeout(function(){mo.disconnect();var top=Object.keys(o).sort(function(a,b){return o[b]-o[a]}).slice(0,2).map(function(k){return k+' '+o[k]+'번'});res({n:n,top:top})},3000)})''')
                m['churn'] = churn
            except Exception as e:
                errs.append('LOAD ' + str(e)[:80]); m = {}
            pages[n].update({'idle_changes': (m.get('churn') or {}).get('n'), 'idle_top': (m.get('churn') or {}).get('top'),
                             'errors': errs[:5], 'missing_files': bad[:5], 'overflow': (m.get('sw') or 390) > 392,
                             'height': m.get('h'), 'elements': m.get('n')})
            await pg.close()
        await b.close()
asyncio.run(run_pages())

prev = {}
try: prev = json.load(open(os.path.join(OUT, 'health.json'), encoding='utf-8'))
except Exception: pass

problems = []
for n, p in pages.items():
    if p.get('errors'): problems.append(f'{n}: 페이지 오류 {len(p["errors"])}건')
    if p.get('missing_files'): problems.append(f'{n}: 없는 파일 {len(p["missing_files"])}개')
    if p.get('overflow'): problems.append(f'{n}: 가로 넘침')
    if (p.get('idle_changes') or 0) > 5: problems.append(f"{n}: 쉬는 동안 화면이 계속 바뀜 3초에 {p['idle_changes']}번(버벅임·배터리) — {', '.join(p.get('idle_top') or [])}")
    if p['missing_core']: problems.append(f'{n}: 공용 부품 참조 빠짐 {p["missing_core"]}')
    if not p['doctype_first']: problems.append(f'{n}: 문서 선언이 맨 앞이 아님')
for x in fresh:
    if x['state'] == 'late': problems.append(f'{x["name"]}: {x["age_h"]}시간 갱신 없음(마지막 {x["last"]})')
if drift: problems.append(f'옛 코드로 덮인 페이지 {len(drift)}개(정리 다시 입히면 바뀜): ' + ', '.join(drift[:6]))
if live_lag: problems.append(f"실제 사이트가 옛 판({live_lag['site']})에 멈춰 있음 — 저장소는 {live_lag['repo']}, 사이트 내보내기 막힘 확인 필요")
if lost: problems.append('옛 복사본으로 덮여 사라진 기능 표시: ' + ', '.join(lost))
if posts['bot_under_5min']: problems.append(f'시세 게시 5분 안 연속 {posts["bot_under_5min"]}번')
if posts['hours_over_10']: problems.append(f'시간당 게시 10번 넘은 시간 {posts["hours_over_10"]}개(사이트 빌드 한도)')

res = {'at': now.astimezone(KST).strftime('%Y-%m-%d %H:%M'), 'weekend': weekend, 'problems': problems,
       'total_kb': sum(p['kb'] for p in pages.values()), 'total_inline': sum(p['inline'] for p in pages.values()),
       'prev_total_kb': prev.get('total_kb'), 'prev_total_inline': prev.get('total_inline'),
       'heaviest': sorted(((p['kb'], n) for n, p in pages.items()), reverse=True)[:3],
       'fresh': fresh, 'posts': posts, 'drift': drift, 'lost': lost, 'live_lag': live_lag, 'pages': pages}
json.dump(res, open(os.path.join(OUT, 'health.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
hist = os.path.join(OUT, 'history.jsonl')
with open(hist, 'a', encoding='utf-8') as h:
    h.write(json.dumps({'at': res['at'], 'kb': res['total_kb'], 'inline': res['total_inline'], 'problems': len(problems)}, ensure_ascii=False) + '\n')
print(json.dumps({'at': res['at'], 'problems': problems, 'total_kb': res['total_kb']}, ensure_ascii=False, indent=1))
srv.shutdown()
