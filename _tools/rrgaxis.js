// 업종 회전 지도 축 설명(사용자 2026-11-02 — "영상에서 설명한 대로 가로축·세로축 설명이 더 들어가면 좋겠다")
// 가로 = 3달(63거래일) S&P 대비 상대 수익, 세로 = 최근 1달(21거래일) S&P 대비. 네 칸마다 뜻 한 줄, 세로축 이름, 꼬리 읽는 법
(function(){try{
if(!/p-lights\.html/.test(location.pathname))return;
var NS='http://www.w3.org/2000/svg';
var SUB={'선도':'돈이 몰리는 곳','약해지는 중':'잘 나가다 힘 빠지는 곳','소외':'돈이 빠져나간 곳','살아나는 중':'돈이 돌아오기 시작한 곳'};
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
  var lg=document.createElement('div');lg.className='rx-leg';
  lg.innerHTML='<p><b>이렇게 보면 됩니다</b> — 가운데 십자선이 S&P 500입니다. <b>오른쪽</b>에 있을수록 지난 3달 동안 시장보다 많이 올랐고, <b>위쪽</b>에 있을수록 최근 1달 힘이 붙고 있다는 뜻입니다.</p>'+
   '<p><b>선</b>은 지난 4주 동안 지나온 길(작은 점이 1주씩), <b>큰 점</b>이 지금 자리입니다. 업종은 보통 <b>시계 방향</b>으로 돕니다: 돌아오기 시작 → 몰림 → 힘 빠짐 → 빠져나감 → 다시 돌아옴.</p>'+ex();
  ax.parentNode.insertBefore(lg,ax.nextSibling)}}
// 오늘 자료로 든 예시 한 줄(반도체·기술 중 지금 굵게 보이는 업종)
function ex(){try{var S=window.__MMTOP_S__||null;var se=null;
 [].some.call(document.querySelectorAll('.mm-st-map svg text'),function(t){var n=t.textContent.trim();if(/^(반도체|기술|에너지|헬스케어|통신|금융|산업재|유틸리티|경기소비재|필수소비재)$/.test(n)){se=n;return true}});
 var q=function(x,y){return x>=0&&y>=0?'선도(돈이 몰리는 곳)':x>=0?'약해지는 중':y<0?'소외(돈이 빠져나간 곳)':'살아나는 중'};
 if(!EXD[se])return '';var p=EXD[se],a=p[0],z=p[p.length-1];
 return '<p class="rx-ex"><b>예) '+se+'</b> — 4주 전엔 '+q(a[0],a[1])+' 칸에 있었는데, 지금은 '+(z[0]<0?'3달 성적이 시장보다 약하고':'3달 성적은 시장보다 강하지만')+' '+(z[1]<0?'최근 1달은 더 약해져':'최근 1달 힘이 붙어')+' <b>'+q(z[0],z[1])+'</b> 칸에 있습니다.</p>'}catch(e){return ''}}
var EXD={};fetch('d/stress/stress.json?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.json()}).then(function(j){(j.sectors||[]).forEach(function(s){EXD[s.n]=s.trail});var l=document.querySelector('.rx-leg');if(l&&!l.querySelector('.rx-ex'))l.insertAdjacentHTML('beforeend',ex())}).catch(function(){});
var n=0;(function t(){deco();if(++n<20)setTimeout(t,500)})();
// 업종 버튼을 누르면 지도를 다시 그리므로 그때마다 다시 붙임(이미 붙어 있으면 아무것도 안 함)
document.addEventListener('click',function(){setTimeout(deco,80);setTimeout(deco,400)},true);
}catch(e){}})();
