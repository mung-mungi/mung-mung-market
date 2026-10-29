# 아이디어 페이지 2종(저평가 서치·고수 성적표) 껍데기 만들기(사용자 2026-10-29)
# 내부자·기관 페이지(p-insider.html)의 머리·독·공통 장치는 그대로 쓰고, 가운데 본문만 우리 것으로 바꿈
# 자료는 d/ideas/*.json(_tools/build_ideas.py)을 열 때 불러옴 → 매일 json만 새로 만들면 됨
# 사용: python3 -I _tools/make_idea_pages.py <사이트 폴더>
import os, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
T = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(R, 'p-insider.html'), encoding='utf-8').read()
CSS = open(os.path.join(T, 'ideas.css'), encoding='utf-8').read()
JS = open(os.path.join(T, 'ideas.js'), encoding='utf-8').read()
PAGES = {
 'p-value': {'title': '저평가 서치', 'desc': '사이트에 쌓인 목표주가·실적·밸류·수급 자료로 불 7개를 켜 보는 아이디어 서치(공사중)',
  'body': '''
<div class="in-wrap iv-wrap">
  <header id="top" class="in-mast">
    <p class="in-eyebrow"><i aria-hidden="true"></i>아이디어 · 공사중 샘플</p>
    <h1 class="in-h1"><span class="m">저평가 서치</span> <span class="s">사슬 · 재무 · 자리</span></h1>
    <p class="in-take" id="take"><b id="take-chip">—</b><span id="take-text">불러오는 중</span></p>
  </header>
  <section class="in-tiles" id="tiles"></section>
  <div class="iv-tabs" id="tabs"><button type="button" data-t="find" class="on">종목 찾기</button><button type="button" data-t="my">내 종목 점검</button><button type="button" data-t="heat">반도체 온도판</button></div>
  <div class="iv-tab" id="t-find">
  <section class="in-card"><h3>불 많이 켜진 순</h3>
    <p class="sub">추천 목록이 아니라 '한번 들여다볼 만한 곳'을 고르는 체입니다. 아래에서 어떤 불을 셀지 직접 고를 수 있고, 줄을 누르면 불마다 근거 숫자가 펼쳐집니다.</p>
    <div class="iv-pick" id="pickbox"></div>
    <div class="iv-pills" id="cat"></div>
    <div class="iv-seg" id="sort"></div>
    <div class="iv-list" id="list"></div>
  </section>
  <section class="in-card in-read" id="read-card"><h3>불 7개는 이렇게 읽습니다</h3>
    <div class="in-read-grid"><div class="in-read-col"><ul>
      <li><b>목표가 여력</b> 증권사 평균 목표가가 지금 주가보다 20% 이상 위.</li>
      <li><b>같은 층 대비 싸다</b> 선행 PER이 같은 층(예: 메모리끼리) 가운데값보다 10% 이상 낮음. 같은 층이 3곳 미만이면 전체 가운데값과 비교.</li>
      <li><b>실적 탄력</b> 가장 최근 분기 매출이 예상보다 높고, 전년비 +15% 이상.</li>
      <li><b>고점 대비 눌림</b> 1년 최고가보다 15% 이상 낮은 자리.</li>
    </ul></div><div class="in-read-col"><ul>
      <li><b>목표가 오름세</b> 최근 60일 목표가 상향이 2건 이상이고 하향의 2배 넘음.</li>
      <li><b>고수 상향</b> '고수 성적표' 적중률 상위 10곳 중 한 곳이라도 최근 60일 안에 상향.</li>
      <li><b>수급 개선</b> 공매도 잔고 감소, 기관 보유 비중 증가, 내부자 순매수 가운데 하나 이상.</li>
      <li><b>사슬 확인</b> 같은 층 동료들이 최근 실적에서 AI 매출을 잘 빼고 있고, 이 종목 자신도 실적·AI 판정으로 확인될 때.</li>
      <li><b>재무 체력</b> 몸값·성장·이익률·현금흐름·빚을 묶은 재무 등급이 A·B일 때('내 종목 점검' 탭과 같은 기준).</li>
      <li><b>주의</b> 눌림 불은 '떨어지는 칼'일 수도 있습니다. 3개월 새 30% 넘게 빠진 곳은 따로 표시합니다.</li>
    </ul></div></div>
    <p class="how">자료: 사이트에 이미 쌓인 목표주가 기록·분기 실적·시세(선행 PER 포함)·공매도·13F·내부자 거래, 그리고 미국 증권거래위원회(SEC) 공식 재무 자료. 매수·매도 권유가 아닙니다.</p>
  </section>
  </div>
  <div class="iv-tab" id="t-my" hidden>
  <section class="in-card"><h3>내 종목 점검</h3>
    <p class="sub">담았거나 관심 있는 종목을 고르면 사슬 → 재무 → 자리 순서로 점검합니다. 앞 관문이 흔들리면 자리가 좋아도 '물타기 멈춤'을 띄웁니다. 고른 목록은 이 휴대폰에만 저장됩니다.</p>
    <div id="mypick"></div>
  </section>
  <div class="iv-list" id="mylist"></div>
  </div>
  <div class="iv-tab" id="t-heat" hidden>
  <section class="in-card" id="soxx"></section>
  <section class="in-card" id="layers"></section>
  <section class="in-card" id="bt"></section>
  </div>
</div>'''},
 'p-pros': {'title': '고수 성적표', 'desc': '증권사 의견을 3개월 뒤 실제 주가로 채점한 적중률 순위·최근 상향·큰손 포트폴리오(공사중)',
  'body': '''
<div class="in-wrap iv-wrap">
  <header id="top" class="in-mast">
    <p class="in-eyebrow"><i aria-hidden="true"></i>아이디어 · 공사중 샘플</p>
    <h1 class="in-h1"><span class="m">고수 성적표</span> <span class="s">적중률 순위</span></h1>
    <p class="in-take" id="take"><b id="take-chip">—</b><span id="take-text">불러오는 중</span></p>
  </header>
  <section class="in-tiles" id="tiles"></section>
  <section class="in-card"><h3>증권사 적중률 순위</h3>
    <p class="sub">의견을 낸 날부터 3개월(63거래일) 뒤, 나스닥100(QQQ)보다 의견 방향대로 갔으면 '적중'입니다. 줄을 누르면 1개월 적중률·최고 적중 사례가 펼쳐집니다.</p>
    <div class="iv-seg" id="rsort"></div>
    <div class="iv-list" id="rank"></div>
  </section>
  <section class="in-card"><h3>잘 맞히는 곳의 최근 상향</h3>
    <p class="sub">적중률 상위 10곳이 최근 45일 안에 올린 의견입니다. 오른쪽 숫자는 그날 이후 주가 변화입니다.</p>
    <div class="iv-list" id="recent"></div>
  </section>
  <section class="in-card"><h3>큰손 포트폴리오</h3>
    <div class="iv-seg" id="btab"></div>
    <div class="iv-list" id="big"></div>
  </section>
  <section class="in-card in-read" id="read-card"><h3>성적표는 이렇게 읽습니다</h3>
    <div class="in-read-grid"><div class="in-read-col"><ul>
      <li><b>채점 대상</b> 목표가 상향·투자의견 상향·매수 신규는 '오른다', 목표가 하향·의견 하향·매도 신규는 '내린다'로 봅니다. 의견 유지는 채점하지 않습니다.</li>
      <li><b>적중</b> 3개월 뒤 그 종목 수익률에서 나스닥100 수익률을 뺀 값이 의견 방향과 같으면 적중.</li>
      <li><b>평균 초과수익</b> 의견 방향으로 본 초과수익(%p)의 평균. 높을수록 맞힐 때 크게 맞힌 곳입니다.</li>
    </ul></div><div class="in-read-col"><ul>
      <li><b>종합 순위</b> 적중률(건수 적으면 가운데로 당겨 운빨 보정) + 평균 초과수익. 3개월이 다 지난 의견이 8건 이상인 곳만 올립니다.</li>
      <li><b>한계</b> 지금 자료는 증권사 단위입니다. 애널리스트 개인 이름 순위는 이름을 함께 모으며 쌓아 갈 예정입니다. 한국·대만 종목 의견은 기준 지수가 달라 채점에서 뺐습니다.</li>
      <li><b>강세장 주의</b> 지난 1년 AI 강세장이라 '오른다' 의견이 유리했습니다. 하향을 잘 맞힌 곳은 따로 보시면 좋습니다.</li>
    </ul></div></div>
    <p class="how">자료: 사이트 목표주가 기록(최근 1년)과 일별 종가로 직접 계산했습니다. 큰손은 상황인식(레오폴드) 13F·기관 보유 변화·내부자 거래 공시입니다. 매수·매도 권유가 아닙니다.</p>
  </section>
</div>'''},
}
a = src.find('<div id="dash-root"'); b = src.find('<script data-tick>')
assert a > 0 and b > a
for key, P in PAGES.items():
    s = src[:a] + '<div id="dash-root" data-dash-state="ready"><style data-ideas>' + CSS + '</style>' + P['body'] + '<script data-ideas>window.__IDEA__="' + key + '";' + JS + '</script></div>' + src[b:]
    s = re.sub(r'window\.__PAGE__=\{[^<]*?\};', 'window.__PAGE__={"page": "' + key[2:] + '", "ds": [], "params": {}};', s, 1)
    s = re.sub(r'<title>[^<]*</title>', '<title>' + P['title'] + ' · 멍뭉 터미널</title>', s, 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + P['title'], s, 1)
    s = re.sub(r'(<meta property="og:url" content="[^"]*?)p-insider\.html', r'\1' + key + '.html', s, 1)
    # 페이지 줄(nav.ib): 현재 표시를 옮기고, 끝에 '아이디어' 묶음
    i = s.find('<nav class="ib"'); j = s.find('</nav>', i)
    nav = s[i:j].replace(' aria-current="page"', '')
    nav = re.sub(r'<span class="tg">아이디어</span>.*$', '', nav, flags=re.S)
    ver = (re.search(r'\?v=(\d+)', nav) or [None, ''])[1]
    q = ('?v=' + ver) if ver else ''
    nav += '<span class="tg">아이디어</span>' + ''.join('<a href="%s.html%s"%s>%s</a>' % (k, q, ' aria-current="page"' if k == key else '', PAGES[k]['title']) for k in PAGES)
    s = s[:i] + nav + s[j:]
    open(os.path.join(R, key + '.html'), 'w', encoding='utf-8').write(s)
    print('made', key)
