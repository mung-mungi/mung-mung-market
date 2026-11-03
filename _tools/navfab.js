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
// 숨김 상태는 메뉴(.mmd)·이전홈(#mm-fab)·소리(#mm-snd)에만, 아래 여백은 body 인라인으로(사용자 2026-11-02 버벅임 점검)
function isH(){var d=document.querySelector('.mmd');return !!(d&&d.classList.contains('mmd-hide'))}
function setH(v){['.mmd','#mm-fab','#mm-snd'].forEach(function(q){var e=document.querySelector(q);if(e)e.classList.toggle('mmd-hide',v)});
 if(v&&B.classList.contains('mmd-on'))B.style.setProperty('padding-bottom','calc(64px + env(safe-area-inset-bottom))','important');else B.style.removeProperty('padding-bottom')}
function sheetOpen(){var s=document.querySelector('.mmd-sheet');return s&&!s.hidden}
function arm(){clearTimeout(t);t=setTimeout(function(){if(!sheetOpen()&&document.querySelector('.mmd'))setH(true)},IDLE)}
function show(){setH(false);arm()}
function init(){B=document.body;if(!document.querySelector('.mmd'))return setTimeout(init,500);
// 손잡이는 독 박스 위 가운데에 붙어 함께 움직임(일체형) — 독이 내려가면 손잡이만 바닥에 남음
var dk=document.querySelector('.mmd');
var p=document.createElement('button');p.id='mm-pull';p.setAttribute('aria-label','아래 메뉴 올리기·내리기');p.innerHTML='<b>메뉴</b>';dk.appendChild(p);
function hide(){if(sheetOpen())return;setH(true);clearTimeout(t)}
var y0=0,moved=0;
p.addEventListener('touchstart',function(e){y0=e.touches[0].clientY;moved=0;e.stopPropagation()},{passive:true});
p.addEventListener('touchmove',function(e){var d=e.touches[0].clientY-y0;e.preventDefault();e.stopPropagation();if(moved)return;
if(d<-12){moved=1;show()}else if(d>12){moved=1;hide()}},{passive:false});
p.addEventListener('touchend',function(e){e.stopPropagation();if(!moved&&isH()){moved=1;show()}},{passive:true});
p.addEventListener('click',function(e){e.stopPropagation();if(moved){moved=0;return}isH()?show():hide()});
['touchstart','click'].forEach(function(ev){document.addEventListener(ev,function(e){if(e.target.closest&&e.target.closest('.mmd,#mm-fab,.mmd-sheet')&&!e.target.closest('#mm-pull'))show()},{passive:true})});
var ly=scrollY,up=0,dn=0,sq=0;addEventListener('scroll',function(){if(sq)return;sq=1;requestAnimationFrame(function(){sq=0;var y=scrollY;
if(y<ly){dn=0;up+=ly-y;if(up>48||y<40)show()}else{up=0;dn+=y-ly;if(dn>14&&y>60&&!sheetOpen()){setH(true);clearTimeout(t)}}ly=y})},{passive:true}); /* 반응 속도(사용자 2026-11-01): 스크롤 1픽셀마다가 아니라 화면 그릴 때 한 번 */
// 아이패드 트랙패드·마우스(사용자 2026-11-01): 커서를 화면 아래 끝 가까이 내리면 숨었던 아래 메뉴가 올라옴(아이패드 독처럼)
addEventListener('pointermove',function(e){if(e.pointerType==='mouse'&&e.clientY>innerHeight-36&&isH())show()},{passive:true});
// 독을 아래로 쓸어내리면 바로 숨김(위로 올리는 동작의 반대)
var dy=0;
dk.addEventListener('touchstart',function(e){dy=e.touches[0].clientY},{passive:true});
dk.addEventListener('touchmove',function(e){if(e.touches[0].clientY-dy>22&&!sheetOpen()){setH(true);clearTimeout(t)}},{passive:true});
arm()}
if(document.body)init();else document.addEventListener('DOMContentLoaded',init);
}catch(e){}})();
// 좌우로 크게 밀면 옆 페이지로(사용자 2026-10-29) — 왼쪽으로 밀면 다음, 오른쪽으로 밀면 이전 페이지(아래 메뉴 순서)
// 옆으로 스크롤되는 줄·표·차트 위, 화면 가장자리(브라우저 뒤로가기 몸짓), 메뉴판 열림 중에는 동작 안 함
(function(){try{
var TH=0.3,box=null,x0,y0,dx=0,on=0,tgt=null,fl=0,flm=0; /* fl: 차트 가운데에서 시작 — 손가락이 처음부터 바로 옆으로 움직이면(0.16초 안 24px, 초당 약 150px 이상) 페이지 넘김, 잠깐 멈췄다 움직이면 가격 추적(사용자 2026-11-01) */
function list(){return [].slice.call(document.querySelectorAll('.mmd .row>a[href]'))}
function cur(){var a=list();for(var i=0;i<a.length;i++)if(a[i].classList.contains('on'))return i;return -1}
function scrollX(el){for(;el&&el!==document.body;el=el.parentElement){var c=getComputedStyle(el);if(/(auto|scroll)/.test(c.overflowX)&&el.scrollWidth>el.clientWidth+4)return 1}return 0}
document.addEventListener('touchstart',function(e){on=0;if(e.touches.length>1)return;var t=e.touches[0],w=innerWidth;
var SA=(window.navigator.standalone===true)||(window.matchMedia&&matchMedia('(display-mode: standalone)').matches),EG=SA?0:26; if(t.clientX<EG||t.clientX>w-EG)return;var g=e.target;fl=0;
if(g.closest&&g.closest('canvas,input,textarea,select,.mmd,.mmd-sheet,#mm-fab,[data-noswipe]'))return;
var sv=g.closest&&g.closest('svg');while(sv&&sv.parentElement&&sv.parentElement.closest('svg'))sv=sv.parentElement.closest('svg');
if(sv&&sv.getBoundingClientRect().width>140){ /* 큰 차트 위(사용자 2026-11-01): 좌우 가장자리(차트 폭 22%, 최소 72px)는 넘김 전용 — 가격 추적 안 함. 가운데는 처음부터 옆으로 밀면 넘김, 멈췄다 움직이면 추적 */ var rb=sv.getBoundingClientRect(),H=document.documentElement; if(H.classList.contains('mm-full')||H.classList.contains('mm-land')||(window.__mmT&&window.__mmT.draw))return; var EZ=Math.max(72,rb.width*0.22); if(!(t.clientX-rb.left<EZ||rb.right-t.clientX<EZ)){ fl=Date.now(); flm=0; } }
else{ /* 넘기면 안 되는 곳(사용자 2026-11-01): 차트 영역(칩·기간·도구·작은 그래프), 작은 버튼·알약·칩·탭 줄 — 누르다 손가락이 미끄러져 페이지가 넘어가지 않게. 화면 폭 절반 넘는 큰 카드·글은 그대로 넘김 */ if(g.closest&&g.closest('.mmt,.mmt-nav,.mmt-per,[role=tablist],[class*="pill"],[class*="chip"],[class*="seg"],[class$="-tabs"],[class~="tabs"]'))return; var bt=g.closest&&g.closest('button,[role=button],[role=tab],[aria-pressed],label'); if(bt&&bt.getBoundingClientRect().width<w*0.5)return; for(var el=g;el&&el!==document.body;el=el.parentElement){ var cs=getComputedStyle(el); if(/(auto|scroll)/.test(cs.overflowX)&&el.getBoundingClientRect().height<90)return; } }if(scrollX(g))return;var s=document.querySelector('.mmd-sheet');if(s&&!s.hidden)return;
if(cur()<0)return;x0=t.clientX;y0=t.clientY;dx=0;on=1;tgt=null},{passive:true,capture:true});
document.addEventListener('touchmove',function(e){if(!on)return;var t=e.touches[0];dx=t.clientX-x0;var dy=t.clientY-y0;
if(fl&&!flm){ var el=Date.now()-fl; if(Math.abs(dx)>=24&&Math.abs(dx)>Math.abs(dy)*1.5&&el<=160){ flm=1; document.documentElement.classList.add('mm-swiping'); } else if(el>160){ on=0; fl=0; return; } else return; }
if(!tgt){if(Math.abs(dx)+Math.abs(dy)<16)return;if(Math.abs(dx)<Math.abs(dy)*1.2){on=0;return}
var a=list(),i=cur(),j=dx<0?i+1:i-1;if(j<0||j>=a.length){on=0;return}tgt=a[j];
box=document.getElementById('mm-swp')||document.body.appendChild(Object.assign(document.createElement('div'),{id:'mm-swp'}));
box.textContent=dx<0?(tgt.textContent.trim()+' ›'):('‹ '+tgt.textContent.trim())}
if((dx<0)!==(box.textContent.slice(-1)==='›')){hideBox();on=0;return}
var w=innerWidth,f=Math.min(Math.abs(dx)/(w*TH),1),pos=-120+f*136;
box.style.opacity=Math.min(1,f*1.6);box.style.transform='translateY(-50%)';
if(dx<0){box.style.right=pos+'px';box.style.left='auto'}else{box.style.left=pos+'px';box.style.right='auto'}
box.classList.toggle('ready',f>=1)},{passive:true,capture:true});
function hideBox(){document.documentElement.classList.remove('mm-swiping');if(box){box.style.opacity=0;box.classList.remove('ready')}}
document.addEventListener('touchend',function(){if(!on)return;on=0;
fl=0;flm=0;
if(tgt&&Math.abs(dx)>=innerWidth*TH){var h=tgt.getAttribute('href');document.documentElement.classList.add('mm-leave');setTimeout(function(){location.href=h},140)}else hideBox()},{passive:true,capture:true});
document.addEventListener('touchcancel',function(){on=0;hideBox()},{passive:true,capture:true});
addEventListener('pageshow',function(){document.documentElement.classList.remove('mm-leave');hideBox()});
// 아이패드 트랙패드·마우스 두 손가락 좌우 밀기 = 옆 페이지(사용자 2026-11-01) — 사파리 '뒤로 가기' 몸짓 대신 아래 메뉴 순서로. 옆으로 넘기는 표·띠·차트·작은 그래프 위에서는 그 칸이 움직임
var wx=0,wt=0,wgo=0,wtg=null;
function wscroll(el){for(;el&&el!==document.body;el=el.parentElement){if(el.closest&&el.closest('#main .mmt-box,.mmt-nav,canvas,input,textarea,select,.mmd,.mmd-sheet,[data-noswipe]'))return 1;var c=getComputedStyle(el);if(/(auto|scroll)/.test(c.overflowX)&&el.scrollWidth>el.clientWidth+4)return 1}return 0}
addEventListener('wheel',function(e){ if(wgo||e.ctrlKey)return; var ax=Math.abs(e.deltaX),ay=Math.abs(e.deltaY);
  if(ax<=ay*1.5||ax<2){ if(ay>ax*1.5){wx=0;hideBox();} return; }
  if(wscroll(e.target))return; var s=document.querySelector('.mmd-sheet');if(s&&!s.hidden)return;
  var a=list(),i=cur();if(i<0)return; var now=Date.now(); if(now-wt>300)wx=0; wt=now; wx+=e.deltaX; e.preventDefault();
  var j=wx>0?i+1:i-1; if(j<0||j>=a.length){hideBox();return} wtg=a[j];
  box=document.getElementById('mm-swp')||document.body.appendChild(Object.assign(document.createElement('div'),{id:'mm-swp'}));
  box.textContent=wx>0?(wtg.textContent.trim()+' ›'):('‹ '+wtg.textContent.trim());
  var f=Math.min(Math.abs(wx)/160,1),pos=-120+f*136; box.style.opacity=Math.min(1,f*1.6);box.style.transform='translateY(-50%)';
  if(wx>0){box.style.right=pos+'px';box.style.left='auto'}else{box.style.left=pos+'px';box.style.right='auto'} box.classList.toggle('ready',f>=1);
  clearTimeout(window.__mmWt); window.__mmWt=setTimeout(function(){ if(Math.abs(wx)>=160&&wtg){ wgo=1; var h=wtg.getAttribute('href'); document.documentElement.classList.add('mm-leave'); setTimeout(function(){location.href=h},140); } else { wx=0; hideBox(); } },140);
},{passive:false});
}catch(e){}})();
// 차트 가장자리 = 넘김 전용(사용자 2026-11-01): 여기서 시작한 손가락·마우스는 차트 가격 추적으로 보내지 않음
(function(){try{
function edge(x,g){ if(!g||!g.closest)return 0; var H=document.documentElement; if(H.classList.contains('mm-full')||H.classList.contains('mm-land')||(window.__mmT&&window.__mmT.draw))return 0;
  var sv=g.closest('#main .mmt-box > svg'); if(!sv)return 0; var rb=sv.getBoundingClientRect(), EZ=Math.max(72,rb.width*0.22); return (x-rb.left<EZ||rb.right-x<EZ)?1:0; }
var hold=0;
function stop(e){ if(hold) e.stopPropagation(); }
document.addEventListener('pointerdown',function(e){ hold=e.pointerType!=='mouse'&&edge(e.clientX,e.target); if(hold) e.stopPropagation(); },true);
document.addEventListener('touchstart',function(e){ var t=e.touches[0]; hold=e.touches.length===1&&edge(t.clientX,e.target); if(hold) e.stopPropagation(); },{capture:true,passive:true});
['pointermove','touchmove'].forEach(function(n){ document.addEventListener(n,stop,{capture:true,passive:true}); });
['pointerup','pointercancel','touchend','touchcancel'].forEach(function(n){ document.addEventListener(n,function(e){ if(hold){ e.stopPropagation(); setTimeout(function(){hold=0},0); } },{capture:true,passive:true}); });
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

// 아이폰 키보드 닫은 뒤 아래 메뉴가 화면 가운데 떠 있던 것(사용자 2026-11-04, iOS 26 버그: 키보드를 닫아도 화면 높이를 '키보드 떠 있던 높이'로 기억)
// ① 키보드가 닫히면 페이지를 1px 움직였다 되돌려 다시 재게 함 ② 그래도 남는 차이(화면 높이 − 보이는 높이)가 있으면 아래 메뉴·이전홈·소리·손잡이를 그만큼 내려 붙임
(function(){try{var V=window.visualViewport;if(!V)return;var cur=0,q=0;
function ed(){var a=document.activeElement;return !!(a&&(a.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)))}
function put(g){if(g===cur)return;cur=g;['.mmd','#mm-fab','#mm-snd'].forEach(function(s){var e=document.querySelector(s);if(e){if(g)e.style.setProperty('translate','0 '+g+'px');else e.style.removeProperty('translate')}})}
function fix(){q=0;if(ed())return put(0);var g=Math.round(innerHeight-V.height-V.offsetTop);put(g>40&&g<innerHeight*.7?g:0)}
function sch(){if(!q){q=1;requestAnimationFrame(fix)}}
V.addEventListener('resize',sch);V.addEventListener('scroll',sch);addEventListener('scroll',sch,{passive:true});addEventListener('pageshow',sch);
document.addEventListener('focusout',function(){setTimeout(function(){if(ed())return;var y=scrollY;scrollTo(scrollX,y+1);requestAnimationFrame(function(){scrollTo(scrollX,y);sch()})},120);setTimeout(sch,600)},true);
}catch(e){}})();
