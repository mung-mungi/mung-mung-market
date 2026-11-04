# 실적 결과 노트를 공유 사이트에 바로 올리는 도구(사용자 2026-11-04)
# 왜: 원본(실적 결과 노트 DB) → 사이트 동기화는 'DB 문서를 파일로 받기'가 막혀(다른 대화가 쓴 문서는 파일 저장 불가)
#     11/3 09:06 이후 새 노트가 사이트에 하나도 안 올라갔음. 노트를 쓴 실행이 자기 손에 있는 노트를 직접 올리면 막히지 않음.
# 사용: python3 -I _tools/note_push.py <사이트 폴더> <노트.json> [<노트.json> ...]
#   노트.json = {"id","date","ts","name","run","html","updated"} 하나 또는 그 배열
#   또는 <id>.html(본문 <article …>) + <id>.meta.json({"id","date","ts","name","run","updated"}) 짝 — html만 따로 쓰기 편하게
# 하는 일: d/notes.json과 p-earn.html의 seed(<script id="seed">)에 같은 id는 교체·새 id는 추가(id 순), stamp = 지금(UTC).
#          그다음 _tools/bump_ver.py 실행은 부르는 쪽이 함(git add d/notes.json p-earn.html version.json *.html → push_safe.sh).
import json, os, re, sys, datetime as dt

R = sys.argv[1]
SEED = re.compile(r'(<script type="application/json" id="seed">)(.*?)(</script>)', re.S)


def load_inputs(paths):
    out = []
    for p in paths:
        if p.endswith('.meta.json'):
            continue
        if p.endswith('.html'):
            mp = p[:-5] + '.meta.json'
            m = json.load(open(mp, encoding='utf-8'))
            m['html'] = open(p, encoding='utf-8').read().strip()
            out.append(m)
            continue
        j = json.load(open(p, encoding='utf-8'))
        out.extend(j if isinstance(j, list) else [j])
    for n in out:
        for k in ('id', 'date', 'html'):
            if not n.get(k):
                sys.exit('빠진 칸: %s (%s)' % (k, n.get('id')))
        if not n['html'].lstrip().startswith('<article') or n['html'].count('<article') != n['html'].count('</article>'):
            sys.exit('본문이 <article>…</article> 한 덩어리가 아님: ' + n['id'])
        if 'id="%s"' % n['id'] not in n['html'][:300]:
            sys.exit('본문 article id가 노트 id와 다름: ' + n['id'])
        n.setdefault('ts', None); n.setdefault('name', ''); n.setdefault('run', '')
        n.setdefault('updated', dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
    return out


def merge(old, new):
    by = {n['id']: n for n in old}
    for n in new:
        by[n['id']] = {k: n.get(k) for k in ('id', 'date', 'ts', 'name', 'run', 'html', 'updated')}
    return [by[k] for k in sorted(by)]


def main():
    new = load_inputs(sys.argv[2:])
    if not new:
        sys.exit('올릴 노트 없음')
    np = os.path.join(R, 'd/notes.json')
    notes = merge(json.load(open(np, encoding='utf-8')), new)
    json.dump(notes, open(np, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    pp = os.path.join(R, 'p-earn.html')
    s = open(pp, encoding='utf-8').read()
    m = SEED.search(s)
    if not m:
        sys.exit('p-earn.html에 seed가 없음')
    seed = json.loads(m.group(2).replace('<\\/', '</'))
    seed['notes'] = merge(seed.get('notes') or [], new)
    seed['stamp'] = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    body = json.dumps(seed, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + body + s[m.end(2):]
    open(pp, 'w', encoding='utf-8').write(s)
    print(json.dumps({'pushed': [n['id'] for n in new], 'total': len(seed['notes'])}, ensure_ascii=False))


main()
