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
    sys.path.insert(0, T); import hub_tidy as _ht
    for f in _g_all(root):
        s0 = open(f, encoding='utf-8').read(); s1 = _ht.tidy_ibdrag(s0)
        if s1 != s0: open(f, 'w', encoding='utf-8').write(s1); n.append('ibdrag:' + os.path.basename(f))
    # 누름 소리: 통합본 빌더가 넣은 예전 틱을 사이트 최신본(_tools/tick.js)으로 교체(사용자 2026-10-29 — 들릴 듯 말 듯하게)
    import glob as _g
    TK = open(os.path.join(T, 'tick.js'), encoding='utf-8').read()
    for f in _g.glob(os.path.join(root, '*.html')):
        s0 = open(f, encoding='utf-8').read()
        s1 = re.sub(r'<script data-tick>[\s\S]*?</script>', lambda m: '<script data-tick>' + TK + '</script>', s0)
        if s1 != s0: open(f, 'w', encoding='utf-8').write(s1); n.append('tick:' + os.path.basename(f))
    n += fix_hub(root)
    n += rename_cal(root)
    sys.path.insert(0, T); import page_tidy; n += page_tidy.run(root)
    pe = os.path.join(root, 'p-earn.html')
    if os.path.exists(pe):
        sys.path.insert(0, T); import hub_tidy
        o = open(pe, encoding='utf-8').read(); b = hub_tidy.tidy_hits(o)
        if b != o: open(pe, 'w', encoding='utf-8').write(b); n.append('p-earn')
    ptr = os.path.join(root, 'p-trend.html')
    if os.path.exists(ptr):
        sys.path.insert(0, T); import hub_tidy
        o = open(ptr, encoding='utf-8').read(); b = hub_tidy.tidy_pergo(o)
        if b != o: open(ptr, 'w', encoding='utf-8').write(b); n.append('p-trend')
    sys.path.insert(0, T); import hub_tidy
    for _f in hub_tidy.UNI_PAGES:
        _p = os.path.join(root, _f)
        if os.path.exists(_p):
            o = open(_p, encoding='utf-8').read(); b = hub_tidy.tidy_uni(o)
            if b != o: open(_p, 'w', encoding='utf-8').write(b); n.append(_f[:-5])
    pc = os.path.join(root, 'p-cal.html')
    if os.path.exists(pc):
        sys.path.insert(0, T); import hub_tidy
        o = open(pc, encoding='utf-8').read(); b = hub_tidy.tidy_cal(o)
        if b != o: open(pc, 'w', encoding='utf-8').write(b); n.append('p-cal')
    pl = os.path.join(root, 'p-lights.html')
    if os.path.exists(pl):
        sys.path.insert(0, T); import hub_tidy
        o = open(pl, encoding='utf-8').read(); b = hub_tidy.tidy_lights(o)
        if b != o: open(pl, 'w', encoding='utf-8').write(b); n.append('p-lights')
    po = os.path.join(root, 'p-opt.html')
    if os.path.exists(po):
        sys.path.insert(0, T); import hub_tidy
        o = open(po, encoding='utf-8').read(); b = hub_tidy.tidy_opt(o)
        if b != o: open(po, 'w', encoding='utf-8').write(b); n.append('p-opt')
    pt = os.path.join(root, 'p-targets.html')
    if os.path.exists(pt):
        sys.path.insert(0, T); import hub_tidy
        o = open(pt, encoding='utf-8').read(); b = hub_tidy.tidy_targets(o)
        if b != o: open(pt, 'w', encoding='utf-8').write(b); n.append('p-targets')
    pb = os.path.join(root, 'p-brief.html')
    if os.path.exists(pb):
        sys.path.insert(0, T); import hub_tidy
        o = open(pb, encoding='utf-8').read(); b = hub_tidy.tidy_brief(o)
        if b != o: open(pb, 'w', encoding='utf-8').write(b); n.append('p-brief')
    print('site_live', n)



def _g_all(root):
    import glob
    return glob.glob(os.path.join(root, '*.html'))


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


def fix_hub(root):
    # 홈 배너 멍뭉이: 배경 없는 그림을 배너 위에 얹고, '하루 6~8회 갱신' 대신 '80종목 한눈에'(사용자 2026-10-28·29 지시)
    import base64
    p = os.path.join(root, 'index.html')
    if not os.path.exists(p): return []
    s = o = open(p, encoding='utf-8').read()
    uri = 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(T, 'cat-hub.webp'), 'rb').read()).decode()
    s = re.sub(r'<img alt="" src="data:image/jpeg;base64,[^"]+"', '<img class="bn-cat" alt="" src="' + uri + '"', s, count=1)
    s = s.replace('.bn img{flex:none;height:100%;width:auto;max-width:42%;object-fit:cover;object-position:left top}',
                  '.bn img{position:absolute;right:4px;bottom:-34px;height:148px;width:auto;max-width:none;pointer-events:none;filter:drop-shadow(0 4px 8px rgba(80,50,10,.16))}\n.bn .tx{padding-right:118px!important}')
    s = s.replace(' 기준 · 하루 6~8회 갱신', ' 기준 · 80종목 한눈에')
    s = s.replace('원본 대시보드의 화면과 자료를 하루 네 번(06:37 · 08:37 · 13:37 · 22:37) 옮겨 옵니다.', '실적·브리핑은 나오는 대로, 시세는 장중 5분마다 바뀝니다.')  # 사용자 2026-10-29
    sys.path.insert(0, T); import hub_tidy; s = hub_tidy.tidy(s)  # 첫 화면 정리(사용자 2026-10-29)
    MJ = '<script data-mkt>' + open(os.path.join(T, 'market.js'), encoding='utf-8').read() + '</script>'
    MJ += '<script data-mkt>' + open(os.path.join(T, 'home_order.js'), encoding='utf-8').read() + '</script>'
    s = re.sub(r'<script data-mkt>[\s\S]*?</script>', '', s)
    s = s.replace('</body>', MJ + '</body>', 1) if '</body>' in s else s + MJ
    if s != o: open(p, 'w', encoding='utf-8').write(s); return ['index.html']
    return []



def rename_cal(root):
    # '실적 캘린더' → '실적 일정'(사용자 2026-10-29: 더 직관적) — 맨 위 페이지 줄 링크 글자만
    import glob
    done = []
    for f in glob.glob(os.path.join(root, '*.html')):
        s = o = open(f, encoding='utf-8').read()
        s = re.sub(r'(<a href="p-cal\.html[^"]*"[^>]*>)실적 캘린더(</a>)', r'\1실적 일정\2', s)
        s = re.sub(r'(<a href="p-trend\.html[^"]*"[^>]*>)차트 길잡이(</a>)', r'\1종목 차트\2', s)  # 사용자 2026-10-29: 보통 쓰는 말로
        if s != o: open(f, 'w', encoding='utf-8').write(s); done.append(os.path.basename(f))
    return ['rename_cal:%d' % len(done)] if done else []


if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else '.')
