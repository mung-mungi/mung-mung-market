# 헛걸음 막기(사용자 2026-11-02): 올리기 전에, 바뀐 것이 '갱신 시각' 글자뿐인 JSON 파일은 올리지 않음
# 쓰는 법: git add 뒤에 python3 -I _tools/stamp_only.py  → 시각만 바뀐 파일은 HEAD 상태로 되돌리고 스테이징에서 뺌
import json, subprocess
SKIP = {'updated', 'generated', 'generated_at', 'run_at', 'built', 'built_at', 'fetched', 'fetched_at', 'checked', 'checked_at', 'now'}
def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in SKIP}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o
files = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True).stdout.split()
n = 0
for f in files:
    if not f.endswith('.json'):
        continue
    try:
        old = subprocess.run(['git', 'show', 'HEAD:' + f], capture_output=True, text=True, check=True).stdout
        a = strip(json.loads(old)); b = strip(json.load(open(f, encoding='utf-8')))
    except Exception:
        continue
    if a == b:
        subprocess.run(['git', 'reset', '-q', 'HEAD', '--', f]); subprocess.run(['git', 'checkout', '-q', 'HEAD', '--', f]); n += 1
        print('시각만 바뀜 → 안 올림:', f)
print('stamp-only 되돌림', n)
