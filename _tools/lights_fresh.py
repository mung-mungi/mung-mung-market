# 시장 경고등 '멈춘 값' 표시 + 자동 한 줄(사용자 2026-10-31)
# - 지표마다 실제로 받은 자료의 날짜(src)를 적고, 기준일보다 오래됐으면 stale=True → 화면에 '⚠ 10/28 값' 칩
# - 마지막 날 켜진 불·단계·근접 지표로 '10/30 마감 · 불 1개 → 주의 · 근접: …' 한 줄을 만듦(손으로 쓴 관점 위에 붙음)
# build_lights.py 끝에서 run(R, src)로 부르고, 단독 실행도 됨: python3 -I _tools/lights_fresh.py <사이트 폴더>
import json, os, sys

STAGE = [('🟢', '평온'), ('🟡', '주의'), ('🟠', '경계'), ('🟠', '긴장'), ('🔴', '위험')]


def _load(p, d):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return d


def _last_le(dates, d):
    ks = [k for k in dates if k <= d]
    return max(ks) if ks else None


# 점수제(사용자 2026-11-01, 안 A): 켜짐 = 무게 전부, 근접(기준의 90%↑) 0.8 · 보통(80%↑) 0.4 · 양호(60%↑) 0.2 · 안전 0 을 무게에 곱해 합산.
# 유가는 WTI 100달러 이상이면 근접으로 봄. 만점 = 무게 합(12). 단계: 3 주의 · 4.5 경계 · 6 긴장 · 7.5 위험(지난 1년 중앙값 4.5, 상위 20% 6.2, 최고 7.6)
PT = {5: 1.0, 4: 0.8, 3: 0.4, 2: 0.2, 1: 0.0, 0: 0.0}
LVN = {5: '켜짐', 4: '근접', 3: '보통', 2: '양호', 1: '안전', 0: '자료 없음'}
BANDS = [(7.5, 4), (6, 3), (4.5, 2), (3, 1)]


def level(r, t, wti=None):
    n = r.get('val')
    if n is None or not t:
        return 0
    if r.get('on'):
        return 5
    v = t['value']
    if t['op'] in ('<', '<='):
        x = 1 - (n / 0.5) if v == 0 else (v / n if n else 0)
    else:
        x = n / v if v > 0 else 0
    k = 4 if x >= 0.9 else 3 if x >= 0.8 else 2 if x >= 0.6 else 1
    if r.get('id') == 'oil' and wti and wti >= 100:
        k = max(k, 4)
    return k


def score_stage(sc):
    # 단계는 점수 그대로(사용자 2026-11-02: 켜진 불 수로 깎지 않음 — 전체 점수가 더 정확함)
    for b, i in BANDS:
        if sc >= b:
            return STAGE[i]
    return STAGE[0]


def stage(s, a):
    if s >= 5 or a >= 3:
        return STAGE[4]
    if s >= 3:
        return STAGE[3]
    if s >= 2 or a >= 2:
        return STAGE[2]
    if s > 0:
        return STAGE[1]
    return STAGE[0]


