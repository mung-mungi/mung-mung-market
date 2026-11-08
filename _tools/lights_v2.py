# 시장 경고등 2판 — 5개 영역 동일 가중(사용자 2026-11-09 B안 확정)
# 예전: 무게 합 12점(채권 6 · 옵션 3 · 반도체·유가·신용 1씩) → 채권이 절반, 반도체·AI는 다 켜져도 8%
# 지금: 영역마다 '얼마나 찼나'(0~100%)를 내고 다섯 영역 평균 × 10 = 10점 만점
#   반도체·AI 7(층위 6개 고점 대비 + 반도체 하루 급락) · 유가 4 · 채권·금리 4 · 신용 4 · 옵션·공포 4
# 단계 문턱은 지난 1년 울리는 빈도를 예전과 맞춤(B안): 주의 2.0 · 경계 3.1 · 긴장 4.4 · 위험 6.0
# 문턱값은 지표마다 지난 10년 분포로 잡음(반도체 층 고점 대비 30%, 네오클라우드 45%, BDC 15% …)
# lights_fresh.run() 끝에서 apply(R, out)로 부름 — fresh.json의 점수 칸만 바꿔 씀(다른 칸·기록 파일은 그대로)
import json, os, subprocess, datetime as dt

PT = [0.0, 0.2, 0.4, 0.8, 1.0]
LVN = ['안전', '양호', '보통', '근접', '켜짐']
BANDS = [[0, '평온'], [2.0, '주의'], [3.1, '경계'], [4.4, '긴장'], [6.0, '위험']]
ICON = {'평온': '🟢', '주의': '🟡', '경계': '🟠', '긴장': '🟠', '위험': '🔴'}
LAY = [('semi_design', '칩 설계', ['NVDA', 'AMD', 'AVGO'], 30),
       ('semi_mem', '메모리', ['MU', '000660.KS'], 30),
       ('semi_fab', '파운드리·장비', ['TSM', 'AMAT', 'LRCX'], 30),
       ('semi_net', '네트워크·광', ['ANET', 'COHR'], 30),
       ('semi_pwr', '전력·냉각', ['VRT', 'GEV'], 30),
       ('semi_neo', '네오클라우드', ['CRWV', 'NBIS'], 45)]
NM = {'NVDA': '엔비디아', 'AMD': 'AMD', 'AVGO': '브로드컴', 'MU': '마이크론', '000660.KS': 'SK하이닉스', 'TSM': 'TSMC', 'AMAT': '어플라이드', 'LRCX': '램리서치', 'ANET': '아리스타', 'COHR': '코히어런트', 'VRT': '버티브', 'GEV': 'GE버노바', 'CRWV': '코어위브', 'NBIS': '네비우스'}
TICK = sorted({t for l in LAY for t in l[2]} | {'CL=F', 'BZ=F', 'NG=F', 'BIZD', 'HYG', 'LQD', 'IEF', '^VVIX', '^OVX'})


def _get(u):
    o = subprocess.run(['curl', '-sSL', '-m', '25', '-A', 'Mozilla/5.0', u], capture_output=True, text=True)
    if o.returncode or not o.stdout: raise RuntimeError('fail')
    return o.stdout


def prices(R):
    p = os.path.join(R, 'd', 'lights', 'v2_px.json')
    try: C = json.load(open(p, encoding='utf-8'))
    except Exception: C = {}
    import zoneinfo
    for t in TICK:
        try:
            j = json.loads(_get('https://query1.finance.yahoo.com/v8/finance/chart/%s?range=2y&interval=1d' % t.replace('^', '%5E').replace('=', '%3D')))['chart']['result'][0]
            z = zoneinfo.ZoneInfo(j['meta'].get('exchangeTimezoneName', 'America/New_York')); now = dt.datetime.now(z)
            q = j['indicators'].get('adjclose', [{}])[0].get('adjclose') or j['indicators']['quote'][0]['close']
            m = C.get(t, {})
            for ts, c in zip(j['timestamp'], q):
                if c is None: continue
                d = dt.datetime.fromtimestamp(ts, z)
                if d.date() == now.date() and now.hour < 17: continue   # 마감 전 값은 빼기
                m[d.date().isoformat()] = round(c, 4)
            C[t] = dict(sorted(m.items())[-520:])
        except Exception as e:
            print('::warning::경고등 2판 시세 실패 ' + t)
    json.dump(C, open(p, 'w', encoding='utf-8'), separators=(',', ':'))
    return C


