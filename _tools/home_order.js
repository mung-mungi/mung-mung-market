(function(){
  // 홈 '매일 아침 핵심' 버튼 순서 — 사용자 2026-10-29 지시(자주 쓰는 순). 경고등(넓은 칸)은 맨 위 그대로
  var ORDER = ['p-lights', 'p-brief', 'p-prices', 'p-earn', 'p-cal', 'p-econ', 'p-bond', 'p-opt', 'p-targets'];
  function key(a){ var m = (a.getAttribute('href') || '').match(/(p-[a-z]+)\.html/); return m ? m[1] : ''; }
  function go(){
    var first = document.querySelector('a.item[href*="p-brief.html"]'); var list = first && first.parentElement; if (!list || list.dataset.ord) return;
    var items = [].slice.call(list.querySelectorAll(':scope > a.item')); if (items.length < 3) return; list.dataset.ord = 1;
    items.sort(function(a, b){ var i = ORDER.indexOf(key(a)), j = ORDER.indexOf(key(b)); return (i < 0 ? 99 : i) - (j < 0 ? 99 : j); }).forEach(function(a){ list.appendChild(a); });
    document.querySelectorAll('a.item[href*="p-cal.html"] .ttl').forEach(function(t){ if (/실적 캘린더/.test(t.textContent)) t.textContent = '실적 일정'; });
  }
  go(); document.addEventListener('DOMContentLoaded', go); window.addEventListener('load', go);
  try { new MutationObserver(go).observe(document.documentElement, { subtree: true, childList: true }); } catch (e) {}
})();
