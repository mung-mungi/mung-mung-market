// 타임라인 헤드라인 모드(사용자 2026-11-01): 정책·지정학·테크 행사 공용
// (화면 크기가 바뀌어 타임라인이 다시 그려져도 펼친 칸·고른 흐름은 그대로 유지)
// 칸은 날짜·점·제목 한 줄로 이어 보고, 누르면 요약·시장 반응·출처(+정리본)가 펼쳐짐. 위에 '흐름' 알약으로 같은 흐름만 이어 보기.
(function(){
var P=(window.__PAGE__&&window.__PAGE__.page)||'';if(P!=='policy'&&P!=='tech')return;
var V=window.__SYNC__?'?v='+window.__SYNC__:'';
var EV=null,BY={},DT=null,dtP=null,TH='',OPEN={};
function ev(){return EV?Promise.resolve(EV):fetch('d/'+P+'/events.json'+V).then(function(r){return r.json()}).then(function(d){EV=d;d.forEach(function(e){BY[e.date+'|'+e.title]=e});return d})}
function dt(){if(DT)return Promise.resolve(DT);if(!dtP)dtP=fetch('d/'+P+'/details.json'+V).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){DT=d;return d});return dtP}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function lk(u,t){var a=el('a',null,t);a.href=u;a.target='_blank';a.rel='noopener';return a}
function key(row){var d=row.querySelector('.d'),t=row.querySelector('.t');if(!d||!t)return null;var m=(d.firstChild&&d.firstChild.textContent||'').trim().split('.');
 // 날짜 칸은 'MM.DD' — 연도는 같은 제목으로 찾음
 var hit=null;for(var k in BY){if(BY[k].title===t.textContent){hit=BY[k];break}}return hit}
function build(d){var w=el('div','pd');if(d.lead)w.appendChild(el('p','ld',d.lead));
 (d.blocks||[]).forEach(function(b){var s=el('section');s.appendChild(el('h5',null,b.k));
  if(b.type==='steps'){var g=el('div','st');b.items.forEach(function(i){g.appendChild(el('b',null,i[0]));g.appendChild(el('span',null,i[1]))});s.appendChild(g)}
  else if(b.type==='conds'){var c=el('div','cd'),m={'진전':'g','미정':'y','쟁점':'r'};b.items.forEach(function(i){var r=el('div');r.appendChild(el('em',m[i.s]||'y',i.s));r.appendChild(el('b',null,i.n));r.appendChild(el('span',null,i.t));c.appendChild(r)});s.appendChild(c);if(b.note)s.appendChild(el('p','nt',b.note))}
  else if(b.type==='quotes'){var q=el('div','qt');b.items.forEach(function(i){var p=el('p');p.appendChild(el('b',null,i.who+' '));p.appendChild(el('small',null,i.role));p.appendChild(document.createElement('br'));p.appendChild(document.createTextNode(i.say+' '));if(i.src)p.appendChild(lk(i.src,'· '+(i.media||'출처')));q.appendChild(p)});s.appendChild(q)}
  else if(b.type==='scen'){var g2=el('div','sc');b.items.forEach(function(i){var v=el('div',i.c||'');v.appendChild(el('b',null,i.h));v.appendChild(document.createTextNode(i.t));g2.appendChild(v)});s.appendChild(g2);if(b.con)s.appendChild(el('p','cn',b.con))}
  else if(b.type==='list'){var o=el('ol');b.items.forEach(function(i){o.appendChild(el('li',null,i))});s.appendChild(o)}
  else s.appendChild(el('p','tx',b.text||''));w.appendChild(s)});
 if(d.links&&d.links.length){var l=el('div','lk');l.appendChild(el('h5',null,'원문'));d.links.forEach(function(i){l.appendChild(lk(i.u,i.media+' · '+i.t))});w.appendChild(l)}
 if(d.updated)w.appendChild(el('p','up2',d.updated+' 정리'));return w}
