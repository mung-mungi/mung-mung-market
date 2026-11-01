// 업종 회전 지도 축 설명(사용자 2026-11-02 — "영상에서 설명한 대로 가로축·세로축 설명이 더 들어가면 좋겠다")
// 가로 = 3달(63거래일) S&P 대비 상대 수익, 세로 = 최근 1달(21거래일) S&P 대비. 네 칸마다 뜻 한 줄, 세로축 이름, 꼬리 읽는 법
(function(){try{
if(!/p-lights\.html/.test(location.pathname))return;
var NS='http://www.w3.org/2000/svg';
var SUB={'선도':'3달 강 · 1달도 강','약해지는 중':'3달 강 · 1달 꺾임','소외':'3달 약 · 1달도 약','살아나는 중':'3달 약 · 1달 회복'};
function tx(svg,x,y,t,anc,cls){var e=document.createElementNS(NS,'text');e.setAttribute('x',x);e.setAttribute('y',y);e.setAttribute('text-anchor',anc);e.setAttribute('class',cls);e.textContent=t;svg.appendChild(e);return e}
function deco(){var mp=document.querySelector('.mm-st-map');if(!mp)return;var svg=mp.querySelector('svg');if(!svg||svg.querySelector('.rx-sub'))return;
 var vb=(svg.getAttribute('viewBox')||'0 0 358 330').split(/\s+/).map(Number),W=vb[2],H=vb[3];
 // 네 칸 이름 밑에 뜻 한 줄
 [].forEach.call(svg.querySelectorAll('text'),function(t){var k=t.textContent.trim();if(!SUB[k])return;var y=+t.getAttribute('y'),top=y<H/2;
  tx(svg,t.getAttribute('x'),top?y+14:y-17,SUB[k],t.getAttribute('text-anchor'),'rx-sub')});
 // 세로축 이름(가운데 세로선 위·아래 끝)
 var vl=[].slice.call(svg.querySelectorAll('line')).find(function(l){return l.getAttribute('x1')===l.getAttribute('x2')});
 var hl=[].slice.call(svg.querySelectorAll('line')).find(function(l){return l.getAttribute('y1')===l.getAttribute('y2')});
 if(vl&&hl){var cy=+hl.getAttribute('y1');tx(svg,+vl.getAttribute('x1')+4,cy-4,'S&P 500 = 가운데','start','rx-c')}
 // 가로축 글자와 꼬리 읽는 법
 // 세로축 이름은 지도 바로 위 한 줄(지도 안에 넣으면 업종 이름과 겹침)
 if(!mp.previousElementSibling||!mp.previousElementSibling.classList.contains('rx-top')){var tp=document.createElement('div');tp.className='rx-top';tp.innerHTML='<span>▲ 위 = 최근 1달 S&P보다 강함</span><span>▼ 아래 = 약함</span>';mp.parentNode.insertBefore(tp,mp)}
 var ax=mp.parentNode.querySelector('.mm-st-ax');
 if(ax&&!ax.dataset.rx){ax.dataset.rx=1;var sp=ax.querySelectorAll('span');if(sp[0])sp[0].textContent='◀ 3달 동안 S&P보다 약했음';if(sp[1])sp[1].textContent='3달 동안 S&P보다 강했음 ▶';
  var lg=document.createElement('p');lg.className='rx-leg';lg.innerHTML='<b>선</b> = 지난 4주 동안 지나온 길(작은 점이 1주씩) · <b>큰 점</b> = 지금 위치 · 보통 <b>시계 방향</b>으로 돕니다(살아나는 중 → 선도 → 약해지는 중 → 소외)';ax.parentNode.insertBefore(lg,ax.nextSibling)}}
var n=0;(function t(){deco();if(++n<20)setTimeout(t,500)})();
// 업종 버튼을 누르면 지도를 다시 그리므로 그때마다 다시 붙임(이미 붙어 있으면 아무것도 안 함)
document.addEventListener('click',function(){setTimeout(deco,80);setTimeout(deco,400)},true);
}catch(e){}})();
