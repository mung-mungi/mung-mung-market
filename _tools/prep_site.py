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
OGDESC = '실적 속보·실적 캘린더·목표주가·공매도·시세를 한 곳에서. 매일 6~8회 업데이트.'
shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'og-card.jpg'), os.path.join(src, 'og-card.jpg'))
def og(title, fn):
    t = H.escape(title, quote=True)
    return (f'<meta property="og:type" content="website"><meta property="og:site_name" content="AI 밸류체인 통합본">'
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
    if 'name="robots"' not in s:
        s = re.sub(r'(<head[^>]*>)', r'\1' + META, s, count=1) if '<head' in s else META + s
    if 'property="og:image"' not in s:
        mt = re.search(r'<title>([^<]*)</title>', s)
        tag = og(mt[1] if mt else 'AI 밸류체인 통합본', os.path.basename(f))
        s = re.sub(r'(<meta name="robots"[^>]*>)', lambda x: x[1] + tag, s, count=1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
open(os.path.join(src, 'robots.txt'), 'w').write('User-agent: kakaotalk-scrap\nAllow: /\n\nUser-agent: facebookexternalhit\nAllow: /\n\nUser-agent: *\nDisallow: /\n')
open(os.path.join(src, '.nojekyll'), 'w').write('')
left = [f for f in glob.glob(os.path.join(src, '*.html')) if 'claude.ai/' in open(f, encoding='utf-8').read()]
print('changed', n, 'left-claude-links', left)
