# 사이트 판 번호 올리기: 손으로 고친 뒤 올릴 때 돌리면, 카톡 안 브라우저가 옛 화면을 붙잡지 않고 새 판으로 한 번 다시 불러옴(사용자 2026-10-29)
# 사용: python3 -I _tools/bump_ver.py <사이트 폴더>
import glob, os, re, sys, time
root = sys.argv[1] if len(sys.argv) > 1 else '.'
os.environ['TZ'] = 'Asia/Seoul'; time.tzset()
st = time.strftime('%Y%m%d%H%M')
old = open(os.path.join(root, 'version.json')).read()
m = re.search(r'"v":"(\d+)"', old)
if m and m.group(1) >= st: st = str(int(m.group(1)) + 1)
open(os.path.join(root, 'version.json'), 'w').write('{"v":"' + st + '"}')
n = 0
for f in glob.glob(os.path.join(root, '*.html')):
    s = o = open(f, encoding='utf-8').read()
    s = re.sub(r'data-ver="\d+"', 'data-ver="' + st + '"', s)
    s = re.sub(r'var me="\d+"', 'var me="' + st + '"', s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('ver', st, 'pages', n)
