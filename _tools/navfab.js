// 아래 메뉴 위 왼쪽 '이전·홈' 버튼(사용자 2026-10-29)
(function(){try{
if(/\/(index\.html)?$/.test(location.pathname))return;
function add(){if(document.getElementById('mm-fab'))return;var d=document.createElement('div');d.id='mm-fab';
d.innerHTML='<a role="button" aria-label="이전 화면" data-k="b"><svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg></a><a role="button" aria-label="메인 화면" data-k="h"><svg viewBox="0 0 24 24"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V20h5v-6h4v6h5V9.5"/></svg></a>';
d.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;e.preventDefault();
if(a.dataset.k==='h'){location.href='./';return}
var r=document.referrer;if(history.length>1&&r&&r.indexOf(location.origin)===0)history.back();else location.href='./'});
document.body.appendChild(d)}
if(document.body)add();else document.addEventListener('DOMContentLoaded',add);
}catch(e){}})();
// 독 숨기기(사용자 2026-10-29) — 본문을 아래로 읽어 내려가면 바로 스르륵 숨김 · 독을 아래로 쓸어도 숨김 · 6초 동안 안 건드려도 숨김 → 손잡이만 남음
// 다시 올리기: 손잡이 누르기·위로 밀기, 또는 화면을 위로 크게 되돌려 올릴 때
(function(){try{
var IDLE=6000,t=0,B=document.body;
function sheetOpen(){var s=document.querySelector('.mmd-sheet');return s&&!s.hidden}
function arm(){clearTimeout(t);t=setTimeout(function(){if(!sheetOpen()&&document.querySelector('.mmd'))B.classList.add('mmd-hide')},IDLE)}
function show(){B.classList.remove('mmd-hide');arm()}
function init(){B=document.body;if(!document.querySelector('.mmd'))return setTimeout(init,500);
var p=document.createElement('button');p.id='mm-pull';p.setAttribute('aria-label','아래 메뉴 열기');B.appendChild(p);
p.addEventListener('click',show);var y0=0;
p.addEventListener('touchstart',function(e){y0=e.touches[0].clientY},{passive:true});
p.addEventListener('touchmove',function(e){if(y0-e.touches[0].clientY>12)show();e.preventDefault()},{passive:false});
['touchstart','click'].forEach(function(ev){document.addEventListener(ev,function(e){if(e.target.closest&&e.target.closest('.mmd,#mm-fab,.mmd-sheet'))show()},{passive:true})});
var ly=scrollY,up=0,dn=0;addEventListener('scroll',function(){var y=scrollY;
if(y<ly){dn=0;up+=ly-y;if(up>160||y<40)show()}else{up=0;dn+=y-ly;if(dn>14&&y>60&&!sheetOpen()){B.classList.add('mmd-hide');clearTimeout(t)}}ly=y},{passive:true});
// 독을 아래로 쓸어내리면 바로 숨김(위로 올리는 동작의 반대)
var dy=0,dk=document.querySelector('.mmd');
dk.addEventListener('touchstart',function(e){dy=e.touches[0].clientY},{passive:true});
dk.addEventListener('touchmove',function(e){if(e.touches[0].clientY-dy>22&&!sheetOpen()){B.classList.add('mmd-hide');clearTimeout(t)}},{passive:true});
arm()}
if(document.body)init();else document.addEventListener('DOMContentLoaded',init);
}catch(e){}})();
