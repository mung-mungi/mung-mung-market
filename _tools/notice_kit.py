# 속보 배너 키트(사용자 2026-11-01) — 중요한 일이 터졌을 때 11.1 '과한 공포 속, 기관들이 짚은 네 가지' 양식 배너를 빨리 만들고,
# 바로 공개하지 않고 주인장 자료의 🧪 검수 칸에 먼저 올려 주인장이 앱에서 보고 '공개'를 정함.
#
# 내용은 짧은 JSON 하나만 쓰면 됨(예: _tools/notice_kit_sample.json). 모양·CSS는 _tools/notice_tpl_1101.html에서 그대로 가져옴.
#   python3 -I _tools/notice_kit.py render  초안.json 결과.html          # 배너 HTML만 만들기(미리보기용)
#   python3 -I _tools/notice_kit.py draft   초안.json <저장소> <비번>     # 🧪 검수 칸에 올림(d/notice_draft.enc.json, 비번으로 잠금)
#   python3 -I _tools/notice_kit.py publish <저장소> <비번> [--keep-old]  # 검수 칸 초안을 실제 전달사항(d/notice.html)으로 공개, 검수 칸 비움
#   python3 -I _tools/notice_kit.py cand    후보.json <저장소> <비번>     # 5~6점 '후보' 한 줄만 남김
#   python3 -I _tools/notice_kit.py drop    <저장소> <비번> <id>         # 초안·후보에서 빼기
#   python3 -I _tools/notice_kit.py clear   <저장소>                      # 검수 칸 비우기
#   python3 -I _tools/notice_kit.py auto    판정.json <저장소>            # ★비번 없이(예약 작업용)★ 점수로 초안/후보/기록만을 정해 받은편지함(d/notice_inbox.json, 공개키 잠금)에 넣음 — 주인장 칸이 비번으로 풀어 합쳐 보여 줌
# 초안·후보 JSON에는 score:{time,turn,ai,mkt,conf(각 0~2), force:'무조건 사유', why:{항목:이유}}를 넣음 → 주인장 칸에 점수·이유가 보임
# 비번은 인자 대신 환경변수 OWNER_PIN으로 줘도 됨(GitHub Actions 비밀값용). 비번·평문 초안은 저장소에 절대 올리지 않음.
#
# 초안 JSON 칸: id·date·title / new(맨 위 검은 알림 줄, 선택) / cause[2줄] / k(헤드라인 묶음 제목) / hint /
#   items[{av,color,who,head(*강조*),tag,tagc,body[문단, **굵게**],links[[이름,주소]],figs[{src,cap}]}] /
#   our(🐾 해석 한 줄) / warn(⚠️ 반대 한 줄) / pills[시험대] / end(마무리 한 줄) / src[[이름,주소]](출처 접기)
#   figs.src는 저장소 안 그림 경로 또는 이미 data: 주소 — 공개할 때 휴대폰에서 깨지지 않게 data URI(폭 960·JPEG 78)로 넣음
import sys, os, re, json, html, base64, io, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TAGC = {'경고': '#d8343f', '위험': '#d8343f', '판 쪽': '#d8343f', '완화': '#2fa36b', '산 쪽': '#2fa36b', '호재': '#2fa36b',
        '수요': '#3b78e7', '확인': '#6b4fa0', '일정': '#8a6a2c'}

def esc(t): return html.escape(str(t), quote=False)
def rich(t):  # *강조* → em(빨강), **굵게** → b
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)

def style():
    s = open(os.path.join(HERE, 'notice_tpl_1101.html'), encoding='utf-8').read()
    i = s.find('<style>'); j = s.find('</style>', i)
    # 키트가 쓰는 *강조*를 원인 줄·해석·속보 줄에서도 빨강 굵게(기울임 대신)
    return s[i:j] + '.ntc-c em,.ns-our em,.ntc-p em{font-style:normal;font-weight:800;color:#b03d20}.nc-new em{font-style:normal;font-weight:900;color:#f3d48a}' + s[j:j + 8]

