// 메인 '오늘' 카드(날짜 칩 + 헤드라인)를 다른 카드처럼 누르게 생긴 버튼으로 — 누르면 데일리 시황으로 이동(사용자 2026-11-02)
// 아래 WTI 같은 숫자 칸은 원래대로 그 차트로 감(.stats는 건드리지 않음)
(function(){try{
function fix(){var t=document.querySelector('.today');if(!t)return;var b=t.querySelector('.body');if(!b)return;
 if(t.classList.contains('mm-tb')&&b.querySelector('.mm-tb-go'))return;t.classList.add('mm-tb');
 b.setAttribute('role','button');b.setAttribute('tabindex','0');b.setAttribute('aria-label','데일리 시황 보기');
 var g=document.createElement('span');g.className='mm-tb-go';g.textContent='아침 시황 전체 보기 →';b.appendChild(g);
 var a=document.createElement('span');a.className='mm-tb-ar';a.setAttribute('aria-hidden','true');a.textContent='›';b.appendChild(a);
 if(!b.__tb){b.__tb=1;var go=function(){location.href='p-brief.html'};b.addEventListener('click',function(e){if(e.target.closest('a,.stats'))return;go()});b.addEventListener('keydown',function(e){if(e.key==='Enter')go()})}}
var k=0;(function t(){fix();if(++k<16)setTimeout(t,500)})();
}catch(e){}})();
