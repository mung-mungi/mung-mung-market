# 허브(통합본) 파일 → GitHub Pages용: claude.ai 링크를 사이트 안 페이지로, noindex 추가
import json, os, re, sys, glob
src = sys.argv[1]
conf = json.load(open(os.path.join(src, 'kit/conf.json'), encoding='utf-8'))
m = {}
for page, url in conf['urls'].items():
    m[url.rstrip('/').split('/')[-1]] = 'index.html' if page == 'hub' else f'p-{page}.html'
m['83yn7caQnHU8MWiVLEHSMi'] = 'index.html'
META = '<meta name="robots" content="noindex,nofollow">'
n = 0
for f in glob.glob(os.path.join(src, '*.html')):
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'https://claude\.ai/(?:code/)?artifact/([A-Za-z0-9-]+)[^"\'\s)<]*',
               lambda x: m.get(x[1], x[0]), s)
    s = re.sub(r'(<a [^>]*href="(?:index|p-[a-z]+)\.html"[^>]*?)\s+target="_blank"', r'\1', s)
    if 'name="robots"' not in s:
        s = re.sub(r'(<head[^>]*>)', r'\1' + META, s, count=1) if '<head' in s else META + s
    # 사이트 이름: 멍뭉 마켓
    s = s.replace('<title>AI 밸류체인 통합본</title>', '<title>멍뭉 마켓</title>')
    s = s.replace('<h1>AI 밸류체인 <span class="dim">통합본</span></h1>', '<h1>멍뭉 마켓</h1>')
    s = re.sub(r'<title>(?!멍뭉 마켓)([^<]*?)(?: · 멍뭉 마켓)?</title>', r'<title>\1 · 멍뭉 마켓</title>', s)
    if 'apple-mobile-web-app-title' not in s:
        s = s.replace(META, META + '<meta name="apple-mobile-web-app-title" content="멍뭉 마켓"><meta name="application-name" content="멍뭉 마켓">', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
open(os.path.join(src, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
open(os.path.join(src, '.nojekyll'), 'w').write('')
left = [f for f in glob.glob(os.path.join(src, '*.html')) if 'claude.ai/' in open(f, encoding='utf-8').read()]
print('changed', n, 'left-claude-links', left)
