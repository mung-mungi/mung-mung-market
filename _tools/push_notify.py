# 휴대폰 알림 보내기(사용자 2026-10-30) — 새 실적 노트가 d/earn_feed.json에 생기면 원시그널(OneSignal)로 '알림 받기'를 켠 사람 모두에게 한 번 보냄
# GitHub 비밀값 ONESIGNAL_APP_ID·ONESIGNAL_API_KEY가 없으면 조용히 건너뜀. 보낸 노트는 d/push_state.json에 적어 두 번 보내지 않음
# 사용: python3 -I _tools/push_notify.py <사이트 폴더>
import json, os, sys, urllib.request, datetime as dt
R = sys.argv[1] if len(sys.argv) > 1 else '.'
APP, KEY = (os.environ.get('ONESIGNAL_APP_ID', '').strip() or 'b81f8268-5aef-4a29-b2b8-2173248136a3'), os.environ.get('ONESIGNAL_API_KEY', '').strip()
SITE = 'https://mung-mungi.github.io/mung-mung-market/'
SP = os.path.join(R, 'd/push_state.json')
TEST = os.environ.get('PUSH_TEST', '').strip()  # 시험 알림(수동 실행): 이 문구로 한 번 보내고 끝
if TEST and APP and KEY:
    req = urllib.request.Request('https://api.onesignal.com/notifications', method='POST', headers={'Content-Type': 'application/json', 'Authorization': 'Key ' + KEY},
        data=json.dumps({'app_id': APP, 'included_segments': ['Total Subscriptions'], 'target_channel': 'push', 'headings': {'en': '🔔 멍뭉 터미널 시험 알림', 'ko': '🔔 멍뭉 터미널 시험 알림'},
                         'contents': {'en': TEST, 'ko': TEST}, 'url': SITE + 'p-earn.html'}).encode())
    try: print('::notice::시험 알림 ' + urllib.request.urlopen(req, timeout=20).read().decode()[:300])
    except Exception as e: print('::notice::시험 실패 %s %s' % (e, getattr(e, 'read', lambda: b'')().decode()[:300]))
    sys.exit(0)
feed = json.load(open(os.path.join(R, 'd/earn_feed.json'), encoding='utf-8'))
try: st = json.load(open(SP, encoding='utf-8'))
except Exception: st = {}
sent = set(st.get('sent', []))
first = not st  # 처음 켤 때는 지금까지 노트를 '보낸 것'으로만 표시(옛 노트 폭탄 방지)
now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
def fresh(x):  # 뉴욕 시각 기준 최근 36시간 노트만
    try: return now - dt.datetime.fromisoformat(x['ts']) < dt.timedelta(hours=40)
    except Exception: return False
new = [x for x in feed.get('items', []) if x['id'] not in sent and fresh(x)]
if first or not new:
    st['sent'] = sorted(sent | {x['id'] for x in feed.get('items', [])})[-300:]
    json.dump(st, open(SP, 'w', encoding='utf-8'), ensure_ascii=False); print('push: 보낼 것 없음' + (' (처음 켬)' if first else '')); sys.exit(0)
if not (APP and KEY):
    print('::notice::push: 원시그널 키 없음 — 건너뜀(보낸 것으로 표시하지 않음) 새 노트 %s' % ','.join(x['id'] for x in new)); sys.exit(0)
if len(new) == 1:
    x = new[0]; head = '🔔 새 실적 · ' + x['name']; body = (x.get('sum') or '실적 결과 노트가 올라왔습니다.')[:160]; url = SITE + 'p-earn.html#' + x['id']
else:
    names = ' · '.join(x['name'] for x in new[:4]) + (' 외 %d곳' % (len(new) - 4) if len(new) > 4 else '')
    head = '🔔 새 실적 %d곳' % len(new); body = names; url = SITE + 'p-earn.html'
req = urllib.request.Request('https://api.onesignal.com/notifications', method='POST',
    headers={'Content-Type': 'application/json', 'Authorization': 'Key ' + KEY},
    data=json.dumps({'app_id': APP, 'included_segments': ['Total Subscriptions'], 'target_channel': 'push',
                     'headings': {'en': head, 'ko': head}, 'contents': {'en': body, 'ko': body}, 'url': url}).encode())
try:
    r = json.load(urllib.request.urlopen(req, timeout=20)); print('::notice::push 보냄 %s %s %s' % (head, r.get('id'), r.get('errors')))
    st['sent'] = sorted(sent | {x['id'] for x in new})[-300:]; st['last'] = now.isoformat(timespec='minutes')
    json.dump(st, open(SP, 'w', encoding='utf-8'), ensure_ascii=False)
except Exception as e:
    print('::notice::push 실패 %s %s' % (e, getattr(e, 'read', lambda: b'')().decode()[:300]))
