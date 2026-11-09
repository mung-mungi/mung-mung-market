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
// 펼침·접힘 때 본문·날짜가 새 자리로 미끄러지듯 이동(FLIP, 사용자 2026-11-02 "모션 자연스럽게")
function flip(row,fn){var bd=row.querySelector(':scope>.bd'),d=row.querySelector(':scope>.d');var A=bd&&bd.getBoundingClientRect(),B=d&&d.getBoundingClientRect();fn();
 if(!A||matchMedia('(prefers-reduced-motion: reduce)').matches)return;var A2=bd.getBoundingClientRect(),B2=d&&d.getBoundingClientRect();
 [[bd,A,A2],[d,B,B2]].forEach(function(z){var el=z[0],o=z[1],n=z[2];if(!el||!o)return;var dx=o.left-n.left,dy=o.top-n.top;if(Math.abs(dx)<1&&Math.abs(dy)<1)return;
  el.style.transition='none';el.style.transform='translate('+dx+'px,'+dy+'px)';el.getBoundingClientRect();
  el.style.transition='transform .32s cubic-bezier(.2,.8,.2,1)';el.style.transform='';setTimeout(function(){el.style.transition=''},360)})}
function toggle(row,e,force){var open=force!=null?force:!row.classList.contains('tlx-open');flip(row,function(){row.classList.toggle('tlx-open',open)});if(e)OPEN[e.id]=open;
 // 정리본은 누르면 바로 다 열지 않고 '정리본 펼치기' 버튼으로 따로(사용자 2026-11-02 "누르면 아랫단까지 다 열림 — 연 부분만")
 if(open&&e&&e.has_detail&&!row.querySelector('.tlx-pdb')){var bd=row.querySelector('.bd');var bt=el('button','tlx-pdb','📄 정리본 펼치기 ▾');bt.type='button';bt.setAttribute('role','button');bd.appendChild(bt);
  bt.addEventListener('click',function(ev){ev.stopPropagation();var pd=bd.querySelector('.pd');if(pd){var o=pd.hidden;pd.hidden=!o;bt.textContent=o?'정리본 접기 ▴':'📄 정리본 펼치기 ▾';return}
   bt.textContent='정리본 불러오는 중…';dt().then(function(D){var x=D[e.id];if(x){var b2=build(x);bd.insertBefore(b2,bt.nextSibling);bt.textContent='정리본 접기 ▴'}else bt.textContent='정리본이 없습니다'}).catch(function(){bt.textContent='정리본을 불러오지 못했습니다'})})}}
var FLOWBAR=false; // 흐름 알약 줄은 끔 — 위쪽 분류 알약이 큰 묶음 역할(사용자 2026-11-02 '세션 많으면 복잡')
function chips(){var sec=document.getElementById('tl');if(!sec||!EV)return;if(!FLOWBAR){var ob=document.getElementById('tlx-th');if(ob)ob.remove();TH='';return}var bar=document.getElementById('tlx-th');
 var c={},rc={},lt={},td=new Date(Date.now()-5*3600e3).toISOString().slice(0,10),fr=new Date(Date.now()-5*3600e3-14*864e5).toISOString().slice(0,10);
 // 알약 순서: 최근 2주 새 소식이 많은 흐름 먼저 → 가장 최근 소식 날짜 → 전체 건수(사용자 2026-11-02)
 EV.forEach(function(e){if(!e.thread)return;var t=e.thread;c[t]=(c[t]||0)+1;if(e.date<=td){if(e.date>=fr)rc[t]=(rc[t]||0)+1;if(!lt[t]||e.date+(e.time||'')>lt[t])lt[t]=e.date+(e.time||'')}});
 var ks=Object.keys(c).sort(function(a,b){return (rc[b]||0)-(rc[a]||0)||((lt[b]||'')>(lt[a]||'')?1:(lt[b]||'')<(lt[a]||'')?-1:0)||c[b]-c[a]});if(!ks.length)return;
 if(!bar){bar=el('div','tlx-th');bar.id='tlx-th';bar.setAttribute('data-noswipe','');var box=sec.closest('.pg-card')||sec;box.parentElement.insertBefore(bar,box)}
 if(bar.dataset.n==ks.join('|')+TH)return;bar.dataset.n=ks.join('|')+TH;bar.textContent='';
 bar.appendChild(el('span','tlx-tl','흐름 이어 보기'));
 ['전체'].concat(ks).forEach(function(k){var b=el('button','tlx-c',k==='전체'?'전체':k+' '+c[k]);b.type='button';b.setAttribute('aria-pressed',(k==='전체'?!TH:TH===k)?'true':'false');
  b.onclick=function(){TH=k==='전체'?'':k;if(TH)resetTop();bar.dataset.n='';chips();apply()};bar.appendChild(b)})}
