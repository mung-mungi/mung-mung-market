(function(){
/* 아이폰 사파리: 숨긴 열이 있는 표에서 펼침 줄(colspan)이 숨은 열 폭까지 잡아 표가 찌그러지는 문제 — 펼침 줄 colspan을 보이는 열 수로 맞춤 */
function fix(){var ts=document.querySelectorAll('table');for(var i=0;i<ts.length;i++){var t=ts[i],hs=t.querySelectorAll('thead th');if(!hs.length)continue;var n=0;for(var j=0;j<hs.length;j++)if(getComputedStyle(hs[j]).display!=='none')n++;if(!n)n=hs.length;var cs=t.querySelectorAll('tbody td[colspan]');for(var k=0;k<cs.length;k++){if(cs[k].colSpan!==n)cs[k].colSpan=n}}}
var q=0;function later(){if(q)return;q=1;requestAnimationFrame(function(){q=0;fix()})}
document.addEventListener('click',function(){setTimeout(fix,0);setTimeout(fix,120)},true);
try{new MutationObserver(later).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['class']})}catch(e){}
window.addEventListener('load',fix);setTimeout(fix,600);setTimeout(fix,2000);
})();