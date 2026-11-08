// 업종 회전 지도 축 설명(사용자 2026-11-02 — "영상에서 설명한 대로 가로축·세로축 설명이 더 들어가면 좋겠다")
// 가로 = 3달(63거래일) S&P 대비 상대 수익, 세로 = 최근 1달(21거래일) S&P 대비. 네 칸마다 뜻 한 줄, 세로축 이름, 꼬리 읽는 법
(function(){try{
if(!/p-lights\.html/.test(location.pathname))return;
var NS='http://www.w3.org/2000/svg',MODE=window.__RX_MODE__||'cross';
var SUB={'선도':'돈이 몰리는 곳','약해지는 중':'잘 나가다 힘 빠지는 곳','소외':'돈이 빠져나간 곳','살아나는 중':'돈이 돌아오기 시작한 곳'};/* 옛 지도용(2판 지도에선 쓰지 않음) */
function tx(svg,x,y,t,anc,cls){var e=document.createElementNS(NS,'text');e.setAttribute('x',x);e.setAttribute('y',y);e.setAttribute('text-anchor',anc);e.setAttribute('class',cls);e.textContent=t;svg.appendChild(e);return e}
function deco(){var mp=document.querySelector('.mm-st-map');if(!mp)return;var svg=mp.querySelector('svg');if(!svg||svg.querySelector('.rx-sub')||svg.classList.contains('mm-rrg2'))return;/* 2판 지도(11/9)는 칸 설명·축이 이미 들어 있음 */
 var vb=(svg.getAttribute('viewBox')||'0 0 358 330').split(/\s+/).map(Number),W=vb[2],H=vb[3];
 // 네 칸 이름 밑에 뜻 한 줄
 [].forEach.call(svg.querySelectorAll('text'),function(t){var k=t.textContent.trim();if(!SUB[k])return;var y=+t.getAttribute('y'),top=y<H/2;
  tx(svg,t.getAttribute('x'),top?y+14:y-17,SUB[k],t.getAttribute('text-anchor'),'rx-sub')});
 // 세로축 이름(가운데 세로선 위·아래 끝)
 var vl=[].slice.call(svg.querySelectorAll('line')).find(function(l){return l.getAttribute('x1')===l.getAttribute('x2')});
 var hl=[].slice.call(svg.querySelectorAll('line')).find(function(l){return l.getAttribute('y1')===l.getAttribute('y2')});
 if(vl&&hl){var cy=+hl.getAttribute('y1');tx(svg,+vl.getAttribute('x1')+4,cy-4,'S&P 500 = 가운데','start','rx-c')}
 // 가로축 글자와 꼬리 읽는 법
 if(MODE==='math'||MODE==='cross'){[].forEach.call(svg.querySelectorAll(MODE==='math'?'.rx-sub,.rx-c':'.rx-c'),function(e){e.remove()});
  var df=document.createElementNS(NS,'defs');df.innerHTML='<marker id="rxar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#1d1a16"/></marker>';svg.appendChild(df);
  if(vl&&hl){var X=+vl.getAttribute('x1'),Y=+hl.getAttribute('y1');
   var l1=document.createElementNS(NS,'line');[['x1',10],['y1',Y],['x2',W-6],['y2',Y],['class','rx-axl'],['marker-end','url(#rxar)']].forEach(function(a){l1.setAttribute(a[0],a[1])});svg.appendChild(l1);
   var l2=document.createElementNS(NS,'line');[['x1',X],['y1',H-8],['x2',X],['y2',6],['class','rx-axl'],['marker-end','url(#rxar)']].forEach(function(a){l2.setAttribute(a[0],a[1])});svg.appendChild(l2);
   if(MODE==='cross'){tx(svg,X-5,Y+15,'0','end','rx-o')}
   else{tx(svg,W-8,Y+15,'x','end','rx-axt');tx(svg,X+7,15,'y','start','rx-axt');tx(svg,X-4,Y+14,'0','end','rx-o')}}
  var NUM={'선도':'① ','살아나는 중':'② ','소외':'③ ','약해지는 중':'④ '};
  [].forEach.call(svg.querySelectorAll('text'),function(t){var k=t.textContent.trim();if(NUM[k])t.textContent=NUM[k]+k})}
 // 세로축 이름은 지도 바로 위 한 줄(지도 안에 넣으면 업종 이름과 겹침)
 if(MODE==='cross'){var ot=mp.parentNode.querySelector('.rx-top');if(ot)ot.remove()}
 else if(!mp.previousElementSibling||!mp.previousElementSibling.classList.contains('rx-top')){var tp=document.createElement('div');tp.className='rx-top';tp.innerHTML=MODE==='cross'?'<span><b>가운데 0 = S&P 500</b>(미국 시장 전체) · <b>오른쪽 위</b>로 갈수록 강한 업종</span>':MODE==='math'?'<span><b>x축</b> 3달 성적 · <b>y축</b> 최근 1달 힘 · <b>0</b> = S&P 500</span>':'<span>▲ 위 = 최근 1달 S&P보다 강함</span><span>▼ 아래 = 약함</span>';mp.parentNode.insertBefore(tp,mp)}
 var ax=mp.parentNode.querySelector('.mm-st-ax');
 if(ax&&!ax.dataset.rx){ax.dataset.rx=1;var sp=ax.querySelectorAll('span');if(MODE==='cross'){ax.style.display='none'}if(sp[0])sp[0].textContent=MODE==='math'?'x < 0 : 3달 동안 S&P보다 약함':'◀ 3달 동안 S&P보다 약했음';if(sp[1])sp[1].textContent=MODE==='math'?'x > 0 : 강함':'3달 동안 S&P보다 강했음 ▶';
  var lg=document.createElement('div');lg.className='rx-leg';
  lg.innerHTML=(MODE==='cross'?'<p><b>수학 그래프처럼 보면 됩니다</b> — 가운데 0이 S&P 500입니다.</p><p class="rx-ex rx-sp"><b>S&P 500이 뭔가요?</b> 미국 대표 기업 500곳을 묶은 지수입니다. 보통 \'미국 시장\'이라고 하면 이 지수를 말합니다. 그래서 \'S&P보다 강함\' = \'시장 전체보다 더 잘했다\'는 뜻입니다.</p><p><b>x축(가로)</b> = 지난 3달 동안 S&P보다 얼마나 더(덜) 올랐나. 오른쪽(+)일수록 시장보다 잘했습니다.<br><b>y축(세로)</b> = 최근 1달 동안 S&P보다 얼마나 더(덜) 올랐나. 위쪽(+)일수록 요즘 시장보다 강합니다.</p><p><b>① 오른쪽 위 · 잘나가는 중</b> — 돈이 몰리는 곳 <b>② 왼쪽 위 · 살아나는 중</b> — 돈이 돌아오기 시작한 곳 <b>③ 왼쪽 아래 · 외면받는 중</b> — 돈이 빠져나간 곳 <b>④ 오른쪽 아래 · 식어가는 중</b> — 잘 나가다 힘 빠지는 곳</p><p>업종은 보통 <b>시계 방향</b>으로 돕니다(왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래). 선은 지난 4주 동안 지나온 길(작은 점 1주씩), 큰 점이 지금 자리입니다.</p>':MODE==='math'?'<p><b>수학 그래프처럼 보면 됩니다</b> — 원점 0이 S&P 500입니다. x는 3달 성적(시장보다 강하면 +), y는 최근 1달 힘(붙으면 +). <b>① x+·y+ 잘나가는 중</b>(돈이 몰리는 곳) · <b>② x−·y+ 살아나는 중</b> · <b>③ x−·y− 외면받는 중</b> · <b>④ x+·y− 식어가는 중</b>.</p><p>업종은 보통 2사분면 → 1 → 4 → 3 순서로, 시계 방향으로 돕니다. 선은 지난 4주 동안 지나온 길(작은 점 1주씩), 큰 점이 지금 자리입니다.</p>':'')+(MODE!=='plain'?'':'<p><b>이렇게 보면 됩니다</b> — 가운데 십자선이 S&P 500입니다. <b>오른쪽</b>에 있을수록 지난 3달 동안 시장보다 많이 올랐고, <b>위쪽</b>에 있을수록 최근 1달 힘이 붙고 있다는 뜻입니다.</p>'+
   '<p><b>선</b>은 지난 4주 동안 지나온 길(작은 점이 1주씩), <b>큰 점</b>이 지금 자리입니다. 업종은 보통 <b>시계 방향</b>으로 돕니다: 돌아오기 시작 → 몰림 → 힘 빠짐 → 빠져나감 → 다시 돌아옴.</p>')+ex();
  // 긴 설명은 접어 둠(사용자 2026-11-02 — 알고 싶은 사람만 펼쳐 보게, 스크롤 압박 줄이기): 기존 '이 지도 이렇게 읽습니다' 안 맨 위에 넣음
  var hw=mp.parentNode.querySelector('details.mm-st-how');
  if(hw){var sm=hw.querySelector('summary');if(sm)sm.textContent='▸ 이 지도 쉽게 보기 · 오늘 예시';hw.insertBefore(lg,sm?sm.nextSibling:hw.firstChild)}
  else{var dt=document.createElement('details');dt.className='mm-st-how';dt.innerHTML='<summary>▸ 이 지도 쉽게 보기 · 오늘 예시</summary>';dt.appendChild(lg);ax.parentNode.insertBefore(dt,ax.nextSibling)}}}
// 오늘 자료로 든 예시 한 줄(반도체·기술 중 지금 굵게 보이는 업종)
function ex(){try{var S=window.__MMTOP_S__||null;var se=null;
 [].some.call(document.querySelectorAll('.mm-st-map svg text'),function(t){var n=t.textContent.trim().split(' ')[0];if(/^(반도체|기술|에너지|헬스케어|통신|금융|산업재|유틸리티|경기소비재|필수소비재)$/.test(n)){se=n;return true}});
 var q=function(x,y){return x>=0&&y>=0?'잘나가는 중(돈이 몰리는 곳)':x>=0?'식어가는 중':y<0?'외면받는 중(돈이 빠져나간 곳)':'살아나는 중'};
 if(!EXD[se])return '';var p=EXD[se],a=p[0],z=p[p.length-1];
 return '<p class="rx-ex"><b>예) '+se+'</b> — 4주 전엔 '+q(a[0],a[1])+' 칸에 있었는데, 지금은 '+(z[0]<0?'3달 성적이 시장보다 약하고':'3달 성적은 시장보다 강하지만')+' '+(z[1]<0?'최근 1달은 더 약해져':'최근 1달 힘이 붙어')+' <b>'+q(z[0],z[1])+'</b> 칸에 있습니다.</p>'}catch(e){return ''}}
var EXD={};fetch('d/stress/stress.json?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.json()}).then(function(j){(j.sectors||[]).forEach(function(s){EXD[s.n]=s.trail});var l=document.querySelector('.rx-leg');if(l&&!l.querySelector('.rx-ex:not(.rx-sp)'))l.insertAdjacentHTML('beforeend',ex());watch()}).catch(function(){});
// 축 설명은 지도 밖 알약 3개 + 켜 둔 업종마다 '다음에 볼 방향' 한 줄 카드(사용자 2026-11-02 — 시안 2번 + 가안: '② 쪽으로 머리를 드는지 지켜볼 때')
var QN={1:'잘나가는 중',2:'살아나는 중',3:'외면받는 중',4:'식어가는 중'},WT={3:'살아나는 중 쪽으로 머리를 드는지',2:'잘나가는 중 쪽으로 넘어가는지',1:'식어가는 중 쪽으로 꺾이는지',4:'잘나가는 중 쪽으로 다시 머리를 드는지'};/* 칸 이름 쉬운 말로(11/9) */
function qd(p){return p[0]>=0?(p[1]>=0?1:4):(p[1]>=0?2:3)}
function hd(a,b){var dx=b[0]-a[0],dy=b[1]-a[1];return dy>=0?(dx>=0?'↗':'↖'):(dx>=0?'↘':'↙')}
function watch(){if(MODE!=='cross')return;var mp=document.querySelector('.mm-st-map');if(!mp)return;var svg=mp.querySelector('svg');if(!svg)return;
 var ch=mp.parentNode.querySelector('.rx-chips');if(!ch){ch=document.createElement('div');ch.className='rx-chips';ch.innerHTML='<span>→ 가로 = 3달 성적</span><span>↑ 세로 = 최근 1달 성적</span><span>0 = S&P 500</span>';mp.after(ch)}else if(ch.previousElementSibling!==mp)mp.after(ch);
 var sel=[];[].forEach.call(svg.querySelectorAll('text'),function(t){if(svg.classList.contains('mm-rrg2')&&t.getAttribute('font-size')!=='12.5')return;var n=t.textContent.trim().split(' ')[0];if(!EXD[n]||sel.some(function(x){return x[0]===n}))return;var tx0=+t.getAttribute('x'),ty0=+t.getAttribute('y'),col='#5b5246',bd=1e9;
  [].forEach.call(svg.querySelectorAll('circle'),function(c){var d=Math.hypot(+c.getAttribute('cx')-tx0,+c.getAttribute('cy')-ty0);var f=(svg.classList.contains('mm-rrg2')?c.getAttribute('stroke'):c.getAttribute('fill'))||'';if(+c.getAttribute('r')>=6&&d<bd&&f&&!/^(none|transparent)$/i.test(f)){bd=d;col=f}});sel.push([n,col])});
 var OR=['반도체','기술'];sel.sort(function(a,b){var i=OR.indexOf(a[0]),j=OR.indexOf(b[0]);return (i<0?9:i)-(j<0?9:j)});
 var key=sel.map(function(x){return x[0]}).join(',');var wa=mp.parentNode.querySelector('.rx-wa');
 if(wa&&wa.dataset.k===key&&wa.previousElementSibling===ch)return;if(!wa){wa=document.createElement('div');wa.className='rx-wa'}ch.after(wa);wa.dataset.k=key;wa.textContent='';
 sel.forEach(function(x){var t=EXD[x[0]];if(!t||t.length<2)return;var z=t[t.length-1],Q=qd(z);var r=document.createElement('div');r.className='rx-wr';r.style.setProperty('--c',x[1]);
  // 동그라미 숫자는 글자 대신 CSS로 그림(다른 정리 스크립트가 ①② 앞에 줄바꿈을 넣지 않게)
  var nm=function(s){return s.replace(/^([①②③④])\s*/,'<i class="rx-nb" data-n="$1"></i>')};
  r.innerHTML='<b class="rx-wn"></b><span class="rx-wq">'+nm(QN[Q])+' '+hd(t[t.length-2],z)+'</span><span class="rx-ww">👀 <b>'+nm(WT[Q])+'</b> 지켜볼 때</span>';r.querySelector('.rx-wn').textContent=x[0];wa.appendChild(r)})}
var n=0;(function t(){deco();watch();if(++n<20)setTimeout(t,500)})();
// 업종 버튼을 누르면 지도를 다시 그리므로 그때마다 다시 붙임(이미 붙어 있으면 아무것도 안 함)
document.addEventListener('click',function(){setTimeout(function(){deco();watch()},80);setTimeout(function(){deco();watch()},400)},true);
}catch(e){}})();
