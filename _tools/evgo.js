// 경제지표 알림 누르면 그 발표 줄로 바로 + 그 지표 추세 그래프(사용자 2026-11-04)
// 알림 주소: p-econ.html#ev-<발표 id>(_tools/econ_alert.py). 이번 주·다음 주 카드의 그 줄(없으면 전체 일정표 줄)로 이동해 노랗게 깜빡이고,
// 바로 아래에 최근 2년 추세(d/econ/series.json, 알림 보낼 때 갱신) — 방금 발표 숫자가 아직 추세에 없으면 일정표 '실제'를 끝에 붙임.
(function(){
var KS=['core-cpi','core-pce','cpi','nfp','adp','ur','ahe','jolts','gdp'],SER=null,CAL=null,done='';
function kindOf(id){for(var i=0;i<KS.length;i++)if(id.indexOf(KS[i]+'-')===0)return KS[i];return null}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/6e4),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function fmt(v,u){var a=Math.abs(v),s=a>=100?Math.round(v).toLocaleString('ko-KR'):(+v.toFixed(a>=10?1:2)).toString();return s+(u?(/^%/.test(u)?'%':/^(백만|천|십억)/.test(u)?u:' '+u):'')}
function ml(m,q,lg){var y=m.slice(2,4),n=+m.slice(5,7);return q?y+'년 '+Math.ceil(n/3)+'분기':lg?n+'월':y+'.'+n}
function periodKey(p){var m=/(\d{4})년\s*(\d+)분기/.exec(p||'');if(m)return m[1]+'-'+('0'+(m[2]*3-2)).slice(-2);m=/(\d{4})년\s*(\d+)월/.exec(p||'');return m?m[1]+'-'+('0'+m[2]).slice(-2):''}
function chart(k,row){var S=SER&&SER[k];if(!S||!S.pts||S.pts.length<3)return null;
 var P=S.pts.map(function(p){return[p[0],+p[1]]}),u=row&&row.unit||'',pk=row&&periodKey(row.period),fresh=false;
 if(row&&row.actual!=null&&pk){var ix=-1;P.forEach(function(p,i){if(p[0]===pk)ix=i});if(ix<0&&pk>P[P.length-1][0]){P.push([pk,+row.actual]);fresh=true}else if(ix>=0){P[ix][1]=+row.actual;P=P.slice(0,ix+1)}}
 var W=340,H=150,L=8,R=52,T=16,B=22,vs=P.map(function(p){return p[1]}),lo=Math.min.apply(0,vs),hi=Math.max.apply(0,vs);if(lo>0&&k!=='nfp'&&k!=='adp'&&k!=='gdp')lo=lo-(hi-lo)*.15;var pad=(hi-lo)*.12||1;lo-=pad;hi+=pad;
 var zero=lo<0&&hi>0;function x(i){return L+(W-L-R)*i/(P.length-1)}function y(v){return T+(H-T-B)*(1-(v-lo)/(hi-lo))}
 var bars=(k==='nfp'||k==='adp'||k==='gdp'),ns='http://www.w3.org/2000/svg',sv=document.createElementNS(ns,'svg');sv.setAttribute('viewBox','0 0 '+W+' '+H);sv.setAttribute('class','evg-svg');
 function add(t,a,tx){var e=document.createElementNS(ns,t);for(var q in a)e.setAttribute(q,a[q]);if(tx!=null)e.textContent=tx;sv.appendChild(e);return e}
 [hi-pad,(hi+lo)/2,lo+pad].forEach(function(v){add('line',{x1:L,x2:W-R,y1:y(v),y2:y(v),'class':'evg-gl'});add('text',{x:W-R+6,y:y(v)+4,'class':'evg-ax'},fmt(v,''))});
 if(zero)add('line',{x1:L,x2:W-R,y1:y(0),y2:y(0),'class':'evg-zero'});
 if(bars){var bw=Math.max(3,(W-L-R)/P.length*.62),b0=y(zero?0:lo);P.forEach(function(p,i){var yy=y(p[1]);add('rect',{x:x(i)-bw/2,y:Math.min(yy,b0),width:bw,height:Math.max(1,Math.abs(b0-yy)),rx:1.5,'class':'evg-bar'+(i===P.length-1?' last':'')+(p[1]<0?' neg':'')})})}
 else{var d='',ar='';P.forEach(function(p,i){d+=(i?'L':'M')+x(i).toFixed(1)+','+y(p[1]).toFixed(1)});ar=d+'L'+x(P.length-1).toFixed(1)+','+(H-B)+'L'+L+','+(H-B)+'Z';
  add('path',{d:ar,'class':'evg-area'});add('path',{d:d,'class':'evg-line'});var pl=P.length-2;add('circle',{cx:x(pl),cy:y(P[pl][1]),r:3,'class':'evg-dot prev'})}
 var n=P.length-1;add('circle',{cx:x(n),cy:y(P[n][1]),r:5,'class':'evg-dot last'});
 [0,Math.floor(n/2),n].forEach(function(i,z){add('text',{x:x(i),y:H-6,'class':'evg-ax','text-anchor':z===0?'start':z===2?'end':'middle'},ml(P[i][0],S.q))});
 var last=P[n][1],prv=P[n-1][1],dd=last-prv,mx=Math.max.apply(0,vs.concat([last])),mn=Math.min.apply(0,vs.concat([last])),yrs=S.q?'최근 3년':'최근 2년';
 var pos=last>=mx?yrs+' 가운데 가장 높습니다.':last<=mn?yrs+' 가운데 가장 낮습니다.':yrs+' 범위('+fmt(mn,u)+'~'+fmt(mx,u)+') 안 '+(last-mn>(mx-mn)*.6?'위쪽':last-mn<(mx-mn)*.4?'아래쪽':'가운데')+'입니다.';
 var box=el('div','evg');box.setAttribute('data-noswipe','');
 var hd=el('div','evg-hd');hd.appendChild(el('b',null,S.name+' · '+yrs+' 추세'));var cx=el('button','evg-x','닫기');cx.type='button';cx.onclick=function(){box.remove()};hd.appendChild(cx);box.appendChild(hd);
 var tk=el('p','evg-tk');tk.appendChild(el('b',null,ml(P[n][0],S.q,1)+' '+fmt(last,u)));var du=/^%/.test(u)?'%p':u;tk.appendChild(document.createTextNode(' — 직전('+fmt(prv,u)+')보다 '+(dd===0?'변화 없음':fmt(Math.abs(dd),du)+(dd>0?' 늘었습니다':' 줄었습니다'))+'. '+pos));box.appendChild(tk);
 box.appendChild(sv);box.appendChild(el('p','evg-src','출처: 미국 노동통계국·FRED'+(fresh?' · 마지막 점은 방금 발표치':'')+' · 노란 점이 이번 발표'));return box}
function find(id){var w=document.querySelector('#weeks .mc-ev[data-key="'+id+'"]');if(w)return{row:w,at:w.closest('.mc-wk')||w,box:w.closest('.u-box')};var t=document.querySelector('#calbody tr[data-key="'+id+'"]');if(t)return{row:t,at:document.getElementById('calf')};return null}
function run(){var m=/^#ev-([\w.-]+)$/.exec(location.hash||'');if(!m)return;var id=m[1];if(done===id)return;var tries=0;
 (function wait(){var f=find(id);if(!f){if(++tries<40)setTimeout(wait,300);return}done=id;
  Promise.all([SER?SER:j('d/econ/series.json'),CAL?CAL:j('d/econ/calendar.json'),j('d/econ/alert_extra.json')]).then(function(r){SER=r[0]||{};CAL=r[1]||[];var ex=r[2]||[];
   var row=null;CAL.concat(ex).forEach(function(x){if(x.id===id)row=x});var old=document.querySelector('.evg');if(old)old.remove();
   var k=kindOf(id),box=k?chart(k,row):null,t0=0,tg=null;
   // 알림으로 처음 열면 첫 화면(멍뭉 터미널 시작 그림)이 2초쯤 덮음 → 그게 걷힌 뒤부터 깜빡임
   function cover(){var e=document.getElementById('mm-splash');if(!e||!e.isConnected)return false;var c=getComputedStyle(e);return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>.05}
   // 이번 주 카드·일정표는 자료가 다시 오면 통째로 다시 그려짐 → 그 뒤에도 같은 줄을 다시 찾아 그래프·깜빡임을 붙임(처음 8초)
   function place(){var f=find(id);if(!f)return;if(box&&!box.isConnected)f.at.parentNode.insertBefore(box,f.at);   // 이번 주 카드는 높이 고정 상자라 그래프는 카드 바로 위에(상자 안에 넣으면 잘림)
    if(f.box){var d=f.row.getBoundingClientRect().top-f.box.getBoundingClientRect().top-56;if(Math.abs(d)>20)f.box.scrollTop+=d}
    if(!t0&&!cover())t0=Date.now();
    if(t0&&Date.now()-t0<2600&&!f.row.classList.contains('evg-flash')){var r0=f.row;r0.classList.add('evg-flash');setTimeout(function(){r0.classList.remove('evg-flash')},2600-(Date.now()-t0))}
    tg=box||f.row}
   function to(sm){place();if(!tg||!tg.isConnected)return;var y=tg.getBoundingClientRect().top+scrollY-84;if(Math.abs(y-scrollY)>30)scrollTo({top:y,behavior:sm?'smooth':'auto'})}
   var MO=window.MutationObserver;try{if(MO.__thr)MO=Object.getPrototypeOf(MO)}catch(e){}
   try{var mo=new MO(function(){if(box&&!box.isConnected||tg&&!tg.isConnected)to()});['weeks','calbody'].forEach(function(i){var e=document.getElementById(i);if(e)mo.observe(e,{childList:true,subtree:true})});setTimeout(function(){mo.disconnect()},8000)}catch(e){}
   to(1);setTimeout(to,450);setTimeout(to,1100);setTimeout(to,2200);
   var n=0;(function sp(){if(cover()&&++n<30)return setTimeout(sp,250);if(n)to(1)})()})})()}
addEventListener('hashchange',function(){done='';run()});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();