def run(R, src=None):
    P = lambda *a: os.path.join(R, *a)
    log = _load(P('d/lights/lights_log.json'), [])
    th = {t['id']: t for t in _load(P('d/lights/thresholds.json'), [])}
    if not log or not th:
        return None
    D = max(r['date'] for r in log)
    L = {r['id']: r for r in log if r['date'] == D}
    src = dict(src or {})
    # 자료 파일로 알 수 있는 날짜는 직접 확인(단독 실행 때도 맞게)
    hy = [r['date'] for r in _load(P('d/bond/hy_spread.json'), [])]
    oil = [r['date'] for r in _load(P('d/lights/oil.json'), [])]
    yd = [r['date'] for r in _load(P('d/bond/yields_daily.json'), [])]
    src.setdefault('hy', _last_le(hy, D))
    src.setdefault('oil', _last_le(oil, D))
    for k in ('inv', 'y10', 'y30', 'jump'):
        src.setdefault(k, _last_le(yd, D))
    prevD = _last_le([x for x in yd if x < D], D) or D
    items = {}
    for k, r in L.items():
        t = th.get(k, {})
        s_ = src.get(k)
        # 하이일드(FRED)는 원래 하루 늦게 나옴 → 직전 거래일 값까지는 정상으로 봄
        ok = prevD if k == 'hy' else D
        items[k] = {'name': t.get('name', k), 'src': s_, 'stale': bool(s_ and ok and s_ < ok)}
    oilmap = {r['date']: r.get('wti') for r in _load(P('d/lights/oil.json'), [])}
    by = {}
    for r in log:
        by.setdefault(r['date'], []).append(r)
    hist = []
    for d in sorted(by)[-260:]:
        hist.append([d, round(sum(PT[level(r, th.get(r['id']), oilmap.get(d))] * r.get('w', 1) for r in by[d] if r['id'] in th), 1)])
    area = {}
    for k, r in L.items():
        t = th.get(k)
        if not t:
            continue
        k_ = level(r, t, oilmap.get(D))
        a_ = area.setdefault(t['board'], {'score': 0, 'max': 0, 'items': []})
        w = r.get('w', 1)
        a_['score'] += PT[k_] * w
        a_['max'] += w
        a_['items'].append({'id': k, 'name': t['name'], 'val': r.get('val'), 'th': t['value'], 'op': t['op'], 'unit': t.get('unit', ''),
                            'w': w, 'lv': LVN[k_], 'pt': round(PT[k_] * w, 2)})
        wti = oilmap.get(D)
        if k == 'oil' and wti and wti >= 100 and not r.get('on'):
            a_['items'][-1]['note'] = 'WTI %d달러(100달러 위)' % round(wti)
    for a_ in area.values():
        a_['score'] = round(a_['score'], 1)
    score = round(sum(a_['score'] for a_ in area.values()), 1)
    smax = round(sum(a_['max'] for a_ in area.values()), 1)
    on = [k for k, r in L.items() if r.get('on')]
    s = sum(L[k].get('w', 1) for k in on)
    a = len({L[k]['board'] for k in on})
    ic, nm = score_stage(score)
    near = []
    for k, r in L.items():
        t = th.get(k)
        if not t or r.get('on') or r.get('val') is None:
            continue
        v, b = r['val'], t['value']
        if t['op'] in ('>=', '>') and b and v / b >= 0.95:
            near.append(t['name'])
        elif t['op'] in ('<', '<=') and v - b <= 0.1:
            near.append(t['name'])
    md = '%d/%d' % (int(D[5:7]), int(D[8:10]))
    line = '%s 마감 · 경고등 %.1f점/%g → %s %s · 켜짐: %s' % (md, score, smax, ic, nm, '·'.join(sorted({L[k]['board'] for k in on})) or '없음')
    if near:
        line += ' · 근접: ' + '·'.join(near)
    stale = [items[k]['name'] + ' ' + '%d/%d' % (int(items[k]['src'][5:7]), int(items[k]['src'][8:10])) for k in items if items[k]['stale']]
    boards = sorted({r['board'] for r in L.values()})
    a_on = sorted({L[k]['board'] for k in on})
    a_near = sorted({th[k]['board'] for k in L if k in th and th[k]['name'] in near and th[k]['board'] not in a_on})
    out = {'date': D, 'line': line, 'stage': nm, 'on': len(on), 'near': near, 'items': items, 'stale': stale,
           'areas': len(boards), 'areas_on': a_on, 'areas_near': a_near,
           'score': score, 'score_max': smax, 'area_scores': area, 'score_hist': hist,
           'bands': [[0, '평온'], [3, '주의'], [4.5, '경계'], [6, '긴장'], [7.5, '위험']]}  # 영역 기준 표시(사용자 2026-11-01: '3/12'보다 '켜진 영역 2/5'가 직관적)
    json.dump(out, open(P('d/lights/fresh.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    for x in stale:  # GitHub 실행 주석에 남겨 멈춘 자료를 바로 알아차리게
        print('::warning::경고등 자료 멈춤 — ' + x + ' 값을 이어 쓰는 중')
    return out


if __name__ == '__main__':
    o = run(sys.argv[1] if len(sys.argv) > 1 else '.')
    print(json.dumps(o, ensure_ascii=False)[:600] if o else 'no data')
