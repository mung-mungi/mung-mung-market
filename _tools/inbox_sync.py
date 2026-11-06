# 멍터 알림함(사용자 2026-11-06 — 휴대폰 알림이 쌓이면 뭐가 울렸는지 보기 힘듦): 원시그널에 남은 최근 알림을 d/inbox.json으로 모음
# 주인장 기기만(필터) 보낸 시험·보고 알림은 빼고, 지인 전체에게 간 알림만. 바뀐 게 없으면 파일을 건드리지 않음
# 사용: ONESIGNAL_API_KEY=… python3 -I _tools/inbox_sync.py <사이트 폴더>
import json, os, sys, re, urllib.request, datetime as dt
R = sys.argv[1] if len(sys.argv) > 1 else '.'
APP = os.environ.get('ONESIGNAL_APP_ID', '').strip() or 'b81f8268-5aef-4a29-b2b8-2173248136a3'
KEY = os.environ.get('ONESIGNAL_API_KEY', '').strip()
SITE = 'https://mung-mungi.github.io/mung-mung-market/'
OUT = os.path.join(R, 'd/inbox.json')
if not KEY: print('원시그널 키 없음 — 건너뜀'); sys.exit(0)
req = urllib.request.Request('https://api.onesignal.com/notifications?app_id=%s&limit=50' % APP, headers={'Authorization': 'Key ' + KEY})
ns = json.load(urllib.request.urlopen(req, timeout=30)).get('notifications', [])
KST = dt.timezone(dt.timedelta(hours=9))
def kind(t):
    m = re.match(r'【(.+?)】', t)
    if m: return m.group(1)
    if '실적' in t: return '실적'
    if re.search(r'ADP|고용|물가|GDP|PCE|졸트|FOMC|연준|경제지표', t): return '지표'
    if t.startswith('📢'): return '속보'
    return '전달'
items = []
for n in ns:
    if n.get('filters') or n.get('canceled'): continue          # 주인장만 받은 알림·취소된 알림 제외
    t = ((n.get('headings') or {}).get('ko') or (n.get('headings') or {}).get('en') or '').strip()
    b = ((n.get('contents') or {}).get('ko') or (n.get('contents') or {}).get('en') or '').strip()
    if not t or '시험' in t: continue
    ts = n.get('completed_at') or n.get('send_after') or n.get('queued_at') or 0
    if not ts: continue
    u = n.get('url') or ''
    items.append({'id': n.get('id', '')[:12], 'at': dt.datetime.fromtimestamp(ts, KST).isoformat(timespec='minutes'), 'kind': kind(t),
                  'title': re.sub(r'^【.+?】\s*', '', t).lstrip('📢🔔🏦🎤 ').strip(), 'body': b[:200],
                  'url': u[len(SITE):] if u.startswith(SITE) else 'index.html'})
for x in items: x['title'] = re.sub(r'^새 실적\s*·\s*', '', x['title'])
items.sort(key=lambda x: x['at'], reverse=True)
# 같은 제목을 한 시간 안에 다시 보낸 것(재발송)은 최신 하나만
_k, _o = {}, []
for x in items:
    t0 = dt.datetime.fromisoformat(x['at'])
    if x['title'] in _k and (_k[x['title']] - t0) < dt.timedelta(hours=1): continue
    _k[x['title']] = t0; _o.append(x)
items = _o
items = items[:40]
try: old = json.load(open(OUT, encoding='utf-8')).get('items')
except Exception: old = None
if old == items: print('알림함 변화 없음'); sys.exit(0)
json.dump({'updated': dt.datetime.now(KST).isoformat(timespec='minutes'), 'items': items}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('알림함 %d건 저장' % len(items))
