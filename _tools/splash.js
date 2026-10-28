// 처음 열 때 멍뭉이 로딩 화면(사용자 2026-10-29) — 의자를 돌려 앉으며 화이팅하는 움짤 뒤 앱으로 들어감. 같은 창에서는 다시 안 뜸, 누르면 바로 닫힘
(function(){try{if(sessionStorage.getItem('mmSplash')&&!/splash/.test(location.search))return;sessionStorage.setItem('mmSplash','1')}catch(e){return}
var d=document.createElement('div');d.id='mm-splash';d.innerHTML='<div class="sp-in"><div class="sp-v"><video muted playsinline webkit-playsinline autoplay preload="auto" poster="img/splash0.webp"><source src="img/splash.mp4" type="video/mp4"></video></div><b>멍뭉 터미널</b><small>AI 밸류체인 레이더</small><i><em></em></i><p>성공 투자를 기원합니다 🐾</p></div>';
function add(){(document.body||document.documentElement).appendChild(d);var v=d.querySelector('video');v.muted=true;var p=v.play&&v.play();if(p&&p.catch)p.catch(function(){v.poster='img/splash.webp';setTimeout(close,1400)});v.addEventListener('ended',function(){d.classList.add('done');setTimeout(close,650)});v.addEventListener('error',function(){setTimeout(close,1200)},true)}
if(document.body)add();else document.addEventListener('DOMContentLoaded',add);
function close(){if(d.classList.contains('out'))return;d.classList.add('out');setTimeout(function(){d.remove()},420)}
d.addEventListener('click',close);setTimeout(close,6500)})();
