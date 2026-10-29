// 줄바꿈 다듬기 — 전 페이지 공통(사용자 2026-10-29)
// ① 붙어 있는 괄호 앞에 '끊어도 되는 자리'를 넣음: 국내총생산(GDP) → 국내총생산 / (GDP) 로만 끊김 ('(GDP' / ')' 처럼 깨지지 않게)
//    날짜 요일 10.29(목), 숫자 괄호는 건드리지 않음
// ② 칸(줄 수 제한 있는 글)이 넘치면 글자를 1px씩 줄여(최대 3px) 잘림(…) 없이 다 보이게
(function(){
var SKIP={SCRIPT:1,STYLE:1,TEXTAREA:1,INPUT:1,CODE:1,PRE:1,NOSCRIPT:1};
var RX=/([가-힣A-Za-z])\((?=[^)\d\s][^)]+\))/g;
function txt(root){try{
var w=document.createTreeWalker(root||document.body,NodeFilter.SHOW_TEXT,{acceptNode:function(n){var p=n.parentNode;return p&&!SKIP[p.nodeName]&&!(p.closest&&p.closest('svg,[contenteditable]'))&&RX.test(n.nodeValue)?1:3}});
var a=[],n;while(n=w.nextNode())a.push(n);
a.forEach(function(n){RX.lastIndex=0;n.nodeValue=n.nodeValue.replace(RX,'$1​(')});RX.lastIndex=0}catch(e){}}
var SEL='[class*="tile"] *,[class*="kpi"] *,[class*="cell"] *,[class*="stat"] *';
function fit(){try{document.querySelectorAll(SEL).forEach(function(e){
if(!e.childNodes.length||e.children.length>2)return;var c=getComputedStyle(e);
var clamp=c.webkitLineClamp&&c.webkitLineClamp!=='none';
var over=function(){return (clamp&&e.scrollHeight>e.clientHeight+2)||e.scrollWidth>e.clientWidth+1};
if(!e.dataset.wfBase){if(!over())return;e.dataset.wfBase=parseFloat(c.fontSize)}
var b=+e.dataset.wfBase,s=b;e.style.fontSize=b+'px';
while(over()&&s>b-3&&s>11){s-=1;e.style.fontSize=s+'px'}
})}catch(x){}}
var t=0;function run(){clearTimeout(t);t=setTimeout(function(){txt();fit()},60)}
function start(){run();try{new MutationObserver(function(m){for(var i=0;i<m.length;i++){if(m[i].type!=='attributes'){run();return}}}).observe(document.body,{childList:true,subtree:true,characterData:true})}catch(e){}
addEventListener('resize',function(){document.querySelectorAll('[data-wf-base]').forEach(function(e){e.style.fontSize=''});run()})}
if(document.body)start();else document.addEventListener('DOMContentLoaded',start);
})();
