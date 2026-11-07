// 실적 일정: 이번 주 일정이 끝나면(한국시간 날짜가 주간 마지막 날을 지나면) '다음 주 미리 보기'를 맨 위로(사용자 2026-11-07)
// 새 주 자료(월요일 자정 실행)가 들어오면 저절로 꺼짐. 페이지 원본은 건드리지 않고 순서·문구만 바꿈
(function(){
if(!/p-cal\.html/.test(location.pathname))return;
function kst(){var n=new Date();return new Date(n.getTime()+n.getTimezoneOffset()*6e4+9*36e5)}
var WD=['일','월','화','수','목','금','토'];
function md(d){return (d.getMonth()+1)+'/'+d.getDate()}
function run(){var D,N;try{D=DAYS;N=NEXT}catch(e){return false}
 if(!D||!D.length||!N||!N.length)return true;if(document.querySelector('.mm-nx'))return true;
 var now=kst(),t=new Date(now.getFullYear(),now.getMonth(),now.getDate());
 var z=D[D.length-1].d.split('/'),a=D[0].d.split('/'),last=new Date(now.getFullYear(),+z[0]-1,+z[1]);
 if(last-t>180*864e5)last.setFullYear(last.getFullYear()-1);
 if(t<=last)return true;                       // 아직 이번 주 진행 중
 var mon=new Date(last);while(mon.getDay()!==1)mon.setDate(mon.getDate()+1);var fri=new Date(mon);fri.setDate(mon.getDate()+4);
 if(t>fri)return true;                         // 다음 주까지 지나도록 갱신이 없으면 손대지 않음
 var nw=document.getElementById('nextw'),pn=nw&&nw.closest('section'),top=document.getElementById('next');if(!pn||!top)return false;
 pn.classList.add('mm-nx');var h2=pn.querySelector('h2');
 if(h2){h2.textContent='';var s=document.createElement('span');s.className='mm-nx-tag';s.textContent='이번 주 일정 끝';h2.appendChild(s);
  h2.appendChild(document.createTextNode('다음 주 미리 보기 · '+md(mon)+'(월) – '+md(fri)+'(금)'))}
 var f=N[0],first=(f.h||'').replace(/\s*·.*$/,'').replace(/\s+아시아$/,'')+' '+((f.ev[0]||{}).n||'');
 var p=document.createElement('p');p.className='mm-nx-first';p.innerHTML='<b>다음 발표</b> ';p.appendChild(document.createTextNode(first.trim()+' — '+((f.ev[0]||{}).x||'')));
 h2?h2.after(p):pn.prepend(p);
 top.after(pn);
 // 다음 주 밖 일정(1월 등)은 접어 둠
 var later=[];[].slice.call(nw.children).forEach(function(c,i){var h=(N[i]||{}).h||'',m=h.match(/^(\d+)\/(\d+)/);var dd=m?new Date(mon.getFullYear()+(+m[1]<mon.getMonth()+1-6?1:0),+m[1]-1,+m[2]):null;if(!dd||dd>new Date(fri.getTime()+864e5))later.push(c)});
 if(later.length){var dt=document.createElement('details');dt.className='mm-nx-later';var su=document.createElement('summary');su.textContent='그 뒤 일정 '+later.length+'개 보기';dt.appendChild(su);var g=document.createElement('div');g.className='nextw';later.forEach(function(c){g.appendChild(c)});dt.appendChild(g);nw.after(dt)}
 // 맨 위 '오늘 —곳' 칸 → '다음 발표'(요약 칸은 calui.js가 그림 — 다시 그려져도 덮어씀)
 var ev0=f.ev[0]||{},dl=(f.h||'').match(/^[\d\/~]+(\([^)]*\))?/);dl=dl?dl[0]:'';
 function tile(){var ts=top.querySelectorAll('.cn-tile');var x=ts[1];if(!x||x.dataset.nx)return;x.dataset.nx=1;x.classList.add('mm-nx-tile');
  x.innerHTML='<small>다음 발표</small><b></b><em></em>';x.querySelector('b').textContent=dl;x.querySelector('em').textContent=ev0.n||''}
 var c=0;(function tk(){try{tile()}catch(e){}if(++c<40)setTimeout(tk,300)})();
 var ws=document.getElementById('weekstory');if(ws){var l=document.createElement('div');l.className='mm-nx-past';l.textContent='↓ 지난 주 '+D[0].d+'('+D[0].w+') – '+D[D.length-1].d+'('+D[D.length-1].w+') 발표 결과';ws.before(l)}
 return true}
var k=0;(function go(){var ok=false;try{ok=run()}catch(e){ok=true}if(!ok&&++k<40)setTimeout(go,250)})();
})();
