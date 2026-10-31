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


def stage(s, a):
    if s >= 5 or a >= 3:
        return STAGE[4]
    if s >= 3:
        return STAGE[3]
    if s == 2 or a >= 2:
        return STAGE[2]
    if s == 1:
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
    on = [k for k, r in L.items() if r.get('on')]
    s = sum(L[k].get('w', 1) for k in on)
    a = len({L[k]['board'] for k in on})
    ic, nm = stage(s, a)
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
    line = '%s 마감 · 불 %d개%s → %s %s' % (md, len(on), ('(' + '·'.join(th[k]['name'] for k in on) + ')') if on else '', ic, nm)
    if near:
        line += ' · 근접: ' + '·'.join(near)
    stale = [items[k]['name'] + ' ' + '%d/%d' % (int(items[k]['src'][5:7]), int(items[k]['src'][8:10])) for k in items if items[k]['stale']]
    out = {'date': D, 'line': line, 'stage': nm, 'on': len(on), 'near': near, 'items': items, 'stale': stale}
    json.dump(out, open(P('d/lights/fresh.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    for x in stale:  # GitHub 실행 주석에 남겨 멈춘 자료를 바로 알아차리게
        print('::warning::경고등 자료 멈춤 — ' + x + ' 값을 이어 쓰는 중')
    return out


if __name__ == '__main__':
    o = run(sys.argv[1] if len(sys.argv) > 1 else '.')
    print(json.dumps(o, ensure_ascii=False)[:600] if o else 'no data')