def img_uri(src, root):
    if src.startswith('data:'): return src
    p = src if os.path.isabs(src) else os.path.join(root, src)
    from PIL import Image
    im = Image.open(p).convert('RGB')
    if im.width > 960: im = im.resize((960, round(im.height * 960 / im.width)))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=78, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def render(d, root='.'):
    o = ['<!-- 메인 전달사항 — notice_kit.py로 만든 것(%s). 바꿀 때: data-id를 새로(새로 띄움), data-on="0"이면 내림 -->' % datetime.date.today()]
    _at = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec='minutes')  # 올린 시각 — 배너는 24시간 뒤 자동으로 빠짐(사용자 2026-11-03)
    o.append('<div id="mm-ntc-src" data-on="1" data-id="%s" data-date="%s" data-at="%s" data-title="%s">' % (esc(d['id']), esc(d['date']), _at, html.escape(d['title'])))
    o.append(style())
    if d.get('new'):
        o.append('<div class="nc-new"><span>⚡ 속보</span><b>%s</b></div>' % rich(d['new']))
    if d.get('cause'):
        o.append('<div class="ntc-cause">' + ''.join('<div class="ntc-c"><span class="b">%s</span>%s</div>' % ('①②③④'[i], rich(c)) for i, c in enumerate(d['cause'])) + '</div>')
    if d.get('items'):
        o.append('<div class="ntc-k">%s</div>' % rich(d.get('k', '짚어 볼 것')))
        o.append('<div class="ns-hint">%s</div>' % esc(d.get('hint', '누르면 근거와 원문이 펼쳐집니다')))
        for it in d['items']:
            tc = it.get('tagc') or TAGC.get(it.get('tag', ''), '#6b4fa0')
            b = ''.join('<p>%s</p>' % rich(p) for p in it.get('body', []))
            figs = it.get('figs') or []
            if figs:
                b += '<div class="nq-sw%s">' % (' m' if len(figs) > 1 else '') + ''.join(
                    '<figure class="nq-f"><img src="%s" alt=""><figcaption>%s</figcaption></figure>' % (img_uri(f['src'], root), esc(f.get('cap', ''))) for f in figs) + '</div>'
            if it.get('links'):
                b += '<span class="nq-ln">' + ''.join('<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (html.escape(u), esc(n)) for n, u in it['links']) + '</span>'
            o.append('<details class="nq"><summary role="button"><span class="nq-av" style="background:%s">%s</span><span class="nq-h"><b>%s</b> — %s</span>'
                     '<span class="nq-r"><span class="nq-tag" style="background:%s">%s</span><span class="nq-ar">자세히 ▾</span></span></summary><div class="nq-b">%s</div></details>'
                     % (it.get('color', '#3e556a'), esc(it.get('av', it['who'][:2])), esc(it['who']), rich(it['head']), tc, esc(it.get('tag', '확인')), b))
    if d.get('our'): o.append('<div class="ns-our">🐾 %s</div>' % rich(d['our']))
    if d.get('warn'): o.append('<div class="ntc-warn"><div class="ntc-p">⚠️ %s</div></div>' % rich(d['warn']))
    if d.get('pills'): o.append('<div class="ntc-pills">' + ''.join('<span class="ntc-pill">%s</span>' % esc(p) for p in d['pills']) + '</div>')
    if d.get('end'): o.append('<div class="ntc-end">%s</div>' % rich(d['end']))
    if d.get('src'):
        o.append('<details class="ns-src"><summary role="button">📎 출처 %d곳 ▾</summary><div>%s</div></details>' % (len(d['src']), ' · '.join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (html.escape(u), esc(n)) for n, u in d['src'])))
    o.append('<div class="ntc-end" style="font-size:12px;font-weight:600;color:#9a9182">투자 권유가 아닌 참고 자료입니다.</div>')
    o.append('</div>')
    return '\n'.join(o) + '\n'

# ── 잠금(주인장 자료와 같은 방식: PBKDF2-SHA256 310000회 + AES-GCM, 브라우저 owner.js가 같은 비번으로 풂)
def enc(plain, pin):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=310000).derive(pin.encode())
    b = lambda x: base64.b64encode(x).decode()
    return {'v': 1, 'iter': 310000, 'salt': b(salt), 'iv': b(iv), 'ct': b(AESGCM(key).encrypt(iv, plain.encode(), None))}

def dec(j, pin):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    u = lambda x: base64.b64decode(x)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=u(j['salt']), iterations=j['iter']).derive(pin.encode())
    return AESGCM(key).decrypt(u(j['iv']), u(j['ct']), None).decode()

# ── 올릴지 정하는 점수(사용자 2026-11-01 확정): 5항목 × 0~2점 = 10점. 7+ 초안, 5~6 후보, 4 이하 타임라인만. 무조건(force)은 점수와 상관없이 초안
RUBRIC = [('time', '시간 압박', '48시간 안 날짜=2 · 1주 안=1 · 없음=0'),
          ('turn', '판이 바뀌나', '흐름 뒤집힘=2 · 세짐=1 · 반복=0'),
          ('ai', 'AI 밸류체인 연결', '직접=2 · 유가·금리 거쳐=1 · 무관=0'),
          ('mkt', '시장 충격', '지수·유가·금리 크게=2 · 일부 업종=1 · 없음=0'),
          ('conf', '확인도', '1차·복수 매체=2 · 한 곳=1 · 미확인=0(보류)')]
