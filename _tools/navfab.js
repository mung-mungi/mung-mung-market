// 아래 메뉴 위 왼쪽 '이전·홈' 버튼(사용자 2026-10-29)
(function(){try{
if(/\/(index\.html)?$/.test(location.pathname))return;
function add(){if(document.getElementById('mm-fab'))return;var d=document.createElement('div');d.id='mm-fab';
d.innerHTML='<a role="button" aria-label="이전 화면" data-k="b"><svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg></a><a role="button" aria-label="메인 화면" data-k="h"><svg viewBox="0 0 24 24"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V20h5v-6h4v6h5V9.5"/></svg></a>';
d.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;e.preventDefault();e.stopPropagation();
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
// 손잡이는 독 박스 위 가운데에 붙어 함께 움직임(일체형) — 독이 내려가면 손잡이만 바닥에 남음
var dk=document.querySelector('.mmd');
var p=document.createElement('button');p.id='mm-pull';p.setAttribute('aria-label','아래 메뉴 올리기·내리기');dk.appendChild(p);
function hide(){if(sheetOpen())return;B.classList.add('mmd-hide');clearTimeout(t)}
var y0=0,moved=0;
p.addEventListener('touchstart',function(e){y0=e.touches[0].clientY;moved=0;e.stopPropagation()},{passive:true});
p.addEventListener('touchmove',function(e){var d=e.touches[0].clientY-y0;e.preventDefault();e.stopPropagation();if(moved)return;
if(d<-12){moved=1;show()}else if(d>12){moved=1;hide()}},{passive:false});
p.addEventListener('touchend',function(e){e.stopPropagation()},{passive:true});
p.addEventListener('click',function(e){e.stopPropagation();if(moved){moved=0;return}B.classList.contains('mmd-hide')?show():hide()});
['touchstart','click'].forEach(function(ev){document.addEventListener(ev,function(e){if(e.target.closest&&e.target.closest('.mmd,#mm-fab,.mmd-sheet')&&!e.target.closest('#mm-pull'))show()},{passive:true})});
var ly=scrollY,up=0,dn=0;addEventListener('scroll',function(){var y=scrollY;
if(y<ly){dn=0;up+=ly-y;if(up>160||y<40)show()}else{up=0;dn+=y-ly;if(dn>14&&y>60&&!sheetOpen()){B.classList.add('mmd-hide');clearTimeout(t)}}ly=y},{passive:true});
// 독을 아래로 쓸어내리면 바로 숨김(위로 올리는 동작의 반대)
var dy=0;
dk.addEventListener('touchstart',function(e){dy=e.touches[0].clientY},{passive:true});
dk.addEventListener('touchmove',function(e){if(e.touches[0].clientY-dy>22&&!sheetOpen()){B.classList.add('mmd-hide');clearTimeout(t)}},{passive:true});
arm()}
if(document.body)init();else document.addEventListener('DOMContentLoaded',init);
}catch(e){}})();
// 좌우로 크게 밀면 옆 페이지로(사용자 2026-10-29) — 왼쪽으로 밀면 다음, 오른쪽으로 밀면 이전 페이지(아래 메뉴 순서)
// 옆으로 스크롤되는 줄·표·차트 위, 화면 가장자리(브라우저 뒤로가기 몸짓), 메뉴판 열림 중에는 동작 안 함
(function(){try{
var TH=0.3,box=null,x0,y0,dx=0,on=0,tgt=null;
function list(){return [].slice.call(document.querySelectorAll('.mmd .row>a[href]'))}
function cur(){var a=list();for(var i=0;i<a.length;i++)if(a[i].classList.contains('on'))return i;return -1}
function scrollX(el){for(;el&&el!==document.body;el=el.parentElement){var c=getComputedStyle(el);if(/(auto|scroll)/.test(c.overflowX)&&el.scrollWidth>el.clientWidth+4)return 1}return 0}
document.addEventListener('touchstart',function(e){on=0;if(e.touches.length>1)return;var t=e.touches[0],w=innerWidth;
if(t.clientX<26||t.clientX>w-26)return;var g=e.target;
if(g.closest&&g.closest('canvas,input,textarea,select,.mmd,.mmd-sheet,#mm-fab,[data-noswipe]'))return;
var sv=g.closest&&g.closest('svg');while(sv&&sv.parentElement&&sv.parentElement.closest('svg'))sv=sv.parentElement.closest('svg');
if(sv&&sv.getBoundingClientRect().width>140)return;
if(scrollX(g))return;var s=document.querySelector('.mmd-sheet');if(s&&!s.hidden)return;
if(cur()<0)return;x0=t.clientX;y0=t.clientY;dx=0;on=1;tgt=null},{passive:true,capture:true});
document.addEventListener('touchmove',function(e){if(!on)return;var t=e.touches[0];dx=t.clientX-x0;var dy=t.clientY-y0;
if(!tgt){if(Math.abs(dx)+Math.abs(dy)<16)return;if(Math.abs(dx)<Math.abs(dy)*1.2){on=0;return}
var a=list(),i=cur(),j=dx<0?i+1:i-1;if(j<0||j>=a.length){on=0;return}tgt=a[j];
box=document.getElementById('mm-swp')||document.body.appendChild(Object.assign(document.createElement('div'),{id:'mm-swp'}));
box.textContent=dx<0?(tgt.textContent.trim()+' ›'):('‹ '+tgt.textContent.trim())}
if((dx<0)!==(box.textContent.slice(-1)==='›')){hideBox();on=0;return}
var w=innerWidth,f=Math.min(Math.abs(dx)/(w*TH),1),pos=-120+f*136;
box.style.opacity=Math.min(1,f*1.6);box.style.transform='translateY(-50%)';
if(dx<0){box.style.right=pos+'px';box.style.left='auto'}else{box.style.left=pos+'px';box.style.right='auto'}
box.classList.toggle('ready',f>=1)},{passive:true,capture:true});
function hideBox(){if(box){box.style.opacity=0;box.classList.remove('ready')}}
document.addEventListener('touchend',function(){if(!on)return;on=0;
if(tgt&&Math.abs(dx)>=innerWidth*TH){var h=tgt.getAttribute('href');document.documentElement.classList.add('mm-leave');setTimeout(function(){location.href=h},140)}else hideBox()},{passive:true,capture:true});
document.addEventListener('touchcancel',function(){on=0;hideBox()},{passive:true,capture:true});
addEventListener('pageshow',function(){document.documentElement.classList.remove('mm-leave');hideBox()});
}catch(e){}})();
// 새 실적 알림(사용자 2026-10-29, 실적 시즌) — d/earn_feed.json의 최신 실적이 내가 마지막으로 본 것보다 새로우면
// 메인 화면 위에 '🔔 새 실적 n곳' 띠 + 실적 결과 카드에 NEW, 독의 실적 결과 아이콘에 빨간 점. 실적 결과 페이지를 열면 '봤음'으로 꺼짐
(function(){try{
var K='mm-earn-seen',onEarn=/p-earn\.html$/.test(location.pathname),onHub=/\/(index\.html)?$/.test(location.pathname);
function get(){try{return localStorage.getItem(K)||''}catch(e){return ''}}
function set(v){try{localStorage.setItem(K,v)}catch(e){}}
function vq(){var a=document.querySelector('a[href*="p-earn.html"]');var m=a&&(a.getAttribute('href')||'').match(/\?v=\d+/);return m?m[0]:''}
fetch('d/earn_feed.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(F){
  if(!F||!F.items||!F.items.length)return;
  if(onEarn){set(F.latest);return}
  // 실적 시즌(사용자 2026-10-29): 최근 36시간 실적이 있으면 띠는 늘 보임(여러 사람이 보므로). 안 본 게 있으면 빨강, 다 봤으면 차분한 색
  var seen=get(),cut=new Date(Date.now()-36*3600e3).toISOString().slice(0,16);
  var nw=F.items.filter(function(x){return x.ts>cut});if(!nw.length)return;
  var un=seen?nw.filter(function(x){return x.ts>seen}).length:nw.length;
  var n=0,t=setInterval(function(){paint(nw,un);if(++n>15)clearInterval(t)},700);paint(nw,un);
}).catch(function(){});
function paint(nw,un){
  if(un){var d=document.querySelector('.mmd .row a[href*="p-earn"]');if(d)d.classList.add('mm-new');
    [].forEach.call(document.querySelectorAll('.mmd-sheet a[href*="p-earn"]'),function(a){a.classList.add('mm-new')})}
  if(!onHub)return;
  if(un)[].forEach.call(document.querySelectorAll('a.item[href*="p-earn"] .ttl,a.mm-bar[href*="p-earn"]>b'),function(t){if(!t.querySelector('.mm-newb')){var s=document.createElement('em');s.className='mm-newb';s.textContent='NEW '+un;t.appendChild(s)}});
  if(document.querySelector('.mm-earnnew'))return;
  var sh=document.querySelector('p.sh');if(!sh)return;var box=sh.parentElement;
  var a=document.createElement('a');a.className='mm-earnnew';a.href='p-earn.html'+vq();
  var names=nw.slice(0,3).map(function(x){return x.name}).join(' · ')+(nw.length>3?' 외 '+(nw.length-3)+'곳':'');
  if(!un)a.classList.add('seen');
  a.innerHTML='<i></i><span class="t"><b>'+(un?'새 실적 '+nw.length+'곳':'✓ 최근 나온 실적 '+nw.length+'곳')+'</b><small></small></span><em>›</em>';a.querySelector('small').textContent=names;
  var pc=document.querySelector('.mm-push:not(.bot)');if(pc&&pc.nextElementSibling!==box)pc=null;box.parentElement.insertBefore(a,pc||box);
}
}catch(e){}})();
