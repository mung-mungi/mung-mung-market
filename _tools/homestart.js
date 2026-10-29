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