FORCE = ['시장 경고등 단계 상승', '반도체 −5%·나스닥 −3%·유가 ±8% 이상', '무력 충돌 개시·재개·해협 봉쇄', '반도체·AI 수출통제 신규·큰 변경']
def grade(sc):
    sc = sc or {}
    tot = sum(int(sc.get(k, 0)) for k, _, _ in RUBRIC)
    lv = '무조건' if sc.get('force') else ('초안' if tot >= 7 else ('후보' if tot >= 5 else '타임라인만'))
    return tot, lv

def addlog(b, x, act):
    t, lv = grade(x.get('score'))
    b.setdefault('log', []).insert(0, {'at': kst(), 'title': x['title'], 'total': t, 'level': lv, 'act': act, 'note': x.get('note', '')})
    b['log'] = b['log'][:30]

def load_bundle(repo, p):
    f = os.path.join(repo, 'd', 'notice_draft.enc.json')
    if not os.path.exists(f): return {'drafts': [], 'cands': []}
    t = dec(json.load(open(f)), p)
    try: b = json.loads(t)
    except Exception: b = {'drafts': [{'id': 'old', 'title': '', 'html': t}], 'cands': []}
    b.setdefault('drafts', []); b.setdefault('cands', []); return b

def save_bundle(repo, p, b):
    for x in b['drafts'] + b['cands']:
        x['total'], x['level'] = grade(x.get('score'))
    b['rubric'] = [[k, n, h] for k, n, h in RUBRIC]; b['force'] = FORCE
    json.dump(enc(json.dumps(b, ensure_ascii=False), p), open(os.path.join(repo, 'd', 'notice_draft.enc.json'), 'w'), separators=(',', ':'))
    # 잠그지 않는 건 개수와 시각뿐(제목·내용·점수는 잠금 안에만)
    json.dump({'n': len(b['drafts']), 'c': len(b['cands']), 'at': kst()}, open(os.path.join(repo, 'd', 'notice_draft.json'), 'w'))


