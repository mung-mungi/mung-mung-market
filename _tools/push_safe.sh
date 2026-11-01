#!/bin/bash
# 다른 채팅과 동시에 올릴 때: 받아와서 겹치면 그쪽 최신본 + 우리 화면 정리를 다시 입혀 올림
# 꼬임 방지(2026-11-01): ① 공용 부품(_tools 원본)이 겹치면 그쪽 것으로 덮지 않고 멈춤(직접 합치기)
#                       ② 올리기 직전 guard_check.py — 옛 복사본으로 남의 최근 기능을 지우면 멈춤
cd "$(dirname "$0")/.."
for i in 1 2 3 4; do
  if timeout 60 git pull -q --rebase origin main; then
    if [ -z "$GUARD_OK" ] && [ -f _tools/guard_check.py ]; then python3 -I _tools/guard_check.py . origin/main || exit 3; fi
    timeout 60 git push -q origin HEAD:main && { git log --oneline -1; exit 0; }
  else
    src=$(git diff --name-only --diff-filter=U | grep -E '^_tools/[^/]+\.(js|css|py|html|sh|json)$' | grep -v __pycache__)
    if [ -n "$src" ]; then
      git rebase --abort
      echo "⛔ 공용 부품이 다른 채팅 수정과 겹침: $src"
      echo "   그쪽 최신본을 받아(git pull --rebase) 우리 변경만 Edit로 다시 넣은 뒤 올리세요. (예전처럼 한쪽으로 덮으면 기능이 사라짐)"
      exit 2
    fi
    for f in $(git diff --name-only --diff-filter=U); do git checkout --ours -- "$f"; git add "$f"; done
    python3 -I _tools/reapply_tidy.py . >/dev/null; python3 -I _tools/bump_ver.py . >/dev/null; git add -A
    GIT_EDITOR=true git rebase --continue >/dev/null 2>&1
  fi
  sleep 3
done
echo "push failed"; exit 1