FRED = {'BAMLC0A0CM': 'ig', 'BAMLH0A3HYC': 'ccc', 'WRMFNS': 'mmf_r'}


def fred(R):
    """연준(FRED) 투자등급·CCC 스프레드(매일, 하루 늦음)와 MMF 잔고(매주 목요일) — HTTP/1.1로 하나씩(동시에 받으면 막힘)"""
    p = os.path.join(R, 'd', 'lights', 'v2_fred.json')
    try: C = json.load(open(p, encoding='utf-8'))
    except Exception: C = {}
    import csv, io
    # 2026-11-09: GitHub에서 FRED가 막혀 그록봇이 매일 d/xpost/fred/latest.json에 받아 둠(d/xpost/req/fred.md) → 여기서 합침
    try:
        G = json.load(open(os.path.join(R, 'd', 'xpost', 'fred', 'latest.json'), encoding='utf-8'))
        ch = 0
        for k in ('hy', 'ig', 'ccc', 'mmf_r', 'mmf_total', 'mmf_inst'):
            for d, v in (G.get(k) or {}).items():
                try: v = float(v)
                except Exception: continue
                if C.setdefault(k, {}).get(d) != v: C[k][d] = v; ch += 1
            if k in C: C[k] = dict(sorted(C[k].items())[-800:])
        if C.get('mmf_total'):   # ICI 주간 전체 MMF(개인+기관)가 있으면 그것, 없으면 개인 MMF(11/9)
            C['mmf'] = dict(C['mmf_total'])
        elif C.get('mmf_r'):
            C['mmf'] = dict(C['mmf_r'])
        if ch: json.dump(C, open(p, 'w', encoding='utf-8'), separators=(',', ':'))
    except Exception:
        pass
    return C   # 직접 받기는 fetch_fred.py(fred.yml)가 시도
    for sid, k in FRED.items():
        m = C.get(k, {})
        since = (dt.date.today() - dt.timedelta(days=45)).isoformat()   # 긴 기간은 FRED가 오래 걸려 멈춤(11/9) — 최근 45일만, 지난 기록은 따로 채움
        try:
            o = subprocess.run(['curl', '--http1.1', '-sSL', '-m', '20', '-A', 'Mozilla/5.0',
                                'https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=%s' % (sid, since)], capture_output=True, text=True)
            for r in csv.DictReader(io.StringIO(o.stdout)):
                d = r.get('observation_date') or r.get('DATE'); v = r.get(sid)
                if d and v not in (None, '', '.'): m[d] = float(v)
            if not o.stdout.startswith('observation_date') and not o.stdout.startswith('DATE'):
                print('::warning::경고등 2판 FRED 응답 없음 ' + sid + ' — 나머지 건너뜀'); break
            C[k] = dict(sorted(m.items())[-800:])
        except Exception:
            print('::warning::경고등 2판 FRED 실패 ' + sid)
    if C.get('mmf_r'):
        C['mmf'] = dict(C['mmf_r'])
    json.dump(C, open(p, 'w', encoding='utf-8'), separators=(',', ':'))
    return C


def _bat(w):
    c = w.rstrip()[-1]
    if '가' <= c <= '힣': return (ord(c) - 0xAC00) % 28 != 0
    return c.upper() in 'LMNR0136'


def _j(w, a, b):  # 받침 있으면 a, 없으면 b(은/는, 이/가, 과/와, 이라고/라고)
    return w + (a if _bat(w) else b)


def _and(xs):
    return ''.join(_j(x, '과 ', '와 ') if i < len(xs) - 2 else (x + ('' if i == len(xs) - 1 else '')) if i == len(xs) - 1 else _j(x, '과 ', '와 ') for i, x in enumerate(xs)).strip()


