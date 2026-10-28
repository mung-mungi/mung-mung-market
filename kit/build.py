# 통합본 페이지 빌더. 사용법: python3 build.py <작업폴더>
# 작업폴더 구조:
#   kit/  (이 파일, tokens.css, barcss.css, dbshim.js, shim.js, home.html, conf.json)
#   src/<page>.html   대시보드형 원본의 files/index.html 'text' (13개)
#   src/cal.html      실적 캘린더 원본 페이지 전체(Artifact read path 'index.html')
#   src/earn.html     실적 결과 원본 페이지 전체(Artifact read path 'index.html')
#   src/trend.html    종목 추세 보기 원본 페이지 전체(Artifact read path 'index.html')
#   out/d/meta.json   {"synced", "label"}
# 결과: out/index.html, out/p-<page>.html, out/shim.js
import json, os, re, sys, shutil
W = sys.argv[1].rstrip('/') + '/'
K = W + 'kit/'
C = json.load(open(K + 'conf.json'))
meta = json.load(open(W + 'out/d/meta.json'))
SYNC = re.sub(r'\D', '', meta.get('synced', ''))[:12]
TOKENS = open(K + 'tokens.css').read()
BARCSS = open(K + 'barcss.css').read()

def bar(cur):
    out = '<nav class="ib" aria-label="통합본 페이지"><a class="home" href="index.html">⌂ 홈</a>'
    for g, items in C['groups']:
        out += f'<span class="tg">{g}</span>'
        for v, l in items:
            out += f'<a href="p-{v}.html"' + (' aria-current="page"' if v == cur else '') + f'>{l}</a>'
    return out + '</nav><script>(function(){var c=document.querySelector(".ib a[aria-current]");if(c)c.scrollIntoView({block:"nearest",inline:"center"});})();</script>'

def dash_page(pg):
    body = open(W + f'src/{pg}.html').read()
    cfg = {'page': pg, 'ds': C['datasets'][pg], 'params': C['params'].get(pg, {})}
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{C["titles"][pg]}</title><style>{TOKENS}</style>'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>'
            f'<script>window.__PAGE__={json.dumps(cfg, ensure_ascii=False)};window.__SYNC__="{SYNC}";</script><script src="shim.js"></script></head>'
            f'<body class="ibody">{bar(pg)}<div id="dash-root" data-dash-state="loading">{body}</div></body></html>')

def hand_page(pg, inject=''):
    h = open(W + f'src/{pg}.html').read()
    h = h.replace('</head>', '<style>' + BARCSS + '</style>' + inject + '</head>', 1)
    h = h.replace('<head>', '<head><script>document.documentElement.setAttribute("data-theme","light")</script>', 1)  # 주간 모드 고정
    return re.sub(r'<body([^>]*)>', lambda m: m.group(0) + bar(pg), h, count=1)

for g, items in C['groups']:
    for v, _ in items:
        if v in ('cal', 'trend'):
            txt = hand_page(v)
        elif v == 'earn':
            txt = hand_page(v, '<script>window.__SYNC__="' + SYNC + '";' + open(K + 'dbshim.js').read() + '</script>')
            # 통합본에는 DB 권한이 없어 플랫폼의 claude.use('db')가 null을 줍니다 → 통합본 안에서는 파일(d/notes.json)을 읽는 가짜 DB를 쓰게 바꿉니다
            txt = txt.replace("await claude.use('db')", "await (window.__fakeDB||claude).use('db')")
        else:
            txt = dash_page(v)
        open(W + f'out/p-{v}.html', 'w').write(txt)
shutil.copy(K + 'shim.js', W + 'out/shim.js')
shutil.copy(K + 'home.html', W + 'out/index.html')
print('built', SYNC)
