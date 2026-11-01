// 정책·지정학 순서·일정 미리보기(사용자 2026-11-01): 오늘 한눈에 → 타임라인 → 다가오는 일정(3줄 + 펼치기) → 나머지
(function(){
function ord(){var tl=document.getElementById('tl-sec'),up=document.getElementById('up-sec'),ti=document.getElementById('tiles');if(!tl||!up||!ti)return;
 if(tl.compareDocumentPosition(ti)&Node.DOCUMENT_POSITION_FOLLOWING&&up.previousElementSibling===tl)return;ti.before(tl);ti.before(up)}
function fold(){var u=document.getElementById('up');if(!u)return;var it=[...u.querySelectorAll(':scope>.pg-upi')];var b=u.parentElement.querySelector('.mm-pf');
 if(it.length<=3){if(b)b.remove();u.classList.remove('mm-pfc');return}
 if(b&&b.dataset.n==it.length)return;if(b)b.remove();
 var open=u.classList.contains('mm-pfo');u.classList.add('mm-pfc');var h3=Math.round(it[2].getBoundingClientRect().bottom-u.getBoundingClientRect().top+2);if(h3<60)return;u.style.setProperty('--h3',h3+'px');
 b=document.createElement('button');b.type='button';b.className='mm-pf';b.dataset.n=it.length;
 var set=function(){b.textContent=u.classList.contains('mm-pfo')?'접기 ▴':'일정 '+(it.length-3)+'건 더 보기 ▾';u.style.maxHeight=u.classList.contains('mm-pfo')?u.scrollHeight+'px':'var(--h3)'};
 b.onclick=function(){u.classList.toggle('mm-pfo');set()};u.after(b);set()}
function run(){try{ord()}catch(e){}try{fold()}catch(e){}}
var k=0;(function go(){run();if(++k<15)setTimeout(go,400)})();
var u=document.getElementById('up');if(u&&window.MutationObserver){var t;new MutationObserver(function(){clearTimeout(t);t=setTimeout(run,100)}).observe(u,{childList:true})}
})();