def review(sc, nm, area):
    """총평(사용자 2026-11-09 '시장 전체는 긴장인데 반도체만 가진 사람은 훨씬 아프다 — 오해 없게')
    영역마다 그 영역만 놓고 본 단계(같은 비율 문턱)를 매기고, 시장 전체와 얼마나 엇갈리는지 말로 풂"""
    cut = [(b / 10, t) for b, t in BANDS]
    def st(r):
        n = cut[0][1]
        for b, t in cut:
            if r >= b - 1e-9: n = t
        return n
    R = {a: v['ratio'] for a, v in area.items()}
    hot = [a for a, r in sorted(R.items(), key=lambda x: -x[1]) if r >= .6]
    cold = [a for a, r in sorted(R.items(), key=lambda x: x[1]) if r <= .15]
    spread = max(R.values()) - min(R.values()) if R else 0
    head = '시장 전체는 %s(%.1f점)' % (nm, sc)
    if hot and st(R[hot[0]]) != nm: head += ' — 그런데 %s만 보면 \'%s\'' % (_and(hot), st(R[hot[0]]))
    elif hot: head += ' — %s 쪽이 꽉 찼습니다' % _and(hot)
    body = []
    body.append('경고등 점수는 다섯 영역의 평균이라, 한 영역이 아무리 나빠도 나머지가 멀쩡하면 전체 점수는 덜 올라갑니다.')
    if hot:
        h = hot[0]; it = area[h]['items']; on = [i for i in it if i['lv'] == '켜짐']
        txt = '%s 불 %d개 중 %d개가 켜져 %d%% 찼습니다' % (_j(h, '은', '는'), len(it), len(on), round(R[h] * 100))
        if h == '반도체·AI':
            dd = sorted([i for i in it if i['id'].startswith('semi_')], key=lambda i: -(i['val'] or 0))
            if dd: txt += ' — %s가 고점보다 %.0f%%, %s가 %.0f%% 빠져 있습니다' % (dd[0]['name'].replace(' 고점 대비', ''), dd[0]['val'], dd[-1]['name'].replace(' 고점 대비', ''), dd[-1]['val'])
        body.append(txt + '.')
    if cold:
        body.append('반면 %s 거의 조용합니다(%s). 돈줄·시스템 전체가 흔들리는 위기라기보다, 특정 영역에 몰린 조정에 가깝다는 뜻입니다.' % (_j(_and(cold), '은', '는'), ' · '.join('%d%%' % round(R[a] * 100) for a in cold)))
    if hot and spread >= .5:
        body.append('그래서 반도체·AI 종목 비중이 큰 투자자라면 시장 전체 단계보다 \'%s\' 칸을 기준으로 보는 게 맞습니다. 시장 단계가 %s 해서 내 종목이 안전하다는 뜻은 아닙니다.' % (hot[0], "'" + nm + "'" + ('이라고' if _bat(nm) else '라고')))
    elif not hot:
        body.append('지금은 특별히 튀는 영역 없이 고르게 움직이고 있습니다.')
    return {'head': head, 'body': body, 'by_area': {a: st(r) for a, r in R.items()}}


def lv_of(v, th):
    if v is None: return None
    r = v / th if th else 0
    return 4 if r >= 1 else 3 if r >= .9 else 2 if r >= .8 else 1 if r >= .6 else 0


