# 아시아 통화(원·대만달러·엔) + 달러지수 계산용 교차 환율 — 야후 일별 종가 1년(사용자 2026-11-09 점검: 환율 자료가 10/26에서 멈춤, 대만달러 추가)
# 쓰는 파일: d/fx/usdkrw.json(date·usdkrw·usdjpy·usdtwd), d/fx/crosses.json(date·eur·jpy·gbp·cad·sek·chf) — 페이지가 읽던 모양 그대로
# 사용: python3 -I _tools/build_fx.py .   (GitHub Actions lights.yml에서 매일, 실패하면 이전 파일 유지)
import json, os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refresh_prices as rp

R = sys.argv[1] if len(sys.argv) > 1 else '.'
SYM = {'usdkrw': 'KRW=X', 'usdjpy': 'JPY=X', 'usdtwd': 'TWD=X', 'eur': 'EUR=X', 'gbp': 'GBP=X', 'cad': 'CAD=X', 'sek': 'SEK=X', 'chf': 'CHF=X'}
SRC = 'https://finance.yahoo.com/quote/'


def series(sym):
    r = rp.get('https://query1.finance.yahoo.com/v8/finance/chart/' + sym.replace('=', '%3D') + '?range=1y&interval=1d')
    if not r:
        return {}
    ts, cl = r.get('timestamp') or [], ((r.get('indicators') or {}).get('quote') or [{}])[0].get('close') or []
    out = {}
    for t, c in zip(ts, cl):
        if c is None:
            continue
        d = dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%d')
        out[d] = round(float(c), 5)
    return out


def main():
    S = {k: series(v) for k, v in SYM.items()}
    if len(S['usdkrw']) < 100:
        print('환율: 원·달러를 받지 못해 이전 파일 유지'); return
    days = sorted(S['usdkrw'])
    def last(k, d):
        s = S[k]
        if d in s:
            return s[d]
        ks = [x for x in s if x <= d]
        return s[max(ks)] if ks else None
    kr = [{'date': d, 'usdkrw': round(S['usdkrw'][d], 2), 'usdjpy': round(last('usdjpy', d) or 0, 2) or None,
           'usdtwd': round(last('usdtwd', d) or 0, 3) or None, 'basis': '야후 종가(뉴욕 기준)', 'source': SRC + 'KRW=X/history'} for d in days]
    cr = [{'date': d, 'eur': last('eur', d), 'jpy': last('usdjpy', d), 'gbp': last('gbp', d), 'cad': last('cad', d), 'sek': last('sek', d), 'chf': last('chf', d),
           'source': SRC + 'EUR=X/history'} for d in days]
    cr = [c for c in cr if all(c[k] for k in ('eur', 'jpy', 'gbp', 'cad', 'sek', 'chf'))]
    for nm, rows in (('usdkrw.json', kr), ('crosses.json', cr)):
        p = os.path.join(R, 'd', 'fx', nm)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print('환율:', days[-1], '원', kr[-1]['usdkrw'], '대만달러', kr[-1]['usdtwd'], '엔', kr[-1]['usdjpy'], '·', len(kr), '일')


if __name__ == '__main__':
    main()
