(function(){
/* 아이폰 사파리: 숨긴 열이 있는 표에서 펼침 줄(colspan)이 숨은 열 폭까지 잡아 표가 찌그러지는 문제 — 펼침 줄 colspan을 보이는 열 수로 맞춤 */
function fix(){var ts=document.querySelectorAll('table');for(var i=0;i<ts.length;i++){var t=ts[i],hs=t.querySelectorAll('thead th');if(!hs.length)continue;var n=0;for(var j=0;j<hs.length;j++)if(getComputedStyle(hs[j]).display!=='none')n++;if(!n)n=hs.length;var cs=t.querySelectorAll('tbody td[colspan]');for(var k=0;k<cs.length;k++){if(cs[k].colSpan!==n)cs[k].colSpan=n}}}
var q=0;function later(){if(q)return;q=1;requestAnimationFrame(function(){q=0;fix()})}
document.addEventListener('click',function(){setTimeout(fix,0);setTimeout(fix,120)},true);
/* 반응 속도(사용자 2026-11-01): 예전엔 페이지 어디든 class가 바뀌면(누름 효과·메뉴 숨김 등) 매번 표 전체를 다시 훑었음 → 표 안이 바뀌었을 때·html의 class가 바뀔 때만 */
function rel(m){for(var i=0;i<m.length;i++){var t=m[i].target;if(t===document.documentElement)return 1;if(t.nodeType===1&&(t.tagName==='TABLE'||(t.closest&&t.closest('table'))))return 1;if(m[i].type==='childList'){var a=m[i].addedNodes;for(var j=0;j<a.length;j++){var n=a[j];if(n.nodeType===1&&(n.tagName==='TABLE'||(n.querySelector&&n.querySelector('table'))))return 1}}}return 0}
try{new MutationObserver(function(m){if(rel(m))later()}).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['class']})}catch(e){}
window.addEventListener('load',fix);setTimeout(fix,600);setTimeout(fix,2000);
})();