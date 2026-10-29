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
