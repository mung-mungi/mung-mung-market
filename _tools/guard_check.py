# 올리기 전 꼬임 방지 검사(사용자 2026-11-01) — push_safe.sh가 올리기 직전에 부름. 막히면 아무것도 올라가지 않음
# ① 옛 복사본 덮어쓰기: 이번에 올리는 공용 부품(_tools)에서, 최근 7일 안에 '다른 채팅'이 넣은 줄을 3줄 넘게 지우면 멈춤
#    (2026-11-01 19:16 한 채팅이 옛 navfab.js로 통째 덮어써 차트 넘김·스크롤 감도·아이패드 기능이 사라진 사례)
# ② 기능 표시: _tools/guard.json에 적힌 '있어야 할 글자'가 빠지면 멈춤 — 새 기능을 넣으면 여기에 한 줄 추가
# 정말 지우려는 거면: GUARD_OK=1 ./_tools/push_safe.sh
import os, sys, re, json, subprocess, time

R = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
BASE = sys.argv[2] if len(sys.argv) > 2 else 'origin/main'
SRC = re.compile(r'^_tools/[^/]+\.(js|css|py|html|sh)$')

def git(*a):
    return subprocess.run(['git', *a], cwd=R, capture_output=True, text=True).stdout

def session(sha):
    m = re.search(r'Claude-Session:\s*(\S+)', git('show', '-s', '--format=%B', sha))
    return m.group(1) if m else ''

problems = []
mine = {session(c) for c in git('rev-list', BASE + '..HEAD').split()} - {''}

# ① 다른 채팅이 최근 넣은 줄을 지우는지
for f in git('diff', '--name-only', BASE, 'HEAD').split():
    if not SRC.match(f) or '__pycache__' in f: continue
    rng = []
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? ', git('diff', '-U0', BASE, 'HEAD', '--', f), re.M):
        a, n = int(m.group(1)), int(m.group(2) or 1)
        if n: rng.append((a, a + n - 1))
    if not rng: continue
    args = ['blame', '--line-porcelain']
    for a, b in rng: args += ['-L', f'{a},{b}']
    who = {}
    for m in re.finditer(r'^([0-9a-f]{40}) \d+ \d+', git(*args, BASE, '--', f), re.M):
        who[m.group(1)] = who.get(m.group(1), 0) + 1
    lost = 0; subj = []
    for sha, n in who.items():
        t = int(git('show', '-s', '--format=%ct', sha).strip() or 0)
        s = session(sha)
        if s and s not in mine and time.time() - t < 7 * 86400:
            lost += n; subj.append(git('show', '-s', '--format=%h %s', sha).strip()[:60])
    if lost > 3:
        problems.append(f'{f}: 다른 채팅이 최근 넣은 {lost}줄을 지웁니다 ← ' + ' / '.join(subj[:3]))

# ② 있어야 할 기능 표시
try:
    G = json.load(open(os.path.join(R, '_tools', 'guard.json'), encoding='utf-8'))
except Exception:
    G = {}
for f, keys in G.items():
    if '/' not in f: continue  # _about·_why 같은 설명 칸은 건너뜀
    try: t = open(os.path.join(R, f), encoding='utf-8').read()
    except Exception: problems.append(f'{f} 없음'); continue
    for k in keys:
        if k not in t: problems.append(f'{f}: 기능 표시 "{k}" 가 빠짐 ({G.get("_why", {}).get(k, "")})')

if problems:
    print('⛔ 올리기 멈춤 — 옛 복사본으로 덮어쓴 것 같습니다:')
    for p in problems: print('  - ' + p)
    print('  최신본(git pull)에서 Edit로 필요한 줄만 고친 뒤 다시 올리세요. 정말 지우는 게 맞으면 GUARD_OK=1 ./_tools/push_safe.sh')
    sys.exit(3)
print('guard ok')
