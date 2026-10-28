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
 document.querySelectorAll('#tl-sec .pg-card,#weeks-sec .mc-card,#campus,#mix,#view').forEach(function(c){if(c.dataset.ub||c.offsetHeight<1400)return;c.dataset.ub=1;c.classList.add('u-box');var h=document.createElement('p');h.className='u-hint';h.textContent='↕ 상자 안에서 내려 보면 전체가 있습니다';c.after(h);c.addEventListener('scroll',function(){h.style.opacity=c.scrollTop+c.clientHeight>=c.scrollHeight-8?'0':'1'})});
}
var k=0;(function go(){try{fx()}catch(e){}if(++k<14)setTimeout(go,500)})();
try{var mo=new MutationObserver(function(){try{fx()}catch(e){}});mo.observe(document.body,{childList:true,subtree:true});setTimeout(function(){mo.disconnect()},20000)}catch(e){}
})();
// 공매도 '오늘 한눈에'를 3줄로(사용자 2026-10-29)
(function(){function fx(){var t=document.querySelector('#take.sh-take');if(!t||t.querySelector('.sh3'))return;var b=[].slice.call(t.querySelectorAll(':scope>b'));if(b.length<4)return;var tx=t.textContent;var tail=(tx.split('→')[1]||'').trim().replace(/\.$/,'');
 var ul=document.createElement('ul');ul.className='sh3';ul.innerHTML='<li><i>많이 쌓인 곳</i><span><b>'+b[0].textContent+'</b></span></li><li><i>요즘 몰리는 곳</i><span><b>'+b[1].textContent+'</b> <small style="color:#6f6d68">(최근 5일)</small></span></li><li><i>전체 흐름</i><span>늘어난 <span class="up">'+b[2].textContent.replace(/[^\d]/g,'')+'</span> · 줄어든 <span class="dn">'+b[3].textContent.replace(/[^\d]/g,'')+'</span>곳 → '+tail.replace(/^밸류체인 전체로는\s*/,'')+'</span></li>';t.appendChild(ul);t.classList.add('sh-rows')}
var k=0;(function go(){try{fx()}catch(e){}if(++k<14)setTimeout(go,500)})()})();

// 공매도 표: '22.3 (추정)' → 숫자 + 작은 '추정' 표시, 안내 문구 새로(사용자 2026-10-29)
(function(){function fx(){var t=document.getElementById('tbl');if(!t)return;t.querySelectorAll('tbody td:nth-child(5)').forEach(function(td){var m=td.textContent.match(/^([\d.]+)\s*\(추정\)/);if(m&&!td.querySelector('i')){td.innerHTML=m[1]+'<i class="est">추정</i>'}});
 var c=document.getElementById('list-card');var s=c&&c.querySelector(':scope>p.sub');if(s&&/옆으로 밀어/.test(s.textContent))s.textContent='정렬 버튼으로 순서를 바꾸고, 종목을 누르면 위에 추이가 열립니다. 큰 숫자 = 유통주식 중 숏 비율.'}
var k=0;(function go(){try{fx()}catch(e){}if(++k<16)setTimeout(go,500)})();try{var t0=document.getElementById('list-card');if(t0)new MutationObserver(function(){try{fx()}catch(e){}}).observe(t0,{childList:true,subtree:true})}catch(e){}})();
