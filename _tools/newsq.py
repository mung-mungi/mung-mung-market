# 속보 대기열 — 시험 수집(사용자 2026-11-02). Claude 크레딧 없이 GitHub 자동 갱신이 30분마다 돌림.
# 받는 곳: 1순위 외신 6곳(로이터·AP·블룸버그·WSJ·FT·CNBC) + 중동 2곳(알자지라·타임스오브이스라엘 — 중동 분류만) + 공식 발표.
# 사이트 본문(main)에는 올리지 않고 'newsq' 가지에만 쌓음(사이트 다시 만들기 한도 안 씀). 화면 표시는 시험 결과를 본 뒤 결정.
# 쓰는 법: python3 _tools/newsq.py <이전 결과 폴더> [d/newsq_done.json] → 같은 폴더에 newsq.json(최근 48시간), runs.jsonl(실행 기록)
# 흐름(사용자 2026-11-02 '속보 먼저 올리고, 거를 건 날리고, 남길 건 히스토리로'): 여기서 들어온 소식은 state 'new'(속보 줄에 보임)
#  → 2시간마다 도는 Claude 정리 작업이 하나씩 판정해 main의 d/newsq_done.json에 {id: {act:'up'|'drop', row:'eNN', why, at}} 기록
#  → 'up'은 타임라인(히스토리) 행으로 옮겨지고 속보 줄에서 빠짐, 'drop'은 이유와 함께 빠짐(기록은 남음)
import json, os, re, sys, time, urllib.parse, urllib.request, html
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/newsq'
os.makedirs(OUT, exist_ok=True)
NOW = time.time()
UA = {'User-Agent': 'Mozilla/5.0 (mung-mung-market newsq; +https://mung-mungi.github.io/mung-mung-market/)'}

TIER1 = {'reuters.com': '로이터', 'apnews.com': 'AP', 'bloomberg.com': '블룸버그', 'wsj.com': '월스트리트저널', 'ft.com': '파이낸셜타임스', 'cnbc.com': 'CNBC'}
MIDEAST = {'aljazeera.com': '알자지라', 'timesofisrael.com': '타임스오브이스라엘'}
PAYWALL = {'bloomberg.com', 'wsj.com', 'ft.com'}

# 분류 — 주요 뉴스 페이지와 같은 이름. 키워드는 제목 기준(대소문자 무시)
CATS = {
    '이란 전쟁·유가': ['iran', 'iranian', 'hormuz', 'tehran', 'irgc', 'houthi', 'houthis', 'tanker', 'tankers', 'opec', 'crude', 'oil price', 'oil prices', 'brent', 'strait'],
    '연준·정책': ['federal reserve', 'the fed', 'fed ', "fed's", 'powell', 'rate cut', 'rate hike', 'fomc', 'treasury yield', 'us inflation', 'jobs report', 'nonfarm payrolls', 'consumer prices', 'government shutdown', 'bessent'],
    '반도체 수출통제': ['export control', 'export curbs', 'entity list', 'chip export', 'chip curbs', 'bureau of industry', 'semiconductor curbs', 'chip ban', 'rare earth'],
    'AI 정책': ['ai regulation', 'ai rules', 'ai bill', 'ai act', 'ai executive order', 'ai safety', 'data center power', 'data centers', 'ai copyright', 'preemption'],
    '관세·무역': ['tariff', 'trade deal', 'trade war', 'trade talks', 'ustr', 'greer', 'section 232', 'section 301', 'customs duties'],
    '한국 관련': ['south korea', 'korean', 'seoul', 'lee jae', 'samsung', 'sk hynix', 'hyundai'],
    'AI·테크': ['nvidia', 'amd', 'tsmc', 'broadcom', 'micron', 'openai', 'anthropic', 'microsoft', 'alphabet', 'google', 'amazon', 'meta platforms', 'oracle', 'apple', 'coreweave', 'nebius', 'intel', 'marvell', 'arista', 'palantir', 'supermicro', 'super micro', 'dell', 'asml', 'applied materials', 'lam research', 'qualcomm', 'arm holdings', 'xai', 'stargate', 'data center'],
}
ME_CATS = {'이란 전쟁·유가'}
BIG = ['strike', 'attack', 'ceasefire', 'deal', 'agreement', 'sanction', 'ban', 'announces', 'approves', 'blocks', 'closes', 'seize', 'killed', 'rate cut', 'raises rates', 'cuts rates', 'tariff', 'export control', 'emergency', 'invade', 'launches', 'missile']
DROP = re.compile(r'\b(opinion|analysis|explainer|column|commentary|podcast|live:|live updates|what to know|factbox|breakingviews|newsletter|week ahead|morning bid|could|might|may|interview|review|obituary)\b|^(watch|how|why|what|where|when|who|inside|opinion|letters?)\b|where things stand|\blive\b|\bwar live\b|press release|company announcement|\bunpicking\b|missed a chance|still life|has nada|preview|on deck|risk report|takeaways|food fight|real estate boom|criticism|braces for|promises made|travel blitz|leaves no room|\?$', re.I)

