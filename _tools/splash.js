// 처음 열 때 멍뭉이 로딩 화면(사용자 2026-10-29) — 한 번 연 뒤 같은 창에서는 다시 안 뜸, 누르면 바로 닫힘
(function(){try{if(sessionStorage.getItem('mmSplash'))return;sessionStorage.setItem('mmSplash','1')}catch(e){return}
var d=document.createElement('div');d.id='mm-splash';d.innerHTML='<div class="sp-in"><img src="img/splash.webp" alt=""><b>멍뭉 터미널</b><small>AI 밸류체인 레이더</small><i><em></em></i><p>성공 투자를 기원합니다 🐾</p></div>';
function add(){(document.body||document.documentElement).appendChild(d)}if(document.body)add();else document.addEventListener('DOMContentLoaded',add);
var t0=Date.now();function close(){if(d.classList.contains('out'))return;d.classList.add('out');setTimeout(function(){d.remove()},380)}
d.addEventListener('click',close);window.addEventListener('load',function(){setTimeout(close,Math.max(0,1100-(Date.now()-t0)))});setTimeout(close,3000)})();
