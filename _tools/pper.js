// 시세 보드 '지난 n 강세·약세' 이름표를 숫자 방향에 맞춤(사용자 2026-11-03): 강세 칸이 마이너스면 '가장 덜 빠진 분야', 약세 칸이 플러스면 '가장 덜 오른 분야'
(function(){
// 기간 따라 바뀌는 '중앙값' 칸을 맨 앞으로(사용자 2026-11-03 — 1주일·1개월을 누르면 첫 칸이 그 기간 중앙값으로), 오늘(1일) 칸은 그 자리로
function order(){var g=document.getElementById('tiles');if(!g)return;var pe=g.querySelector('.pb-tile[data-tile="per"]'),d1=g.querySelector('.pb-tile[data-tile="d1"]');if(!pe||!d1||g.firstElementChild===pe)return;g.insertBefore(pe,g.firstElementChild);g.appendChild(d1);g.classList.add('mm-t5')}
function off(){var on=!!window.__mmOff;var k=document.querySelector('#tiles .pb-tile[data-tile="d1"] .k');if(k){var w=on?'1일 중앙값 · 장외':'1일 중앙값';if(k.textContent!==w)k.textContent=w}
 var hd=document.querySelector('#take-line .hd');if(hd){var c=hd.querySelector('.mm-off');if(on&&!c){c=document.createElement('span');c.className='mm-off';c.textContent='장외';c.title='미국 정규장 밖(데이장·프리마켓·애프터) 가격입니다. 전날 정규장 종가와 비교합니다.';c.style.cssText='display:inline-block;margin-left:6px;vertical-align:middle;font:800 12px/1.6 -apple-system,sans-serif;color:#2f5fa8;background:#e8f0fb;border:1px solid #c5d6f0;border-radius:999px;padding:0 8px';hd.appendChild(c)}else if(!on&&c)c.remove()}}
function fix(){var t=document.getElementById('take-line');if(!t)return;try{off()}catch(e){}try{order()}catch(e){}t.querySelectorAll('.two>div').forEach(function(d,i){var sm=d.querySelector('small'),v=d.querySelector('.sv');if(!sm||!v)return;var w=sm.querySelector('.per-word');var x=parseFloat(v.textContent.replace('−','-').replace('+',''));if(isNaN(x))return;
 var lab=i===0?(x<0?' 가장 덜 빠진 분야':' 강세'):(x>0?' 가장 덜 오른 분야':' 약세');var tn=w?w.nextSibling:null;if(tn&&tn.nodeType===3){if(tn.nodeValue!==lab)tn.nodeValue=lab}})}
var k=0;(function go(){try{fix()}catch(e){}if(++k<40)setTimeout(go,500)})();
var t0=null;new MutationObserver(function(){clearTimeout(t0);t0=setTimeout(function(){try{fix()}catch(e){}},60)}).observe(document.documentElement,{childList:true,subtree:true,characterData:true});
})();

// 1일 칸은 숨김(기간 칸 하나로 합침, 사용자 2026-11-03 '두 개나 있을 필요 없음') — 1일을 고르면 첫 칸이 1일 중앙값
(function(){var st=document.createElement('style');st.textContent='#tiles.mm-t5>.pb-tile[data-tile="d1"]{display:none!important}@media (max-width:700px){#tiles.mm-t5{grid-template-columns:repeat(6,minmax(0,1fr))!important}#tiles.mm-t5>.pb-tile{grid-column:span 2}#tiles.mm-t5>.pb-tile[data-tile="lo"],#tiles.mm-t5>.pb-tile[data-tile="upside"]{grid-column:span 3}}@media (min-width:701px){#tiles.mm-t5{grid-template-columns:repeat(5,minmax(0,1fr))!important}}';document.head.appendChild(st)})();
// 52주 고점·저점 칸 살리기 + 읽는 법 기준일 자동(사용자 2026-11-03 '신저가 근처가 활성화 안 되는 것 같음 — 페이지 전체 점검')
(function(){
function md(d){var a=String(d||'').split('-');return a.length===3?(+a[1])+'월 '+(+a[2])+'일':''}
function run(){if(!window.dash)return;var C=dash.data('board_calc'),PR=dash.data('prices');if(!C||C.status!=='ok')return;var rows=C.data;
 var lo=rows.filter(function(r){return r.dist_low!=null&&r.dist_low<=5}),hi=rows.filter(function(r){return r.dist_high!=null&&r.dist_high>=-5});
 var newLo=lo.filter(function(r){return r.dist_low<=0.5}),newHi=hi.filter(function(r){return r.dist_high>=-0.5});
 [['lo',lo,newLo,'#b3261e','신저가'],['hi',hi,newHi,'#2e7d4f','신고가']].forEach(function(a){var t=document.querySelector('#tiles .pb-tile[data-tile="'+a[0]+'"]');if(!t)return;var v=t.querySelector('.v');if(v)v.style.color=a[1].length?a[3]:'';
  t.style.boxShadow=a[1].length?'inset 0 0 0 1.5px '+a[3]+'55':'';var k=t.querySelector('.k');if(!k)return;var c=k.querySelector('.mm-new');var tx=a[2].length?a[4]+' 갱신 '+a[2].length:'';
  if(tx&&!c){c=document.createElement('span');c.className='mm-new';c.style.cssText='display:inline-block;margin-left:4px;font:800 10.5px/1.5 sans-serif;color:#fff;background:'+a[3]+';border-radius:999px;padding:0 6px;vertical-align:middle';k.appendChild(c)}
  if(c){if(tx){c.textContent=tx;c.title=a[2].map(function(r){return r.name}).join(', ')}else c.remove()}});
 var u=document.querySelector('#tiles .pb-tile[data-tile="up"] .k');if(u&&u.textContent==='오른 종목')u.textContent='오른 종목 · 1일';
 // 읽는 법: 등락 기간 기준일을 실제 자료 날짜로
 if(PR&&PR.status==='ok'&&PR.data.length){var r0=PR.data.filter(function(x){return x.m1_date})[0];if(r0){document.querySelectorAll('#howto li').forEach(function(li){if(li.dataset.mmd||li.textContent.indexOf('등락 기간')<0)return;var b=li.querySelector('b:nth-of-type(2)');
  li.innerHTML=li.innerHTML.replace(/1개월\([^)]*\)·3개월\([^)]*\)·6개월\([^)]*\)·12개월\([^)]*\)/,'1일(전날)·1주일(5거래일)·1개월('+md(r0.m1_date)+')·3개월('+md(r0.m3_date)+')·6개월('+md(r0.m6_date)+')·12개월('+String(r0.m12_date).slice(0,4)+'년 '+md(r0.m12_date)+')');li.dataset.mmd=1})}}}
var k=0;(function go(){try{run()}catch(e){}if(++k<40)setTimeout(go,600)})();
})();