# ── 받은편지함(2026-11-02): 예약 작업은 비번 없이 공개키(d/notice_pub.pem)로만 잠가 d/notice_inbox.json에 넣음
#    주인장 칸(owner.js)이 비번으로 개인키(d/notice_key.enc.json)를 풀어 합쳐 보여 줌. 비번은 저장소·예약 지시문 어디에도 없음
def keygen(repo, p):
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    der = k.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    json.dump(enc(base64.b64encode(der).decode(), p), open(os.path.join(repo, 'd', 'notice_key.enc.json'), 'w'), separators=(',', ':'))
    open(os.path.join(repo, 'd', 'notice_pub.pem'), 'wb').write(k.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

def inbox_add(repo, kind, x):
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    pub = serialization.load_pem_public_key(open(os.path.join(repo, 'd', 'notice_pub.pem'), 'rb').read())
    t, lv = grade(x.get('score')); x['total'], x['level'] = t, lv
    msg = {'kind': kind, 'item': x, 'log': {'at': kst(), 'title': x['title'], 'total': t, 'level': lv, 'act': {'draft': '초안', 'cand': '후보'}.get(kind, '기록만') + '(자동)', 'note': x.get('note', '')}}
    key, iv = AESGCM.generate_key(256), os.urandom(12)
    wk = pub.encrypt(key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    b = lambda v: base64.b64encode(v).decode()
    f = os.path.join(repo, 'd', 'notice_inbox.json')
    L = json.load(open(f)) if os.path.exists(f) else []
    L.insert(0, {'k': b(wk), 'iv': b(iv), 'ct': b(AESGCM(key).encrypt(iv, json.dumps(msg, ensure_ascii=False).encode(), None))})
    json.dump(L[:40], open(f, 'w'), separators=(',', ':'))
    mf = os.path.join(repo, 'd', 'notice_draft.json')
    m = json.load(open(mf)) if os.path.exists(mf) else {'n': 0, 'c': 0}
    if kind == 'draft': m['n'] = m.get('n', 0) + 1
    if kind == 'cand': m['c'] = m.get('c', 0) + 1
    m['at'] = kst(); json.dump(m, open(mf, 'w'))
    print('📥 받은편지함', kind, x['title'], f'{t}/10 · {lv}')

def kst(): return (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=9)).strftime('%m.%d %H:%M')

def main(a):
    cmd = a[0]
    pin = lambda i: a[i] if len(a) > i and not a[i].startswith('--') else os.environ.get('OWNER_PIN', '')
    if cmd == 'render':
        d = json.load(open(a[1], encoding='utf-8')); open(a[2], 'w', encoding='utf-8').write(render(d, os.path.dirname(os.path.abspath(a[1]))))
    elif cmd in ('draft', 'cand'):
        # draft: 초안.json(배너 내용 + score) → 🧪 칸 '검수 대기' / cand: {id,title,date,score,note} → '후보' 한 줄
        d = json.load(open(a[1], encoding='utf-8')); repo = a[2]; p = pin(3)
        assert re.fullmatch(r'\d{4}', p or ''), '비번(4자리)이 필요합니다'
        b = load_bundle(repo, p); key = 'drafts' if cmd == 'draft' else 'cands'
        x = {'id': d['id'], 'title': d['title'], 'date': d.get('date', ''), 'at': kst(), 'score': d.get('score', {}), 'note': d.get('note', '')}
        if cmd == 'draft': x['html'] = render(d, repo)
        b['drafts'] = [y for y in b['drafts'] if y['id'] != d['id']]; b['cands'] = [y for y in b['cands'] if y['id'] != d['id']]
        b[key].insert(0, x); b['cands'] = b['cands'][:8]
        addlog(b, x, '초안' if cmd == 'draft' else '후보')
        save_bundle(repo, p, b); t, lv = grade(x['score'])
        print('🧪', '검수 대기' if cmd == 'draft' else '후보', x['title'], f'{t}/10 · {lv}')
    elif cmd == 'auto':
        # auto 판정.json <저장소> — 비번 없이(예약 작업용). 점수로 초안/후보/기록만을 정해 받은편지함에 넣음. 7점↑·무조건 = 초안(배너 html 포함), 5~6 = 후보, 그 아래 = 기록만
        d = json.load(open(a[1], encoding='utf-8')); repo = a[2]
        t, lv = grade(d.get('score'))
        kind = 'draft' if lv in ('초안', '무조건') else ('cand' if lv == '후보' else 'log')
        x = {'id': d['id'], 'title': d['title'], 'date': d.get('date', ''), 'at': kst(), 'score': d.get('score', {}), 'note': d.get('note', '')}
        if kind == 'draft': x['html'] = render(d, repo)
        inbox_add(repo, kind, x)
    elif cmd == 'keygen':
        repo = a[1]; p = pin(2); assert re.fullmatch(r'\d{4}', p or ''), '비번(4자리)이 필요합니다'; keygen(repo, p); print('열쇠 만듦')
    elif cmd == 'log':
        # log 판정.json <저장소> <비번> — 배너로 안 만든 판정(4점 이하 등)도 기록만 남김. 시험 기간에 '쓸데없이 울리나'를 보려는 것
        d = json.load(open(a[1], encoding='utf-8')); repo = a[2]; p = pin(3)
        assert re.fullmatch(r'\d{4}', p or ''), '비번(4자리)이 필요합니다'
        b = load_bundle(repo, p); addlog(b, {'id': d['id'], 'title': d['title'], 'score': d.get('score', {}), 'note': d.get('note', '')}, '기록만')
        save_bundle(repo, p, b)
    elif cmd == 'publish':
        # publish <저장소> <비번> [id] — id를 안 주면 맨 위 초안
        repo = a[1]; p = pin(2); want = a[3] if len(a) > 3 else ''
        b = load_bundle(repo, p)
        x = next((y for y in b['drafts'] if not want or y['id'] == want), None)
        assert x, '공개할 초안이 없습니다'
        open(os.path.join(repo, 'd', 'notice.html'), 'w', encoding='utf-8').write(x['html'])
        b['drafts'] = [y for y in b['drafts'] if y is not x]
        save_bundle(repo, p, b); print('📌 전달사항으로 공개함:', x['title'])
    elif cmd == 'drop':
        # drop <저장소> <비번> <id> — 초안·후보에서 빼기
        repo = a[1]; p = pin(2); b = load_bundle(repo, p)
        b['drafts'] = [y for y in b['drafts'] if y['id'] != a[3]]; b['cands'] = [y for y in b['cands'] if y['id'] != a[3]]
        save_bundle(repo, p, b)
    elif cmd == 'clear':
        repo = a[1]
        f = os.path.join(repo, 'd', 'notice_draft.enc.json')
        if os.path.exists(f): os.remove(f)
        json.dump({'n': 0, 'c': 0, 'at': kst()}, open(os.path.join(repo, 'd', 'notice_draft.json'), 'w'))
    else:
        print(__doc__ or open(__file__).read()[:900])

if __name__ == '__main__':
    main(sys.argv[1:])
