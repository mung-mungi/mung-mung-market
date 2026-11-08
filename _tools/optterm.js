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
 var st=hot?['🔴','공포 쪽(백워데이션)','지금 당장이 더 무섭다는 뜻입니다']:near?['🟡','평온 쪽이지만 문턱 근처','지금 불안이 3개월 뒤 예상 불안에 바짝 붙었습니다']:['🟢','평온 쪽(콘탱고)','당장보다 나중을 더 걱정하는, 보통의 모습입니다'];
 var box=document.createElement('div');box.className='ott-now';
 var old=daysOld(dS);
 var fm=function(r){return (+r.month.slice(5))+'월물'};
 box.innerHTML='<div class="ott-h"><span class="ott-b">'+st[0]+' 지금은 '+st[1]+'</span>'+(old>4?'<span class="ott-old">⚠ 선물 커브 '+md(dS)+' 정산 · '+old+'일 전 자료</span>':'')+'</div>'+
  '<p>'+st[2]+(r?' <span class="ott-num">지금 불안 '+r.vix.toFixed(1)+' vs 3개월 뒤 '+r.vix3m.toFixed(1)+'</span>':'')+'</p>'+
  '<p class="ott-ana">🛡 <b>보험료로 생각하면 쉽습니다.</b> VIX는 \'다음 한 달 주가 폭락 보험료\'입니다. 평소엔 먼 미래가 더 불확실해 <b>3개월짜리 보험이 더 비쌉니다</b>(콘탱고 = 평온). 그런데 당장 사고가 날 것 같으면 <b>이번 달 보험이 더 비싸집니다</b>(백워데이션 = 공포).</p>'+
  '<details class="ott-more"><summary role="button">▸ 숫자로 자세히 · VIX가 뭔가요?</summary>'+
  
  '<p class="ott-q"><b>VIX가 뭔가요?</b> 앞으로 한 달 동안 S&P 500이 얼마나 출렁일지 옵션 시장이 매긴 값입니다. 숫자가 클수록 불안하다는 뜻이고, 보통 15 아래는 차분, 20 위는 긴장, 30 위는 공포로 봅니다.</p>'+
  '<ul><li><b>① 지금 불안 vs 3개월 뒤 불안</b> '+(r?'지금 '+r.vix.toFixed(1)+' · 3개월 뒤 '+r.vix3m.toFixed(1)+' → 나누면 <b>'+ratio.toFixed(2)+'</b>':'—')+'. '+(ratio!=null?(ratio>=1?'1을 넘었습니다 = 지금이 더 무섭다는 신호입니다.':'1보다 낮으면 평온, 1을 넘으면 공포 신호입니다. 지금은 1까지 '+(1-ratio).toFixed(2)+' 남았습니다.'):'')+'</li>'+
  '<li><b>② 달마다의 불안 가격(오른쪽 그림)</b> 가까운 '+fm(F[0])+' '+f.toFixed(1)+' → 먼 '+fm(F[F.length-1])+' '+l.toFixed(1)+'. '+(up?'먼 달이 더 비쌉니다 = \'당장은 괜찮고 나중이 더 걱정\'인 평온한 모습입니다.':'가까운 달이 더 비쌉니다 = \'지금 당장이 더 무섭다\'는 공포의 모습입니다.')+'</li>'+
  (kP?'<li><b>③ 하루 사이 변화</b> 모든 달이 평균 '+(dd>=0?'+':'')+dd.toFixed(2)+'씩 '+(Math.abs(dd)<0.05?'거의 그대로입니다(두 선이 겹침).':dd>0?'비싸졌습니다 → 불안이 조금 커졌다는 뜻입니다(진한 선이 흐린 선 위).':'싸졌습니다 → 불안이 조금 줄었다는 뜻입니다(진한 선이 흐린 선 아래).')+'</li>':'')+'</ul></details>';
 var sub=card.querySelector('.sub');
 if(sub){sub.innerHTML='그림 두 개: 지금 불안 vs 3개월 뒤 불안 · 달마다 매겨진 불안 가격';
  sub.parentNode.insertBefore(box,sub.nextSibling)}else card.insertBefore(box,card.children[1]);
 caps(r,ratio,f,l,up,F,fm);done.v=1;done.dS=dS;done.dP=dP;done.dd=dd}

