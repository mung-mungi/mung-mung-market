# 캡처 담당(사용자 2026-11-01) — GitHub 서버에서 웹페이지·PDF를 그림으로 찍어 'capture' 가지(branch)에 올림.
# Claude 작업 공간은 외부 사이트에 못 나가므로, 아이폰·아이패드만으로도 IR 슬라이드·기관 차트를 받아 오기 위한 통로.
# 입력(CAP_JOBS, JSON 배열): [{"name":"amzn_ir","url":"...","mode":"page|pdf|imgs","pages":"1-4","w":1280,"full":true,"wait":4}]
#   page: 화면 캡처(+ 페이지 안 PDF·이미지 링크 목록을 log.json에 남김) / pdf: 지정 쪽을 PNG로 / imgs: 페이지 안 큰 그림 원본 내려받기
import os, sys, json, re, subprocess, urllib.request, urllib.parse
OUT = sys.argv[1] if len(sys.argv) > 1 else '_cap'
os.makedirs(OUT, exist_ok=True)
JOBS = json.loads(os.environ.get('CAP_JOBS', '[]'))
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
log = []

def get(url, path):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=60) as r, open(path, 'wb') as f:
        f.write(r.read())
    return os.path.getsize(path)

def pdf_job(j):
    raw = os.path.join(OUT, j['name'] + '.pdf')
    get(j['url'], raw)
    a, _, b = str(j.get('pages', '1-3')).partition('-')
    b = b or a
    subprocess.run(['pdftoppm', '-r', str(j.get('dpi', 110)), '-f', a, '-l', b, '-png', raw, os.path.join(OUT, j['name'])], check=True)
    n = subprocess.run(['pdfinfo', raw], capture_output=True, text=True).stdout
    pages = re.search(r'Pages:\s+(\d+)', n)
    txt = subprocess.run(['pdftotext', '-layout', '-f', '1', '-l', str(min(int(pages.group(1)) if pages else 30, 40)), raw, '-'], capture_output=True, text=True).stdout
    open(os.path.join(OUT, j['name'] + '.txt'), 'w').write(txt[:200000])
    os.remove(raw)
    return {'pages_total': int(pages.group(1)) if pages else None}

def page_job(j, pw):
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': j.get('w', 1280), 'height': j.get('h', 900)}, user_agent=UA, device_scale_factor=j.get('scale', 2))
    pg.goto(j['url'], wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(int(j.get('wait', 4)) * 1000)
    try:
        for t in ['Accept', 'Accept all', 'I agree', 'Agree', 'Got it', 'Reject all', 'Decline']:
            el = pg.get_by_role('button', name=t)
            if el.count():
                el.first.click(timeout=1500); break
    except Exception:
        pass
    out = {}
    if j.get('selector'):
        pg.locator(j['selector']).first.screenshot(path=os.path.join(OUT, j['name'] + '.png'))
    else:
        pg.screenshot(path=os.path.join(OUT, j['name'] + '.png'), full_page=bool(j.get('full', True)))
    links = pg.eval_on_selector_all('a[href]', 'els=>els.map(e=>[e.innerText.trim().slice(0,80),e.href])')
    out['pdf_links'] = [l for l in links if re.search(r'\.pdf($|\?)', l[1], re.I)][:80]
    out['links_kw'] = [l for l in links if re.search(r'earn|result|quarter|slide|presentation|release|2026', (l[0] + l[1]), re.I)][:80]
    imgs = pg.eval_on_selector_all('img', 'els=>els.map(e=>[e.currentSrc||e.src,e.naturalWidth,e.naturalHeight,(e.alt||"").slice(0,80)])')
    out['imgs'] = [i for i in imgs if i[1] >= 400][:40]
    if j.get('mode') == 'imgs':
        got = []
        for k, (u, w, h, alt) in enumerate(out['imgs'][:12]):
            if not u.startswith('http'):
                continue
            ext = (re.search(r'\.(png|jpe?g|webp|gif)', u, re.I) or [None, 'png'])[1]
            p = os.path.join(OUT, f"{j['name']}_img{k+1}.{ext}")
            try:
                get(u, p); got.append([os.path.basename(p), u, w, h, alt])
            except Exception as e:
                got.append(['실패', u, str(e)[:80]])
        out['downloaded'] = got
    out['title'] = pg.title()
    b.close()
    return out

need_browser = any(j.get('mode', 'page') != 'pdf' for j in JOBS)
pw = None
if need_browser:
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
for j in JOBS:
    r = {'name': j.get('name'), 'url': j.get('url'), 'mode': j.get('mode', 'page')}
    try:
        r.update(pdf_job(j) if r['mode'] == 'pdf' else page_job(j, pw))
        r['ok'] = True
    except Exception as e:
        r['ok'] = False; r['err'] = str(e)[:300]
    log.append(r)
    print(r['name'], r['ok'], r.get('err', ''))
if pw:
    pw.stop()
json.dump(log, open(os.path.join(OUT, 'log.json'), 'w'), ensure_ascii=False, indent=1)
