// 분류 알약 줄 접기·펼치기(사용자 2026-11-02 확정 시안) — 주요 뉴스·AI·테크 뉴스의 #catf
// 평소 한 줄(새 소식 많은 순은 tlx.js가 정렬) + 오른쪽 흐림 + 끝에 '전체 n ▾', 누르면 3열로 전부 + '접기 ▴'. 숫자 배지(.tlx-cn)는 tlx.js가 씀
(function(){try{
function fix(){var c=document.getElementById('catf');if(!c)return;var w=c.parentNode;
 if(!w.classList.contains('mx-wrap')){w=document.createElement('div');w.className='mx-wrap';c.parentNode.insertBefore(w,c);w.appendChild(c)}
 var n=c.querySelectorAll('button').length;var m=w.querySelector('.mx-more');
 if(!m){m=document.createElement('button');m.type='button';m.className='mx-more';m.setAttribute('role','button');w.appendChild(m);
  m.onclick=function(){var o=w.classList.toggle('mx-open');lab();if(!o)c.scrollLeft=0}}
 function lab(){var t=w.classList.contains('mx-open')?'접기 ▴':'전체 '+n+' ▾';if(m.textContent!==t)m.textContent=t}lab();
 // 펼친 상태에서 분류를 고르면 다시 한 줄로(고른 분류가 맨 앞에 보이게)
 if(!c.__mx){c.__mx=1;c.addEventListener('click',function(e){if(e.target.closest('button')&&w.classList.contains('mx-open')){w.classList.remove('mx-open');lab()}})}}
var k=0;(function t(){fix();if(++k<16)setTimeout(t,500)})();
}catch(e){}})();
