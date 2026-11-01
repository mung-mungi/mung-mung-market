// 분류·필터 알약 줄 통일(사용자 2026-11-02 확정 → 사이트 전체) — 견본: 주요 뉴스·AI·테크 뉴스의 #catf
// 평소 한 줄 밀기 + 화면 폭을 넘으면 오른쪽 흐림 + 끝에 '전체 n ▾' 고정 → 누르면 그 자리에서 3열로 전부 + '접기 ▴'(15개 이상이면 펼친 칸 안에서만 스크롤).
// 펼친 상태에서 알약을 고르면 다시 한 줄로 접음. 폭 안에 다 들어가는 짧은 줄은 흐림·'전체' 없음.
// 숫자 배지(.tlx-cn, 새 소식 수)는 뉴스 두 페이지의 tlx.js가 씀 — 뉴스는 '지금 시장의 관심도'라 새 소식 많은 순 정렬도 그쪽. 나머지 페이지는 순서·글자를 바꾸지 않고 접기·펼치기만.
// 고르면 페이지가 줄을 다시 그리는 경우가 있어 '이미 했음'은 부모가 실제 .mx-wrap인지로 판단(MutationObserver로 다시 확인).
(function(){try{
var PG=(location.pathname.split('/').pop()||'').replace(/\.html$/,'');
// 실적 결과 '기간'(#fd)은 이미 회색 홈 탭(하위 줄 양식)이라 그대로 둠
var SEL={'p-policy':['#catf'],'p-tech':['#catf'],'p-prices':['#chips'],'p-trend':['#cats'],'p-short':['#lchips','.dp-l','.dp-t'],
 'p-targets':['#vs-chips','#trend-chips'],'p-earn':['.ir-pills','#fl'],'p-qtr':['#qchips']}[PG];
if(!SEL)return;
// 아래(하위) 줄 — 위 줄과 모양을 달리함(회색 홈 탭, 사용자 2026-11-02)
var SUB={'p-short':['.dp-t']}[PG]||[];
function cnt(c){var n=0;for(var i=0;i<c.children.length;i++){var x=c.children[i];if(!x.classList.contains('mx-more')&&getComputedStyle(x).display!=='none')n++}return n}
function lab(w){var c=w.querySelector(':scope>.mx-row'),m=w.querySelector(':scope>.mx-more');if(!c||!m)return;var t=w.classList.contains('mx-open')?'접기 ▴':'전체 '+cnt(c)+' ▾';if(m.textContent!==t)m.textContent=t}
function one(c){var w=c.parentNode;if(!w)return;
 if(!w.classList.contains('mx-wrap')){w=document.createElement('div');w.className='mx-wrap';c.parentNode.insertBefore(w,c);w.appendChild(c)}
 if(!c.classList.contains('mx-row'))c.classList.add('mx-row');
 if(SUB.some(function(q){return c.matches(q)})&&!w.classList.contains('mx-sub'))w.classList.add('mx-sub');
 var n=cnt(c);if(w.classList.contains('mx-long')!==(n>=15))w.classList.toggle('mx-long',n>=15);
 var m=w.querySelector(':scope>.mx-more');
 if(!m){m=document.createElement('button');m.type='button';m.className='mx-more';m.setAttribute('role','button');w.appendChild(m);
  m.onclick=function(){var o=w.classList.toggle('mx-open');lab(w);if(!o){c.scrollLeft=0;var r=w.getBoundingClientRect();if(r.top<0)scrollBy(0,r.top-60)}}}
 if(!c.__mx){c.__mx=1;c.addEventListener('click',function(e){if(e.target.closest('button,a,[role=button]')&&w.classList.contains('mx-open')){setTimeout(function(){w.classList.remove('mx-open');lab(w)},0)}},true)}  // 잡기 단계(true): 페이지가 클릭 전파를 막아도 접힘
 // 폭 안에 다 들어가면 흐림·'전체' 없음(펼친 상태가 아닐 때만, 보이는 줄만 잼)
 if(!w.classList.contains('mx-open')&&c.clientWidth>0){var fit=c.scrollWidth<=c.clientWidth+2+(w.classList.contains('mx-fit')?0:72);if(w.classList.contains('mx-fit')!==fit)w.classList.toggle('mx-fit',fit)}
 lab(w)}
function fix(){SEL.forEach(function(s){document.querySelectorAll(s).forEach(function(c){try{one(c)}catch(e){}})})}
var k=0;(function t(){fix();if(++k<30)setTimeout(t,500)})();
try{new MutationObserver(function(){fix()}).observe(document.body,{childList:true,subtree:true})}catch(e){}
}catch(e){}})();
