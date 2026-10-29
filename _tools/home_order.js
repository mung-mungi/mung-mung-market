(function(){
  // 홈 정리 — 사용자 2026-10-29 지시
  // ① '매일 아침 핵심' 버튼 순서(자주 쓰는 순) ② 경고등·차트 길잡이는 맨 위 가로 슬림 2줄 ③ 카드는 아래 버튼 없이 제목 옆 › (여백은 조금)
  var ORDER = ['p-brief', 'p-prices', 'p-earn', 'p-cal', 'p-econ', 'p-bond', 'p-opt', 'p-targets'];
  function key(a){ var m = (a.getAttribute('href') || '').match(/(p-[a-z]+)\.html/); return m ? m[1] : ''; }
  function bar(item, label, mid){
    var a = document.createElement('a'); a.className = 'mm-bar'; a.href = item.getAttribute('href');
    var c = (item.getAttribute('style') || '').match(/--c\s*:\s*([^;]+)/); a.style.setProperty('--c', c ? c[1].trim() : '#9a6200');
    var ic = item.querySelector('.ic'); if (ic) a.appendChild(ic.cloneNode(true));
    var b = document.createElement('b'); b.textContent = label; a.appendChild(b);
    var m = document.createElement('span'); m.className = 'mid'; m.innerHTML = mid; a.appendChild(m);
    var r = document.createElement('span'); r.className = 'ar'; r.textContent = '›'; a.appendChild(r);
    return a;
  }
  function lightsMid(L){
    var t = (L.querySelector('.hl') || L).textContent.replace(/\s+/g, ' ');
    var n = t.match(/불\s*(\d+)\s*\/\s*(\d+)/), st = t.match(/(평온|주의|경계|긴장|위험)/);
    var col = !st ? '#2f9a4c' : /주의/.test(st[1]) ? '#b08a00' : /경계|긴장/.test(st[1]) ? '#d9822b' : /위험/.test(st[1]) ? '#c4453a' : '#2f9a4c';
    return (n ? '불 ' + n[1] + '/' + n[2] : '') + (st ? ' · <em style="color:' + col + '">● ' + st[1] + '</em>' : '');
  }
  var busy = false;
  // 아이디어 페이지 묶음(공사중) — 메인 화면 맨 아래에 붙임(사용자 2026-10-29)
  function ideas(){
    if (document.querySelector('a.item[href^="p-value"]')) return;
    var last = document.querySelector('a.item[href^="p-insider"]'); if (!last) return;
    var grp = last.closest('nav.list') && last.closest('nav.list').parentElement; if (!grp) return;
    var vq = ((last.getAttribute('href') || '').match(/\?v=\d+/) || [''])[0];
    var IC = {v:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/><path d="M8 13l2-2 2 1.5L14.5 9"/></svg>',
      p:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8"/><path d="M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3"/><path d="M7 5H4v2a3 3 0 0 0 3 3"/></svg>'};
    function card(h, ic, t, w, hl, g){ return '<a class="item" style="--c:#c2410c" href="' + h + vq + '"><div class="top"><div class="ic" aria-hidden="true">' + ic + '</div><div><div class="ttl">' + t + ' <em class="mm-wip">공사중</em></div><div class="when">' + w + '</div></div></div><div class="hl">' + hl + '</div><div class="go">' + g + '<span aria-hidden="true">→</span></div></a>'; }
    var d = document.createElement('div'); d.className = 'mm-ideas';
    d.innerHTML = '<p class="sh">아이디어 · 공사중<span>2개</span></p><nav class="list">'
      + card('p-value.html', IC.v, '저평가 서치', '불 7개 · 내 기준 고르기', '목표가·실적·밸류·수급 불을 켜서 들여다볼 종목을 넓혀 봅니다', '서치 보기')
      + card('p-pros.html', IC.p, '고수 성적표', '증권사 적중률 · 큰손 포트폴리오', '의견을 3개월 뒤 주가로 채점한 순위와 잘 맞히는 곳의 최근 상향을 봅니다', '성적표 보기') + '</nav>';
    grp.after(d);
  }
  function go(){ try { ideas(); } catch (e) {}
    if (busy) return; busy = true;
    try {
      var first = document.querySelector('a.item[href*="p-brief.html"]'); var list = first && first.parentElement;
      if (!list || list.dataset.ord2) return;
      var L = list.querySelector('a.item[href*="p-lights"]'); if (!L || !/불\s*\d/.test(L.textContent)) return; // 경고등 숫자가 그려진 뒤에
      list.dataset.ord2 = 1;
      var C = document.querySelector('a.item[href*="p-trend"]');
      var box = document.createElement('div'); box.className = 'mm-bars';
      box.appendChild(bar(L, '시장 경고등', lightsMid(L))); L.remove();
      if (C) { box.appendChild(bar(C, '종목 차트', '지지·저항 바로 보기')); C.remove(); }
      var sh = list.previousElementSibling; (sh || list).before(box);
      [].slice.call(list.querySelectorAll(':scope > a.item')).sort(function(a, b){ var i = ORDER.indexOf(key(a)), j = ORDER.indexOf(key(b)); return (i < 0 ? 99 : i) - (j < 0 ? 99 : j); }).forEach(function(a){ list.appendChild(a); });
      var SHORT = {'p-cal': '실적 일정', 'p-opt': '옵션 온도계', 'p-neo': '네오클라우드', 'p-supply': '한국·대만 실적', 'p-qtr': '분기 실적 추이', 'p-insider': '내부자·기관', 'p-capex': '설비투자', 'p-econ': '경제지표'};
      document.querySelectorAll('a.item .ttl').forEach(function(t){ var k = key(t.closest('a.item')); if (SHORT[k]) t.textContent = SHORT[k]; });
      document.documentElement.classList.add('mm-compact');
    } finally { busy = false; }
  }
  var st = document.createElement('style');
  st.textContent = '.mm-bars{display:flex;flex-direction:column;gap:8px;margin:0 0 10px}'
   + '.mm-bar{display:flex;align-items:center;gap:10px;height:52px;padding:0 14px 0 10px;background:var(--panel,#fff);border-radius:14px;border:1px solid var(--line,rgba(0,0,0,.08));border-left:4px solid var(--c);text-decoration:none;color:inherit;box-shadow:0 3px 0 rgba(30,22,8,.08),0 6px 14px rgba(30,22,8,.06)}'
   + '.mm-bar .ic{width:34px!important;height:34px!important;border-radius:10px!important;flex:none}.mm-bar .ic svg{width:20px!important;height:20px!important}'
   + '.mm-bar b{font-size:16px;font-weight:800;white-space:nowrap}.mm-bar .mid{margin-left:auto;font-size:13.5px;color:var(--muted,#6b675f);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.mm-bar .mid em{font-style:normal;font-weight:700}'
   + '.mm-bar .ar{font-size:24px;line-height:1;color:var(--c);font-weight:700;margin-left:2px}'
   + '.mm-compact .list .item:not(.wide){padding:13px 12px 12px!important}'
   + '.mm-compact .list .item .top{gap:9px!important;align-items:center!important}'
   + '.mm-compact .list .item .ic{width:30px!important;height:30px!important;border-radius:9px!important}.mm-compact .list .item .ic svg{width:18px!important;height:18px!important}'
   + '.mm-compact .list .item .ttl{font-size:15.5px!important;line-height:1.25!important}'
   + '.mm-compact .list .item .top>div:last-child{flex:1;min-width:0}'
   + '.mm-compact .list .item .top::after{content:"›";flex:none;margin-left:auto;font-size:22px;line-height:1;font-weight:700;color:var(--c)}'
   + '.mm-compact .list .item .hl{font-size:13px!important;line-height:1.5!important;margin:9px 0 0!important;-webkit-line-clamp:2!important}'
   + '.mm-compact .list .item .go{display:none!important}'
   + '.mm-compact .list{gap:10px!important}'
   + '.mm-wip{font-style:normal;display:inline-block;vertical-align:2px;margin-left:4px;padding:2px 6px;border-radius:6px;background:#e07a12;color:#fff;font-size:10.5px;font-weight:800;letter-spacing:-.02em}';
  (document.head || document.documentElement).appendChild(st);
  go(); document.addEventListener('DOMContentLoaded', go); window.addEventListener('load', go);
  var q = 0; try { new MutationObserver(function(){ if (q) return; q = 1; setTimeout(function(){ q = 0; go(); }, 80); }).observe(document.documentElement, { subtree: true, childList: true }); } catch (e) {}
})();
