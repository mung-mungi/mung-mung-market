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
    o = open(p, encoding='utf-8').read(); a = h.ibdrag_place(h.tidy_hero(h.tidy_tick(h.tidy_splash(h.tidy_perf(h.tidy_dock(h.tidy_rdbox(h.tidy_navorder(h.tidy_headui(o)))))))))
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
# 종목 찾기 한글 별명·초성(2026-11-02)
for f in h.SEARCH_PAGES:
    p = os.path.join(R, f)
    if os.path.exists(p):
        o = open(p, encoding='utf-8').read(); a = h.tidy_search(o)
        if a != o: open(p, 'w', encoding='utf-8').write(a)

# 메인 머리 양식·아이디어 페이지 공통 양식도 공용 파일로(사용자 2026-11-02)
for _n, _mk, _c, _j in [('index.html', 'headui', 'headui.css', 'headui.js'), ('p-pros.html', 'uniui', 'uniui.css', 'uniui.js'), ('p-value.html', 'uniui', 'uniui.css', 'uniui.js')]:
    _p = os.path.join(R, _n)
    if os.path.exists(_p):
        _o = open(_p, encoding='utf-8').read(); _a = h.inline_to_ref(_o, _mk, _c, _j)
        if _a != _o: open(_p, 'w', encoding='utf-8').write(_a); print('tidy', _n)

# 페이지별 '쉽게 읽기'(사용자 2026-11-02)
for _n in h.EASY:
    _p = os.path.join(R, _n)
    if os.path.exists(_p):
        _o = open(_p, encoding='utf-8').read(); _a = h.tidy_easy(_o, _n)
        if _a != _o: open(_p, 'w', encoding='utf-8').write(_a); print('tidy', _n)
# 대만 8개사 작은 차트 눈금(2026-11-09)
_sp = os.path.join(R, 'p-supply.html')
if os.path.exists(_sp):
    _o = open(_sp, encoding='utf-8').read(); _a = h.tidy_supply_tw(_o)
    if _a != _o: open(_sp, 'w', encoding='utf-8').write(_a); print('tidy supply tw')
# 2026-11-09 점검 작은 고장 묶음
for _nm in ('p-qtr.html', 'p-insider.html', 'p-capex.html', 'p-prices.html', 'p-fx.html'):
    _fp = os.path.join(R, _nm)
    if os.path.exists(_fp):
        _o = open(_fp, encoding='utf-8').read(); _a = h.tidy_patch1109(_nm, _o)
        if _a != _o: open(_fp, 'w', encoding='utf-8').write(_a); print('tidy 1109', _nm)
# 시세 보드 기간 1일·1주일(2026-11-03)
_pp = os.path.join(R, 'p-prices.html')
if os.path.exists(_pp):
    _o = open(_pp, encoding='utf-8').read(); _a = h.tidy_prices_per(_o)
    if _a != _o: open(_pp, 'w', encoding='utf-8').write(_a); print('tidy prices per')
# 공매도 자료 가볍게(사용자 2026-11-03 속도 작업): 사이트에 올릴 때만 일별 공매도(sv)·종가(px)에서 화면이 안 쓰는 id·빈 값을 빼고 촘촘하게 씀.
# 원본(공매도 대시보드 자료)은 그대로 — 동기화로 다시 들어와도 여기서 다시 줄임(멱등). 약 4.9MB → 3.1MB
try:
    import json as _j
    for _f in ('sv', 'px'):
        _p = os.path.join(R, 'd', 'short', _f + '.json')
        if not os.path.exists(_p):
            continue
        _d = _j.load(open(_p, encoding='utf-8'))
        if isinstance(_d, list) and _d and isinstance(_d[0], dict) and 'id' in _d[0]:
            _o = [{k: v for k, v in r.items() if k != 'id' and v is not None} for r in _d]
            _j.dump(_o, open(_p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
            print('slim', _f)
except Exception as _e:
    print('slim fail', _e)
