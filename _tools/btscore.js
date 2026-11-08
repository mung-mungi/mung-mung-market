// 옵션·채권 페이지 '경고등 흐름' 카드를 시장 경고등과 같은 점수 양식으로(사용자 2026-11-02 — "비슷한 차트는 보는 법 통일, 앞단과 같은 양식이라야 넘기면서 보기 좋다")
// 원래 카드(#bt-card: 불 n개 그대로 · 0.4개→0.8개)는 숨기고, 같은 자리에 '점수 x.x / 만점 → 단계' + 단계 막대 + 최근 15거래일 점수 막대 + '지금' 한 줄 + 시장 전체 알약을 그린다.
// 점수 = 지표마다 (켜짐 1 · 근접 0.8 · 보통 0.4 · 양호 0.2 · 안전 0) × 무게. 단계 구간은 시장 경고등(12점: 3·4.5·6·7.5)과 같은 비율.
(function(){try{
var P=/p-opt\.html/.test(location.pathname)?'opt':/p-bond\.html/.test(location.pathname)?'bond':null;if(!P)return;
var CFG={opt:{ids:['vix','term','pc'],nm:'옵션 경고등',sh:{vix:'VIX',term:'기간구조',pc:'풋콜'},calm:'옵션 쪽은 조용합니다.'},
 bond:{ids:['y10','why','y30','auc','hy'],nm:'채권 경고등',sh:{why:'금리 움직임',auc:'국채 입찰',inv:'장단기차',y10:'10년물',jump:'10년물 2주',y30:'30년물',hy:'하이일드'},calm:'금리·신용 쪽은 조용합니다.'}}[P];
var BR=[[0,'평온','#2e9d5b'],[.25,'주의','#c99a06'],[.392,'경계','#e07b16'],[.55,'긴장','#c8501c'],[.7,'위험','#b3261e']];
var L=null,T=null,F=null;
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function md(d){var a=String(d).split('-');return (+a[1])+'.'+(+a[2])}
function f1(v){return (Math.round(v*10)/10).toFixed(1)}
function ratio(t,v){if(v==null)return 0;if(t.op==='<'||t.op==='<=')return t.value===0?1-(v/0.5):t.value/v;return t.value>0?v/t.value:0}
function lv(t,r){if(Number(r.on)===1)return[1,'켜짐'];var q=ratio(t,Number(r.val));return q>=.9?[.8,'근접']:q>=.8?[.4,'보통']:q>=.6?[.2,'양호']:[0,'안전']}
function stg(sc,mx){var r=BR[0];BR.forEach(function(b){if(sc>=b[0]*mx-1e-9)r=b});return r}
function fv(t,v){v=Number(v);var u=t.unit||'';return (Math.round(v*100)/100)+(u==='%p'?'%p':u)}
function calc(){var TH={};T.forEach(function(t){TH[t.id]=t});var by={};
 L.forEach(function(r){if(CFG.ids.indexOf(r.id)<0||!TH[r.id])return;var d=String(r.date).slice(0,10);(by[d]=by[d]||{})[r.id]=r});
 var ds=Object.keys(by).sort(),mx=CFG.ids.reduce(function(a,id){return a+(TH[id]?Number(TH[id].weight||1):0)},0);
 var day=function(d){var s=0,it=[];CFG.ids.forEach(function(id){var r=by[d][id],t=TH[id];if(!r||!t)return;var w=Number(t.weight||1),q=lv(t,r);s+=q[0]*w;it.push({id:id,t:t,r:r,lv:q[1]})});return{d:d,s:Math.round(s*10)/10,it:it}};
 return{mx:mx,days:ds.map(day)}}
function draw(){var card=document.getElementById('bt-card');if(!card||!L||!T)return;
 /* 경고등 3판이면 옛 불 기준 점수 카드는 숨김 — 위 '오늘 한눈에'·'바뀐 점'이 3판 영역 점수(10점 만점)를 보여 줌(사용자 2026-11-09 점검 '잣대 하나로') */
 if(F&&F.ver3&&F.area_scores){card.classList.add('mm-bs-hide');card.style.display='none';var lc0=document.getElementById('lights-card');if(lc0){var t0=lc0.querySelector('.mm-bs-tr');if(t0)t0.remove()}return}
 var C=calc();if(C.days.length<2)return;var now=C.days[C.days.length-1],pv=C.days[C.days.length-2],g=stg(now.s,C.mx);
 if(P==='opt')top(now,C.mx,g);
 if(P==='bond'){bond(C,now,pv);return}
 var key=now.d+':'+now.s;var w=card.querySelector('.mm-bs');if(w&&w.dataset.k===key)return;
 card.classList.add('mm-bs-on');card.style.setProperty('--btc',g[2]);
 if(!w){w=el('div','mm-bs');card.appendChild(w)}w.dataset.k=key;w.textContent='';
 var h=el('div','mm-bs-h');h.appendChild(el('span','k',CFG.nm+' 점수'));h.appendChild(el('span','d',md(now.d)+' 마감'));w.appendChild(h);
 var n=el('div','mm-bs-n');n.appendChild(el('b','',f1(now.s)));n.appendChild(el('span','of','/ '+C.mx+'점'));var st=el('span','st','→ '+g[1]);st.style.color=g[2];n.appendChild(st);w.appendChild(n);
 // 단계 막대(시장 경고등 큰 카드와 같은 모양)
 var bar=el('div','mm-bs-bar');BR.forEach(function(b,i){var s=el('i');s.style.background=b[2];s.style.flex=String(((BR[i+1]?BR[i+1][0]:1)-b[0])*100);bar.appendChild(s)});
 var ring=el('em');ring.style.left=Math.min(100,now.s/C.mx*100)+'%';bar.appendChild(ring);w.appendChild(bar);
 var lb=el('div','mm-bs-lb');BR.forEach(function(b,i){var s=el('span');s.style.flex=String(((BR[i+1]?BR[i+1][0]:1)-b[0])*100);s.appendChild(el('b','',b[1])).style.color=b===g?b[2]:'';s.appendChild(el('small','',(Math.round(b[0]*C.mx*100)/100)+'~'));lb.appendChild(s)});w.appendChild(lb);
 // 최근 15거래일 점수 막대
 var tr=el('div','mm-bs-tr');tr.appendChild(el('span','k','최근 15거래일'));var bx=el('div','bars');var D=C.days.slice(-15);
 D.forEach(function(x,i){var b=el('i');b.style.height=Math.max(10,x.s/C.mx*100)+'%';b.style.background=stg(x.s,C.mx)[2];b.title=md(x.d)+' '+f1(x.s)+'점';if(i===D.length-1)b.className='last';bx.appendChild(b)});tr.appendChild(bx);
 var dd=Math.round((now.s-pv.s)*10)/10;tr.appendChild(el('span','dt',dd>0?'▲ '+f1(dd)+'점':dd<0?'▼ '+f1(-dd)+'점':'전날과 같음'));w.appendChild(tr);
 // '지금' 한 줄
 var on=now.it.filter(function(x){return x.lv==='켜짐'}),nr=now.it.filter(function(x){return x.lv==='근접'});
 var nm=function(x){return CFG.sh[x.id]+' '+fv(x.t,x.r.val)};
 var txt=on.length&&nr.length?'켜짐: '+on.map(nm).join(' · ')+' / 문턱 바로 아래: '+nr.map(nm).join(' · ')+' — 한 번만 밀려도 더 켜집니다.':on.length?'켜짐: '+on.map(nm).join(' · ')+'.':nr.length?nr.map(nm).join(' · ')+' — 문턱 바로 아래입니다. 한 번만 밀려도 켜집니다.':CFG.calm;
 var nw=el('div','mm-bs-now');nw.appendChild(el('b','','지금'));nw.appendChild(el('span','',txt));w.appendChild(nw);
 if(P==='opt'&&F&&F.score!=null){var em={'평온':'🟢','주의':'🟡','경계':'🟠','긴장':'🟠','위험':'🔴'}[F.stage]||'';var a=el('a','mm-bs-all','시장 전체 경고등 '+em+' '+F.stage+' · '+F.score.toFixed(1)+'/'+F.score_max+'점 →');a.href='p-lights.html';w.appendChild(a)}}
// 옵션 페이지 '오늘 한눈에'의 옛 점수(1/4 · 경계)도 같은 점수로 맞춤
function top(now,mx,g){var o=document.querySelector('.o-top');if(!o)return;var s=o.querySelector('.o-st'),c=o.querySelector('.o-sc');
 var em={'평온':'🟢','주의':'🟡','경계':'🟠','긴장':'🟠','위험':'🔴'}[g[1]];var t=em+' '+g[1];if(s&&s.textContent!==t){s.textContent=t;s.style.color=g[2]}
 if(c&&!c.querySelector('.mm-bs-x')){c.innerHTML='점수 <b class="mm-bs-x">'+f1(now.s)+'</b> / '+mx}}
// 채권: 바로 아래 '채권 경고등' 카드(bdnear)에 같은 점수가 이미 있으므로 흐름 카드는 숨기고, 15거래일 점수 막대만 그 카드 단계 칸 아래로 합침(사용자 2026-11-02 '진행')
function bond(C,now,pv){var lc=document.getElementById('lights-card');if(!lc)return;var anc=lc.querySelector('.mm-bd-steps')||lc.querySelector('.mm-bd-sc');if(!anc)return;
 var bc=document.getElementById('bt-card');if(bc)bc.classList.add('mm-bs-hide');
 var key=now.d+':'+now.s,tr=lc.querySelector('.mm-bs-tr');if(tr&&tr.dataset.k===key&&tr.previousElementSibling===anc)return;if(tr)tr.remove();
 tr=el('div','mm-bs-tr mm-bs-in');tr.dataset.k=key;tr.appendChild(el('span','k','최근 15거래일'));var bx=el('div','bars');var D=C.days.slice(-15);
 D.forEach(function(x,i){var b=el('i');b.style.height=Math.max(10,x.s/C.mx*100)+'%';b.style.background=stg(x.s,C.mx)[2];b.title=md(x.d)+' '+f1(x.s)+'점';if(i===D.length-1)b.className='last';bx.appendChild(b)});tr.appendChild(bx);
 var dd=Math.round((now.s-pv.s)*10)/10;tr.appendChild(el('span','dt',dd>0?'▲ '+f1(dd)+'점':dd<0?'▼ '+f1(-dd)+'점':'전날과 같음'));anc.after(tr)}
Promise.all([j('d/lights/lights_log.json'),j('d/lights/thresholds.json'),j('d/lights/fresh.json')]).then(function(a){L=a[0];T=a[1];F=a[2];if(!L||!T)return;
 var k=0;(function t(){try{draw()}catch(e){}if(++k<25)setTimeout(t,400)})()});
}catch(e){}})();
