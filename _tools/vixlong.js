// 옵션 온도계 VIX 차트 기간 고르기(사용자 2026-11-09) — 3개월(원래 차트)·1년·5년·10년, 역사적 사건 표시 + '지금은 어디쯤' 한 줄
// 자료 d/opt/vix_long.json(CBOE 공식 종가, build_opt.py가 매일 붙임). 3개월은 페이지 원래 차트 그대로
(function(){
if(!/p-opt\.html/.test(location.pathname))return;
var EV=[['2018-02-05','변동성 상품 폭발'],['2018-12-24','연준 긴축 공포'],['2020-03-16','코로나 폭락'],['2022-03-07','러-우 전쟁·긴축'],['2023-03-13','SVB 은행 사태'],['2024-08-05','엔 캐리 청산'],['2025-04-08','관세 충격']];
var P=[['3m','3개월',0],['1y','1년',365],['5y','5년',1826],['10y','10년',3653]],L=null,cur='3m',NS='http://www.w3.org/2000/svg';
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function sv(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);return e}
function md(d){var a=d.split('-');return a[0].slice(2)+'.'+a[1]}
function ymd(d){var a=d.split('-');return a[0]+'.'+(+a[1])+'.'+(+a[2])}
function series(days){var n=L.d.length,end=L.d[n-1],c=new Date(end);c.setDate(c.getDate()-days);var cut=c.toISOString().slice(0,10),i=0;while(i<n&&L.d[i]<cut)i++;
 var D=L.d.slice(i),C=L.c.slice(i);if(days<=400)return{d:D,c:C};
 var od=[],oc=[],w=days>2000?5:3;for(var j=0;j<D.length;j+=w){var m=j;for(var k=j;k<Math.min(j+w,D.length);k++)if(C[k]>C[m])m=k;od.push(D[m]);oc.push(C[m])}
 if(od[od.length-1]!==D[D.length-1]){od.push(D[D.length-1]);oc.push(C[C.length-1])}return{d:od,c:oc}}
function peak(dt){var b=-1,bi=-1;for(var i=0;i<L.d.length;i++){var x=L.d[i];if(x>=shift(dt,-6)&&x<=shift(dt,6)&&L.c[i]>b){b=L.c[i];bi=i}}return bi<0?null:{d:L.d[bi],c:b}}
function shift(d,k){var t=new Date(d);t.setDate(t.getDate()+k);return t.toISOString().slice(0,10)}
function draw(box,key){var p=P.filter(function(x){return x[0]===key})[0],S=series(p[2]);box.textContent='';
 var W=Math.max(320,box.clientWidth||340),H=250,m={l:34,r:10,t:14,b:22},mx=Math.max(35,Math.ceil(Math.max.apply(null,S.c)/10)*10);
 var X=function(i){return m.l+(W-m.l-m.r)*i/(S.d.length-1)},Y=function(v){return H-m.b-(H-m.t-m.b)*(v-8)/(mx-8)};
 var g=sv('svg',{viewBox:'0 0 '+W+' '+H,width:'100%',class:'mm-vl-svg'});
 [10,20,30,40,50,60,70,80,90].filter(function(v){return v<=mx}).forEach(function(v){if(mx>45&&v%20&&v!==30)return;var y=Y(v);g.appendChild(sv('line',{x1:m.l,x2:W-m.r,y1:y,y2:y,stroke:v===20?'#b8862b':v===30?'#c0392b':'#ece6d8','stroke-dasharray':v===20||v===30?'4 4':'', 'stroke-width':1}));var t=sv('text',{x:m.l-5,y:y+4,'text-anchor':'end',class:'ax'});t.textContent=v;g.appendChild(t)});
 var dd='';S.c.forEach(function(v,i){dd+=(i?'L':'M')+X(i).toFixed(1)+' '+Y(v).toFixed(1)});g.appendChild(sv('path',{d:dd,fill:'none',stroke:'#2f4fae','stroke-width':key==='1y'?1.6:1.2}));
 var nl=key==='1y'?4:5;for(var q=0;q<nl;q++){var i=Math.round((S.d.length-1)*q/(nl-1)),t=sv('text',{x:X(i),y:H-5,'text-anchor':q===0?'start':q===nl-1?'end':'middle',class:'ax'});t.textContent=key==='1y'?S.d[i].slice(5).replace('-','.'):md(S.d[i]);g.appendChild(t)}
 var evs=[];EV.forEach(function(e,n){if(e[0]<S.d[0])return;var pk=peak(e[0]);if(!pk)return;var i=0;while(i<S.d.length-1&&S.d[i]<pk.d)i++;evs.push({n:evs.length+1,nm:e[1],d:pk.d,c:pk.c,x:X(i),y:Y(Math.min(pk.c,mx))})});
 evs.forEach(function(e){g.appendChild(sv('circle',{cx:e.x,cy:e.y,r:8,fill:'#c8501c'}));var t=sv('text',{x:e.x,y:e.y+3.5,'text-anchor':'middle',class:'ev'});t.textContent=e.n;g.appendChild(t)});
 var li=S.d.length-1;g.appendChild(sv('circle',{cx:X(li),cy:Y(S.c[li]),r:5,fill:'#e8a317',stroke:'#fff','stroke-width':2}));
 var tip=el('div','mm-vl-tip','점이나 선을 누르면 그날 값이 보입니다.'),cross=sv('line',{y1:m.t,y2:H-m.b,stroke:'#999','stroke-width':1,visibility:'hidden'});g.appendChild(cross);
 function mv(ev){var r=g.getBoundingClientRect(),cx=((ev.touches?ev.touches[0].clientX:ev.clientX)-r.left)*W/r.width,i=Math.round((cx-m.l)/(W-m.l-m.r)*(S.d.length-1));i=Math.max(0,Math.min(S.d.length-1,i));cross.setAttribute('x1',X(i));cross.setAttribute('x2',X(i));cross.setAttribute('visibility','visible');tip.textContent=ymd(S.d[i])+(key==='1y'?' 마감':' 무렵') +' · VIX '+S.c[i].toFixed(2)}
 g.addEventListener('mousemove',mv);g.addEventListener('touchmove',mv,{passive:true});g.addEventListener('touchstart',mv,{passive:true});
 box.appendChild(tip);box.appendChild(g);
 // 지금은 어디쯤
 var now=L.c[L.c.length-1],nd=L.d[L.d.length-1],win=series(p[2]===0?91:p[2]),hi=0;var raw=L.c.slice(L.d.indexOf(win.d[0])<0?0:L.d.indexOf(win.d[0]));raw.forEach(function(v){if(v>now)hi++});
 var pct=Math.round(hi/raw.length*100),nw=el('p','mm-vl-now');nw.innerHTML='<b>지금 '+now.toFixed(2)+'</b> <small>('+ymd(nd)+' 마감)</small> — 지난 '+p[1]+' 가운데 지금보다 높았던 날은 <b>'+(pct<1?'1% 미만':pct+'%')+'</b>입니다.';box.appendChild(nw);
 if(evs.length){var ul=el('ol','mm-vl-ev');var hd=el('li','hd');hd.appendChild(el('span','','시장이 크게 흔들렸던 날 · 그때 VIX'));hd.appendChild(el('em','','지금 값은'));ul.appendChild(hd);evs.forEach(function(e){var li=el('li');var b=el('b','',e.n);li.appendChild(b);li.appendChild(document.createTextNode(e.nm+' '));var s=el('span','',ymd(e.d)+' · '+e.c.toFixed(2));li.appendChild(s);var r=el('em','',now>=e.c?'지금이 더 높음':'그때의 '+Math.round(now/e.c*100)+'%');li.appendChild(r);ul.appendChild(li)});box.appendChild(ul)}
}
function set(key){cur=key;var card=document.getElementById('vix-card'),orig=document.getElementById('vix-chart'),box=document.getElementById('mm-vl');if(!card||!orig)return;
 [].forEach.call(card.querySelectorAll('.mm-vseg button'),function(b){b.setAttribute('aria-pressed',b.dataset.k===key)});
 var h=card.querySelector('h3'),sub=card.querySelector('.sub');var p=P.filter(function(x){return x[0]===key})[0];if(h)h.textContent='VIX '+(key==='3m'?'최근 3개월':'지난 '+p[1]);
 if(key==='3m'){orig.style.display='';box.style.display='none';if(sub)sub.dataset.mmv&&(sub.textContent=sub.dataset.mmv);return}
 if(!L)return;orig.style.display='none';box.style.display='';if(sub){if(!sub.dataset.mmv)sub.dataset.mmv=sub.textContent;sub.textContent='점선 = 20(경계)·30(공포) 기준선. 주황 번호 = 시장이 크게 흔들렸던 날(그 무렵 가장 높았던 마감 값), 노란 점 = 지금.'+(key==='1y'?'':' 긴 기간은 몇 날씩 묶어 그중 가장 높은 값으로 그립니다.')}
 draw(box,key)}
function init(){var card=document.getElementById('vix-card'),orig=document.getElementById('vix-chart');if(!card||!orig||card.querySelector('.mm-vseg'))return!!card;
 var seg=el('div','mm-vseg');P.forEach(function(p){var b=el('button','',p[1]);b.dataset.k=p[0];b.setAttribute('aria-pressed',p[0]==='3m');b.onclick=function(){set(p[0])};seg.appendChild(b)});
 orig.before(seg);var box=el('div','mm-vl');box.id='mm-vl';box.style.display='none';orig.after(box);return true}
fetch('d/opt/vix_long.json?t='+Math.floor(Date.now()/36e5)).then(function(r){return r.ok?r.json():null}).then(function(j){if(j&&j.d&&j.d.length)L=j;if(cur!=='3m')set(cur)}).catch(function(){});
var k=0;(function go(){var ok=false;try{ok=init()}catch(e){}if(!ok&&++k<40)setTimeout(go,300)})();
var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if(cur!=='3m')set(cur)},250)});
})();
