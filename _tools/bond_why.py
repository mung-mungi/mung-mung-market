# 채권 온도계 '금리가 움직인 이유'(사용자 2026-11-02): 불 칸 채우기보다 지금 시장에서 이 금리 움직임이 무슨 뜻인지로 점수를 매김.
# "10년물이 내려도 물가가 내려서가 아니라 기술주에서 빠진 돈이 안전자산으로 간 것이면 좋은 신호가 아니다" — 사용자.
# 최근 10거래일(2주) 10년물 변화를 물가 몫(기대 인플레 be10)과 실질 몫으로 나누고, 같은 기간 나스닥100(QQQ)·2년물·30년물을 함께 봐서 한 가지로 판정:
#   재정 우려형(장기물이 앞서 오름) · 긴축형(단기물이 앞서 오름) · 급등 · 금리 상승 · 보합 · 피난형(실질 몫 하락 + 기술주 하락) · 물가 안정형(기대 인플레가 하락의 절반 이상) · 금리 하락(주식 버팀)
# 시장 경고등 '채권·금리' 영역에서 장단기 역전(inv)·10년물 2주 급등(jump) 몫(각 1점)을 이 지표(무게 2)로 바꿈 — 12점 만점·단계 구간은 그대로.
# lights_fresh.run()이 맨 처음 부름(build_lights 끝 · 단독 실행 모두). 지난 1년 기록도 같은 규칙으로 다시 계산.
import json, os

WHY = {'id': 'why', 'board': '채권·금리', 'name': '금리 움직인 이유', 'op': '>=', 'value': 1, 'unit': '', 'weight': 2,
       'rule': '최근 2주 10년물 변화를 물가 몫·실질 몫으로 나누고 기술주·단기물·장기물과 함께 봐서 판정(재정 우려·긴축·급등 = 켜짐, 피난형은 기술주 낙폭에 따라 근접·보통)',
       'why': '같은 금리 하락이라도 물가가 내려서면 주식에 좋고, 기술주에서 빠진 돈이 안전자산으로 피한 것이면 불안 신호입니다. 금리 상승도 장기물이 앞서면(재정 우려) 성장주에 가장 나쁩니다.',
       'since': '2026-11-02', 'history': []}
OFF = ('inv', 'jump')  # 지금 시장에서 중요도 낮음(사용자 2026-11-02) — 기록·표시는 남기고 점수 무게만 0
SEV = {5: 1.0, 4: 0.92, 3: 0.82, 2: 0.65, 1: 0.0}  # 5단계(켜짐·근접·보통·양호·안전)를 공용 계산식(값÷기준)이 그대로 읽게 하는 값


def _load(p, d):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return d


def _le(rows, d, k):
    v = None
    for r in rows:
        if r['date'] > d:
            break
        if r.get(k) is not None:
            v = r
    return v


def judge(yd, be, qq, d):
    ys = [r for r in yd if r['date'] <= d and r.get('us10y') is not None]
    if len(ys) < 11:
        return None
    a, b = ys[-1], ys[-11]
    d10 = a['us10y'] - b['us10y']
    d2 = (a.get('us2y') or 0) - (b.get('us2y') or 0)
    d30 = (a.get('us30y') or 0) - (b.get('us30y') or 0)
    ea, eb = _le(be, a['date'], 'be10'), _le(be, b['date'], 'be10')
    dbe = ea['be10'] - eb['be10'] if ea and eb else None
    qa, qb = _le(qq, a['date'], 'close'), _le(qq, b['date'], 'close')
    q = (qa['close'] / qb['close'] - 1) * 100 if qa and qb and qa is not qb else None
    if abs(d10) < 0.10:
        kind, k = '보합', 2 if d10 >= 0.05 else 1
    elif d10 > 0:
        if d30 - d2 >= 0.05:
            kind, k = '재정 우려형', 5 if d10 >= 0.15 else 4
        elif d2 - d10 >= 0.05:
            kind, k = '긴축형', 4
        else:
            kind, k = '금리 상승', 2
        if d10 >= 0.25:
            k = 5
            if kind == '금리 상승':
                kind = '급등'
    else:
        if dbe is not None and dbe <= d10 * 0.5:
            kind, k = '물가 안정형', 1
        elif q is not None and q <= -2:
            kind, k = '피난형', 4 if q <= -5 else 3
        else:
            kind, k = '금리 하락', 1
    bp = lambda x: ('+' if x > 0 else '−' if x < 0 else '±') + str(abs(round(x * 100)))
    note = '10년물 2주 ' + bp(d10) + 'bp'
    if dbe is not None:
        note += '(물가 몫 ' + bp(dbe) + ' · 실질 몫 ' + bp(d10 - dbe) + ')'
    if q is not None:
        note += ' · 나스닥100 ' + ('%+.1f' % q).replace('-', '−') + '%'
    return {'k': k, 'kind': kind, 'note': note, 'd10': round(d10, 3), 'dbe': None if dbe is None else round(dbe, 3), 'q': None if q is None else round(q, 2)}


def apply(R):
    P = lambda *a: os.path.join(R, *a)
    tl = _load(P('d/lights/thresholds.json'), [])
    log = _load(P('d/lights/lights_log.json'), [])
    if not tl or not log:
        return None
    tl = [t for t in tl if t.get('id') != 'why']
    for t in tl:
        if t.get('id') in OFF:
            t['weight'] = 0
            t['weight_why'] = '지금 시장에서 중요도가 낮아 점수에서 뺌 — 기록·표시만(사용자 2026-11-02)'
    # '금리 움직인 이유'는 채권·금리 영역 맨 앞(10년물 다음)에
    i = next((n for n, t in enumerate(tl) if t.get('id') == 'y10'), len(tl) - 1)
    tl.insert(i + 1, dict(WHY))
    json.dump(tl, open(P('d/lights/thresholds.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    yd = _load(P('d/bond/yields_daily.json'), [])
    be = _load(P('d/bond/real_be.json'), [])
    qq = _load(P('d/lights/qqq_px.json'), [])
    out, last = [], None
    for r in log:
        if r.get('id') == 'why':
            continue
        if r.get('id') in OFF:
            r['w'] = 0
        out.append(r)
    dates = sorted({r['date'] for r in out})
    rows = []
    for d in dates:
        j = judge(yd, be, qq, d)
        if not j:
            continue
        rows.append({'date': d, 'board': '채권·금리', 'id': 'why', 'val': SEV[j['k']], 'on': int(j['k'] == 5), 'w': 2,
                     'kind': j['kind'], 'note': j['note']})
        last = j
    order = [t['id'] for t in tl]
    out = sorted(out + rows, key=lambda r: (r['date'], order.index(r['id']) if r['id'] in order else 99))
    json.dump(out, open(P('d/lights/lights_log.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return last


if __name__ == '__main__':
    import sys
    print(apply(sys.argv[1] if len(sys.argv) > 1 else '.'))
