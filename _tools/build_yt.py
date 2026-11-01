# 유튜브 '멍뭉 터미널' 채널 새 영상 → d/yt.json (사용자 2026-11-02 '영상 올리면 자연스럽게 배너 알림')
# 공개 RSS(https://www.youtube.com/feeds/videos.xml?channel_id=...)만 씀 — API 키·크레딧 없음. Actions yt.yml이 30분마다 실행
import json, os, re, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
R = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = os.path.join(R, 'd', 'yt.json')
HANDLE = '@멍뭉터미널'
UA = {'User-Agent': 'Mozilla/5.0 (mung-terminal yt check)', 'Accept-Language': 'ko-KR,ko;q=0.9'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read().decode('utf-8', 'ignore')
old = {}
try:
    old = json.load(open(OUT, encoding='utf-8'))
except Exception:
    pass
cid = old.get('channel_id')
if not cid:
    h = get('https://www.youtube.com/' + urllib.parse.quote(HANDLE))
    m = re.search(r'"(?:channelId|externalId)":"(UC[\w-]{22})"', h) or re.search(r'channel_id=(UC[\w-]{22})', h)
    if not m:
        print('채널 ID를 못 찾음'); sys.exit(0)
    cid = m.group(1)
x = get('https://www.youtube.com/feeds/videos.xml?channel_id=' + cid)
ns = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'm': 'http://search.yahoo.com/mrss/'}
root = ET.fromstring(x)
items = []
for e in root.findall('a:entry', ns)[:6]:
    vid = e.findtext('yt:videoId', '', ns)
    link = (e.find('a:link', ns).get('href') if e.find('a:link', ns) is not None else '') or ('https://www.youtube.com/watch?v=' + vid)
    items.append({'id': vid, 'title': e.findtext('a:title', '', ns).strip(), 'published': e.findtext('a:published', '', ns),
                  'url': link, 'short': '/shorts/' in link, 'thumb': 'https://i.ytimg.com/vi/' + vid + '/mqdefault.jpg'})
new = {'channel_id': cid, 'handle': HANDLE, 'channel_url': 'https://www.youtube.com/' + HANDLE, 'items': items}
if json.dumps(new, sort_keys=True) == json.dumps({k: old.get(k) for k in new}, sort_keys=True):
    print('변화 없음'); sys.exit(0)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(new, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('갱신', items[0]['title'] if items else '(영상 없음)')
