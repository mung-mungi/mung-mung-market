# 충돌 뒤 우리 화면 정리를 다시 입힘(사이트 동기화와 같은 함수) — 사용법: python3 -I _tools/reapply_tidy.py .
import os, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
sys.path.insert(0, os.path.join(R, '_tools')); import hub_tidy as h
M = {'index.html': lambda x: h.tidy_mkt(h.tidy_hero(h.tidy_tick(h.tidy_owner(h.tidy_notice(h.tidy_splash(h.tidy(x))))))), 'p-brief.html': h.tidy_brief, 'p-earn.html': h.tidy_hits, 'p-targets.html': h.tidy_targets,
     'p-lights.html': h.tidy_lights, 'p-trend.html': h.tidy_pergo, 'p-opt.html': h.tidy_opt, 'p-cal.html': h.tidy_cal, 'p-bond.html': h.tidy_bond, 'p-policy.html': h.tidy_policy, 'p-tech.html': h.tidy_policy}
for f, fn in M.items():
    p = os.path.join(R, f)
    if not os.path.exists(p): continue
    o = open(p, encoding='utf-8').read(); a = fn(fn(o))
    if a != o: open(p, 'w', encoding='utf-8').write(a); print('tidy', f)
import glob as _g
for p in _g.glob(os.path.join(R, 'p-*.html')):
    o = open(p, encoding='utf-8').read(); a = h.tidy_hero(h.tidy_tick(h.tidy_splash(h.tidy_perf(h.tidy_dock(h.tidy_rdbox(h.tidy_navorder(h.tidy_headui(o))))))))
    if a != o: open(p, 'w', encoding='utf-8').write(a)
for f in h.UNI_PAGES:
    p = os.path.join(R, f)
    if os.path.exists(p):
        o = open(p, encoding='utf-8').read(); a = h.tidy_uni(o)
        if a != o: open(p, 'w', encoding='utf-8').write(a)
# 페이지 줄 이름(실적 일정·종목 차트·주요 뉴스·AI·테크 뉴스) — 동기화 때와 같게(2026-11-01)
try:
    import site_live as _sl; _sl.rename_cal(R)
except Exception as _e:
    print('rename fail', _e)
# 종목 차트 자료를 페이지 밖 예비본으로(2026-11-01)
_pt2 = os.path.join(R, 'p-trend.html')
if os.path.exists(_pt2):
    _o = open(_pt2, encoding='utf-8').read(); _a = h.tidy_trend(_o, R)
    if _a != _o: open(_pt2, 'w', encoding='utf-8').write(_a); print('tidy trend')
# 종목 차트 등 page_tidy 정리도 다시(충돌 뒤 빠지지 않게, 2026-10-29)
try:
    import page_tidy as _pt; _pt.run(R)
except Exception as _e:
    print('page_tidy fail', _e)
