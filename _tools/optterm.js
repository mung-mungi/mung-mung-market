// 옵션 온도계 '기간구조' 쉽게 읽기(사용자 2026-11-02 — "그래프 설명이 어렵고 오른쪽 진한 선·옅은 선 관계를 모르겠다")
// ① 맨 위 '지금은' 한 줄 판정 ② 설명 문장을 쉬운 말로 ③ 선 끝에 이름표(최근·하루 전 / 지금 공포·3개월 뒤) ④ 하루 새 변화 한 줄 ⑤ 자료가 오래되면 경고
(function(){try{
if(!/p-opt\.html/.test(location.pathname))return;
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
var F=null,R=null,done={};
function md(d){return d?(+d.slice(5,7))+'.'+(+d.slice(8,10)):''}
function daysOld(d){return Math.round((Date.now()-new Date(d+'T21:00:00Z'))/864e5)}
function verdict(){var card=document.getElementById('term-card');if(!card||!F||done.v)return;
 var keys=Object.keys(F[0]).filter(function(k){return /^settle_/.test(k)}).sort();var kS=keys[keys.length-1],kP=keys[keys.length-2],dS=kS.slice(7),dP=kP?kP.slice(7):'';
 var f=F[0][kS],l=F[F.length-1][kS],up=l>f,dd=kP?F.reduce(function(a,r){return a+(r[kS]-r[kP])},0)/F.length:0;
 var r=R&&R.length?R[R.length-1]:null,ratio=r?r.ratio:null;
 var hot=ratio!=null?ratio>=1:!up,near=ratio!=null&&ratio>=0.9&&ratio<1;
 var st=hot?['🔴','공포 쪽(백워데이션)','지금 당장이 더 무섭다는 뜻입니다']:near?['🟡','평온 쪽이지만 문턱 근처','지금 공포가 3개월 뒤 예상에 바짝 붙었습니다']:['🟢','평온 쪽(콘탱고)','당장보다 나중을 더 걱정하는, 보통의 모습입니다'];
 var box=document.createElement('div');box.className='ott-now';
 var old=daysOld(dS);
 box.innerHTML='<div class="ott-h"><span class="ott-b">'+st[0]+' 지금은 '+st[1]+'</span>'+(old>4?'<span class="ott-old">⚠ 선물 커브 '+md(dS)+' 정산 · '+old+'일 전 자료</span>':'')+'</div>'+
  '<p>'+st[2]+'</p>'+
  '<ul><li><b>VIX ÷ VIX3M</b> '+(ratio!=null?ratio.toFixed(2):'—')+(r?' ('+md(r.date)+')':'')+' — 1을 넘으면 공포 쪽, 지금은 '+(ratio!=null?(ratio>=1?'넘었습니다':'1보다 '+(1-ratio).toFixed(2)+' 아래'):'—')+'</li>'+
  '<li><b>선물 커브</b> 가까운 달 '+f.toFixed(1)+' → 먼 달 '+l.toFixed(1)+' · '+(up?'오른쪽으로 갈수록 오름 = 평온':'오른쪽으로 갈수록 내림 = 공포')+'</li>'+
  (kP?'<li><b>하루 새</b> 커브 전체가 평균 '+(dd>=0?'+':'')+dd.toFixed(2)+' '+(Math.abs(dd)<0.05?'— 거의 그대로':dd>0?'— 공포 가격이 조금 올랐습니다(진한 선이 흐린 선 위)':'— 공포 가격이 조금 내렸습니다(진한 선이 흐린 선 아래)')+'</li>':'')+'</ul>';
 var sub=card.querySelector('.sub');
 if(sub){sub.innerHTML='<b>왼쪽</b> 파랑 = 지금 공포(VIX), 노랑 = 3개월 뒤 예상 공포(VIX3M). <b>파랑이 노랑 위로 올라오면</b> 지금이 더 무섭다는 신호입니다. <b>오른쪽</b> = 달마다의 공포 가격(VIX 선물). <b>오른쪽으로 갈수록 오르면 평온</b>, 내려가면 공포입니다. 진한 선은 최근, 흐린 선은 하루 전입니다.';
  sub.parentNode.insertBefore(box,sub.nextSibling)}else card.insertBefore(box,card.children[1]);
 done.v=1;done.dS=dS;done.dP=dP;done.dd=dd}
function svgText(svg,x,y,t,cls,anchor){var e=document.createElementNS('http://www.w3.org/2000/svg','text');e.setAttribute('x',x);e.setAttribute('y',y);e.setAttribute('class',cls);e.setAttribute('text-anchor',anchor||'end');e.textContent=t;svg.appendChild(e);return e}
function lastPt(p){var d=p.getAttribute('d')||'';var m=d.match(/[ML]([\d.]+),([\d.]+)(?!.*[ML][\d.]+,[\d.]+)/);return m?[+m[1],+m[2]]:null}
function firstPt(p){var m=(p.getAttribute('d')||'').match(/M([\d.]+),([\d.]+)/);return m?[+m[1],+m[2]]:null}
function labels(){
 var fs=document.querySelector('#fut-chart svg');
 if(fs&&!fs.querySelector('.ott-lb')&&done.v){var ps=[].slice.call(fs.querySelectorAll('path')).filter(function(p){return /dc4/.test(p.getAttribute('stroke')||'')});
  var light=ps.find(function(p){return +(p.getAttribute('stroke-opacity')||p.getAttribute('opacity')||1)<1}),dark=ps.find(function(p){return p!==light});
  if(dark&&light){var a=firstPt(dark),b=firstPt(light);
   // 선 위 이름표는 값 숫자와 겹쳐서 범례 이름 + 위쪽 한 줄 설명으로 대신함
   svgText(fs,318,14,done.dd>=0.05?'진한 선이 위 = 하루 새 공포 가격 ↑':done.dd<=-0.05?'진한 선이 아래 = 하루 새 공포 가격 ↓':'두 선이 거의 겹침 = 하루 새 변화 없음','ott-lb ott-note','end')}}
 var ts=document.querySelector('#term-chart svg');
 if(ts&&!ts.querySelector('.ott-lb')){var pv=[].slice.call(ts.querySelectorAll('path')).filter(function(p){return /dc1/.test(p.getAttribute('stroke')||'')}).sort(function(a,b){return (b.getAttribute('d')||'').length-(a.getAttribute('d')||'').length})[0];
  var p3=[].slice.call(ts.querySelectorAll('path')).filter(function(p){return /dc2/.test(p.getAttribute('stroke')||'')}).sort(function(a,b){return (b.getAttribute('d')||'').length-(a.getAttribute('d')||'').length})[0];
  if(pv){var e=lastPt(pv);if(e)svgText(ts,e[0]-4,e[1]+16,'지금 공포','ott-lb ott-v')}
  if(p3){var e3=lastPt(p3);if(e3)svgText(ts,e3[0]-4,e3[1]-8,'3개월 뒤 예상','ott-lb ott-3')}}
 // 범례 이름도 쉬운 말로
 [].forEach.call(document.querySelectorAll('#fut-legend span, #term-legend span'),function(s){var t=s.lastChild;if(!t||t.nodeType!==3)return;var v=t.nodeValue;
  if(done.dS&&v.indexOf(done.dS.slice(5).replace('-','.'))>=0&&v.indexOf('최근')<0)t.nodeValue=v+' (최근·진한 선)';
  else if(done.dP&&v.indexOf(done.dP.slice(5).replace('-','.'))>=0&&v.indexOf('하루 전')<0)t.nodeValue=v+' (하루 전·흐린 선)'})}
function go(){verdict();labels()}
Promise.all([j('d/opt/vix_futures.json'),j('d/opt/vix_ratio.json')]).then(function(a){F=a[0];R=a[1];if(!F||!F.length)return;
 var n=0;(function t(){go();if(++n<12)setTimeout(t,500)})();
 // 화면 크기가 바뀌어 차트가 다시 그려지면 이름표만 다시(값이 같으면 다시 쓰지 않음)
 addEventListener('resize',function(){setTimeout(labels,400)})});
}catch(e){}})();
