// 실적 결과: 탭(최근 나온·발표 예정·이전 노트)·다음 발표·알약 등락·노트 한 줄 카드 (사용자 2026-10-29)
(function(){
function stepTabs(){(function(){var f=document.getElementById('find'),h=document.getElementById('hits'),u=document.getElementById('ups');if(!f||!h||f.dataset.etab)return;f.dataset.etab=1;
var hk=f.querySelector('.hk');var rest=h.querySelector('.hrest'),more=h.querySelector('.hmore'),day=h.querySelector('.hday');
var latest=[...h.children].filter(x=>x.tagName==='BUTTON'&&!x.classList.contains('hmore'));var older=rest?[...rest.children]:[];
var tabs=document.createElement('div');tabs.className='etab';
var nUp=u?u.querySelectorAll('.un>:not(button)').length:0;
var T=[['latest','최근 나온 '+latest.length],['up','발표 예정'+(nUp?' '+nUp:'')],['old','이전 노트 '+older.length]];
var P={};
P.latest=document.createElement('div');P.latest.className='ep ep-l';var row=document.createElement('div');row.className='ep-row';latest.forEach(b=>row.appendChild(b));P.latest.appendChild(row);
var all=document.createElement('button');all.type='button';all.className='ep-all';all.textContent='전체 ▾';all.onclick=function(){P.latest.classList.toggle('wrap');all.textContent=P.latest.classList.contains('wrap')?'접기 ▴':'전체 ▾'};P.latest.appendChild(all);
P.up=document.createElement('div');P.up.className='ep';if(u)P.up.appendChild(u);
P.old=document.createElement('div');P.old.className='ep ep-o';older.forEach(b=>P.old.appendChild(b));
T.forEach(function(t,i){var b=document.createElement('button');b.type='button';b.textContent=t[1];b.setAttribute('aria-pressed',i===0);b.onclick=function(){tabs.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));Object.keys(P).forEach(k=>P[k].hidden=k!==t[0])};tabs.appendChild(b)});
h.hidden=true;if(hk)hk.hidden=true;
var box=document.createElement('div');box.className='ebox';box.appendChild(tabs);Object.keys(P).forEach(function(k,i){P[k].hidden=i!==0;box.appendChild(P[k])});
h.parentNode.insertBefore(box,h);
})();}
function stepIdeas(){(function(){var f=document.getElementById('find');if(!f)return;
// 1) 알약에 주가 반응
var arts=[...document.querySelectorAll('article[data-sum]')];
function react(name){var a=arts.find(x=>(x.dataset.name||'').split(' ')[0]===name||(x.dataset.name||'').indexOf(name)===0);if(!a)return null;var m=(a.dataset.sum||'').match(/(프리마켓|시간외|장중|종가)[^·]*?([+\-−][\d.~]+%)/);return m?{p:m[2],a:a}:{p:null,a:a}}
f.querySelectorAll('.ep-row>button,.ep-o>button').forEach(function(b){if(b.dataset.px)return;b.dataset.px=1;var nm=((b.querySelector('b')||b).textContent||'').trim();var r=react(nm);if(r&&r.p){var s=document.createElement('em');s.className='px '+(/[\-−]/.test(r.p)?'dn':'up');s.textContent=r.p.replace('−','-');b.appendChild(s)}
 b.addEventListener('click',function(){var a=r&&r.a;if(!a)return;var btn=a.querySelector('.sumrow');if(btn&&btn.getAttribute('aria-expanded')!=='true')btn.click();requestAnimationFrame(function(){requestAnimationFrame(function(){var y=a.getBoundingClientRect().top+window.scrollY-70;window.scrollTo(0,y)})});a.classList.remove('flash');void a.offsetWidth;a.classList.add('flash')})});
// 2) 다음 발표
var u=document.getElementById('ups');if(u&&!f.querySelector('.nx')){var now=new Date(),T={'새벽 장후':[5,30],'아시아':[15,0],'저녁 장전':[20,30]};var best=null;
 u.querySelectorAll('.ud').forEach(function(d){var md=(d.querySelector('em')||{}).textContent||'';var p=md.split('/');d.querySelectorAll('.ur').forEach(function(r){var sl=(r.querySelector('.slot')||{}).textContent||'';var pend=[...r.querySelectorAll('.un>:not(button)')].map(x=>x.textContent.trim());if(!pend.length||!T[sl])return;var t=new Date(now.getFullYear(),+p[0]-1,+p[1],T[sl][0],T[sl][1]);if(t<now)return;if(!best||t<best.t)best={t:t,sl:sl,n:pend,md:md}})});
 if(best){var h=Math.round((best.t-now)/36e5);var nx=document.createElement('div');nx.className='nx';nx.innerHTML='<b>⏳ 다음 발표</b><span><em class="sl">'+best.sl+'</em> '+best.n.slice(0,3).join('·')+(best.n.length>3?' 외 '+(best.n.length-3):'')+'</span><i>'+(h<1?'곧':'약 '+h+'시간 뒤')+'</i>';var box=f.querySelector('.ebox');box.insertBefore(nx,box.firstChild)}
 // 발표 예정 탭 숫자 = 아직 안 나온 회사 수
 var n=u.querySelectorAll('.un>:not(button)').length;var tb=f.querySelectorAll('.etab button')[1];if(tb)tb.textContent='발표 예정 '+n}
// 검색창 → 돋보기
var q=document.getElementById('fq');if(q&&!f.querySelector('.qbtn')){q.classList.add('qhide');var qb=document.createElement('button');qb.type='button';qb.className='qbtn';qb.textContent='🔍';qb.onclick=function(){q.classList.toggle('qhide');if(!q.classList.contains('qhide'))q.focus()};var et=f.querySelector('.etab');et.parentNode.insertBefore(qb,et.nextSibling);var w=document.createElement('div');w.className='etw';et.parentNode.insertBefore(w,et);w.appendChild(et);w.appendChild(qb)}
})();}
function stepCards(){(function(){document.querySelectorAll('article>.sumrow').forEach(function(b){var a=b.parentElement;if(a.dataset.mk)return;var sm=b.querySelector('.sm.sx');if(!sm)return;a.dataset.mk=1;
var nm=b.querySelector('.nm');var lt=nm.querySelector('.lt'),gr=nm.querySelector('.gr');var name=[...nm.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
var ai=sm.querySelector('.sx-ai'),ck=sm.querySelector('.sx-ck'),et=sm.querySelector('.sx-et');var mv=ck?ck.querySelector('i.m'):null;var mt=mv?mv.textContent:'';var mm=mt.match(/^(\S+)\s*(.*)$/)||['','',''];
var pct=(mm[2].match(/[+\-−~\d.]+%/)||[mm[2]])[0];var lab=mm[1]+(mm[2].replace(pct,'').trim()?' '+mm[2].replace(pct,'').trim():'');
if(mv)mv.remove();var dt=(a.dataset.date||'').slice(5).replace('-','/');
var row=document.createElement('div');row.className='mk-row';
row.innerHTML='<div class="mk-l"><b>'+(lt?'<i class="mk-new">최신</i>':'')+name+'</b><small>'+(ai?ai.innerHTML:'')+'</small></div><div class="mk-r '+(mv&&mv.classList.contains('dn')?'dn':'up')+'"><b>'+(pct||'')+'</b><small>'+(mv?lab+' · ':'')+dt+'</small></div>';
var inner=b.firstElementChild;inner.textContent='';inner.appendChild(row);if(ck&&ck.children.length){ck.className='mk-ck';inner.appendChild(ck)}if(et){et.className='mk-et';inner.appendChild(et)}
})})()}
var k=0;(function go(){try{var h=document.getElementById('hits'),u=document.getElementById('ups');
 if(h&&h.querySelector('button')&&(!u||u.querySelector('.ud .ur'))){stepTabs();stepIdeas()}
 stepCards()}catch(e){}
 if(++k<16)setTimeout(go,400)})();
})();
