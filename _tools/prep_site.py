# 허브(통합본) 파일 → GitHub Pages용: claude.ai 링크를 사이트 안 페이지로, noindex 추가
import json, os, re, sys, glob, shutil, html as H
src = sys.argv[1]
conf = json.load(open(os.path.join(src, 'kit/conf.json'), encoding='utf-8'))
m = {}
for page, url in conf['urls'].items():
    m[url.rstrip('/').split('/')[-1]] = 'index.html' if page == 'hub' else f'p-{page}.html'
m['83yn7caQnHU8MWiVLEHSMi'] = 'index.html'
META = '<meta name="robots" content="noindex,nofollow">'
# 카톡·SNS 링크 미리보기 카드(og 태그) — 이미지는 _tools/og-card.jpg를 사이트 루트로 복사
SITE = 'https://mung-mungi.github.io/mung-mung-market/'
OGDESC = 'AI 밸류체인 80종목의 실적 속보·실적 캘린더·목표주가·공매도·시세를 한 화면에서.'
shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'og-card.jpg'), os.path.join(src, 'og-card.jpg'))
def og(title, fn):
    if fn == 'index.html': title = '멍뭉 터미널 · AI 밸류체인 레이더'
    t = H.escape(title, quote=True)
    return (f'<meta property="og:type" content="website"><meta property="og:site_name" content="멍뭉 터미널">'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{OGDESC}">'
            f'<meta property="og:url" content="{SITE}{"" if fn == "index.html" else fn}">'
            f'<meta property="og:image" content="{SITE}og-card.jpg"><meta property="og:image:width" content="1200">'
            f'<meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">')