# 공식 발표(되는 것만 — 실패는 runs.jsonl에 기록)
OFFICIAL = [
    ('연준', 'https://www.federalreserve.gov/feeds/press_all.xml', '연준·정책'),
    ('백악관', 'https://www.whitehouse.gov/news/feed/', None),
    ('무역대표부', 'https://ustr.gov/rss.xml', '관세·무역'),
]

def get(url, t=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read()

def gnews(q):
    u = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({'q': q, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})
    return get(u)

def items(xml):
    root = ET.fromstring(xml)
    for it in root.iter('item'):
        g = lambda k: (it.findtext(k) or '').strip()
        src = it.find('source')
        yield {'title': html.unescape(g('title')), 'link': g('link'), 'pub': g('pubDate'), 'src_url': (src.get('url') if src is not None else ''), 'src_name': (src.text if src is not None else '')}

def ts(pub):
    try: return parsedate_to_datetime(pub).timestamp()
    except Exception: return None

MATERIAL = re.compile(r'\$|billion|\bdeal\b|acquir|\bbuy\b|\bbuys\b|merger|stake|contract|agreement|\border|guidance|results|earnings|revenue|\bipo\b|raises|funding|launch|unveil|\bban\b|probe|lawsuit|antitrust|tariff|export|chip|data cent|capex|spending|layoff|ceo|plans?\b|sign', re.I)
_RX = {c: re.compile(r'\b(' + '|'.join(re.escape(k.strip()) for k in ks) + r')\b', re.I) for c, ks in CATS.items()}
def cats(title):
    cs = [c for c, rx in _RX.items() if rx.search(title)]
    if 'AI·테크' in cs and not MATERIAL.search(title):
        cs.remove('AI·테크')
    return cs

def norm(title):
    t = re.sub(r'\s+-\s+[^-]{2,40}$', '', title)  # 구글 뉴스 제목 끝 ' - 매체명' 떼기
    t = t.strip().lstrip('-–— ').strip()
    if re.fullmatch(r'(the )?times of israel|al jazeera|reuters|bloomberg|cnbc', t, re.I) or re.search(r' - (al jazeera|the times of israel)$', t, re.I):
        return ''
    return '' if len(t) < 15 else t

def key(title):
    w = re.findall(r'[a-z0-9]+', title.lower())
    stop = {'the', 'a', 'an', 'of', 'to', 'in', 'on', 'for', 'and', 'as', 'at', 'with', 'by', 'from', 'after', 'over', 'says', 'said', 'is', 'are', 'be', 'its', 'us', 'u', 's'}
    return {x for x in w if x not in stop and len(x) > 2}

log = {'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'ok': [], 'fail': [], 'raw': 0, 'kept': 0, 'dropped': {'old': 0, 'opinion': 0, 'nocat': 0, 'me_only': 0}}
raw = []
ALLKW = sorted({k.strip() for ks in CATS.values() for k in ks if len(k.strip()) > 3})
# 구글 뉴스 검색은 매체별로 한 번씩, 최근 6시간
for dom, nm in {**TIER1, **MIDEAST}.items():
    try:
        x = gnews(f'site:{dom} when:6h')
        n = 0
        for it in items(x):
            if it['src_url'] and dom not in it['src_url']:
                continue
            it['dom'] = dom; it['media'] = nm; n += 1; raw.append(it)
        log['ok'].append(f'{nm} {n}')
    except Exception as e:
        log['fail'].append(f'{nm}: {type(e).__name__} {str(e)[:60]}')
    time.sleep(1.5)
for nm, url, cat in OFFICIAL:
    try:
        x = get(url); n = 0
        for it in items(x):
            it['dom'] = 'official'; it['media'] = nm; it['force_cat'] = cat; n += 1; raw.append(it)
        log['ok'].append(f'{nm} {n}')
    except Exception as e:
        log['fail'].append(f'{nm}: {type(e).__name__} {str(e)[:60]}')

for nm, site, cat in [('재무부', 'home.treasury.gov', None), ('상무부 산업안보국', 'bis.gov', '반도체 수출통제')]:
    try:
        n = 0
        for it in items(gnews(f'site:{site} when:2d')):
            it['dom'] = 'official'; it['media'] = nm; it['force_cat'] = cat; n += 1; raw.append(it)
        log['ok'].append(f'{nm} {n}')
    except Exception as e:
        log['fail'].append(f'{nm}: {type(e).__name__} {str(e)[:60]}')
log['raw'] = len(raw)
kept = []
for it in raw:
    t = ts(it['pub'])
    if t is None or NOW - t > 6 * 3600:
        log['dropped']['old'] += 1; continue
    title = norm(it['title'])
    if not title:
        log['dropped']['opinion'] += 1; continue
    if DROP.search(title):
        log['dropped']['opinion'] += 1; continue
    cs = [it['force_cat']] if it.get('force_cat') else cats(title)
    if not cs and it['dom'] == 'official':
        cs = ['공식 발표']
    if not cs:
        log['dropped']['nocat'] += 1; continue
    if it['dom'] in MIDEAST:
        cs = [c for c in cs if c in ME_CATS]
        if not cs:
            log['dropped']['me_only'] += 1; continue
    kept.append({'title': title, 'link': it['link'], 't': int(t), 'media': it['media'], 'dom': it['dom'], 'cats': cs, 'big': any(b in title.lower() for b in BIG)})

# 같은 사건 묶기(제목 단어 겹침)
groups = []
for k in sorted(kept, key=lambda x: x['t']):
    kk = key(k['title'])
    for g in groups:
        if len(kk & g['key']) >= max(3, int(0.5 * min(len(kk), len(g['key'])))) and abs(k['t'] - g['t0']) < 8 * 3600:
            g['items'].append(k); g['key'] |= kk; break
    else:
        groups.append({'key': kk, 't0': k['t'], 'items': [k]})

DONE = {}
try:
    DONE = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else {}
except Exception:
    DONE = {}
prev = {}
try:
    for g in json.load(open(os.path.join(OUT, 'newsq.json'), encoding='utf-8')).get('items', []):
        # 이전 실행 것도 지금 규칙으로 다시 거름(규칙을 고치면 옛 오탐이 남지 않게)
        if not norm(g.get('title', '')) or DROP.search(g['title']):
            continue
        if g.get('media') not in ('연준', '백악관', '재무부', '무역대표부', '상무부 산업안보국'):
            c2 = cats(g['title'])
            if g.get('media') in MIDEAST.values():
                c2 = [c for c in c2 if c in ME_CATS]
            if not c2:
                continue
            g['cats'] = c2
        prev[g['id']] = g
except Exception:
    pass

out = []
for g in groups:
    its = g['items']
    medias = sorted({i['media'] for i in its})
    # 대표 제목: 유료 아닌 1순위 > 1순위 > 그 밖
    def rank(i):
        return (0 if i['dom'] in TIER1 and i['dom'] not in PAYWALL else 1 if i['dom'] in TIER1 else 2 if i['dom'] == 'official' else 3, i['t'])
    lead = sorted(its, key=rank)[0]
    cs = sorted({c for i in its for c in i['cats']})
    score = len(medias) * 2 + (3 if any(i['dom'] == 'official' for i in its) else 0) + (2 if any(i['big'] for i in its) else 0)
    gid = re.sub(r'[^a-z0-9]', '', lead['title'].lower())[:40] + '-' + str(min(i['t'] for i in its))[-5:]
    first = prev.get(gid, {}).get('first_seen') or log['at']
    out.append({'id': gid, 'title': lead['title'], 'link': lead['link'], 'media': lead['media'], 'others': [m for m in medias if m != lead['media']], 'n': len(medias), 'cats': cs, 'score': score, 't': min(i['t'] for i in its), 'first_seen': first, 'paywall': lead['dom'] in PAYWALL})

# 이전 실행에서 본 것 중 48시간 안 것은 남김(시험 기간 동안 무엇이 들어왔는지 모아 보기)
seen = {o['id'] for o in out}
for gid, g in prev.items():
    if gid not in seen and NOW - g.get('t', 0) < 48 * 3600:
        out.append(g)
for o in out:
    d = DONE.get(o['id'])
    o['state'] = d['act'] if d else 'new'
    if d: o['row'] = d.get('row'); o['why'] = d.get('why')

# 한글 제목(사용자 2026-11-02 '한글로 변환') — 구글 번역 무료 주소로 기계 번역(크레딧 0). 새로 들어온 것만, 한 번 번역한 건 다시 안 함.
def ko(title):
    u = 'https://translate.googleapis.com/translate_a/single?' + urllib.parse.urlencode({'client': 'gtx', 'sl': 'en', 'tl': 'ko', 'dt': 't', 'q': title})
    j = json.loads(get(u, 15).decode('utf-8'))
    return ''.join(seg[0] for seg in j[0] if seg and seg[0]).strip()
nko = 0
for o in out:
    if o.get('title_ko') and o.get('title_src') == o['title']:
        continue
    pv = prev.get(o['id'])
    if pv and pv.get('title_ko') and pv.get('title_src') == o['title']:
        o['title_ko'] = pv['title_ko']; o['title_src'] = o['title']; continue
    if nko >= 60:
        continue
    try:
        o['title_ko'] = ko(o['title']); o['title_src'] = o['title']; nko += 1
        time.sleep(0.3)
    except Exception as e:
        log.setdefault('ko_fail', 0); log['ko_fail'] = log.get('ko_fail', 0) + 1
log['ko_new'] = nko
out.sort(key=lambda x: (-x['t']))
_seen = set(); _u = []
for o in out:
    k = re.sub(r'[^a-z0-9]', '', o['title'].lower())[:60]
    if k in _seen:
        continue
    _seen.add(k); _u.append(o)
out = _u
# 시장 시황성 제목(유가·증시·달러·금·국채 '오르고 내림')은 최근 6시간 안 가장 새것 1개만 남김 — 같은 하루 흐름이 여러 줄로 반복되지 않게
WRAP = re.compile(r'\b(oil|crude|stocks?|futures|dollar|gold|treasur\w*|yields?|markets?|currenc\w*|fx|shares)\b.*\b(fall|falls|fell|drop|drops|slide|slides|rise|rises|rose|gain|gains|climb|climbs|jump|jumps|decline|declines|mixed|lower|higher|settle|settles|retreat|retreats|edge|edges|slip|slips|tumble|tumbles|rally|rallies)\b|\b(fall|falls|drop|drops|rise|rises|decline|declines|slip|slips)\b.*\b(oil|crude|stocks?|dollar|gold|yields?)\b', re.I)
_w = [o for o in out if WRAP.search(o['title']) and NOW - o['t'] < 6 * 3600]
if len(_w) > 1:
    keep = max(_w, key=lambda o: o['t'])
    keep['wraps'] = len(_w)
    out = [o for o in out if o is keep or o not in _w]
# 굵직한 사건만 표시(사용자 2026-11-02 '히스토리에 올릴 정도 굵직한 사건만 트래킹') — major 표시는 화면이 거르는 기준
MAJOR = re.compile(r'\b(strikes?|struck|attacks?|ceasefire|truce|deal|agreement|sanctions?|ban|bans|banned|blockade|seiz\w+|missiles?|invad\w+|reopen\w*|clos(e|es|ed|ure)|talks|rate cut|rate hike|raise[sd]? rates|cut[s]? rates|tariffs?|export controls?|curbs|acquir\w+|to buy|buys|merger|ipo|files? for|halt\w*|suspend\w*|resign\w*|fired|indict\w*|emergency|default|downgrade\w*|record)\b|\$\d+(\.\d+)? ?(billion|bn|trillion)|\d+ billion', re.I)
for o in out:
    o['major'] = bool((o.get('n', 1) >= 2 and not WRAP.search(o['title'])) or (o.get('media') == '연준') or (MAJOR.search(o['title']) and not WRAP.search(o['title'])))
COMMON = {'the','a','an','us','u.s.','trump','iran','iran’s',"iran's",'china','china’s','israel','oil','ai','new','after','as','in','on','for','with','says','say','exclusive:','breaking','report:','reports:','president','ambassador','united','states','america’s'}
def ent(t):
    for w in re.findall(r"[A-Z][A-Za-z0-9’'\.-]+", t):
        lw = w.lower().strip("’'.")
        if lw not in COMMON and len(lw) > 2:
            return re.sub(r"(’s|'s)$", '', lw)
    return None
_g = {}
for o in sorted([o for o in out if o.get('major') and NOW - o['t'] < 12 * 3600], key=lambda o: -o['t']):
    e = ent(o['title'])
    if not e:
        continue
    k = (e, (o.get('cats') or [''])[0])
    if k in _g:
        _g[k]['same'] = _g[k].get('same', 1) + 1
        _g[k]['n'] = max(_g[k].get('n', 1), o.get('n', 1))
        o['major'] = False; o['dup_of'] = _g[k]['id']
    else:
        _g[k] = o; o['same'] = 1
log['kept'] = len([o for o in out if o['id'] in seen])
json.dump({'at': log['at'], 'items': out}, open(os.path.join(OUT, 'newsq.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(os.path.join(OUT, 'runs.jsonl'), 'a', encoding='utf-8') as f:
    f.write(json.dumps(log, ensure_ascii=False) + '\n')
print(json.dumps(log, ensure_ascii=False))
