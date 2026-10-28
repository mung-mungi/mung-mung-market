// 옵션 온도계: 시세 보드 양식(사용자 2026-10-29) — 오늘 한눈에 3줄+5단계 막대, 숫자 칸 3열, 긴 설명 2줄, 실적 표 한 줄 카드(탭·상자 스크롤), 초보자용·출처 접기
(function(){
var LV=['','안전','양호','보통','근접','위험'];
function lvOf(n,t){if(isNaN(n)||isNaN(t))return 0;if(n>=t)return 5;var x=n/t;return x>=0.9?4:x>=0.8?3:x>=0.6?2:1}
function meter(k){return '<span class="o-lv" data-lv="'+k+'"><i></i><i></i><i></i><i></i><i></i><em>'+LV[k]+'</em></span>'}
function take(){var tk=document.getElementById('take'),tx=document.getElementById('take-txt');if(!tk||!tx)return;var s=tx.textContent;if(tk.dataset.sig===s)return;
 var v=s.match(/VIX\s*([\d.]+)\(([+\-−]?[\d.]+)\)/),r=s.match(/VIX3M\s*([\d.]+)\(([^)]+)\)/),p=s.match(/풋콜\s*([\d.]+)/),st=(s.match(/「([^」]+)」/)||[])[1],sc=(s.match(/점수\s*(\d+)점/)||[])[1];if(!v||!r||!p||!st)return;tk.dataset.sig=s;
 var col=st==='안정'?'#1a7f37':st==='경계'?'#e07b16':'#c62828',em=st==='안정'?'🟢':st==='경계'?'🟠':'🔴';
 var rows=[['VIX',v[1],'공포지수 · 20 넘으면 경계',lvOf(+v[1],20),(/^[+\-−]/.test(v[2])?'':'+')+v[2]],['기간구조',r[1],(/백워/.test(r[2])?'백워데이션(당장 불안 큼)':'콘탱고(정상)')+' · 1 넘으면 백워데이션',lvOf(+r[1],1),''],['풋콜',p[1],'하락 보험 비율 · 0.9 넘으면 경계',lvOf(+p[1],0.9),'']];
 var w=tk.querySelector('.o-new');if(!w){w=document.createElement('div');w.className='o-new';tk.appendChild(w)}
 w.innerHTML='<div class="o-top"><span class="o-st" style="color:'+col+'">'+em+' '+st+'</span><span class="o-sc">점수 <b>'+(sc||0)+'</b> / 4</span></div><ul class="o-rows">'+rows.map(function(x){return '<li><span class="o-k"><b>'+x[0]+'</b><small>'+x[2]+'</small></span><span class="o-v" data-lv="'+x[3]+'">'+x[1]+(x[4]?'<small>'+x[4]+'</small>':'')+'</span>'+meter(x[3])+'</li>'}).join('')+'</ul>';
 tk.classList.add('o-on')}
function hows(){document.querySelectorAll('.ot-card .how:not([data-o])').forEach(function(p){p.dataset.o=1;p.classList.add('o-clamp');var b=document.createElement('button');b.type='button';b.className='o-more';b.textContent='읽는 법 ▾';p.after(b);b.onclick=function(){p.classList.toggle('op');b.textContent=p.classList.contains('op')?'접기 ▴':'읽는 법 ▾'}})}
function folds(){['read-card','src-card'].forEach(function(id){var c=document.getElementById(id);if(!c||c.dataset.o)return;var h=c.querySelector('h2,h3');if(!h)return;c.dataset.o=1;c.classList.add('o-fold');h.addEventListener('click',function(){c.classList.toggle('op')})})}
function earn(){var c=document.getElementById('earn-card');if(!c)return;var t=c.querySelector('table');if(!t)return;var rows=[...t.querySelectorAll('tbody tr')];if(!rows.length)return;var sig=rows.length+':'+t.textContent.length;if(c.dataset.sig===sig)return;c.dataset.sig=sig;
 var old=c.querySelector('.o-earn');if(old)old.remove();var box=document.createElement('div');box.className='o-earn';
 var done=[],todo=[];rows.forEach(function(r){var d=[...r.children].map(function(x){return x.textContent.trim()});if(d.length<7)return;
  var exp=d[5].replace(/자료 없음/,'—'),act=d[6],am=(act.match(/^([+\-−][\d.]+%)/)||[])[1],tag=(act.match(/예상 (초과|이내)/)||[])[1],dt=d[3].slice(5).replace('-','/'),tm=d[4].replace('장 마감 후','장후').replace('장 시작 전','장전');
  var cls=/^[\-−]/.test(am||'')?'dn':'up';
  var h='<div class="o-row"><div class="o-l"><b>'+d[0]+'</b><small>'+d[1]+' · '+dt+' '+tm+'</small></div><div class="o-m"><small>예상</small><b>'+exp+'</b></div><div class="o-r '+(am?cls:'mu')+'">'+(am?'<b>'+am+'</b><small class="'+(tag==='초과'?'big':'')+'">예상 '+tag+'</small>':'<b>—</b><small>발표 전</small>')+'</div></div>';
  (am?done:todo).push(h)});
 var tabs=document.createElement('div');tabs.className='o-tab';tabs.innerHTML='<button type="button" aria-pressed="true">나온 것 '+done.length+'</button><button type="button" aria-pressed="false">발표 예정 '+todo.length+'</button>';
 var L1=document.createElement('div'),L2=document.createElement('div');L1.className=L2.className='o-list';L1.innerHTML=done.join('');L2.innerHTML=todo.join('');L2.hidden=true;
 if(!done.length){L1.hidden=true;L2.hidden=false;tabs.children[0].setAttribute('aria-pressed','false');tabs.children[1].setAttribute('aria-pressed','true')}
 [].forEach.call(tabs.children,function(b,i){b.onclick=function(){[].forEach.call(tabs.children,function(x){x.setAttribute('aria-pressed',x===b)});L1.hidden=i!==0;L2.hidden=i!==1}});
 box.appendChild(tabs);box.appendChild(L1);box.appendChild(L2);var tw=t.closest('.ot-tbl,.tbl,div')||t;t.classList.add('o-hide');if(tw!==c&&tw.querySelector('table')===t&&tw.children.length===1)tw.classList.add('o-hide');t.parentNode.insertBefore(box,t)}
function all(){try{take()}catch(e){}try{hows()}catch(e){}try{folds()}catch(e){}try{earn()}catch(e){}}
var k=0;(function go(){all();if(++k<16)setTimeout(go,400)})();
try{var root=document.querySelector('main')||document.body;new MutationObserver(function(){all()}).observe(root,{childList:true,subtree:true,characterData:true})}catch(e){}
})();
