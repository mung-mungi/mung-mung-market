// 나머지 페이지 공통 정리(사용자 2026-10-29): 숫자 칸 3열, 읽는 법·출처 접기, 넓은/긴 표는 상자 안 스크롤, 긴 설명 2줄+더 읽기, 아주 긴 목록은 상자 스크롤
(function(){
function more(p,label){if(p.dataset.u)return;p.dataset.u=1;p.classList.add('u-clamp');var b=document.createElement('button');b.type='button';b.className='u-more';b.textContent=label+' ▾';p.after(b);b.onclick=function(){p.classList.toggle('op');b.textContent=p.classList.contains('op')?'접기 ▴':label+' ▾'}}
function fx(){
 // 1) 읽는 법·출처·준비 중 카드 접기
 document.querySelectorAll('section,[class*="-card"],[class*="-sec"],.card,.panel').forEach(function(c){if(c.dataset.uf||c.closest('[data-uf]'))return;var h=c.querySelector(':scope>h2,:scope>h3,:scope>header h2,:scope>header h3,:scope>.hd h2');if(!h)return;var t=h.textContent.trim();
  if(/^(읽는 법|출처|연결 준비 중|자동 실행 규칙|\* 알아두면)/.test(t)||/^(howto|sources|src-|read-sec)/.test(c.id||'')){if(c.querySelector('canvas,svg.chart'))return;c.dataset.uf=1;c.classList.add('u-fold');h.classList.add('u-fh');h.addEventListener('click',function(){c.classList.toggle('op')})}});
 // 2) 넓은 표·긴 표: 상자 안 스크롤
 document.querySelectorAll('table').forEach(function(t){if(t.dataset.ut||!t.rows.length||!t.offsetParent)return;var p=t.parentElement;var wide=t.scrollWidth>p.clientWidth+4,long=t.rows.length>14;if(!wide&&!long)return;t.dataset.ut=1;
  var w=document.createElement('div');w.className='u-tbox'+(long?' u-long':'');t.parentNode.insertBefore(w,t);w.appendChild(t);if(wide)t.classList.add('u-wide')});
 // 3) 긴 설명 문단: 2줄 + 더 읽기
 document.querySelectorAll('p.sub,p.note,p[class$="-note"],p.m,p.nt,p[class$="-one"],p.how,p.nc-sub,.sh-guide,p.in-foot').forEach(function(p){if(p.dataset.u||p.closest('.u-fold')||p.closest('.mm-take')||p.closest('details'))return;if(p.textContent.trim().length<110)return;more(p,/how|guide/.test(p.className)?'읽는 법':'더 읽기')});
 // 4) 아주 긴 목록(타임라인·주간 일정)은 상자 안 스크롤
 document.querySelectorAll('#tl-sec .pg-card,#week,#weeks-sec .mc-card,#campus,#mix,#view').forEach(function(c){if(c.dataset.ub||c.offsetHeight<1400)return;c.dataset.ub=1;c.classList.add('u-box');var h=document.createElement('p');h.className='u-hint';h.textContent='↕ 상자 안에서 내려 보면 전체가 있습니다';c.after(h);c.addEventListener('scroll',function(){h.style.opacity=c.scrollTop+c.clientHeight>=c.scrollHeight-8?'0':'1'})});
}
var k=0;(function go(){try{fx()}catch(e){}if(++k<14)setTimeout(go,500)})();
try{var mo=new MutationObserver(function(){try{fx()}catch(e){}});mo.observe(document.body,{childList:true,subtree:true});setTimeout(function(){mo.disconnect()},20000)}catch(e){}
})();
