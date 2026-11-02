# 실적 일정 '지난달' 보기 자료(사용자 2026-11-02) — p-earn.html 실적 카드를 한국에서 받아 본 날 기준으로 월별로 쌓아 d/cal_arc.json에 씀
# 실적 결과 페이지에서 오래된 카드가 빠져도 한 번 쌓인 기록은 지우지 않음(새 값이 같은 id를 덮어씀)
import datetime as D, html, json, os, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
P = os.path.join(R, 'd/cal_arc.json')
s = open(os.path.join(R, 'p-earn.html'), encoding='utf-8').read().replace('\\"', '"')
try: tm = {x['name']: x for x in json.load(open(os.path.join(R, 'd/qtr/earnings.json'), encoding='utf-8')) if (x.get('report_date') or '') >= '2026-10-01'}
except Exception: tm = {}
try: old = {x['id']: x for x in json.load(open(P, encoding='utf-8')).get('items', [])}
except Exception: old = {}
TOP = ['마이크로소프트', '알파벳', '아마존', '메타', '애플', '엔비디아', '테슬라', 'TSMC', 'SK하이닉스', '삼성전자', 'AMD', '브로드컴', 'ASML']
for m in re.finditer(r'<article\b([^>]*)>', s):
    a = dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
    i = (re.search(r'\bid="([^"]+)"', m.group(1)) or [None, ''])[1]
    if not i or not a.get('name') or not a.get('date'): continue
    nm, _, tk = html.unescape(a['name']).rpartition(' ')
    if not nm: nm, tk = tk, ''
    asia = bool(re.search(r'\d', tk)) or tk == 'TSM'
    ts = a.get('ts', '')
    if asia: slot = '아시아'
    elif ts: slot = '장전' if ts[11:13] < '12' else '장후'
    else: slot = (tm.get(nm) or {}).get('timing') or ''
    d = D.date.fromisoformat(a['date'])
    if slot == '장후': d += D.timedelta(1)   # 미국 장 마감 뒤 발표는 한국에서 다음 날 새벽에 받음
    sm = html.unescape(a.get('sum', ''))
    v = re.search(r'AI 관점 ([가-힣]+)', sm)
    old[i] = {'id': i, 'n': nm, 'd': d.isoformat(), 's': slot, 'v': v.group(1) if v else '',
              'x': re.sub(r'^AI 관점 [가-힣]+(\([^)]*\))?\s*·?\s*', '', sm)[:64], 'r': TOP.index(nm) if nm in TOP else 99, 'ts': ts}
it = sorted(old.values(), key=lambda x: x['d'] + '%02d' % x['r'] + x['ts'])
json.dump({'n': len(it), 'items': it}, open(P, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('cal arc', len(it))