def apply(R, out):
    P = lambda *a: os.path.join(R, *a)
    log = json.load(open(P('d/lights/lights_log.json'), encoding='utf-8'))
    TH = {t['id']: t for t in json.load(open(P('d/lights/thresholds.json'), encoding='utf-8'))}
    C = prices(R)
    try: FR = fred(R)
    except Exception: FR = {}
    LOG = {}
    for r in log: LOG.setdefault(r['date'], {})[r['id']] = r
    days = sorted(LOG)[-260:]
    K = {t: sorted(C.get(t, {})) for t in C}

    def upto(t, d, n):
        ks = [k for k in K.get(t, []) if k <= d][-n:]; return ks
    def asof(t, d):
        ks = upto(t, d, 1); return C[t][ks[-1]] if ks else None
    def dd(t, d, n=252):
        ks = upto(t, d, n)
        if len(ks) < 20: return None
        return (1 - C[t][ks[-1]] / max(C[t][k] for k in ks)) * 100
    def ddr(a, b, d):   # a/b 비율의 고점 대비 낙폭(회사채 ETF ÷ 국채 ETF)
        ks = [k for k in upto(a, d, 252) if k in C.get(b, {})]
        if len(ks) < 20: return None
        s = [C[a][k] / C[b][k] for k in ks]; return (1 - s[-1] / max(s)) * 100
    def chg(t, d, n):
        ks = upto(t, d, n + 1)
        return (C[t][ks[-1]] / C[t][ks[0]] - 1) * 100 if len(ks) == n + 1 else None
    def lvl1y(t, d):
        ks = upto(t, d, 252)
        return (C[t][ks[-1]] / (sum(C[t][k] for k in ks) / len(ks)) - 1) * 100 if len(ks) >= 100 else None
    def logv(d, k):
        r = LOG.get(d, {}).get(k); return None if r is None else r.get('val')
    def logit(d, k, name=None, w=None):   # 예전 경고등 지표 그대로(켜짐 판정·무게는 기준표)
        r = LOG.get(d, {}).get(k); t = TH.get(k)
        if not r or not t or r.get('val') is None: return None
        if r.get('on'): L = 4
        else: L = lv_of(r['val'], t['value']) if t['op'] in ('>=', '>') else (4 if r['val'] < t['value'] else 0)
        it = {'id': k, 'name': name or t['name'], 'val': r['val'], 'th': t['value'], 'op': t['op'], 'unit': t.get('unit', ''), 'w': w or t.get('weight', 1), 'L': L}
        if r.get('kind'): it['kind'] = r['kind']; it['note'] = r['kind'] + ' — ' + r.get('note', '')
        return it
    def mk(i, name, v, th, unit, w=1):
        return None if v is None else {'id': i, 'name': name, 'val': round(v, 2), 'th': th, 'op': '>=', 'unit': unit, 'w': w, 'L': lv_of(v, th)}

    def areas(d):
        A = {}
        semi = []
        for i, nm, ts, th in LAY:
            v = [x for x in (dd(t, d) for t in ts) if x is not None]
            x = mk(i, nm + ' 고점 대비', sum(v) / len(v) if v else None, th, '%')
            if x: x['who'] = ' · '.join(NM.get(t, t) for t in ts)
            semi.append(x)
        semi.append(logit(d, 'soxday', '반도체 하루 급락(최근 5일)', 1))
        A['반도체·AI'] = semi
        w_, b_ = asof('CL=F', d), asof('BZ=F', d)
        A['유가'] = [logit(d, 'oil', '유가 한 달 급등', 1), mk('oil_lvl', 'WTI 1년 평균 대비 높이', lvl1y('CL=F', d), 14, '%'),
                    mk('oil_bw', '중동 위험 웃돈(브렌트-WTI 차이)', (b_ - w_) if (w_ and b_) else None, 8, '달러'), mk('ovx', '유가 출렁임(OVX)', asof('^OVX', d), 60, ''), mk('ng', '천연가스 한 달 급등', chg('NG=F', d, 21), 30, '%')]
        A['채권·금리'] = [logit(d, k) for k in ('y10', 'why', 'y30', 'auc')]
        def fv(k):
            m = FR.get(k) or {}; ks = [x for x in m if x <= d]
            return m[max(ks)] if ks and max(ks) >= (dt.date.fromisoformat(d) - dt.timedelta(days=10)).isoformat() else None
        def mmf4(d):   # MMF 잔고 4주 증가율(위험자산에서 현금으로 숨는 돈)
            m = FR.get('mmf') or {}; ks = sorted(x for x in m if x <= d)
            return (m[ks[-1]] / m[ks[-5]] - 1) * 100 if len(ks) >= 5 and ks[-1] >= (dt.date.fromisoformat(d) - dt.timedelta(days=14)).isoformat() else None
        ig, ccc = fv('ig'), fv('ccc')
        A['신용'] = [logit(d, 'hy', '하이일드 스프레드', 1),
                   mk('ig', '투자등급 스프레드', ig, 1.5, '%p') if ig is not None else mk('ig_px', '투자등급 회사채 약세(국채 대비)', ddr('LQD', 'IEF', d), 5, '%'),
                   mk('ccc', '최저등급(CCC) 스프레드', ccc, 14, '%p') if ccc is not None else mk('hy_px', '하이일드 회사채 약세(국채 대비)', ddr('HYG', 'IEF', d), 6, '%'),
                   mk('bdc', '사모신용(BDC) 고점 대비', dd('BIZD', d), 15, '%'), mk('mmf', 'MMF 잔고 4주 급증', mmf4(d), 3, '%')]
        A['옵션·공포'] = [logit(d, 'vix', 'VIX', 1), logit(d, 'term', '기간구조 뒤집힘', 1), logit(d, 'pc', '풋콜 비율 높음', 1), mk('vvix', 'VVIX', asof('^VVIX', d), 115, '')]
        return {a: [x for x in v if x and x['L'] is not None] for a, v in A.items()}

    def score(A):
        rs = []
        for v in A.values():
            sw = sum(x['w'] for x in v)
            rs.append(sum(PT[x['L']] * x['w'] for x in v) / sw if sw else 0)
        return round(sum(rs) / len(rs) * 10, 1) if rs else 0

    def stage(s):
        n = BANDS[0][1]
        for b, t in BANDS:
            if s >= b - 1e-9: n = t
        return n

    hist = []
    for d in days:
        try: hist.append([d, score(areas(d))])
        except Exception: pass
    D = days[-1]; A = areas(D); sc = score(A); nm = stage(sc)
    prev = areas(days[-2]) if len(days) > 1 else {}
    PL = {x['id']: LVN[x['L']] for v in prev.values() for x in v}
    area = {}
    for a, v in A.items():
        sw = sum(x['w'] for x in v); sp = sum(PT[x['L']] * x['w'] for x in v)
        area[a] = {'score': round(sp, 1), 'max': sw, 'ratio': round(sp / sw, 3) if sw else 0,
                   'items': [dict({k: x[k] for k in x if k != 'L'}, lv=LVN[x['L']], pt=round(PT[x['L']] * x['w'], 2)) for x in v]}
    on = [x for v in A.values() for x in v if x['L'] == 4]
    near = [x['name'] for v in A.values() for x in v if x['L'] == 3]
    a_on = sorted({a for a, v in A.items() if any(x['L'] == 4 for x in v)})
    md = '%d/%d' % (int(D[5:7]), int(D[8:10]))
    line = '%s 마감 · 경고등 %.1f점/10 → %s %s · 켜진 영역: %s' % (md, sc, ICON[nm], nm, '·'.join(a_on) or '없음')
    if near: line += ' · 근접: ' + '·'.join(near[:4])
    out.update({'ver': 2, 'date': D, 'line': line, 'stage': nm, 'on': len(on), 'near': near, 'score': sc, 'score_max': 10,
                'area_scores': area, 'score_hist': hist, 'bands': BANDS, 'areas': len(area), 'areas_on': a_on,
                'areas_near': sorted({a for a, v in A.items() if a not in a_on and any(x['L'] == 3 for x in v)}),
                'prev_lv': PL, 'prev_date': days[-2] if len(days) > 1 else None,
                'method': '5개 영역(반도체·AI·유가·채권·금리·신용·옵션·공포)이 얼마나 찼는지의 평균 × 10',
                'review': review(sc, nm, area)})
    json.dump(out, open(P('d/lights/fresh.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('경고등 2판: %s %.1f/10 %s' % (D, sc, nm))
    return out


if __name__ == '__main__':
    import sys
    R = sys.argv[1] if len(sys.argv) > 1 else '.'
    o = json.load(open(os.path.join(R, 'd/lights/fresh.json'), encoding='utf-8'))
    apply(R, o)
