// 메인 13칸 재구성(사용자 2026-11-09 점검 '다 순서대로 해보자') — home_order.js가 순서·이름을 잡은 뒤(.mm-compact) 한 번 더 정리
// ① 시세 보드 + 종목 차트 → '시세·차트' ② 실적 결과 + 실적 일정 → '실적' ③ 주요 뉴스 + AI·테크 뉴스 → '뉴스' ④ 공매도 + 내부자·기관 → '수급'
// ⑤ 이름 정리(아시아 반도체 수출·빅테크 설비투자·아시아 통화) ⑥ 헤더 종목 수 = 시세 보드 기준 ⑦ 경고등 줄 아래 '꽉 찬 곳 · 조용한 곳'
// 합친 칸 안의 작은 알약(.mm-sub)은 각자 원래 페이지로 감(카드 전체는 첫 페이지로)
(function(){
  if (!/(^|\/)(index\.html)?$/.test(location.pathname)) return;
  function $(s, r){ return (r || document).querySelector(s); }
  function card(k){ return $('a.item[href*="' + k + '.html"]'); }
  function el(t, c, x){ var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function j(u){ return fetch(u + '?t=' + Math.floor(Date.now() / 3e5), { cache: 'no-store' }).then(function(r){ return r.ok ? r.json() : null; }).catch(function(){ return null; }); }
  function first(s, n){ s = String(s || '').replace(/\*\*/g, ''); var m = s.match(/^[^.]*?(다|요)\./); s = m ? m[0] : s; return s.length > n ? s.slice(0, n - 1) + '…' : s; }
  function sub(href, label, text){ var s = el('span', 'mm-sub'); s.dataset.go = href; s.setAttribute('role', 'link'); s.appendChild(el('b', '', label + ' ›')); if (text) s.appendChild(document.createTextNode(' ' + text)); return s; }
  function hl(a){ var h = a.querySelector('.hl'); if (!h) { h = el('div', 'hl'); a.appendChild(h); } return h; }
  function ttl(a, t){ var x = a.querySelector('.ttl'); if (x && x.firstChild && x.firstChild.nodeType === 3) x.firstChild.textContent = t; else if (x) x.textContent = t; }
  function recount(){ document.querySelectorAll('nav.list').forEach(function(n){ var sh = n.previousElementSibling, sp = sh && sh.querySelector('span'); if (sp && /\d/.test(sp.textContent)) sp.textContent = sp.textContent.replace(/\d+/, String(n.querySelectorAll(':scope > a.item').length)); }); }
  var D = {}, done = false;
  // A안(사용자 2026-11-09 '스크롤 편의성' — 칸 높이는 그대로, [가|나] 버튼으로 그 자리에서 내용만 바뀜, 칸을 누르면 고른 쪽 페이지로)
  function ls(k, v){ try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function merge(main, other, name, lines, def){ var a = card(main), b = card(other); if (!a) return; if (a.dataset.v2) return; a.dataset.v2 = 1; ttl(a, name);
    var opts = lines.filter(Boolean).map(function(l){ return { go: l.dataset.go, k: l.querySelector('b').textContent.replace(' ›', ''), t: l.textContent.replace(l.querySelector('b').textContent, '').trim() }; });
    var vq = (a.getAttribute('href') || '').match(/\?v=\d+/); vq = vq ? vq[0] : '';
    var h = hl(a); h.classList.remove('mm-two'); h.classList.add('mm-segt');
    var seg = el('span', 'mm-seg'); seg.setAttribute('role', 'tablist');
    var key = 'mm_seg_' + main, cur = +(ls(key) || (def != null ? def : 0)); if (!opts[cur]) cur = 0;
    function pick(i){ cur = i; [].forEach.call(seg.children, function(x, j){ x.classList.toggle('on', j === i); x.setAttribute('aria-selected', j === i); }); h.textContent = opts[i].t || ''; a.setAttribute('href', opts[i].go + vq); }
    opts.forEach(function(o, i){ var bt = el('button', '', o.k); bt.type = 'button'; bt.setAttribute('role', 'tab'); bt.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); pick(i); ls(key, String(i)); }, true); seg.appendChild(bt); });
    a.querySelector('.top').after(seg); pick(cur); if (b) b.remove(); }
  function run(){
    if (done || !document.documentElement.classList.contains('mm-compact')) return false;
    var pr = card('p-prices'); if (!pr) return false; done = true;
    // ① 시세·차트 — 위 '종목 차트' 긴 줄은 없애고 카드 안 알약으로
    var tb = $('a.mm-bar[href*="p-trend"]'); if (tb) tb.remove();
    merge('p-prices', 'p-trend-none', '시세·차트', [sub('p-prices.html', '시세', (D.n || 83) + '종목 종가·기간 등락·52주 위치'), sub('p-trend.html', '차트', '지지·저항·매물대 바로 보기')]);
    // ② 실적
    var hc = (D.hub && D.hub.cards) || {};
    var kh = new Date(Date.now() + 9 * 36e5).getUTCHours();
    merge('p-earn', 'p-cal', '실적', [sub('p-earn.html', '결과', first((hc.results || {}).line, 46)), sub('p-cal.html', '일정', first((hc.calendar || {}).line, 46))], kh >= 5 && kh < 12 ? 0 : 1);
    // ③ 뉴스
    merge('p-policy', 'p-tech', '뉴스', [sub('p-policy.html', '시장·정책', first(D.pol && D.pol.headline, 44)), sub('p-tech.html', 'AI·테크', first(D.tech && D.tech.headline, 44))]);
    // ④ 수급 — 공매도 칸에 내부자·기관을 합침
    merge('p-short', 'p-insider', '수급', [sub('p-short.html', '공매도', first((hc.shorts || {}).line, 40)), sub('p-insider.html', '내부자', '임원 매수·매도 · 기관 13F 보유 변화')]);
    // ⑤ 이름 정리 + 설비투자는 분기 묶음으로
    var sp = card('p-supply'); if (sp) ttl(sp, '아시아 반도체 수출');
    var fx = card('p-fx'); if (fx) { ttl(fx, '아시아 통화'); var fh = hl(fx); fh.textContent = '원·대만달러·엔 — 아시아 반도체로 드나드는 외국인 돈의 방향을 봅니다'; }
    var cx = card('p-capex'); if (cx) { ttl(cx, '빅테크 설비투자'); var nq = card('p-neo'); if (nq && nq.parentElement !== cx.parentElement) nq.parentElement.insertBefore(cx, nq); }
    // ⑥ 헤더 종목 수
    var dt = $('p.dt'); if (dt && D.n) dt.innerHTML = dt.innerHTML.replace(/\d+종목/, D.n + '종목');
    // ⑦ 경고등 아래 한 줄
    var lb = $('a.mm-bar[href*="p-lights"]'), F = D.F;
    if (lb && F && F.ver3 && F.area_scores && !$('.mm-lt-line')) {
      var A = Object.keys(F.area_scores).map(function(k){ return [k, F.area_scores[k].ratio]; }).sort(function(x, y){ return y[1] - x[1]; });
      var hot = A.filter(function(x){ return x[1] >= .55; }), calm = A.filter(function(x){ return x[1] < .3; });
      var ln = el('a', 'mm-lt-line'); ln.href = 'p-lights.html#area-card';
      if (hot.length) { ln.appendChild(el('span', 'k', '꽉 찬 곳')); ln.appendChild(el('b', 'hot', hot.map(function(x){ return x[0] + ' ' + Math.round(x[1] * 100) + '%'; }).join(' · '))); }
      if (calm.length) { ln.appendChild(el('span', 'k', '조용한 곳')); ln.appendChild(el('b', 'calm', calm.map(function(x){ return x[0] + ' ' + Math.round(x[1] * 100) + '%'; }).join(' · '))); }
      lb.after(ln);
    }
    recount(); return true;
  }
  document.addEventListener('click', function(e){ var s = e.target.closest && e.target.closest('.mm-sub[data-go]'); if (!s) return; e.preventDefault(); e.stopPropagation(); var a = s.closest('a'); var v = a && (a.getAttribute('href') || '').match(/\?v=\d+/); location.href = s.dataset.go + (v ? v[0] : ''); }, true);
  Promise.all([j('d/hub.json'), j('d/policy/meta.json'), j('d/tech/meta.json'), j('d/lights/fresh.json'), j('d/prices/prices.json')]).then(function(r){
    D.hub = r[0]; D.pol = r[1] && r[1][0]; D.tech = r[2] && r[2][0]; D.F = r[3];
    try { var P = r[4]; if (Array.isArray(P)) D.n = P.length; } catch (e) {}
    var k = 0; (function go(){ var ok = false; try { ok = run(); } catch (e) { ok = true; } if (!ok && ++k < 60) setTimeout(go, 250); })();
  });
})();
