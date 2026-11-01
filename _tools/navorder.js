(function(){var O=['p-lights','p-brief','p-prices','p-trend','p-earn','p-cal','p-policy','p-tech','p-econ','p-targets','p-opt','p-bond']; /* 사용자 2026-11-01: 주요 뉴스·AI·테크 뉴스를 옵션 온도계 자리로 / 2026-11-02: 채권·금리 → '채권 온도계', 옵션 온도계 옆으로 */
var NM={'p-bond':'채권 온도계'};
function key(a){var m=(a.getAttribute('href')||'').match(/(p-[a-z]+)\.html/);return m?m[1]:''}
function fx(){document.querySelectorAll('nav.ib').forEach(function(n){n.querySelectorAll(':scope>a').forEach(function(a){var k=NM[key(a)];if(k&&a.textContent!==k)a.textContent=k});if(n.dataset.ord)return;var as=[].slice.call(n.querySelectorAll(':scope>a')).filter(function(a){return O.indexOf(key(a))>=0});if(as.length<3)return;
 as.sort(function(a,b){return O.indexOf(key(a))-O.indexOf(key(b))});var after=n.querySelector(':scope>.tg')||n.querySelector(':scope>a.home');if(!after)return;as.forEach(function(a){after.after(a);after=a});n.dataset.ord=1;
 var c=n.querySelector('[aria-current=page]');if(c)try{n.scrollLeft=c.offsetLeft-n.clientWidth/2+c.offsetWidth/2}catch(e){}})}
fx();document.addEventListener('DOMContentLoaded',fx);
function ctr(){document.querySelectorAll('nav.ib').forEach(function(n){var c=n.querySelector('[aria-current=page]');if(c)n.scrollLeft=c.offsetLeft-n.clientWidth/2+c.offsetWidth/2})}
window.addEventListener('load',function(){ctr();setTimeout(ctr,300);setTimeout(ctr,1200)})})();