function toggle(row,e,force){var open=force!=null?force:!row.classList.contains('tlx-open');row.classList.toggle('tlx-open',open);if(e)OPEN[e.id]=open;
 if(open&&e&&e.has_detail&&!row.querySelector('.pd')){var bd=row.querySelector('.bd');var w=el('p','tlx-ld','정리본 불러오는 중…');bd.appendChild(w);
  dt().then(function(D){w.remove();var x=D[e.id];if(x)bd.appendChild(build(x))}).catch(function(){w.textContent='정리본을 불러오지 못했습니다'})}}
function chips(){var sec=document.getElementById('tl');if(!sec||!EV)return;var bar=document.getElementById('tlx-th');
 var c={};EV.forEach(function(e){if(e.thread)c[e.thread]=(c[e.thread]||0)+1});var ks=Object.keys(c).sort(function(a,b){return c[b]-c[a]});if(!ks.length)return;
 if(!bar){bar=el('div','tlx-th');bar.id='tlx-th';bar.setAttribute('data-noswipe','');var box=sec.closest('.pg-card')||sec;box.parentElement.insertBefore(bar,box)}
 if(bar.dataset.n==ks.join('|')+TH)return;bar.dataset.n=ks.join('|')+TH;bar.textContent='';
 bar.appendChild(el('span','tlx-tl','흐름 이어 보기'));
 ['전체'].concat(ks).forEach(function(k){var b=el('button','tlx-c',k==='전체'?'전체':k+' '+c[k]);b.type='button';b.setAttribute('aria-pressed',(k==='전체'?!TH:TH===k)?'true':'false');
  b.onclick=function(){TH=k==='전체'?'':k;if(TH)resetTop();bar.dataset.n='';chips();apply()};bar.appendChild(b)})}
// 흐름 알약과 위쪽 분류·상태 알약이 겹치면 빈 화면이 됨(사용자 2026-11-02) → 흐름을 고르면 위쪽은 '전체'로, 위쪽을 고르면 흐름은 '전체'로
function resetTop(){[['catf','c'],['stf','s']].forEach(function(x){var box=document.getElementById(x[0]);if(!box)return;var on=box.querySelector('button[aria-pressed=true]');if(on&&on.dataset[x[1]]){var all=box.querySelector('button[data-'+x[1]+'=""]');if(all)all.click()}})}
function hookTop(){['catf','stf'].forEach(function(id){var box=document.getElementById(id);if(!box||box.dataset.tlx)return;box.dataset.tlx='1';box.addEventListener('click',function(e){if(!e.isTrusted||!TH)return;if(!e.target.closest('button'))return;TH='';var bar=document.getElementById('tlx-th');if(bar)bar.dataset.n='';setTimeout(function(){chips();apply()},0)},true)})}
function apply(){var rows=document.querySelectorAll('#tl article.pg-ev');setTimeout(empty,0);
 [].forEach.call(rows,function(row){var e=row.__tlx;if(!e)return;row.style.display=(!TH||e.thread===TH)?'':'none'});
 [].forEach.call(document.querySelectorAll('#tl .pg-mon'),function(m){var vis=[].some.call(m.querySelectorAll('article.pg-ev'),function(r){return r.style.display!=='none'});m.style.display=vis?'':'none';var s=m.querySelector('.mh span');if(s){var n=[].filter.call(m.querySelectorAll('article.pg-ev'),function(r){return r.style.display!=='none'}).length;s.textContent=n+'건'}})}
function empty(){var tl=document.getElementById('tl');if(!tl)return;var vis=[].some.call(tl.querySelectorAll('article.pg-ev'),function(r){return r.style.display!=='none'});var m=document.getElementById('tlx-empty');
 if(vis){if(m)m.remove();return}if(m)return;m=el('div','tlx-empty');m.id='tlx-empty';m.appendChild(el('span',null,'이 조건에 맞는 소식이 없습니다'));var b=el('button','tlx-c','전체 보기');b.type='button';b.onclick=function(){TH='';resetTop();var bar=document.getElementById('tlx-th');if(bar)bar.dataset.n='';chips();apply()};m.appendChild(b);tl.prepend(m)}
