# 사이트 전용 실시간 장치 넣기 — prep_site.py가 부르고, 혼자 돌려도 됨: python3 -I site_live.py <사이트 폴더>
# ① shim.js: 시세 보드(prices)는 GitHub Actions 5분 갱신이 만든 live/ 파일이 같은 바탕(통합본 동기화 시각)이면 그걸 먼저 씀
# ② p-trend.html: live/trend.json이 더 새것이면 그걸 씀
# ③ p-prices.html·p-trend.html: 미국 종목 차트를 열면 Finnhub 실시간 시세(live.js)
import os, re, sys

T = os.path.dirname(os.path.abspath(__file__))
OLD = "  Promise.all(cfg.ds.map((id) => fetch('d/' + cfg.page + '/' + id + '.json' + bust)"
NEW = ("  const liveSt = cfg.page === 'prices' ? fetch('live/stamp.json?t=' + Date.now(), { cache: 'no-store' }).then((r) => (r.ok ? r.json() : null)).catch(() => null) : Promise.resolve(null);\n"
       "  liveSt.then((st) => { const useLive = !!(st && st.base === window.__SYNC__ && Array.isArray(st.files)); window.__LIVE__ = useLive ? st : null;\n"
       "  Promise.all(cfg.ds.map((id) => fetch(useLive && st.files.indexOf(id) >= 0 ? 'live/' + id + '.json?t=' + st.key : 'd/' + cfg.page + '/' + id + '.json' + bust)")
TAIL_OLD = "    const named = location.hash && document.getElementById(location.hash.slice(1)); if (named) named.scrollIntoView();\n  });\n})();"
TAIL_NEW = "    const named = location.hash && document.getElementById(location.hash.slice(1)); if (named) named.scrollIntoView();\n  });\n  });\n})();"
TREND_LOADER = ("(function(d){try{var x=new XMLHttpRequest();x.open('GET','live/trend.json?t='+Date.now(),false);x.send();"
                "if(x.status===200){var j=JSON.parse(x.responseText);if(j&&j.P&&j.P.length&&j.asof>=d.asof&&(j.at||'')>(d.at||'')){window.__LIVE_TREND__=j.label;return j}}}catch(e){}return d})(")


def run(root):
    n = []
    p = os.path.join(root, 'shim.js')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if 'live/stamp.json' not in s and OLD in s and TAIL_OLD in s:
            s = s.replace(OLD, NEW, 1).replace(TAIL_OLD, TAIL_NEW, 1)
            open(p, 'w', encoding='utf-8').write(s); n.append('shim')
    p = os.path.join(root, 'p-trend.html')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if 'live/trend.json' not in s and 'const DATA = {' in s:
            i = s.index('const DATA = {') + len('const DATA = '); j = s.index('\n', i)
            line = s[i:j].rstrip()
            if line.endswith(';'):
                s = s[:i] + TREND_LOADER + line[:-1] + ');' + s[j:]
                open(p, 'w', encoding='utf-8').write(s); n.append('trend')
    LJ = '<script data-live>' + open(os.path.join(T, 'live.js'), encoding='utf-8').read() + '</script>'
    for f in ('p-prices.html', 'p-trend.html'):
        p = os.path.join(root, f)
        if not os.path.exists(p): continue
        s = o = open(p, encoding='utf-8').read()
        s = re.sub(r'<script data-live>[\s\S]*?</script>', '', s)
        s = s.replace('</body>', LJ + '</body>', 1) if '</body>' in s else s + LJ
        if s != o: open(p, 'w', encoding='utf-8').write(s); n.append(f)
    n += fix_nav(root)
    print('site_live', n)



def fix_nav(root):
    # 손으로 만든 페이지(실적 캘린더·실적 결과·차트 길잡이)는 <head>·<body> 꼬리표가 없어 빌더가 맨 위 페이지 줄(⌂ 홈 …)을 못 넣음 → 여기서 넣음(사용자 2026-10-29 지적)
    import glob
    src = None
    for f in sorted(glob.glob(os.path.join(root, 'p-*.html'))):
        m = re.search(r'<nav class="ib"[\s\S]*?</nav><script>[\s\S]*?</script>', open(f, encoding='utf-8').read())
        if m: src = m.group(0); break
    css_p = os.path.join(root, 'kit', 'barcss.css')
    if not src or not os.path.exists(css_p): return []
    css = open(css_p, encoding='utf-8').read(); done = []
    for f in sorted(glob.glob(os.path.join(root, 'p-*.html'))):
        s = open(f, encoding='utf-8').read()
        if 'class="ib"' in s: continue
        me = os.path.basename(f)
        nav = re.sub(r' aria-current="page"', '', src)
        nav = re.sub(r'(<a href="' + re.escape(me) + r'(?:\?v=\d+)?")', r'\1 aria-current="page"', nav)
        add = '<style data-barcss>' + css + '\n.ib{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;white-space:nowrap!important}.ib>*{flex:none!important}</style>'
        # 첫 화면 요소 바로 앞에 페이지 줄 — title·style·script·meta·link·주석은 건너뜀
        k = 0; skip = re.compile(r'\s*(?:<!doctype[^>]*>|<!--[\s\S]*?-->|<(script|style|title)\b[\s\S]*?</\1>|<(?:meta|link|html|head|body)\b[^>]*>|</(?:head|html)>)', re.I)
        while True:
            m = skip.match(s, k)
            if not m or m.end() == k: break
            k = m.end()
        if not re.match(r'\s*<[a-zA-Z]', s[k:]): continue
        s = s[:k] + add + nav + s[k:]
        open(f, 'w', encoding='utf-8').write(s); done.append(me)
    return done

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else '.')
