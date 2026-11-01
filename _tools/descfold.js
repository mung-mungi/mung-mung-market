// 설명 문단 접기(사용자 2026-11-02 "설명이 많아 스크롤 압박 — 설명은 필요한 사람만 보게") — 전 페이지 공통
// 단락 제목(h2·h3) 바로 아래 설명 문단(P, 45자 이상)을 첫 줄만 보이게 접고 오른쪽에 '설명 보기 ▾'. 누르면 펼침·'접기 ▴'.
// 같은 제목 아래 설명이 여러 개면 첫 문단만 첫 줄, 나머지는 펼칠 때 같이. 데일리 시황(신문 본문)·메인은 제외.
(function(){try{
var PG=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'');
if(PG==='index'||PG==='p-brief'||PG==='')return;
var SKIP='#take,.mm-take,.mm-bo,.pg3,.mm-hero,nav,details,summary,.mm-ntc,.tlx,.tl-row,.ir-lib,.mm-st-hero,.mm-top,.o-new,.mm-bs';
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function ok(e){return e&&e.tagName==='P'&&!e.dataset.df&&e.offsetParent!==null&&e.textContent.trim().length>=45&&!e.querySelector('button,input,select,svg,canvas,table,img')&&!e.closest(SKIP)}
function group(h){var s=h.nextElementSibling;if(!s&&h.parentElement&&h.parentElement.children.length<=2)s=h.parentElement.nextElementSibling;var g=[];while(s&&g.length<3&&ok(s)){g.push(s);s=s.nextElementSibling}return g}
function fold(g){var last=g[g.length-1];g.forEach(function(p,i){p.dataset.df=1;p.classList.add(i?'df-h':'df-c')});
 var b=el('button','df-b','설명 보기 ▾');b.type='button';b.setAttribute('role','button');b.setAttribute('aria-expanded','false');
 b.onclick=function(){var o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',o);b.textContent=o?'접기 ▴':'설명 보기 ▾';g.forEach(function(p){p.classList.toggle('df-o',o)})};
 last.after(b)}
function run(){document.querySelectorAll('h2,h3').forEach(function(h){if(h.offsetParent===null||h.closest(SKIP))return;var g=group(h);if(g.length)fold(g)})}
var k=0;(function t(){run();if(++k<20)setTimeout(t,500)})();
try{new MutationObserver(function(){run()}).observe(document.body,{childList:true,subtree:true})}catch(e){}
}catch(e){}})();
