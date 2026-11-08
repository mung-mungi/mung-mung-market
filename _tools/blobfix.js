// 데일리 시황 그림 중 원래 아티팩트 안에서만 열리던 주소(/_blob/…)는 공유 사이트에서 깨진 그림으로 나옴 → 그 그림 칸만 숨김(2026-11-09 점검)
(function(){function go(){document.querySelectorAll('img[src*="/_blob/"]:not([data-bx])').forEach(function(i){i.dataset.bx=1;var w=i.closest('.bf-vi,figure')||i;w.style.display='none'})}
var k=0;(function t(){try{go()}catch(e){}if(++k<30)setTimeout(t,500)})();
try{new MutationObserver(go).observe(document.body,{childList:true,subtree:true})}catch(e){}})();