n = 0
for f in glob.glob(os.path.join(src, '*.html')):
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'https://claude\.ai/(?:code/)?artifact/([A-Za-z0-9-]+)[^"\'\s)<]*',
               lambda x: m.get(x[1], x[0]), s)
    s = re.sub(r'(<a [^>]*href="(?:index|p-[a-z]+)\.html"[^>]*?)\s+target="_blank"', r'\1', s)
    if not re.search(r"<meta charset", s, re.I):
        s = '<meta charset="utf-8">' + s
    # 휴대폰(카톡 안 브라우저 포함)에서 화면 폭에 맞게 — 없으면 PC 화면처럼 작게 보임
    if not re.search(r'<meta name=["\']?viewport', s, re.I):
        s = '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + s
    if 'http-equiv="Cache-Control"' not in s:  # 카톡 안 브라우저가 예전 화면을 붙잡지 않게
        s = re.sub(r'(<meta charset[^>]*>)', r'\1<meta http-equiv="Cache-Control" content="no-cache, must-revalidate"><meta http-equiv="Pragma" content="no-cache">', s, count=1, flags=re.I)
    if 'setAttribute("data-theme","light")' not in s:  # 사용자 지시: 주간(라이트) 모드로만 보이게
        s = re.sub(r'(<meta charset[^>]*>)', r'\1<meta name="color-scheme" content="light"><script>document.documentElement.setAttribute("data-theme","light")</script>', s, count=1, flags=re.I)
    if 'data-vt' not in s:  # 페이지 전환 슬라이드(아이폰 앱 느낌) — 사용자 2026-10-28 지시
        VT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vt.html'), encoding='utf-8').read()
        s = re.sub(r'(</head>)', lambda m: VT + m.group(1), s, count=1, flags=re.I) if re.search(r'</head>', s, re.I) else VT + s
    if 'data-tick' not in s:  # 누름 소리(틱) — 사용자 2026-10-28 지시
        TK = '<script data-tick>' + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tick.js'), encoding='utf-8').read() + '</script>'
        s = s.replace('</body>', TK + '</body>', 1) if '</body>' in s else s + TK
    # 페이지 머리(제목 영역) 통일 + 정보와 무관한 안내문 숨김 — 사용자 2026-10-28 지시. 판을 바꾸면 예전 것을 지우고 새로 넣음
    HERO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hero.html'), encoding='utf-8').read()
    s = re.sub(r'<style data-hero>[\s\S]*?</style>\s*<script data-hero>[\s\S]*?</script>\s*(?:<script data-hero-fix>[\s\S]*?</script>\s*)?', '', s)
    s = s.replace('</body>', HERO + '</body>', 1) if '</body>' in s else s + HERO
    if os.path.basename(f).startswith('p-'):  # 머리 2판(파스텔 배너+멍뭉이) — 사용자 2026-10-28 지시
        H2 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hero2.html'), encoding='utf-8').read()
        s = re.sub(r'<style data-hero2>[\s\S]*?</style>\s*<script data-hero2>[\s\S]*?</script>\s*', '', s)
        s = s.replace('</body>', H2 + '</body>', 1) if '</body>' in s else s + H2
    if not re.match(r'\s*<!doctype', s, re.I):
        s = '<!doctype html>' + s
    if 'name="robots"' not in s:
        s = re.sub(r'(<head[^>]*>)', r'\1' + META, s, count=1) if '<head' in s else META + s
    s = re.sub(r'<meta (?:property="og:[a-z:_]+"|name="twitter:card") content="[^"]*">', '', s)
    if True:
        mt = re.search(r'<title>([^<]*)</title>', s)
        tag = og(mt[1] if mt else 'AI 밸류체인 통합본', os.path.basename(f))
        s = re.sub(r'(<meta name="robots"[^>]*>)', lambda x: x[1] + tag, s, count=1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
# 사이트 안 링크에 판 번호(?v=)를 붙여, 휴대폰·카톡 브라우저가 10분 동안 예전 페이지를 붙잡지 않게 합니다
import time as _t
STAMP = _t.strftime('%Y%m%d%H%M')
for f in glob.glob(os.path.join(src, '*.html')):
    s = open(f, encoding='utf-8').read()
    n2 = re.sub(r'href="((?:index|p-[a-z0-9]+)\.html)(?:\?v=\d+)?(#[^"]*)?"', lambda x: 'href="' + x[1] + '?v=' + STAMP + (x[2] or '') + '"', s)
    if n2 != s: open(f, 'w', encoding='utf-8').write(n2)
# 자동 새로고침: 페이지에 판 번호를 심고, 더 새 판이 올라와 있으면(version.json) 한 번 다시 불러옵니다 — 카톡 안 브라우저 캐시 대응
open(os.path.join(src, 'version.json'), 'w').write('{"v":"' + STAMP + '"}')
VS = ('<script data-ver="' + STAMP + '">(function(){var me="' + STAMP + '";try{fetch("version.json?t="+Date.now(),{cache:"no-store"}).then(function(r){return r.json()}).then(function(j){'
      'if(!j||!j.v||j.v<=me)return;var k="mmv-"+j.v+location.pathname;if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,"1");'
      'var u=new URL(location.href);u.searchParams.set("v",j.v);location.replace(u.toString())}).catch(function(){})}catch(e){}})();</script>')
for f in glob.glob(os.path.join(src, '*.html')):
    s2 = open(f, encoding='utf-8').read()
    s3 = re.sub(r'<script data-ver="\d+">[\s\S]*?</script>', '', s2)
    s3 = re.sub(r'(<meta charset[^>]*>)', lambda m: m.group(1) + VS, s3, count=1, flags=re.I) if re.search(r'<meta charset', s3, re.I) else VS + s3
    if s3 != s2: open(f, 'w', encoding='utf-8').write(s3)
open(os.path.join(src, 'robots.txt'), 'w').write('User-agent: kakaotalk-scrap\nAllow: /\n\nUser-agent: facebookexternalhit\nAllow: /\n\nUser-agent: *\nDisallow: /\n')
open(os.path.join(src, '.nojekyll'), 'w').write('')
left = [f for f in glob.glob(os.path.join(src, '*.html')) if 'claude.ai/' in open(f, encoding='utf-8').read()]
print('changed', n, 'left-claude-links', left)
