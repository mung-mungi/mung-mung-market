# 연준(FRED) 자료 따로 받기(사용자 2026-11-09) — GitHub에서 FRED가 자주 막혀(긴 기간·연속 요청에 멈춤) 경고등 실행을 멈추던 문제
# 경고등 실행과 떼어 3시간마다 따로 시도: 시리즈마다 90일씩 끊어 천천히 받고, 받은 만큼 d/lights/v2_fred.json에 쌓음(크레딧 0)
# 경고등 2판(lights_v2.py)은 이 파일을 읽기만 함. 처음엔 2년 치를 몇 번에 나눠 채움
import csv, io, json, os, subprocess, sys, time, datetime as dt
R = sys.argv[1] if len(sys.argv) > 1 else '.'
P = os.path.join(R, 'd', 'lights', 'v2_fred.json')
S = {'BAMLH0A0HYM2': 'hy', 'BAMLC0A0CM': 'ig', 'BAMLH0A3HYC': 'ccc', 'WRMFNS': 'mmf_r', 'WIMFNS': 'mmf_i'}
try: C = json.load(open(P, encoding='utf-8'))
except Exception: C = {}
t0 = time.time(); got = []
for sid, k in S.items():
    m = C.get(k, {}); today = dt.date.today()
    start = today - dt.timedelta(days=730) if len(m) < 300 else today - dt.timedelta(days=45)
    a = start
    while a < today and time.time() - t0 < 600:
        b = min(today, a + dt.timedelta(days=120))
        o = subprocess.run(['curl', '--http1.1', '-sSL', '-m', '25', '-A', 'Mozilla/5.0',
                            'https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=%s&coed=%s' % (sid, a, b)], capture_output=True, text=True)
        if not o.stdout.startswith(('observation_date', 'DATE')):
            print('FRED 막힘', sid, a); break
        for r in csv.DictReader(io.StringIO(o.stdout)):
            d = r.get('observation_date') or r.get('DATE'); v = r.get(sid)
            if d and v not in (None, '', '.'): m[d] = float(v)
        a = b + dt.timedelta(days=1); time.sleep(3)
    C[k] = dict(sorted(m.items())[-800:]); got.append('%s %d' % (k, len(C[k])))
if C.get('mmf_r') and C.get('mmf_i'):
    C['mmf'] = {d: round(C['mmf_r'][d] + C['mmf_i'][d], 1) for d in C['mmf_r'] if d in C['mmf_i']}
json.dump(C, open(P, 'w', encoding='utf-8'), separators=(',', ':'))
print('FRED:', ' · '.join(got))
