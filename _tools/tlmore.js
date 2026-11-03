// 뉴스 타임라인 '더 보기' + 날짜 바로가기(사용자 2026-11-03) — 주요 뉴스·AI 테크 뉴스
// 예전: 긴 기록 전체를 높이 고정 상자(u-box) 안에 넣어 상자 안에서 따로 스크롤 → 아이폰에서 손가락이 상자에 걸림
// 지금: 상자 없이 페이지 스크롤 하나로. '지난 일'은 처음 12건, '앞으로 예정'은 5건만 보이고 아래 '더 보기'로 이어서 펼침.
//       위에 '바로가기' 알약(오늘·어제·지난주·지난달들·예정) — 누르면 그 날짜까지 펼치고 그 자리로 이동.
// 분류·상태·순서를 바꿔 타임라인이 다시 그려지면 처음 개수로 돌아감. 숨김은 tm-h 클래스만 씀(tlx.js의 흐름 숨김 style.display와 겹치지 않게)
(function(){
var P=(window.__PAGE__&&window.__PAGE__.page)||'';if(P!=='policy'&&P!=='tech')return;
var BASE={past:12,up:5},STEP={past:20,up:10},LIM={past:12,up:5},KEY='';
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function td(n){return new Date(Date.now()-5*3600e3-(n||0)*864e5).toISOString().slice(0,10)}
function vis(r){return r.style.display!=='none'}
function segs(tl){var S=[],cur=null;[].forEach.call(tl.children,function(c){if(c.classList.contains('pg-div')){cur={k:/예정/.test(c.textContent)?'up':'past',div:c,mons:[]};S.push(cur)}else if(c.classList.contains('pg-mon')){if(!cur){cur={k:'past',div:null,mons:[]};S.push(cur)}cur.mons.push(c)}});return S}
function rowsOf(s){var a=[];s.mons.forEach(function(m){[].forEach.call(m.querySelectorAll('article.pg-ev'),function(r){if(vis(r))a.push(r)})});return a}
function unbox(card){if(!card)return;card.dataset.ub=1;if(card.classList.contains('u-box')){card.classList.remove('u-box');var h=card.nextElementSibling;if(h&&h.classList.contains('u-hint'))h.remove()}}
function tog(e,c,on){if(e.classList.contains(c)!==on)e.classList.toggle(c,on)}
function apply(){var tl=document.getElementById('tl');if(!tl)return;unbox(tl.closest('.pg-card'));
 var S=segs(tl);if(!S.length)return;
 var all=tl.querySelectorAll('article.pg-ev'),f=all[0];var k=all.length+'|'+(f?f.textContent.slice(0,40):'')+'|'+[].filter.call(all,vis).length;
 if(k!==KEY){KEY=k;LIM.past=BASE.past;LIM.up=BASE.up}
 S.forEach(function(s){var R=rowsOf(s),lim=LIM[s.k];R.forEach(function(r,i){tog(r,'tm-h',i>=lim)});
  s.mons.forEach(function(m){var any=[].some.call(m.querySelectorAll('article.pg-ev'),function(r){return vis(r)&&!r.classList.contains('tm-h')});var has=[].some.call(m.querySelectorAll('article.pg-ev'),vis);tog(m,'tm-h',has&&!any)});
  var last=s.mons[s.mons.length-1];if(!last)return;var bx=last.nextElementSibling;if(!(bx&&bx.classList.contains('tm-more'))){bx=el('div','tm-more');bx.dataset.k=s.k;last.after(bx)}
  var left=Math.max(0,R.length-lim),t=left?'▾ '+(s.k==='up'?'예정 더 보기':'이전 기록 더 보기')+' · 남은 '+left+'건':'',sig=left+'|'+(lim>BASE[s.k]);
  if(bx.dataset.sig===sig)return;bx.dataset.sig=sig;bx.textContent='';
  if(left){var b=el('button','tm-b',t);b.type='button';b.onclick=function(){LIM[s.k]+=STEP[s.k];apply()};bx.appendChild(b)}
  if(lim>BASE[s.k]){var c=el('button','tm-c','접기 ▴');c.type='button';c.onclick=function(){LIM[s.k]=BASE[s.k];apply();var t2=s.div||tl;scrollTo({top:t2.getBoundingClientRect().top+scrollY-70,behavior:'smooth'})};bx.appendChild(c)}
  bx.hidden=!bx.children.length});
 jumps(tl,S)}
function dOf(r){return r.__tlx&&r.__tlx.date||''}
function jumps(tl,S){var card=tl.closest('.pg-card')||tl,past=S.filter(function(s){return s.k==='past'})[0],up=S.filter(function(s){return s.k==='up'})[0];
 var R=past?rowsOf(past):[],J=[],T=td(),Y=td(1),W=td(7),mon=T.slice(0,7);
 function best(test){var m='';R.forEach(function(r){var d=dOf(r);if(d&&test(d)&&d>m)m=d});if(!m)return null;for(var i=0;i<R.length;i++)if(dOf(R[i])===m)return R[i];return null}
 var a=best(function(d){return d===T});if(a)J.push(['오늘',a]);
 var b=best(function(d){return d===Y});if(b)J.push(['어제',b]);
 var w=best(function(d){return d<=W});if(w&&w!==b)J.push(['지난주',w]);
 var ms={};R.forEach(function(r){var d=dOf(r);if(d&&d.slice(0,7)<mon)ms[d.slice(0,7)]=1});Object.keys(ms).sort().reverse().slice(0,3).forEach(function(m){var r=best(function(d){return d.slice(0,7)===m});if(r)J.push([(+m.slice(5))+'월',r])});
 if(up&&rowsOf(up).length)J.push(['예정',up.div||up.mons[0]]);
 var bar=document.getElementById('tm-jump'),sig=J.map(function(j){return j[0]+(j[1].__tlx?j[1].__tlx.id||dOf(j[1]):'')}).join(',');
 if(J.length<2){if(bar)bar.remove();return}
 if(bar&&bar.dataset.sig===sig&&bar.nextElementSibling===card){bar.__J=J;return}
 if(!bar){bar=el('div','tm-jump');bar.id='tm-jump';bar.setAttribute('data-noswipe','')}bar.dataset.sig=sig;bar.__J=J;bar.textContent='';bar.appendChild(el('span','tm-jl','바로가기'));
 J.forEach(function(j,i){var x=el('button','tm-j',j[0]);x.type='button';x.onclick=function(){go(i)};bar.appendChild(x)});
 card.parentElement.insertBefore(bar,card)}
function go(i){var bar=document.getElementById('tm-jump');var j=bar&&bar.__J&&bar.__J[i];if(!j)return;var t=j[1];
 if(t.tagName==='ARTICLE'){var tl=document.getElementById('tl'),S=segs(tl);S.forEach(function(s){var R=rowsOf(s),ix=R.indexOf(t);if(ix>=LIM[s.k])LIM[s.k]=ix+8})}
 else{LIM.past=Math.max(LIM.past,BASE.past)}
 apply();
 // 펼친 칸이 뒤늦게 자리 잡으면(설명 접기·표 맞춤 등) 목표가 밀림 → 멀면 바로 이동, 0.3·0.8초 뒤 한 번씩 다시 맞춤
 function to(sm){var y=t.getBoundingClientRect().top+scrollY-90;if(Math.abs(y-scrollY)>40)scrollTo({top:y,behavior:sm&&Math.abs(y-scrollY)<1500?'smooth':'auto'})}
 to(1);setTimeout(to,350);setTimeout(to,850);
 if(t.tagName==='ARTICLE'){t.classList.add('tm-flash');setTimeout(function(){t.classList.remove('tm-flash')},1400)}}
var q=0;function sched(){if(q)return;q=1;requestAnimationFrame(function(){q=0;try{apply()}catch(e){}})}
var k=0;(function t(){sched();if(++k<16)setTimeout(t,500)})();
var MO=window.MutationObserver;try{if(MO.__thr)MO=Object.getPrototypeOf(MO)}catch(e){}
function watch(){var tl=document.getElementById('tl');if(!tl){setTimeout(watch,400);return}try{new MO(sched).observe(tl,{childList:true,subtree:true,attributes:true,attributeFilter:['style']})}catch(e){}}watch();
})();
