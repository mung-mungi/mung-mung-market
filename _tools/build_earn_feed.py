# 실적 결과 새 소식 목록(사용자 2026-10-29) — p-earn.html의 실적 카드(article)에서 이름·시각만 뽑아 d/earn_feed.json으로
# 메인 화면·독이 이걸 보고 '새 실적 n곳'을 띄움(본 사람은 실적 결과 페이지를 열면 꺼짐)
import json, os, re, sys, html
R = sys.argv[1] if len(sys.argv) > 1 else '.'
s = open(os.path.join(R, 'p-earn.html'), encoding='utf-8').read().replace('\\"', '"')
out, seen = [], set()
for m in re.finditer(r'<article\b([^>]*)>', s):
    a = dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
    i = (re.search(r'\bid="([^"]+)"', m.group(1)) or [None, ''])[1]
    if not a.get('ts') or not a.get('name') or i in seen: continue
    seen.add(i)
    nm = html.unescape(a['name']); nm = re.sub(r'\s+[A-Z0-9.]{1,6}$', '', nm).strip()
    out.append({'id': i, 'name': nm, 'ts': a['ts'], 'date': a.get('date', a['ts'][:10]), 'sum': html.unescape(a.get('sum', ''))[:90]})
out.sort(key=lambda x: x['ts'], reverse=True)
json.dump({'n': len(out), 'latest': out[0]['ts'] if out else '', 'items': out[:30]}, open(os.path.join(R, 'd/earn_feed.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('earn feed', len(out), out[0]['ts'] if out else '-', [o['name'] for o in out[:5]])