function sortDay(){[].forEach.call(document.querySelectorAll('#tl .pg-mon'),function(m){var rows=[].slice.call(m.querySelectorAll(':scope>article.pg-ev'));if(rows.length<2)return;
 var desc=true,p=m.previousElementSibling;while(p&&!p.classList.contains('pg-div'))p=p.previousElementSibling;if(p&&/가까운 날|오래된/.test(p.textContent))desc=false;
 var tm=function(r){return (r.__tlx&&r.__tlx.time)||''};
 var sorted=rows.slice().sort(function(a,b){var da=a.__tlx?a.__tlx.date:'',db=b.__tlx?b.__tlx.date:'';if(da!==db)return rows.indexOf(a)-rows.indexOf(b);var ta=tm(a),tb=tm(b);if(!ta||!tb||ta===tb)return rows.indexOf(a)-rows.indexOf(b);return desc?(ta<tb?1:-1):(ta<tb?-1:1)});
 if(sorted.every(function(r,i){return r===rows[i]}))return;var anchor=rows[rows.length-1].nextSibling;sorted.forEach(function(r){m.insertBefore(r,anchor)})})}
function mark(){var rows=document.querySelectorAll('#tl article.pg-ev');if(!rows.length)return;
 ev().then(function(){chips();
  [].forEach.call(rows,function(row){if(row.dataset.tlx)return;row.dataset.tlx='1';row.classList.add('tlx');var e=key(row);row.__tlx=e;
   var dc=row.querySelector('.d');if(dc&&!dc.dataset.tlx){dc.dataset.tlx='1';var sm=dc.querySelector('small');if(sm)sm.className='tlx-wd';}
   if(e&&e.time&&dc&&!dc.querySelector('.tlx-tm')){dc.appendChild(el('span','tlx-tm',e.time))}
   [].forEach.call(row.querySelectorAll('.bd .x span'),function(sp){if(/반응 자료 없음|^자료 없음$/.test(sp.textContent.trim()))sp.remove()});
   if(e){if(e.tier==='small')row.classList.add('tlx-s');if(e.has_detail)row.classList.add('tlx-d');
    var t=row.querySelector('.t');if(t&&e.thread&&!t.querySelector('.tlx-tn')){t.appendChild(el('span','tlx-tn',e.thread))}}
   row.addEventListener('click',function(ev2){if(ev2.target.closest('a,button,.pd'))return;toggle(row,row.__tlx)});
   if(e&&OPEN[e.id])toggle(row,e,true)});
  try{sortDay()}catch(x){}apply()}).catch(function(){})}
var mo=new MutationObserver(function(){clearTimeout(window.__tlxT);window.__tlxT=setTimeout(mark,120)});
function note(){var n=document.getElementById('tl-note');if(!n||n.dataset.tlx)return;n.dataset.tlx='1';n.style.display='none';var b=el('button','tlx-nb','읽는 법 ▾');b.type='button';b.onclick=function(){var o=n.style.display==='none';n.style.display=o?'':'none';b.textContent=o?'접기 ▴':'읽는 법 ▾'};n.before(b)}
function hint(){var o=document.getElementById('ordbtn');if(!o||document.getElementById('tlx-hint'))return;var h=el('span','tlx-hint','제목을 누르면 요약이 펼쳐집니다');h.id='tlx-hint';o.after(h)}
function init(){var tl=document.getElementById('tl');if(!tl)return setTimeout(init,400);note();hint();hookTop();document.documentElement.classList.add('tlx-on');mo.observe(tl,{childList:true,subtree:true});mark()}
init();
})();
