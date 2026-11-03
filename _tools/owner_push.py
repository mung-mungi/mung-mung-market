# 주인장 칸에 새 글이 올라오면 주인장 기기에만 알림(사용자 2026-11-03)
# 직전 커밋과 비교: d/notice_draft.json의 n(초안 수)이 늘었거나, d/owner.enc.json의 updated가 바뀌면 보냄
# 출력: GitHub Actions용 title=…, msg=… (보낼 게 없으면 아무것도 안 씀)
# 사용: python3 -I _tools/owner_push.py <사이트 폴더>
import json, os, subprocess, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
def now(f):
    try: return json.load(open(os.path.join(R, f), encoding='utf-8'))
    except Exception: return {}
def before(f):
    try: return json.loads(subprocess.run(['git', '-C', R, 'show', 'HEAD~1:' + f], capture_output=True, text=True, check=True).stdout)
    except Exception: return {}
out = []
a, b = before('d/notice_draft.json'), now('d/notice_draft.json')
if (b.get('n') or 0) > (a.get('n') or 0):
    out.append('새 전달사항 초안 %d건' % ((b.get('n') or 0) - (a.get('n') or 0)))
a, b = before('d/owner.enc.json'), now('d/owner.enc.json')
if b.get('updated') and b.get('updated') != a.get('updated'):
    out.append('주인장 자료 갱신')
# 업무 보고(사용자 2026-11-03): Claude가 d/report/latest.json({"id","title","msg","path"})을 바꾸면 그 문구 그대로 주인장 기기에만
a, b = before('d/report/latest.json'), now('d/report/latest.json')
if b.get('id') and b.get('id') != a.get('id'):
    print('업무 보고:', b.get('title'), b.get('msg'))
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/stdout'), 'a', encoding='utf-8') as g:
        g.write('title=%s\nmsg=%s\npath=%s\n' % ((b.get('title') or '🐾 작업 보고')[:60], (b.get('msg') or '')[:180].replace('\n', ' '), b.get('path') or 'index.html'))
    sys.exit(0)
if out:
    msg = ' · '.join(out) + ' — 주인장 칸에서 확인하세요'
    print('주인장 알림:', msg)
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/stdout'), 'a', encoding='utf-8') as g:
        g.write('title=🔒 주인장 칸 새 글\nmsg=%s\n' % msg)
else:
    print('주인장 칸 변화 없음(또는 후보만 바뀜) — 알림 안 보냄')
