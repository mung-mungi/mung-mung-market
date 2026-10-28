# GitHub Actions 5분 시세 갱신(사용자 2026-10-29 지시) — 시세 보드·차트 길잡이·한국 종목
# 장 시간에만: 미국 프리(04:00)~애프터(20:00) 뉴욕 평일, 한국 09:00~15:40 평일. 그 외·주말은 쉼.
# Claude 우선: 최근 1시간 사이트 게시(커밋) 7번 이상이면 건너뜀, Claude(봇 아닌 커밋)가 10분 안에 올렸으면 쉼.
# 실적 시간대(뉴욕 06:00~09:30, 16:00~19:30)는 15분 간격.
# 결과는 live/ 에만 씀(통합본 동기화가 덮어쓰는 d/prices 와 분리). 충돌 시 최신본 받고 다시 계산.
import datetime as dt, json, os, shutil, subprocess, sys
from zoneinfo import ZoneInfo

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(R, '_tools')
BOT = 'mung-bot'
FORCE = os.environ.get('FORCE') == '1'


def sh(*a, check=True):
    return subprocess.run(a, cwd=R, capture_output=True, text=True, check=check).stdout.strip()


def window(now):
    ny = now.astimezone(ZoneInfo('America/New_York')); kr = now.astimezone(ZoneInfo('Asia/Seoul'))
    m_ny = ny.hour * 60 + ny.minute; m_kr = kr.hour * 60 + kr.minute
    us = ny.weekday() < 5 and 4 * 60 <= m_ny < 20 * 60
    ko = kr.weekday() < 5 and 9 * 60 <= m_kr < 15 * 60 + 40
    earn = ny.weekday() < 5 and (6 * 60 <= m_ny < 9 * 60 + 30 or 16 * 60 <= m_ny < 19 * 60 + 30)
    return us, ko, earn


def gate(now):
    us, ko, earn = window(now)
    if not (us or ko):
        # 장 밖이라도 통합본 동기화로 바탕이 바뀌었으면 한 번만 다시 맞춤(주말에 옛 가격으로 돌아가지 않게)
        try:
            meta = json.load(open(os.path.join(R, 'd', 'meta.json'), encoding='utf-8'))
            base = dt.datetime.fromisoformat(meta['synced']).strftime('%Y%m%d%H%M')
            st = json.load(open(os.path.join(R, 'live', 'stamp.json'), encoding='utf-8'))
            if st.get('base') == base: return 'rest: 장 시간 아님'
        except Exception:
            return 'rest: 장 시간 아님'
        earn = False
    if FORCE: return None
    log = sh('git', 'log', '-40', '--format=%ct|%an', 'origin/main').splitlines()
    ts = [(int(x.split('|')[0]), x.split('|', 1)[1]) for x in log if '|' in x]
    t0 = now.timestamp()
    if sum(1 for t, _ in ts if t0 - t < 3600) >= 7: return 'skip: 최근 1시간 게시 7번'
    human = [t for t, a in ts if a != BOT]
    if human and t0 - human[0] < 600: return 'skip: Claude가 10분 안에 올림'
    if earn:
        mine = [t for t, a in ts if a == BOT]
        if mine and t0 - mine[0] < 14 * 60: return 'skip: 실적 시간대 15분 간격'
    return None


def build():
    W = os.path.join(R, '.live_tmp'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
    for f in ('prices.json', 'history.json'):
        shutil.copy(os.path.join(R, 'd', 'prices', f), os.path.join(W, f))
    out = sh(sys.executable, '-I', os.path.join(T, 'refresh_prices.py'), 'update', os.path.join(W, 'prices.json'), os.path.join(W, 'history.json'))
    res = json.loads(out.splitlines()[-1])
    if not res.get('ok'): print('fail: 시세 받기 실패', res); return None
    sh(sys.executable, '-I', os.path.join(T, 'refresh_prices.py'), 'trendjson', os.path.join(W, 'trend.json'), os.path.join(W, 'prices.json'), os.path.join(W, 'history.json'))
    L = os.path.join(R, 'live'); os.makedirs(L, exist_ok=True)
    old = None
    try: old = json.load(open(os.path.join(L, 'prices.json'), encoding='utf-8'))
    except Exception: pass
    new = json.load(open(os.path.join(W, 'prices.json'), encoding='utf-8'))
    try: meta = json.load(open(os.path.join(R, 'd', 'meta.json'), encoding='utf-8'))
    except Exception: meta = {}
    base = dt.datetime.fromisoformat(meta['synced']).strftime('%Y%m%d%H%M') if meta.get('synced') else ''
    oldst = {}
    try: oldst = json.load(open(os.path.join(L, 'stamp.json'), encoding='utf-8'))
    except Exception: pass
    if old == new and oldst.get('base') == base:
        print('same: 시세 변화 없음', res); shutil.rmtree(W, ignore_errors=True); return None
    now = dt.datetime.now(ZoneInfo('Asia/Seoul'))
    tr = json.load(open(os.path.join(W, 'trend.json'), encoding='utf-8')); tr['at'] = now.isoformat(timespec='seconds')
    json.dump(tr, open(os.path.join(L, 'trend.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    for f in ('prices.json', 'history.json'):
        shutil.copy(os.path.join(W, f), os.path.join(L, f))
    kinds = res.get('kinds', {})
    st = {'at': now.isoformat(timespec='seconds'), 'key': now.strftime('%Y%m%d%H%M'), 'label': now.strftime('%m.%d %H:%M') + ' 기준(5분 갱신)',
          'base': base, 'files': ['prices', 'history'], 'ok': res.get('ok'), 'fail': res.get('fail', []), 'kinds': kinds}
    json.dump(st, open(os.path.join(L, 'stamp.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    shutil.rmtree(W, ignore_errors=True)
    return st


def main():
    now = dt.datetime.now(dt.timezone.utc)
    g = gate(now)
    if g: print(g); return
    for k in range(4):
        st = build()
        if not st: return
        sh('git', 'add', 'live')
        if not sh('git', 'status', '--porcelain', 'live'): print('same'); return
        sh('git', '-c', f'user.name={BOT}', '-c', 'user.email=mung-bot@users.noreply.github.com', 'commit', '-q', '-m', '시세 5분 갱신 ' + st['label'])
        if subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:main'], cwd=R).returncode == 0:
            print('pushed', st['label'], st['kinds']); return
        # 충돌: 최신본 받고 다시 계산
        sh('git', 'fetch', '-q', 'origin', 'main'); sh('git', 'reset', '-q', '--hard', 'origin/main')
        g = gate(dt.datetime.now(dt.timezone.utc))
        if g: print('retry stop:', g); return
    print('push failed 4x')


if __name__ == '__main__':
    main()
