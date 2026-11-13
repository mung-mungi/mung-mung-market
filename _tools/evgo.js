// 경제지표 발표 줄 누르면 그 자리에서 펼침(사용자 2026-11-04)
// - 발표된 지표: 실제 vs 예상(상회·하회·부합) · 이전 · 그날 지수 + 최근 2년 추세 그래프
// - 기다리는 지표: 예상치·이전 + 이렇게 읽습니다 한 줄 + 지금까지 추세
// - 알림(p-econ.html#ev-<발표 id>, _tools/econ_alert.py)으로 들어오면 그 줄로 이동해 깜빡이고 바로 펼침
// 추세: d/econ/series.json(econ_alert.py가 FRED·노동통계국에서 채움). 이번 주 카드·일정표는 자료가 다시 오면 통째로 다시 그려지므로 펼친 칸은 다시 붙임
(function(){
var KS=['core-cpi','core-pce','claims','umich','retail','ism-m','ism-s','jolts','cpi','nfp','adp','ahe','gdp','pce','ppi','ur'],SER=null,CAL=null,OPEN='',busy=null;
var HOW={cpi:'예상보다 높으면 금리 인하 기대가 줄어 주식에 부담입니다.','core-cpi':'에너지·식품을 뺀 물가 — 연준이 더 눈여겨봅니다. 높으면 금리 부담입니다.',
 ppi:'기업이 받는 가격 — 높으면 몇 달 뒤 소비자물가로 번질 수 있습니다.',nfp:'너무 약하면 경기 걱정, 너무 강하면 금리 부담 — 예상과 비슷한 게 가장 편합니다.',
 ur:'오르면 노동시장이 식는다는 신호입니다.',ahe:'임금이 빨리 오르면 물가 압력이 됩니다.',adp:'금요일 정부 고용 발표의 예고편입니다.',
 jolts:'기업이 뽑으려는 자리 수 — 줄면 노동시장이 식는다는 뜻입니다.',claims:'갑자기 늘기 시작하면 해고가 시작됐다는 신호입니다.',
 'ism-m':'50 위면 확장, 아래면 위축입니다. 함께 나오는 가격 지수도 봅니다.','ism-s':'50 위면 확장, 아래면 위축입니다. 경제의 큰 몫인 서비스업 체온입니다.',
 umich:'소비 심리 — 낮을수록 지갑이 닫힙니다. 함께 나오는 기대 물가도 봅니다.',gdp:'경제 성장 속도(연율)입니다.','core-pce':'연준이 목표로 삼는 물가입니다.',pce:'연준이 보는 물가(전체)입니다.',retail:'소비가 얼마나 버티는지 봅니다.'};
// 판정(사용자 2026-11-04): 숫자가 '경제 강함/약함 · 물가 뜨거움/식음'인지, 지금 상황(연준 금리 흐름)에서 금리를 어느 쪽으로 미는지, 주식엔 어떤지
var SENSE={cpi:'inf','core-cpi':'inf',ppi:'inf','core-pce':'inf',pce:'inf',ahe:'inf',nfp:'grow',adp:'grow',jolts:'grow','ism-m':'grow','ism-s':'grow',retail:'grow',gdp:'grow',umich:'grow',ur:'slack',claims:'slack'},REG=null;
// 전년비가 안 나오는 달(2026년 10월 CPI — 2025년 10월 셧다운)은 전월비 줄로: 일정 줄의 kind가 우선(2026-11-10)
KS.unshift('core-cpi-mom','cpi-mom');HOW['cpi-mom']='전월비 물가 — 예상보다 높으면 금리 인하 기대가 줄어 주식에 부담입니다.';HOW['core-cpi-mom']='에너지·식품을 뺀 전월비 물가 — 연준이 더 눈여겨봅니다.';SENSE['cpi-mom']=SENSE['core-cpi-mom']='inf';
var kindOf0=kindOf;kindOf=function(id){var R=rowOf(id);return R&&R.kind?R.kind:kindOf0(id)};
KS.unshift('core-ppi');HOW['core-ppi']='식품·에너지를 뺀 생산자물가 전월비 — 몇 달 뒤 소비자물가로 넘어오는 기초 압력입니다.';SENSE['core-ppi']='inf';
function regime(T){if(!T||!T.length)return null;var ff=T.filter(function(r){return r.ff_upper!=null}),cp=T.filter(function(r){return r.cpi_yoy!=null});if(!ff.length)return null;
 var last=ff[ff.length-1],ch=null;for(var i=ff.length-1;i>0;i--)if(ff[i].ff_upper!==ff[i-1].ff_upper){ch={dir:ff[i].ff_upper>ff[i-1].ff_upper?1:-1,m:+ff[i].month.slice(5,7)};break}
 return {dir:ch?ch.dir:0,m:ch?ch.m:0,lo:last.ff_lower,hi:last.ff_upper,cpi:cp.length?cp[cp.length-1].cpi_yoy:null}}
function tolOf(u,c){return /^%/.test(u)?0.05:u==='지수'?0.3:Math.max(Math.abs(c||0)*0.03,1e-6)}
function heat(k,d){var S=SENSE[k];if(!S||!d)return {t:'예상 수준',c:'eq',rate:0};
 if(S==='grow')return d>0?{t:'경제 강함',c:'hot',rate:1}:{t:'경제 약함',c:'cold',rate:-1};
 if(S==='inf')return d>0?{t:'물가 뜨거움',c:'hot',rate:1}:{t:'물가 식음',c:'cold',rate:-1};
 return d>0?{t:'고용 약해짐',c:'cold',rate:-1}:{t:'고용 탄탄',c:'hot',rate:1}}
function rateChip(v){return v>0?['금리 ↑ 쪽','up']:v<0?['금리 ↓ 쪽','dn']:['금리 영향 작음','eq']}
function regLine(){var R=REG;if(!R)return '';return R.dir>0?'연준이 '+R.m+'월에 금리를 올렸고(상단 '+R.hi.toFixed(2)+'%)'+(R.cpi!=null?' 물가가 '+R.cpi+'%라':'')+' 추가 인상을 저울질하는 중입니다.':R.dir<0?'연준이 '+R.m+'월에 금리를 내렸고(상단 '+R.hi.toFixed(2)+'%) 인하를 더 이어 갈지 보는 중입니다.':'연준은 금리를 '+R.lo.toFixed(2)+'~'+R.hi.toFixed(2)+'%에 묶어 두고 있습니다.'}
function effect(k,h){var S=SENSE[k],R=REG,up=R&&R.dir>0;if(!h.rate)return ['금리 전망을 크게 바꾸지 않습니다.','큰 영향 없음 — 다른 지표와 함께 봅니다.'];
 if(h.rate>0)return [up?'추가 인상 쪽에 힘이 실립니다.':R&&R.dir<0?'인하를 늦출 이유가 됩니다.':'인하 기대가 줄어듭니다.',S==='grow'?'기술·성장주엔 금리 부담, 다만 경기 걱정은 줄어듭니다.':'금리 부담이 커져 기술·성장주에 불리합니다.'];
 return [up?'추가 인상 압력이 줄어듭니다.':'인하 기대가 커집니다.',S==='inf'?'금리 부담이 덜어져 우호적입니다.':'금리 부담은 덜지만 경기 걱정이 커져 엇갈립니다.']}
function eff(w,k,h,lead){var e=effect(k,h);if(lead)w.appendChild(el('p','evj-h',lead));[['금리 ',e[0]],['주식 ',e[1]]].forEach(function(x){var p=el('p','evj-t');p.appendChild(el('b',null,x[0]));p.appendChild(document.createTextNode(x[1]));w.appendChild(p)})}
function judge(box,k,r){if(!SENSE[k]||r.unit==null)return;var u=r.unit,done=r.actual!=null,w=el('div','evj'),rl=regLine();
 if(done){var base=r.consensus!=null?r.consensus:r.previous;if(base==null)return;var d=+r.actual-base,tol=tolOf(u,base),h=heat(k,Math.abs(d)<tol?0:d),rc=rateChip(h.rate);
  var cs=el('div','evj-chips');cs.appendChild(el('span','evj-c '+h.c,h.t));cs.appendChild(el('span','evj-c r'+rc[1],rc[0]));w.appendChild(cs);
  if(rl)w.appendChild(el('p','evj-ctx','지금 상황: '+rl));eff(w,k,h,r.consensus==null?'예상치가 없어 이전과 비교했습니다':'')}
 else{var hi=heat(k,1),lo=heat(k,-1),a=rateChip(hi.rate),b=rateChip(lo.rate);
  w.appendChild(el('p','evj-h','이렇게 나오면'));
  [['예상보다 높게',hi,a],['예상보다 낮게',lo,b]].forEach(function(x){var q=el('div','evj-sc');q.appendChild(el('span','evj-k',x[0]));q.appendChild(el('span','evj-c '+x[1].c,x[1].t));q.appendChild(el('span','evj-c r'+x[2][1],x[2][0]));w.appendChild(q)});
  if(rl)w.appendChild(el('p','evj-ctx','지금 상황: '+rl));var hh=SENSE[k]==='slack'?lo:hi;eff(w,k,hh,(SENSE[k]==='slack'?'낮게':'높게')+' 나오면')}
 box.appendChild(w)}
function kindOf(id){for(var i=0;i<KS.length;i++)if(id.indexOf(KS[i]+'-')===0)return KS[i];return null}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/6e4),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function load(){if(!busy)busy=Promise.all([j('d/econ/series.json'),j('d/econ/calendar.json'),j('d/econ/alert_extra.json'),j('d/econ/trends.json'),css()]).then(function(r){SER=r[0]||{};CAL=(r[1]||[]).concat(r[2]||[]);try{REG=regime(r[3])}catch(e){}CSS=(r[4]||'').replace(/html body /g,'')});return busy}
function rowOf(id){for(var i=0;i<(CAL||[]).length;i++)if(CAL[i].id===id)return CAL[i];return null}
function fmt(v,u){if(v==null||isNaN(v))return '자료 없음';var a=Math.abs(v),s=a>=100?Math.round(v).toLocaleString('ko-KR'):(+(+v).toFixed(a>=10?1:2)).toString();
 if(!u||u==='지수')return s;if(u==='포인트')return (+(+v).toFixed(1))+'포인트';if(/^%/.test(u))return s+'%';if(u==='%p')return s+'%p';if(/^(백만|천|십억)/.test(u))return s+u.replace(' ','');return s+' '+u}
function ml(m,q,lg){if(m.length>7)return (+m.slice(5,7))+'.'+(+m.slice(8,10));var y=m.slice(2,4),n=+m.slice(5,7);return q?y+'년 '+Math.ceil(n/3)+'분기':lg?n+'월':y+'.'+n}
function periodKey(p){var m=/(\d{4})년\s*(\d+)분기/.exec(p||'');if(m)return m[1]+'-'+('0'+(m[2]*3-2)).slice(-2);m=/(\d{4})년\s*(\d+)월/.exec(p||'');return m?m[1]+'-'+('0'+m[2]).slice(-2):''}
// 추세 그래프(SVG) — 발표 숫자가 아직 추세에 없으면 일정표 '실제'를 끝에 붙임
function chart(k,row){var S=SER&&SER[k];if(!S||!S.pts||S.pts.length<3)return null;
 var P=S.pts.map(function(p){return[p[0],+p[1]]}),u=row&&row.unit||'',pk=row&&periodKey(row.period),fresh=false,wk=P[0][0].length>7;
 if(!wk&&row&&row.actual!=null&&pk){var ix=-1;P.forEach(function(p,i){if(p[0]===pk)ix=i});if(ix<0&&pk>P[P.length-1][0]){P.push([pk,+row.actual]);fresh=true}else if(ix>=0){P[ix][1]=+row.actual;P=P.slice(0,ix+1)}}
 if(!wk&&row&&row.actual==null&&pk){P=P.filter(function(p){return p[0]<pk})}
 if(P.length<3)return null;
 var W=340,H=140,L=8,R=46,T=12,B=22,vs=P.map(function(p){return p[1]}),bars=(k==='nfp'||k==='adp'||k==='gdp'||k==='ppi'||k==='retail');
 var lo=Math.min.apply(0,vs),hi=Math.max.apply(0,vs);if(bars){lo=Math.min(lo,0);hi=Math.max(hi,0)}var pad=(hi-lo)*.12||1;lo-=pad;hi+=pad;
 var zero=lo<0&&hi>0;function x(i){return L+(W-L-R)*i/(P.length-1)}function y(v){return T+(H-T-B)*(1-(v-lo)/(hi-lo))}
 var ns='http://www.w3.org/2000/svg',sv=document.createElementNS(ns,'svg');sv.setAttribute('viewBox','0 0 '+W+' '+H);sv.setAttribute('class','evg-svg');
 function add(t,a,tx){var e=document.createElementNS(ns,t);for(var q in a)e.setAttribute(q,a[q]);if(tx!=null)e.textContent=tx;sv.appendChild(e);return e}
 [hi-pad,(hi+lo)/2,lo+pad].forEach(function(v){add('line',{x1:L,x2:W-R,y1:y(v),y2:y(v),'class':'evg-gl'});add('text',{x:W-R+6,y:y(v)+4,'class':'evg-ax'},fmt(v,''))});
 if(zero)add('line',{x1:L,x2:W-R,y1:y(0),y2:y(0),'class':'evg-zero'});
 if(k==='ism-m'||k==='ism-s'){if(lo<50&&hi>50)add('line',{x1:L,x2:W-R,y1:y(50),y2:y(50),'class':'evg-zero'})}
 var n=P.length-1;
 if(bars){var bw=Math.max(3,(W-L-R)/P.length*.62),b0=y(zero?0:lo);P.forEach(function(p,i){var yy=y(p[1]);add('rect',{x:x(i)-bw/2,y:Math.min(yy,b0),width:bw,height:Math.max(1,Math.abs(b0-yy)),rx:1.5,'class':'evg-bar'+(i===n?' last':'')+(p[1]<0?' neg':'')})})}
 else{var d='';P.forEach(function(p,i){d+=(i?'L':'M')+x(i).toFixed(1)+','+y(p[1]).toFixed(1)});
  add('path',{d:d+'L'+x(n).toFixed(1)+','+(H-B)+'L'+L+','+(H-B)+'Z','class':'evg-area'});add('path',{d:d,'class':'evg-line'});add('circle',{cx:x(n-1),cy:y(P[n-1][1]),r:3,'class':'evg-dot prev'})}
 add('circle',{cx:x(n),cy:y(P[n][1]),r:5,'class':'evg-dot last'+(row&&row.actual==null?' old':'')});
 [0,Math.floor(n/2),n].forEach(function(i,z){add('text',{x:x(i),y:H-6,'class':'evg-ax','text-anchor':z===0?'start':z===2?'end':'middle'},ml(P[i][0],S.q))});
 var last=P[n][1],mx=Math.max.apply(0,vs.concat([last])),mn=Math.min.apply(0,vs.concat([last])),yrs=wk?'최근 반년':S.q?'최근 3년':'최근 2년';
 var pos=last>=mx?yrs+' 가운데 가장 높습니다.':last<=mn?yrs+' 가운데 가장 낮습니다.':yrs+' 범위('+fmt(mn,u)+'~'+fmt(mx,u)+') 안 '+(last-mn>(mx-mn)*.6?'위쪽':last-mn<(mx-mn)*.4?'아래쪽':'가운데')+'입니다.';
 return {svg:sv,pos:pos,yrs:yrs,fresh:fresh,last:P[n],prev:P[n-1],u:u,q:S.q}}
function line(b,t){var p=el('p','evg-ln');if(b){p.appendChild(el('b',null,b))}if(t)p.appendChild(document.createTextNode(t));return p}
function panel(id){var r=rowOf(id),k=kindOf(id);if(!r)return null;var u=r.unit||'',du=/^%/.test(u)?'%p':u==='지수'?'포인트':u,box=el('div','evg');box.setAttribute('data-noswipe','');box.dataset.for=id;
 var C=k?chart(k,r):null,done=r.actual!=null;
 var hd=el('div','evg-hd');hd.appendChild(el('b',null,(done?'결과 · ':'예상치 · ')+r.event));var cx=el('button','evg-x','접기 ▴');cx.type='button';cx.onclick=function(e){e.stopPropagation();close()};hd.appendChild(cx);box.appendChild(hd);
 if(!u){box.appendChild(line(null,r.note||'숫자로 나오는 발표가 아닙니다.'));return box}
 if(done){var a=+r.actual,c=r.consensus,pv=r.previous,g=el('div','evg-big');g.appendChild(el('span','evg-v',fmt(a,u)));
  if(c!=null){var dd=a-c,tag=Math.abs(dd)<1e-9?['예상 부합','eq']:dd>0?['예상 상회','up']:['예상 하회','dn'];g.appendChild(el('span','evg-tag '+tag[1],tag[0]))}
  box.appendChild(g);
  box.appendChild(line(null,'예상 '+(c!=null?fmt(c,u):'자료 없음')+' · 이전 '+(pv!=null?fmt(pv,u):'자료 없음')+(pv!=null?' → 이전보다 '+(a===pv?'변화 없음':fmt(Math.abs(a-pv),du)+(a>pv?' 높음':' 낮음')):'')));
  if(c!=null&&a!==c){var dc=a-c,pc=(!/%/.test(u||'')&&c)?' ('+(dc>0?'+':'−')+Math.abs(Math.round(dc/Math.abs(c)*1000)/10)+'%)':'';box.appendChild(line('예상 대비 ',fmt(Math.abs(dc),du)+(dc>0?' 많음':' 적음')+pc+(dc>0?' — 예상보다 높게 나왔습니다':' — 예상보다 낮게 나왔습니다')))}  // 컨센 대비 몇이나·몇 %(사용자 2026-11-04)
  if(r.note)box.appendChild(line('짚을 점 ',r.note));
  if(r.spx_chg_pct!=null)box.appendChild(line('그날 지수 ','S&P 500 '+(r.spx_chg_pct>0?'+':'')+r.spx_chg_pct+'% · 나스닥 '+(r.ndx_chg_pct>0?'+':'')+r.ndx_chg_pct+'%'));
}
 else{var c2=r.consensus,p2=r.previous,g2=el('div','evg-big');g2.appendChild(el('span','evg-v'+(c2==null?' na':' evc'),c2!=null?'예상치 '+fmt(c2,u):'예상치 아직'));box.appendChild(g2);
  box.appendChild(line(null,c2!=null?'이전 '+(p2!=null?fmt(p2,u):'자료 없음')+(p2!=null?' → 예상대로면 '+(c2===p2?'그대로':fmt(Math.abs(c2-p2),du)+(c2>p2?' 높아짐':' 낮아짐')):''):'시장 예상치는 보통 발표 주 초에 나옵니다 · 이전 '+(p2!=null?fmt(p2,u):'자료 없음')));
}
 judge(box,k,r);
 if(HOW[k])box.appendChild(line('이렇게 읽습니다 ',HOW[k]));
 if(C){box.appendChild(el('p','evg-sub',(done?C.yrs+' 추세 · ':'지금까지 '+C.yrs+' 추세 · ')+C.pos));box.appendChild(C.svg);
  box.appendChild(el('p','evg-src','출처: 미국 노동통계국·FRED'+(C.fresh?' · 마지막 점은 방금 발표치':'')+' · 노란 점이 '+(done?'이번 발표':'가장 최근 발표')))}
 return box}
// 줄 찾기 · 펼치기 · 다시 붙이기
// 빠르게(2026-11-04): 이 페이지엔 '화면이 바뀌면 페이지 전체를 다시 훑는' 공용 감시기가 여럿(줄바꿈·상자·사명 표기 등) 있어,
// 펼칠 때마다 칸을 새로 끼우면 아이폰에서 1~2초 멈춤 → 줄마다 빈 자리(그림자 칸)를 처음 한 번만 붙이고, 누를 땐 그 안만 채우고 보이기만 바꿈(감시기에 안 걸림)
var CSS='';
function css(){var l=document.querySelector('link[data-evgo]');return l?fetch(l.href).then(function(r){return r.ok?r.text():''}).catch(function(){return ''}):Promise.resolve('')}
function find(id){var w=document.querySelector('#weeks .mc-ev[data-key="'+id+'"]');if(w)return{row:w,box:w.closest('.u-box')};var t=document.querySelector('#calbody tr[data-key="'+id+'"]');return t?{row:t,box:t.closest('.u-box,.mc-tbox')}:null}
function hostOf(row,make){var h=row.nextElementSibling;if(h&&h.classList.contains('evg-host')&&h.dataset.for===row.dataset.key)return h;if(!make)return null;
 if(row.tagName==='TR'){h=el('tr','evg-host evg-tr');var td=el('td');td.colSpan=row.children.length||9;h.appendChild(td);h.__slot=td}else{h=el('div','evg-host');h.__slot=h}
 h.dataset.for=row.dataset.key;h.hidden=true;try{h.__sr=h.__slot.attachShadow({mode:'open'})}catch(e){h.__sr=null}row.after(h);return h}
function fill(h,id){var p=panel(id);if(!p)return null;var sr=h.__sr;if(sr){var st=document.createElement('style');st.textContent=CSS;sr.replaceChildren(st,p)}else{h.__slot.replaceChildren(p)}h.hidden=false;return h}
function hideAll(){[].forEach.call(document.querySelectorAll('.evg-host:not([hidden])'),function(h){h.hidden=true})}
function close(){OPEN='';hideAll();mark()}
function show(id,how){var f=find(id);if(!f)return;hideAll();OPEN=id;
 var cd=f.row.closest('#weeks .mc-card');if(cd&&!cd.classList.contains('u-box'))cd.dataset.ub=1;   // 펼쳐 길어져도 높이 고정 상자로 안 바뀌게(넓은 화면 두 칸 배치 유지)
 var p=fill(hostOf(f.row,true),id);mark();
 if(f.box&&f.box.scrollHeight>f.box.clientHeight+4){var d=(how==='alert'?f.row:p||f.row).getBoundingClientRect().top-f.box.getBoundingClientRect().top-(how==='alert'?10:70);f.box.scrollTo({top:f.box.scrollTop+d,behavior:'auto'})}
 if(how==='alert'){var t0=0;function to(sm){var g=find(id);if(!g)return;var tg=g.box&&g.box.scrollHeight>g.box.clientHeight+4?g.box:g.row,y=tg.getBoundingClientRect().top+scrollY-84;if(Math.abs(y-scrollY)>30)scrollTo({top:y,behavior:sm?'smooth':'auto'})}
  function flash(){var g=find(id);if(!g)return;if(!t0&&!cover())t0=Date.now();if(t0&&Date.now()-t0<2600&&!g.row.classList.contains('evg-flash')){var r0=g.row;r0.classList.add('evg-flash');setTimeout(function(){r0.classList.remove('evg-flash')},2600-(Date.now()-t0))}}
  to(1);flash();[450,1100,2200].forEach(function(ms){setTimeout(function(){to();flash()},ms)});var n=0;(function sp(){if(cover()&&++n<30)return setTimeout(sp,250);if(n){to(1);flash()}})()}
 else{var b=p&&p.getBoundingClientRect();if(b&&b.bottom>innerHeight-90&&!(f.box&&f.box.scrollHeight>f.box.clientHeight+4))scrollTo({top:scrollY+Math.min(b.bottom-innerHeight+110,b.top-90),behavior:'smooth'})}}
function cover(){var e=document.getElementById('mm-splash');if(!e||!e.isConnected)return false;var c=getComputedStyle(e);return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>.05}
// 줄마다 '결과 보기 ▾ / 예상치 보기 ▾' 알약(글자는 속성으로 바꿈 → 감시기에 안 걸림) + 이번 주 카드 줄마다 빈 자리 미리
function mark(){if(!CAL)return;[].forEach.call(document.querySelectorAll('#weeks .mc-ev[data-key],#calbody tr[data-key]'),function(e){var id=e.dataset.key,r=rowOf(id);if(!r||!r.unit){e.classList.remove('evg-can');return}
  var on=OPEN===id,lab=(r.actual!=null?'결과 ':'예상치 ')+(on?'접기 ▴':'보기 ▾'),host=e.tagName==='TR'?e.querySelector('td:nth-child(3)'):e.querySelector('.ex')||e,pill=e.querySelector('.evg-pill');
  if(!e.classList.contains('evg-can'))e.classList.add('evg-can');if(e.classList.contains('evg-on')!==on)e.classList.toggle('evg-on',on);
  if(!pill){pill=el('span','evg-pill');host.appendChild(pill)}if(pill.dataset.lab!==lab)pill.dataset.lab=lab;if(pill.classList.contains('done')!==(r.actual!=null))pill.classList.toggle('done',r.actual!=null);
  if(e.tagName!=='TR')hostOf(e,true)});
 if(OPEN){var f=find(OPEN),h=f&&hostOf(f.row,false);if(f&&(!h||h.hidden||!h.__sr||!h.__sr.querySelector('.evg')))fill(hostOf(f.row,true),OPEN)}}
// 아이폰: 상자 안을 밀다가 바로 누르면 첫 누름이 '스크롤 멈춤'으로만 쓰이고 click이 안 옴 → 손을 뗄 때(pointerup) 바로 열고, 뒤따르는 click은 무시
var PD=null,LAST=0;
function rowAt(t){if(!t||!t.closest||t.closest('a,.evg-host'))return null;var r=t.closest('#weeks .mc-ev[data-key],#calbody tr[data-key]');return r&&r.classList.contains('evg-can')?r:null}
function toggle(r,up){var id=r.dataset.key;if(up)LAST=Date.now();if(OPEN===id)close();else show(id,'tap')}
document.addEventListener('pointerdown',function(e){var r=rowAt(e.target);PD=r?{r:r,x:e.clientX,y:e.clientY,t:Date.now()}:null;if(r){var p=r.querySelector('.evg-pill');if(p)p.classList.add('prs')}},{passive:true});
document.addEventListener('pointercancel',function(){if(PD){var p=PD.r.querySelector('.evg-pill');if(p)p.classList.remove('prs')}PD=null},{passive:true});
document.addEventListener('pointerup',function(e){var d=PD;PD=null;if(!d)return;var p=d.r.querySelector('.evg-pill');if(p)p.classList.remove('prs');
 if(Math.abs(e.clientX-d.x)>10||Math.abs(e.clientY-d.y)>10||Date.now()-d.t>700||rowAt(e.target)!==d.r)return;toggle(d.r,1)},{passive:true});
document.addEventListener('click',function(e){var r=rowAt(e.target);if(!r)return;if(Date.now()-LAST<600)return;toggle(r)});
document.addEventListener('click',function(e){if(CAL)return;var t=e.target,r=t.closest&&t.closest('#weeks .mc-ev[data-key],#calbody tr[data-key]');if(r&&!t.closest('a,.evg-host'))load().then(function(){show(r.dataset.key,'tap')})});
var q=0;function sched(){if(q)return;q=1;requestAnimationFrame(function(){q=0;try{mark()}catch(e){}})}
var MO=window.MutationObserver;try{if(MO.__thr)MO=Object.getPrototypeOf(MO)}catch(e){}
function watch(){var a=document.getElementById('weeks'),b=document.getElementById('calbody');if(!a||!b){setTimeout(watch,400);return}try{var mo=new MO(function(ms){for(var i=0;i<ms.length;i++){var m=ms[i],n=m.target;if(n.closest&&n.closest('.evg-host'))continue;var ad=[].slice.call(m.addedNodes||[]);if(ad.length&&ad.every(function(x){return x.classList&&(x.classList.contains('evg-host')||x.classList.contains('evg-pill'))}))continue;sched();return}});mo.observe(a,{childList:true,subtree:true});mo.observe(b,{childList:true})}catch(e){}}
// 일정 표에 줄이 없는 알림 지표(ADP 등 alert_extra)도 알림 누르면 맨 위에 그 지표 칸을 만들어 바로 보여 줌(사용자 2026-11-04)
function stub(id){var r=rowOf(id),w=document.getElementById('weeks');if(!r||!w)return false;var c=document.getElementById('evg-stub');if(!c){c=el('div','mc-card evg-stub');c.id='evg-stub';w.insertBefore(c,w.firstChild)}
 c.innerHTML='';var h=el('div','evg-stub-h');h.textContent='⚡ 방금 알림 온 지표';var e=el('div','mc-ev');e.dataset.key=id;var b=el('b');b.textContent=(r.event||id)+(r.period?' · '+r.period:'');var x=el('div','ex');x.textContent=(r.date_kst||'')+' '+(r.time_kst||'')+' 발표';e.appendChild(b);e.appendChild(x);c.appendChild(h);c.appendChild(e);return true}
function hash(){var m=/^#ev-([\w.-]+)$/.exec(location.hash||'');if(!m)return;var id=m[1],tries=0;(function wait(){if(!find(id)||!CAL){if(CAL&&tries>=10&&!find(id)&&stub(id)){mark();show(id,'alert');return}if(++tries<40)setTimeout(wait,300);return}show(id,'alert')})()}
addEventListener('hashchange',hash);
load();function start(){watch();load().then(function(){mark();hash();var w=window.requestIdleCallback||function(f){setTimeout(f,1200)};w(function(){try{var r=document.querySelector('#weeks .mc-ev.evg-can');if(r)panel(r.dataset.key)}catch(e){}})})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
