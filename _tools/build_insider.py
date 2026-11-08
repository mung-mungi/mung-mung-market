# 내부자 거래(최근 60일 공개시장 매수·매도) — 오픈인사이더 종목별 표(SEC Form 4 기반)를 받아 d/insider/insider_tx.json·coverage.json·meta.json을 고친다
# 사용자 2026-11-09 점검: 10/26에서 멈춤 → GitHub Actions(insider.yml)에서 매일 자동. 작업 공간에서는 사이트가 막혀 Actions에서만 돈다
# 받지 못한 종목이 절반을 넘으면 파일을 그대로 둔다(헛 갱신 방지). 13F(inst_13f.json)는 분기 자료라 손대지 않는다
import json, os, re, sys, time, html, subprocess, datetime as dt

R = sys.argv[1] if len(sys.argv) > 1 else '.'
D = os.path.join(R, 'd', 'insider')
UA = 'Mozilla/5.0 (mung-terminal insider sync)'
TITLE = [(r'\bCEO\b|Chief Executive', 'CEO'), (r'\bCFO\b|Chief Financial', 'CFO'), (r'\bCOO\b|Chief Operating', 'COO'), (r'\bCTO\b|Chief Technology', 'CTO'),
         (r'Chief Legal|General Counsel|\bGC\b', '법무총괄'), (r'Chief Accounting|\bCAO\b', '회계총괄'), (r'Pres', '사장'), (r'\bEVP\b|Exec(utive)? VP', '부사장'),
         (r'\bSVP\b|Senior VP', '수석부사장'), (r'\bVP\b', '부사장'), (r'COB|Chairman|Chair\b', '회장'), (r'\bDir\b|Director', '이사'), (r'10%', '10% 주주')]


def ko_title(t):
    out = []
    for pat, ko in TITLE:
        if re.search(pat, t or '', re.I) and ko not in out:
            out.append(ko)
    return '·'.join(out[:3]) or (t or '')


def get(url):
    for k in range(3):
        try:
            o = subprocess.run(['curl', '-sS', '-m', '25', '-A', UA, url], capture_output=True, text=True).stdout
            if 'tinytable' in o or 'No results' in o or 'no results' in o:
                return o
        except Exception:
            pass
        time.sleep(2 + 2 * k)
    return None


def num(s):
    s = re.sub(r'[^\d.\-]', '', s or '')
    try:
        return float(s) if s not in ('', '-', '.') else None
    except ValueError:
        return None


def rows(page):
    m = re.search(r'<table[^>]*class="tinytable"[^>]*>(.*?)</table>', page, re.S)
    if not m:
        return []
    body = m.group(1).split('</thead>')[-1]
    out = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.S):
        td = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]
        if len(td) >= 12:
            out.append(td)
    return out


def main():
    cov = json.load(open(os.path.join(D, 'coverage.json'), encoding='utf-8'))
    today = dt.date.today(); start = today - dt.timedelta(days=60)
    tx, ok, newcov = [], 0, []
    for c in cov:
        t = c['ticker']
        url = ('http://openinsider.com/screener?s=' + t + '&o=&pl=&ph=&ll=&lh=&fd=60&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1'
               '&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=200&page=1')
        pg = get(url)
        if pg is None:
            newcov.append(c); continue
        ok += 1; n = 0
        for i, td in enumerate(rows(pg)):
            # X · 신고일 · 거래일 · 티커 · 이름 · 직함 · 거래 종류 · 가격 · 수량 · 보유 · 보유 변화 · 금액
            typ = td[6]
            side = '매수' if typ.startswith('P') else '매도' if typ.startswith('S') else None
            if not side:
                continue
            trade = td[2][:10]; filed = td[1][:10]
            if trade < start.isoformat():
                continue
            sh, pr, val, own = num(td[8]), num(td[7]), num(td[11]), num(td[9])
            n += 1
            tx.append({'id': t + '-' + trade + '-' + str(n), 'trade_date': trade, 'filed_date': filed, 'ticker': t, 'company': c.get('company', t),
                       'insider': td[4], 'title': ko_title(td[5]), 'title_raw': td[5], 'side': side, 'shares': int(abs(sh)) if sh is not None else None,
                       'price_usd': pr, 'value_usd': int(abs(val)) if val is not None else None, 'owned_after': int(own) if own is not None else None,
                       'plan_10b5_1': None, 'source': 'http://openinsider.com/' + t})
        c2 = dict(c); c2['rows_in_window'] = n; c2['status'] = '집계' if c.get('status') in (None, '', '집계') else c['status']
        newcov.append(c2)
        time.sleep(1.2)
    if ok < len(cov) / 2:
        print('내부자: 받은 종목', ok, '/', len(cov), '— 이전 파일 유지'); return
    tx.sort(key=lambda x: (x['trade_date'], x['value_usd'] or 0), reverse=True)
    json.dump(tx, open(os.path.join(D, 'insider_tx.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(newcov, open(os.path.join(D, 'coverage.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    mp = os.path.join(D, 'meta.json'); m = json.load(open(mp, encoding='utf-8'))
    m0 = m[0] if isinstance(m, list) else m
    m0.update({'as_of': today.isoformat(), 'window_start': start.isoformat(), 'window_end': today.isoformat(), 'window_days': 60, 'sources': 'openinsider.com (SEC Form 4 원문 기반)'})
    json.dump(m if isinstance(m, list) else m0, open(mp, 'w', encoding='utf-8'), ensure_ascii=False)
    print('내부자:', today, '거래', len(tx), '건 · 받은 종목', ok, '/', len(cov))


if __name__ == '__main__':
    main()
