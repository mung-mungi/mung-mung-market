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
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
open(os.path.join(src, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
open(os.path.join(src, '.nojekyll'), 'w').write('')
left = [f for f in glob.glob(os.path.join(src, '*.html')) if 'claude.ai/' in open(f, encoding='utf-8').read()]
print('changed', n, 'left-claude-links', left)