function caps(r,ratio,f,l,up,F,fm){var card=document.getElementById('term-card');if(!card)return;
 var gg=card.querySelector('.ot-grid2'),side=!gg||!gg.children[1]||Math.abs(gg.children[0].getBoundingClientRect().top-gg.children[1].getBoundingClientRect().top)<40;
 var LA=side?'◀ 왼쪽 그림':'▲ 위 그림',LB=side?'오른쪽 그림 ▶':'▼ 아래 그림';
 var g=card.querySelector('.ot-grid2');if(g&&!g.querySelector('.ott-cap')){var c=g.children;
  var a=document.createElement('p');a.className='ott-cap';a.innerHTML='<b>'+LA+'</b> 지금 불안 vs 3개월 뒤 불안';c[0]&&c[0].prepend(a);
  var b=document.createElement('p');b.className='ott-cap';b.innerHTML='<b>'+LB+'</b> 달마다 매겨진 불안 가격';c[1]&&c[1].prepend(b)}
 var how=card.querySelector('p.how');if(!how||how.dataset.ott)return;how.dataset.ott=1;
 how.innerHTML='<b class="ott-hh">이렇게 읽습니다</b>'+
  '<span class="ott-row"><b>'+LA+'</b> <i>파란 선</i> = 지금 한 달 불안(VIX), <i>노란 선</i> = 3개월 뒤 예상 불안(VIX3M).<br>'+
  '평소엔 노란 선이 위에 있습니다. <b>파란 선이 노란 선 위로 올라오면</b> 지금 당장이 더 무섭다는 신호입니다.'+(r?'<br><em>지금: 파랑 '+r.vix.toFixed(1)+' / 노랑 '+r.vix3m.toFixed(1)+' → '+(ratio>=1?'파랑이 위 = 공포 쪽':'노랑이 위 = 평온 쪽')+'</em>':'')+'</span>'+
  '<span class="ott-row"><b>'+LB+'</b> 이번 달·다음 달·… 달마다 시장이 매긴 불안 가격(VIX 선물)입니다.<br>'+
  '선이 <b>오른쪽 위로 올라가면 평온</b>(먼 달이 더 비쌈), <b>오른쪽 아래로 내려가면 공포</b>(가까운 달이 더 비쌈). 진한 선 = 최근, 흐린 선 = 하루 전.'+
  '<br><em>지금: '+fm(F[0])+' '+f.toFixed(1)+' → '+fm(F[F.length-1])+' '+l.toFixed(1)+' = '+(up?'오른쪽 위로 = 평온 쪽':'오른쪽 아래로 = 공포 쪽')+'</em></span>'+
  '<span class="ott-row ott-tip">두 그림이 같은 쪽(둘 다 공포)을 가리키면 신호가 강하고, 엇갈리면 아직 한쪽만 놀란 상태입니다.</span>'}
function svgText(svg,x,y,t,cls,anchor){var e=document.createElementNS('http://www.w3.org/2000/svg','text');e.setAttribute('x',x);e.setAttribute('y',y);e.setAttribute('class',cls);e.setAttribute('text-anchor',anchor||'end');e.textContent=t;svg.appendChild(e);return e}
function lastPt(p){var d=p.getAttribute('d')||'';var m=d.match(/[ML]([\d.]+),([\d.]+)(?!.*[ML][\d.]+,[\d.]+)/);return m?[+m[1],+m[2]]:null}
function firstPt(p){var m=(p.getAttribute('d')||'').match(/M([\d.]+),([\d.]+)/);return m?[+m[1],+m[2]]:null}
function labels(){
 var fs=document.querySelector('#fut-chart svg');
 if(fs&&!fs.querySelector('.ott-lb')&&done.v){var ps=[].slice.call(fs.querySelectorAll('path')).filter(function(p){return /dc4/.test(p.getAttribute('stroke')||'')});
  var light=ps.find(function(p){return +(p.getAttribute('stroke-opacity')||p.getAttribute('opacity')||1)<1}),dark=ps.find(function(p){return p!==light});
  if(dark&&light){var a=firstPt(dark),b=firstPt(light);
   // 선 위 이름표는 값 숫자와 겹쳐서 범례 이름 + 위쪽 한 줄 설명으로 대신함
   svgText(fs,318,14,done.dd>=0.05?'진한 선이 위 = 하루 새 불안 가격 ↑':done.dd<=-0.05?'진한 선이 아래 = 하루 새 불안 가격 ↓':'두 선이 거의 겹침 = 하루 새 변화 없음','ott-lb ott-note','end')}}
 var ts=document.querySelector('#term-chart svg');
 if(ts&&!ts.querySelector('.ott-lb')){var pv=[].slice.call(ts.querySelectorAll('path')).filter(function(p){return /dc1/.test(p.getAttribute('stroke')||'')}).sort(function(a,b){return (b.getAttribute('d')||'').length-(a.getAttribute('d')||'').length})[0];
  var p3=[].slice.call(ts.querySelectorAll('path')).filter(function(p){return /dc2/.test(p.getAttribute('stroke')||'')}).sort(function(a,b){return (b.getAttribute('d')||'').length-(a.getAttribute('d')||'').length})[0];
  if(pv){var e=lastPt(pv);if(e)svgText(ts,e[0]-4,e[1]+16,'지금 불안','ott-lb ott-v')}
  if(p3){var e3=lastPt(p3);if(e3)svgText(ts,e3[0]-4,e3[1]-8,'3개월 뒤 예상 불안','ott-lb ott-3')}}
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
