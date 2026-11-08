// '어제보다 바뀐 점' 카드(사용자 2026-11-03, A안) — 경고등·채권·옵션 페이지 맨 위
// 점수·단계가 전 거래일과 어떻게 달라졌는지 + 단계가 바뀐 지표 + '시장 한 줄'(새벽 브리핑 헤드라인). 자료만 비교해 자동으로 씀(크레딧 없음)
// ✕를 누르면 그날은 작은 알약으로 접힘(누르면 다시 펼침)
(function(){
var P=/p-opt\.html/.test(location.pathname)?'opt':/p-bond\.html/.test(location.pathname)?'bond':/p-lights\.html/.test(location.pathname)?'lights':null;if(!P)return;
var CFG={opt:{ids:['vix','term','pc'],nm:'옵션 경고등'},bond:{ids:['y10','why','y30','auc','hy'],nm:'채권 경고등'},lights:{ids:null,nm:'시장 경고등'}}[P];
var BR=[[0,'평온'],[.25,'주의'],[.392,'경계'],[.55,'긴장'],[.7,'위험']];
var SH={soxdd:'반도체 고점 대비',soxday:'반도체 하루 급락',inv:'장단기차',y10:'10년물',why:'금리 움직인 이유',jump:'10년물 2주 급등',y30:'30년물',hy:'하이일드',auc:'국채 입찰',vix:'VIX',term:'기간구조',pc:'풋콜',oil:'유가'};
var LV=['안전','양호','보통','근접','켜짐'],PT=[0,.2,.4,.8,1];
function j(u){return fetch(u+'?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function md(d){var a=String(d).slice(0,10).split('-');return (+a[1])+'.'+(+a[2])}
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function ratio(t,v){if(v==null)return 0;if(t.op==='<'||t.op==='<=')return t.value===0?1-(v/0.5):t.value/v;return t.value>0?v/t.value:0}
function lvi(t,r){if(Number(r.on)===1)return 4;var q=ratio(t,Number(r.val));return q>=.9?3:q>=.8?2:q>=.6?1:0}
function stg(sc,mx,bands){var r=bands[0][1];bands.forEach(function(b){if(sc>=b[0]-1e-9)r=b[1]});return r}
function build(L,T,F,B){var TH={};T.forEach(function(t){TH[t.id]=t});var ids=CFG.ids||T.map(function(t){return t.id});
 var by={};L.forEach(function(r){if(ids.indexOf(r.id)<0||!TH[r.id])return;var d=String(r.date).slice(0,10);(by[d]=by[d]||{})[r.id]=r});
 var ds=Object.keys(by).sort();if(ds.length<2)return null;var d1=ds[ds.length-1],d0=ds[ds.length-2];
 var mx=ids.reduce(function(a,id){return a+(TH[id]?Number(TH[id].weight==null?1:TH[id].weight):0)},0);
 function day(d){var s=0,lv={};ids.forEach(function(id){var r=by[d][id],t=TH[id];if(!r||!t)return;var i=lvi(t,r);lv[id]=i;s+=PT[i]*Number(t.weight==null?1:t.weight)});return{s:Math.round(s*10)/10,lv:lv}}
 var a=day(d0),b=day(d1),bands=BR.map(function(x){return[x[0]*mx,x[1]]});
 if(P==='lights'&&F&&F.score_hist&&F.bands){var h=F.score_hist,n=h.length;if(n>=2){d1=h[n-1][0];d0=h[n-2][0];a.s=h[n-2][1];b.s=h[n-1][1];mx=F.score_max||mx;bands=F.bands.map(function(x){return[x[0],x[1]]})}}
 var up=[],dn=[];if(P==='lights'&&F&&F.ver===2&&F.prev_lv&&F.area_scores){Object.keys(F.area_scores).forEach(function(a){F.area_scores[a].items.forEach(function(i){var x=LV.indexOf(F.prev_lv[i.id]),y=LV.indexOf(i.lv);if(x<0||y<0||x===y)return;(y>x?up:dn).push(i.name.replace(/\(.*?\)/,'')+' '+LV[x]+'→'+LV[y])})});ids=[]}
 ids.forEach(function(id){var x=a.lv[id],y=b.lv[id];if(x==null||y==null||x===y||TH[id].weight===0)return;(y>x?up:dn).push((SH[id]||TH[id].name)+' '+LV[x]+'→'+LV[y])});
 /* 옵션·채권도 경고등 3판 영역 점수(10점 만점)로 — 사용자 2026-11-09 점검 '잣대 하나로' */
 var AN={opt:'옵션·공포',bond:'채권·금리'}[P];if(AN&&F&&F.ver3&&F.area_scores&&F.area_scores[AN]&&F.bands){var A3=F.area_scores[AN],it=A3.items||[],s1=Math.round(A3.ratio*100)/10,dd=0;up=[];dn=[];
  it.forEach(function(i){var x=LV.indexOf((F.prev_lv||{})[i.id]),y=LV.indexOf(i.lv);if(x<0||y<0||x===y)return;dd+=(PT[y]-PT[x])/it.length*10;(y>x?up:dn).push(i.name.replace(/\(.*?\)/,'')+' '+LV[x]+'→'+LV[y])});
  var s0=Math.max(0,Math.min(10,Math.round((s1-dd)*10)/10));bands=F.bands.map(function(x){return[x[0],x[1]]});mx=10;a.s=s0;b.s=s1;CFG.nm=AN+' 영역';var hs=F.score_hist||[];if(hs.length){d1=hs[hs.length-1][0];if(hs.length>1)d0=hs[hs.length-2][0]}}
 var head=B&&B.length?B.slice().sort(function(p,q){return p.date<q.date?-1:1}).pop():null;
 var mk3=(AN&&F&&F.ver3&&F.score!=null&&F.bands)?(+F.score).toFixed(1)+'점 · '+stg(+F.score,10,F.bands):null;
 return{d0:d0,d1:d1,s0:a.s,s1:b.s,mx:mx,g0:stg(a.s,mx,bands),g1:stg(b.s,mx,bands),up:up,dn:dn,head:head,mk3:mk3}}
function render(X){if(!X)return;var host=P==='lights'?document.querySelector('.mm-st-hero'):P==='bond'?(document.querySelector('#take')||{}).closest&&document.querySelector('#take').closest('.bd-take'):document.getElementById('take');
 if(!host||!host.parentNode)return false;var ex=document.querySelector('.mm-mv');if(ex&&ex.nextElementSibling===host)return true;if(ex)ex.remove();
 var key='mm_mv_'+P+'_'+X.d1,closed=ls(key)==='1';var w=el('section','mm-mv'+(closed?' fold':''));
 var hd=el('div','hd');hd.appendChild(el('span','',(X.g0!==X.g1||Math.abs(X.s1-X.s0)>=0.05?'📍 어제보다 바뀐 점':'📍 오늘의 경고등')+' · '+md(X.d1)+' 마감 (전 거래일 '+md(X.d0)+' 대비)'));var x=el('button','x','✕');x.setAttribute('aria-label','접기');hd.appendChild(x);w.appendChild(hd);
 var dv=Math.round((X.s1-X.s0)*10)/10;var ln=el('p','ln');ln.appendChild(document.createTextNode(CFG.nm+' '+(X.mk3?'':X.s0.toFixed(1)+' → ')));var em=el('em','',X.s1.toFixed(1)+'점 · '+(X.g0===X.g1?X.g1+' 그대로':X.g0+' → '+X.g1));ln.appendChild(em);
 ln.appendChild(el('small','',X.mk3?(X.up.length&&!X.dn.length?' 전날보다 올라옴':X.dn.length&&!X.up.length?' 전날보다 내려옴':X.up.length?' 엇갈림':' 제자리'):dv>0?' ▲'+dv:dv<0?' ▼'+Math.abs(dv):' 제자리'));w.appendChild(ln);
 if(X.mk3){var m3=el('p','why');m3.appendChild(el('b','','시장 전체 '));m3.appendChild(document.createTextNode(X.mk3+' — 10점 만점, 같은 잣대(10년 중 자리)로 잰 점수입니다.'));w.appendChild(m3)}
 var why=[];if(X.up.length)why.push('더 가까워진 불: '+X.up.join(' · '));if(X.dn.length)why.push('물러난 불: '+X.dn.join(' · '));
 var p=el('p','why');p.appendChild(el('b','','왜 '));p.appendChild(document.createTextNode(why.length?why.join(' / ')+'.':'지표 단계는 그대로이고 숫자만 조금 움직였습니다.'));w.appendChild(p);
 if(X.head&&X.head.headline){var mk=el('a','mk');mk.href='p-brief.html';mk.appendChild(el('b','','시장 한 줄 · '+md(X.head.date)));mk.appendChild(document.createTextNode(String(X.head.headline).replace(/\*\*/g,'')+' ›'));w.appendChild(mk)}
 var chip=el('button','chip','📍 어제보다 바뀐 점 · '+(X.g0===X.g1?X.g1:X.g0+'→'+X.g1)+' ›');w.appendChild(chip);
 x.onclick=function(){w.classList.add('fold');ls(key,'1')};chip.onclick=function(){w.classList.remove('fold');ls(key,'0')};
 host.parentNode.insertBefore(w,host);return true}
Promise.all([j('d/lights/lights_log.json'),j('d/lights/thresholds.json'),j('d/lights/fresh.json'),j('d/brief/briefs.json')]).then(function(r){if(!r[0]||!r[1])return;var X=null;try{X=build(r[0],r[1],r[2],r[3])}catch(e){}if(!X)return;
 var k=0;(function go(){var ok=false;try{ok=render(X)}catch(e){}if(++k<30)setTimeout(go,ok?800:400)})()});
})();
