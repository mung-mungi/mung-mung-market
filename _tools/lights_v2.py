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
TICK = sorted({t for l in LAY for t in l[2]} | {'CL=F', 'BZ=F', 'NG=F', 'BIZD', 'HYG', 'LQD', 'IEF', '^VVIX'})


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


def lv_of(v, th):
    if v is None: return None
    r = v / th if th else 0
    return 4 if r >= 1 else 3 if r >= .9 else 2 if r >= .8 else 1 if r >= .6 else 0


def apply(R, out):
    P = lambda *a: os.path.join(R, *a)
    log = json.load(open(P('d/lights/lights_log.json'), encoding='utf-8'))
    TH = {t['id']: t for t in json.load(open(P('d/lights/thresholds.json'), encoding='utf-8'))}
    C = prices(R)
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
                    mk('oil_bw', '브렌트-WTI 차이', (b_ - w_) if (w_ and b_) else None, 8, '달러'), mk('ng', '천연가스 한 달 급등', chg('NG=F', d, 21), 30, '%')]
        A['채권·금리'] = [logit(d, k) for k in ('y10', 'why', 'y30', 'auc')]
        A['신용'] = [logit(d, 'hy', '하이일드 스프레드', 1), mk('bdc', '사모신용(BDC) 고점 대비', dd('BIZD', d), 15, '%'),
                   mk('ig_px', '투자등급 회사채 약세(국채 대비)', ddr('LQD', 'IEF', d), 5, '%'), mk('hy_px', '하이일드 회사채 약세(국채 대비)', ddr('HYG', 'IEF', d), 6, '%')]
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
                'method': '5개 영역(반도체·AI·유가·채권·금리·신용·옵션·공포)이 얼마나 찼는지의 평균 × 10'})
    json.dump(out, open(P('d/lights/fresh.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('경고등 2판: %s %.1f/10 %s' % (D, sc, nm))
    return out


if __name__ == '__main__':
    import sys
    R = sys.argv[1] if len(sys.argv) > 1 else '.'
    o = json.load(open(os.path.join(R, 'd/lights/fresh.json'), encoding='utf-8'))
    apply(R, o)
