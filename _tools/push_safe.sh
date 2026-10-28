#!/bin/bash
# 다른 채팅과 동시에 올릴 때: 받아와서 겹치면 그쪽 최신본 + 우리 화면 정리를 다시 입혀 올림
cd "$(dirname "$0")/.."
for i in 1 2 3 4; do
  if timeout 60 git pull -q --rebase origin main; then
    timeout 60 git push -q origin HEAD:main && { git log --oneline -1; exit 0; }
  else
    for f in $(git diff --name-only --diff-filter=U); do git checkout --ours -- "$f"; git add "$f"; done
    python3 -I _tools/reapply_tidy.py . >/dev/null; python3 -I _tools/bump_ver.py . >/dev/null; git add -A
    GIT_EDITOR=true git rebase --continue >/dev/null 2>&1
  fi
  sleep 3
done
echo "push failed"; exit 1
