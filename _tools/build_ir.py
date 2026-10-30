# IR 서재 목록 만들기 + 회사별 최근 4분기만 남기기 (사용자 2026-10-30)
# 그록봇이 d/ir/items/에 한 건당 파일 하나, PDF는 릴리스(ir-YYYYMMDD)에 올림 → 이 스크립트가 d/ir/ir.json을 다시 만듦
# 사용법: python3 -I _tools/build_ir.py <저장소> [--prune]   (--prune: 5번째 이전 분기 목록 파일·릴리스 PDF 삭제, gh CLI 필요)
import json, os, re, sys, glob, subprocess, datetime

R = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else '.'
PRUNE = '--prune' in sys.argv
KEEP = 4
D = os.path.join(R, 'd', 'ir')
OUT = os.path.join(D, 'ir.json')
TIME_ORDER = {'아시아': 0, '장전': 1, '장후': 2}
FIELDS = ['name', 'ticker', 'q', 'date', 'time', 'title', 'body', 'src', 'pdf_kr', 'pdf_orig', 'pdf_slides', 'by']


def load_items():
    good, bad = [], []
    for p in sorted(glob.glob(os.path.join(D, 'items', '*.json'))):
        try:
            x = json.load(open(p, encoding='utf-8'))
            if not isinstance(x, dict) or not x.get('name') or not x.get('ticker'):
                raise ValueError('name·ticker 없음')
            if not re.match(r'^\d{4}-\d\d-\d\d$', str(x.get('date', ''))):
                m = re.match(r'(\d{4})(\d\d)(\d\d)_', os.path.basename(p))
                if not m:
                    raise ValueError('date 형식')
                x['date'] = '%s-%s-%s' % m.groups()
            y = {k: (str(x.get(k)).strip() if x.get(k) is not None else '') for k in FIELDS}
            y['ticker'] = y['ticker'].upper()
            y['id'] = os.path.splitext(os.path.basename(p))[0]
            y['_file'] = p
            good.append(y)
        except Exception as e:
            bad.append((os.path.basename(p), str(e)))
    return good, bad


def rel_asset(url):
    m = re.search(r'/releases/download/([^/]+)/([^/?#]+)', url or '')
    return m.groups() if m else None


def prune(items):
    by = {}
    for x in items:
        by.setdefault(x['ticker'], []).append(x)
    keep, drop = [], []
    for t, xs in by.items():
        xs.sort(key=lambda x: x['date'], reverse=True)
        keep += xs[:KEEP]
        drop += xs[KEEP:]
    for x in drop:
        ok = True
        for k in ('pdf_kr', 'pdf_orig', 'pdf_slides'):
            a = rel_asset(x.get(k))
            if a:
                r = subprocess.run(['gh', 'release', 'delete-asset', a[0], a[1], '-y'], cwd=R, capture_output=True, text=True)
                gone = r.returncode == 0 or 'not found' in (r.stderr or '').lower()
                print('asset del', a, 'ok' if gone else 'fail: ' + (r.stderr or '').strip()[:120])
                ok = ok and gone
        if ok:  # PDF를 못 지웠으면 목록은 남겨 두고 다음 날 다시 시도(고아 PDF 방지)
            os.remove(x['_file']); print('item del', x['id'])
        else:
            keep.append(x)
    # 비어 버린 릴리스(ir-*) 정리
    if drop:
        r = subprocess.run(['gh', 'release', 'list', '--limit', '200', '--json', 'tagName'], cwd=R, capture_output=True, text=True)
        try:
            tags = [t['tagName'] for t in json.loads(r.stdout or '[]') if t['tagName'].startswith('ir-')]
        except Exception:
            tags = []
        for tag in tags:
            v = subprocess.run(['gh', 'release', 'view', tag, '--json', 'assets'], cwd=R, capture_output=True, text=True)
            try:
                if not json.loads(v.stdout).get('assets'):
                    subprocess.run(['gh', 'release', 'delete', tag, '-y', '--cleanup-tag'], cwd=R)
                    print('release del', tag)
            except Exception:
                pass
    return keep


PDFDIR = os.path.join(D, 'pdf')


def mirror(items):
    # 번역본 PDF를 사이트 안(d/ir/pdf/)에도 둠(사용자 2026-10-30) — 릴리스 PDF는 '내려받기'로만 열려 휴대폰·카톡에서 안 열림.
    # 사이트 안 파일은 사이트 PDF 보기 화면(돌아가기 버튼)으로 바로 열림. 용량 때문에 번역본만, 목록에서 빠진 건 같이 지움
    os.makedirs(PDFDIR, exist_ok=True)
    want = set()
    for x in items:
        # 번역본이 없는 회사(한국 회사 — 원문이 한글)는 원문 PDF를 사이트 안에 둠(사용자 2026-10-30, 릴리스로 열면 느림)
        src = x.get('pdf_kr') if rel_asset(x.get('pdf_kr')) else (x.get('pdf_orig') if not x.get('pdf_kr') and rel_asset(x.get('pdf_orig')) else '')
        if not src:
            continue
        fn = x['id'] + ('_kr.pdf' if src == x.get('pdf_kr') else '_ko.pdf'); dst = os.path.join(PDFDIR, fn); want.add(fn)
        if not os.path.exists(dst):
            r = subprocess.run(['curl', '-sSLf', '-m', '60', '-o', dst, src], capture_output=True, text=True)  # 공개 저장소라 주소로 바로 받음
            print('mirror', fn, 'ok' if r.returncode == 0 else 'fail: ' + (r.stderr or '').strip()[:120])
        if os.path.exists(dst):
            x['pdf_kr_site'] = 'd/ir/pdf/' + fn
    for f in os.listdir(PDFDIR):
        if f.endswith('.pdf') and f not in want:
            os.remove(os.path.join(PDFDIR, f)); print('mirror del', f)


def main():
    items, bad = load_items()
    if PRUNE:
        items = prune(items)
    if os.environ.get('GH_TOKEN') or os.environ.get('MIRROR'):
        mirror(items)
    else:
        for x in items:
            for sfx in ('_kr.pdf', '_ko.pdf'):
                if os.path.exists(os.path.join(PDFDIR, x['id'] + sfx)): x['pdf_kr_site'] = 'd/ir/pdf/' + x['id'] + sfx; break
    items.sort(key=lambda x: (x['date'], -TIME_ORDER.get(x['time'], 9)), reverse=True)
    for x in items:
        x.pop('_file', None)
    old = {}
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT, encoding='utf-8'))
        except Exception:
            old = {}
    note = old.get('note') or 'IR 서재 — 자동 생성 파일(손대지 말 것). 원본은 d/ir/items/*.json'
    new = {'note': note, 'items': items, 'skipped': [b[0] + ': ' + b[1] for b in bad]}
    if {k: v for k, v in old.items() if k != 'updated'} == new:
        print('no change'); return
    new['updated'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    json.dump(new, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ir.json', len(items), 'items', len(bad), 'skipped')


main()