// 흐름 알약과 위쪽 분류·상태 알약이 겹치면 빈 화면이 됨(사용자 2026-11-02) → 흐름을 고르면 위쪽은 '전체'로, 위쪽을 고르면 흐름은 '전체'로
function resetTop(){[['catf','c'],['stf','s']].forEach(function(x){var box=document.getElementById(x[0]);if(!box)return;var on=box.querySelector('button[aria-pressed=true]');if(on&&on.dataset[x[1]]){var all=box.querySelector('button[data-'+x[1]+'=""]');if(all)all.click()}})}
function hookTop(){['catf','stf'].forEach(function(id){var box=document.getElementById(id);if(!box||box.dataset.tlx)return;box.dataset.tlx='1';box.addEventListener('click',function(e){if(!e.isTrusted||!TH)return;if(!e.target.closest('button'))return;TH='';var bar=document.getElementById('tlx-th');if(bar)bar.dataset.n='';setTimeout(function(){chips();apply()},0)},true)})}
// 반복 고리 끊기(사용자 2026-11-02 버벅임 점검): 글자·제목·표시·알약 순서는 값이 바뀔 때만 씀 — 그대로 다시 쓰면 화면 감시가 또 깨어나 1초에 50번 넘게 돌았음
function apply(){var rows=document.querySelectorAll('#tl article.pg-ev');setTimeout(empty,0);
 [].forEach.call(rows,function(row){var e=row.__tlx;if(!e)return;row.style.display=(!TH||e.thread===TH)?'':'none'});
 [].forEach.call(document.querySelectorAll('#tl .pg-mon'),function(m){var vis=[].some.call(m.querySelectorAll('article.pg-ev'),function(r){return r.style.display!=='none'});m.style.display=vis?'':'none';var s=m.querySelector('.mh span');if(s){var n=[].filter.call(m.querySelectorAll('article.pg-ev'),function(r){return r.style.display!=='none'}).length;if(s.textContent!==n+'건')s.textContent=n+'건'}})}
function empty(){var tl=document.getElementById('tl');if(!tl)return;var vis=[].some.call(tl.querySelectorAll('article.pg-ev'),function(r){return r.style.display!=='none'});var m=document.getElementById('tlx-empty');
 if(vis){if(m)m.remove();return}if(m)return;m=el('div','tlx-empty');m.id='tlx-empty';var b=el('button','tlx-c','전체 보기');b.type='button';b.onclick=function(){TH='';resetTop();var bar=document.getElementById('tlx-th');if(bar)bar.dataset.n='';chips();apply()};m.appendChild(b);m.appendChild(el('span',null,'이 조건에 맞는 소식이 없습니다'));tl.prepend(m)}
