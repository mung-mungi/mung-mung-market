// 홈 화면 앱으로 다시 시작하면 마지막 본 페이지 대신 메인(index)부터(사용자 2026-10-29)
// - 앱을 완전히 닫았다 다시 열면(새 세션) → 메인으로
// - 30분 넘게 다른 앱에 있다가 돌아와도 → 메인으로
// - 카톡 링크 등 일반 브라우저로 연 페이지는 그대로 둠(공유 링크가 메인으로 튀지 않게)
(function(){try{
var sa=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
var home=/\/(index\.html)?$/.test(location.pathname),LIM=30*60*1000,ss=sessionStorage,ls=localStorage;
function go(){try{ls.removeItem('mmHid')}catch(e){}location.replace('./')}
if(!sa){ss.setItem('mmAlive','1');return}
var h=+(ls.getItem('mmHid')||0),stale=h&&Date.now()-h>LIM;
if(!home&&(!ss.getItem('mmAlive')||stale)){ss.setItem('mmAlive','1');go();return}
ss.setItem('mmAlive','1');ls.removeItem('mmHid');
document.addEventListener('visibilitychange',function(){try{
if(document.hidden){ls.setItem('mmHid',String(Date.now()));return}
var t=+(ls.getItem('mmHid')||0);ls.removeItem('mmHid');
if(!home&&t&&Date.now()-t>LIM)go()}catch(e){}});
window.addEventListener('pageshow',function(e){try{if(!e.persisted||home)return;var t=+(ls.getItem('mmHid')||0);if(t&&Date.now()-t>LIM)go()}catch(x){}});
}catch(e){}})();
// 새 판 자동 반영(사용자 2026-10-29) — 페이지를 열어 둔 채(앱이 메모리에 남아) 있어도 화면 수정이 올라오면 반영
// - 다른 앱 갔다 돌아올 때 새 판이 있으면 → 조용히 새로 불러옴
// - 보고 있는 중(10분마다 확인)에 새 판이 나오면 → 아래 작은 '새 화면 ↻' 알약만 띄움(읽는 도중 화면이 튀지 않게)
// - 5분 시세 갱신은 판 번호를 안 올리므로 여기에 걸리지 않음
(function(){try{
function me(){var s=document.querySelector('script[data-ver]');return s?s.getAttribute('data-ver'):''}
function reload(v){var u=new URL(location.href);u.searchParams.set('v',v);location.replace(u.toString())}
var busy=0,pill=null;
function check(quiet){if(busy||!me())return;busy=1;
fetch('version.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){busy=0;
if(!j||!j.v||j.v<=me())return;if(quiet)return reload(j.v);if(pill)return;
pill=document.createElement('button');pill.textContent='새 화면이 나왔습니다 ↻';
pill.setAttribute('style','position:fixed;left:50%;transform:translateX(-50%);bottom:calc(92px + env(safe-area-inset-bottom));z-index:99999;border:0;border-radius:999px;padding:9px 16px;font:700 14px/1 inherit;background:#1f2329;color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.25)');
pill.onclick=function(){reload(j.v)};(document.body||document.documentElement).appendChild(pill)}).catch(function(){busy=0})}
var hidAt=0;
document.addEventListener('visibilitychange',function(){if(document.hidden){hidAt=Date.now();return}if(hidAt&&Date.now()-hidAt>15000)check(true)});
window.addEventListener('pageshow',function(e){if(e.persisted)check(true)});
setInterval(function(){if(!document.hidden)check(false)},10*60*1000);
}catch(e){}})();
