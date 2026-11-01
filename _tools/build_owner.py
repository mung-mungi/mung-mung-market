# 주인장 자료(사용자 2026-11-01) — 원문(평문 HTML)은 저장소에 올리지 않고, 비번으로 암호화한 d/owner.enc.json만 올림
# 사용: python3 -I _tools/build_owner.py <원문.html> <저장소경로> <비번>
# 원문 형식: <div id="mm-own-src" data-date="11.1"> ... 자료 카드 ... </div>
import sys, os, json, base64, datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

src, repo, pin = sys.argv[1], sys.argv[2], sys.argv[3]
ITER = 310000
plain = open(src, encoding='utf-8').read().encode('utf-8')
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pin.encode())
ct = AESGCM(key).encrypt(iv, plain, None)
b = lambda x: base64.b64encode(x).decode()
out = {'v': 1, 'iter': ITER, 'salt': b(salt), 'iv': b(iv), 'ct': b(ct),
       'updated': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')}
p = os.path.join(repo, 'd', 'owner.enc.json')
json.dump(out, open(p, 'w'), separators=(',', ':'))
print(p, len(ct), 'bytes')
