// 처음 열 때 멍뭉이 로딩 화면(사용자 2026-10-29, 2026-11-01 개정) — 의자 돌려 앉기 → 살짝 쉬고 → 화이팅 → '딸깍' 하고 앱으로 들어감(약 2.2초).
// 움짤은 프레임 보간으로 끊김을 없앤 splash-v2. 같은 창에서는 다시 안 뜸, 누르면 바로 닫힘, ?splash 로 확인 가능
(function(){try{if(sessionStorage.getItem('mmSplash')&&!/splash/.test(location.search))return;sessionStorage.setItem('mmSplash','1')}catch(e){return}
var d=document.createElement('div');d.id='mm-splash';d.innerHTML='<div class="sp-in"><div class="sp-v"><video muted playsinline webkit-playsinline autoplay preload="auto" poster="img/splash-v2.webp"><source src="img/splash-v2.mp4" type="video/mp4"></video></div><b>멍뭉 터미널</b><small>AI 밸류체인 레이더</small><i><em></em></i><p>성공 투자를 기원합니다 🐾</p></div>';
function add(){(document.body||document.documentElement).appendChild(d);var v=d.querySelector('video');v.muted=true;var p=v.play&&v.play();if(p&&p.catch)p.catch(function(){setTimeout(close,900)});v.addEventListener('ended',function(){d.classList.add('click');setTimeout(close,140)});v.addEventListener('error',function(){setTimeout(close,900)},true)}
add(); // 본문을 기다리지 않고 바로 붙임 — 메인이 먼저 깜빡 보이던 것 방지(2026-11-01)
function close(){if(d.classList.contains('out'))return;d.classList.add('out');setTimeout(function(){d.remove()},240)}
d.addEventListener('click',close);setTimeout(close,3200)})();