// 위쪽 분류 알약에 최근 7일 새 소식 수(사용자 2026-11-02 — 흐름 알약 대신)
function catN(){var box=document.getElementById('catf');if(!box||!EV)return;var td=new Date(Date.now()-5*3600e3).toISOString().slice(0,10),fr=new Date(Date.now()-5*3600e3-6*864e5).toISOString().slice(0,10),n={},all=0;
 EV.forEach(function(e){if(e.date>=fr&&e.date<=td){n[e.category]=(n[e.category]||0)+1;all++}});
 var bs=[].slice.call(box.querySelectorAll('button'));bs.forEach(function(b,i){if(b.dataset.o==null)b.dataset.o=i});
 // 새 소식 많은 분류를 앞으로(전체는 항상 맨 앞, 사용자 2026-11-02)
 var so=bs.slice().sort(function(a,b){var ka=a.dataset.c?(n[a.dataset.c]||0):1e9,kb=b.dataset.c?(n[b.dataset.c]||0):1e9;return kb-ka||a.dataset.o-b.dataset.o});var cur=[].slice.call(box.querySelectorAll('button'));if(so.some(function(b,i){return cur[i]!==b}))so.forEach(function(b){box.appendChild(b)});
 bs.forEach(function(b){var v=b.dataset.c,k=v?(n[v]||0):all,x=b.querySelector('.tlx-cn');if(!x){x=el('span','tlx-cn');b.appendChild(x)}var nt=k?String(k):'';if(x.textContent!==nt)x.textContent=nt;if(x.title!=='최근 7일 새 소식')x.title='최근 7일 새 소식';var nd=k?'':'none';if(x.style.display!==nd)x.style.display=nd})}
function relabel(){if(P!=='policy')return;var root=document.querySelector('main')||document.body,w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),n;var RL=[['AI·전력 정책','AI 정책'],['한국 관련','외신 한미 정책']];while(n=w.nextNode()){RL.forEach(function(r){if(n.nodeValue.indexOf(r[0])>=0)n.nodeValue=n.nodeValue.split(r[0]).join(r[1])})}}
// 분류 알약을 누르면 짧은 설명 + 최근·다음 소식 한 줄씩(사용자 2026-11-02 '간단하고 명확하게')
var CM={'이란 전쟁·유가':'이란 협상, 호르무즈 해상 충돌, 미국 공습 여부와 유가 흐름입니다.','연준·정책':'금리 결정, 연준 인사 발언, 선거·예산처럼 시장 금리를 움직이는 일정입니다.','반도체 수출통제':'미국의 대중국 칩·장비 수출 규제와 중국의 맞대응입니다.','AI·전력 정책':'AI 규제·행정명령·안전 법안과 데이터센터 전력·인허가 문제입니다.','관세·무역':'미국 관세 조치와 무역 협상, 정상회의 일정입니다.','한국 관련':'관세·대미 투자·미국 측 요구를 외신과 공식 발표로만 봅니다.',
 '칩·하드웨어 행사':'엔비디아·AMD 같은 칩 회사의 신제품 발표 행사입니다.','대형 거래·상장':'AI 회사들의 대형 계약·투자·상장 소식입니다.','클라우드·빅테크':'빅테크·클라우드 회사의 행사와 발표입니다.','AI 모델 공개':'오픈AI·앤트로픽·구글 등의 새 AI 모델 출시입니다.','반도체 공급망':'파운드리·장비·소재 업계 행사와 공급망 소식입니다.','업계 컨퍼런스':'AI·반도체 업계가 모이는 주요 학회·전시회 일정입니다.','주요 인물':'젠슨 황·샘 올트먼 같은 업계 핵심 인물의 굵직한 발언과 거취입니다. 주요 매체 헤드라인급만 싣습니다.'};
function md(d){return d.slice(5).replace('-','.')}
function catNote(){var box=document.getElementById('catf');if(!box||!EV)return;var on=box.querySelector('button[aria-pressed=true]'),c=on&&on.dataset.c,m=document.getElementById('tlx-cm');
 if(!c){if(m)m.remove();return}if(!m){m=el('div','tlx-cm');m.id='tlx-cm';box.after(m)}
 var td=new Date(Date.now()-5*3600e3).toISOString().slice(0,10),past=null,next=null;
 EV.forEach(function(e){if(e.category!==c)return;if(e.status==='예정'||e.date>td){if(!next||e.date<next.date)next=e}else if(!past||e.date>past.date||(e.date===past.date&&(e.time||'')>(past.time||'')))past=e});
 m.textContent='';m.appendChild(el('p','tlx-cm-d',CM[c]||''));
 if(past){var a=el('p','tlx-cm-l');a.appendChild(el('b',null,'최근 '+md(past.date)));a.appendChild(document.createTextNode(' '+past.title));m.appendChild(a)}
 if(next){var b=el('p','tlx-cm-l');b.appendChild(el('b',null,'다음 '+md(next.date)));b.appendChild(document.createTextNode(' '+next.title));m.appendChild(b)}
 relabel()}
