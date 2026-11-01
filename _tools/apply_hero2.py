# 전 페이지에 머리 2판(hero2.html) 넣기 — 예전 판은 지우고 새로. prep_site.py 뒤에 돌려도 됨
import re, glob, os, sys
root = sys.argv[1] if len(sys.argv) > 1 else '.'
H = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hero2.html'), encoding='utf-8').read()
n = 0
for f in glob.glob(os.path.join(root, 'p-*.html')):
    s = o = open(f, encoding='utf-8').read()
    s = re.sub(r'<style data-hero2>[\s\S]*?</style>\s*<script data-hero2>[\s\S]*?</script>\s*', '', s)
    s = re.sub(r'<link data-hero2 rel[^>]*>\s*<script data-hero2 src[^>]*></script>\s*', '', s)  # 공용 파일 참조판(2026-11-01)
    s = s.replace('</body>', H + '</body>', 1) if '</body>' in s else s + H
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('hero2', n)