function hookCat(){var box=document.getElementById('catf');if(!box||box.dataset.tlxc)return;box.dataset.tlxc='1';box.addEventListener('click',function(){setTimeout(catNote,0)})}
function sortDay(){[].forEach.call(document.querySelectorAll('#tl .pg-mon'),function(m){var rows=[].slice.call(m.querySelectorAll(':scope>article.pg-ev'));if(rows.length<2)return;
 var desc=true,p=m.previousElementSibling;while(p&&!p.classList.contains('pg-div'))p=p.previousElementSibling;if(p&&/가까운 날|오래된/.test(p.textContent))desc=false;
 var tm=function(r){return (r.__tlx&&r.__tlx.time)||''};
 var sorted=rows.slice().sort(function(a,b){var da=a.__tlx?a.__tlx.date:'',db=b.__tlx?b.__tlx.date:'';if(da!==db)return rows.indexOf(a)-rows.indexOf(b);var ta=tm(a),tb=tm(b);if(!ta||!tb||ta===tb)return rows.indexOf(a)-rows.indexOf(b);return desc?(ta<tb?1:-1):(ta<tb?-1:1)});
 if(sorted.every(function(r,i){return r===rows[i]}))return;var anchor=rows[rows.length-1].nextSibling;sorted.forEach(function(r){m.insertBefore(r,anchor)})})}
function mark(){var rows=document.querySelectorAll('#tl article.pg-ev');if(!rows.length)return;
 ev().then(function(){chips();catN();hookCat();catNote();relabel();
  [].forEach.call(rows,function(row){if(row.dataset.tlx)return;row.dataset.tlx='1';row.classList.add('tlx');var e=key(row);row.__tlx=e;
   var dc=row.querySelector('.d');if(dc&&!dc.dataset.tlx){dc.dataset.tlx='1';var sm=dc.querySelector('small');if(sm)sm.className='tlx-wd';}
   if(e&&e.time&&dc&&!dc.querySelector('.tlx-tm')){dc.appendChild(el('span','tlx-tm',e.time))}
   [].forEach.call(row.querySelectorAll('.bd .x span'),function(sp){if(/반응 자료 없음|^자료 없음$/.test(sp.textContent.trim()))sp.remove()});
   if(e){if(e.tier==='small')row.classList.add('tlx-s');if(e.has_detail)row.classList.add('tlx-d');
    var t=row.querySelector('.t');if(t&&e.has_detail&&!t.querySelector('.tlx-tn')){t.appendChild(el('span','tlx-tn tlx-pd','정리본'))}}
   row.addEventListener('click',function(ev2){if(ev2.target.closest('a,button,.pd'))return;toggle(row,row.__tlx)});
   if(e&&OPEN[e.id])toggle(row,e,true)});
  try{sortDay()}catch(x){}apply()}).catch(function(){})}
var mo=new MutationObserver(function(){clearTimeout(window.__tlxT);window.__tlxT=setTimeout(mark,120)});
function note(){var n=document.getElementById('tl-note');if(!n||n.dataset.tlx)return;n.dataset.tlx='1';n.style.display='none';var b=el('button','tlx-nb','읽는 법 ▾');b.type='button';b.onclick=function(){var o=n.style.display==='none';n.style.display=o?'':'none';b.textContent=o?'접기 ▴':'읽는 법 ▾'};n.before(b)}
function hint(){var o=document.getElementById('ordbtn');if(!o||document.getElementById('tlx-hint'))return;var h=el('span','tlx-hint','제목을 누르면 요약이 펼쳐집니다');h.id='tlx-hint';o.after(h)}
function init(){var tl=document.getElementById('tl');if(!tl)return setTimeout(init,400);note();hint();hookTop();document.documentElement.classList.add('tlx-on');mo.observe(tl,{childList:true,subtree:true});mark()}
init();
})();
