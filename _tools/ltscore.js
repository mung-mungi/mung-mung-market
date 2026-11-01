// 시장 경고등 점수제(사용자 2026-11-01, 안 A) — 자료 d/lights/fresh.json(lights_fresh.py가 계산)
// 켜짐 = 무게 전부 · 근접 0.8 · 보통 0.4 · 양호 0.2 · 안전 0 을 무게에 곱해 더한 점수(만점 12)로 단계를 정함.
// 큰 카드(#big)를 점수 카드로 바꾸고, 1년 기록 칸 맨 위에 점수 흐름 그래프를 붙임.
(function(){
var F=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function md(d){var a=String(d||'').split('-');return a.length===3?(+a[1])+'/'+(+a[2]):d}
var BC=[[0,'#2e9d5b','평온'],[3,'#c99a06','주의'],[4.7,'#e07b16','경계'],[6.6,'#c8501c','긴장'],[8.4,'#b3261e','위험']];
function col(v){var c=BC[0][1];BC.forEach(function(b){if(v>=b[0])c=b[1]});return c}
function stn(v){var c=BC[0][2];BC.forEach(function(b){if(v>=b[0])c=b[2]});return c}
var ORD=['반도체·AI','유가','채권·금리','신용','옵션·공포'];
var SH={'10년물 5% 이상':'10년물','30년물 5.5% 이상':'30년물','VIX 20 이상':'VIX','기간구조 뒤집힘':'기간구조','풋콜 비율 높음':'풋콜','하이일드 스프레드 4.5%p 이상':'하이일드','유가 급등':'유가','장단기 금리 역전':'장단기차','10년물 2주 급등':'10년물 2주','국채 입찰 부진 잇따름':'입찰 부진','반도체 고점 대비 낙폭':'고점 대비','반도체 하루 급락(최근 5일)':'하루 급락'};
function fv(i){if(i.note)return i.note;var v=i.val;if(v==null)return'—';var u=i.unit||'';return (Math.round(v*100)/100)+(u==='%p'?'%p':u)}
function stats(h){var v=h.map(function(x){return x[1]}).slice().sort(function(a,b){return a-b});var q=function(p){return v[Math.min(v.length-1,Math.floor(p*v.length))]};var mx=h.reduce(function(a,b){return b[1]>a[1]?b:a},h[0]);return{med:q(.5),p80:q(.8),max:mx}}
function card(){var big=document.getElementById('big');if(!big||!F||F.score==null)return;
 var old=big.querySelector('.mm-sc');var sig=F.date+'|'+F.score;if(old&&old.dataset.sig===sig)return;if(old)old.remove();
 big.classList.add('mm-sc-on');var c=col(F.score);big.style.setProperty('--sc',c);
 var w=el('div','mm-sc');w.dataset.sig=sig;
 var h=F.score_hist||[];var t15=h.slice(-15);var st=h.length>20?stats(h):null;
 var hd=el('div','hd');hd.appendChild(el('b','','시장 경고등 점수'));hd.appendChild(el('span','',md(F.date)+' 마감'));w.appendChild(hd);
 var row=el('div','row');var n=el('span','n',F.score.toFixed(1));row.appendChild(n);row.appendChild(el('span','of','/ '+F.score_max+'점'));var s=el('span','st','→ '+F.stage+' 단계');s.style.color=c;row.appendChild(s);w.appendChild(row);
 // 단계 막대
 var mx=F.score_max||12;var gb=el('div','gb');BC.forEach(function(b,i){var e=(BC[i+1]||[mx])[0];var x=el('i');x.style.flex=(e-b[0]);x.style.background=b[1];gb.appendChild(x)});var m=el('em');m.style.left=Math.min(98,F.score/mx*100)+'%';gb.appendChild(m);w.appendChild(gb);
 var gl=el('div','gl');BC.forEach(function(b,i){var e=(BC[i+1]||[mx])[0];var x=el('span');x.style.flex=(e-b[0]);x.textContent=b[2];if(b[2]===F.stage){x.style.color=b[1];x.style.fontWeight=800}x.appendChild(el('small','',b[0]+'~'));gl.appendChild(x)});w.appendChild(gl);
 // 15일 흐름
 if(t15.length>3){var tr=el('div','tr');tr.appendChild(el('span','k','최근 15거래일'));var bx=el('div','bars');var tm=Math.max.apply(null,t15.map(function(x){return x[1]}).concat([8]));t15.forEach(function(x,i){var b=el('i');b.style.height=Math.max(8,x[1]/tm*100)+'%';b.style.background=col(x[1]);b.title=md(x[0])+' '+x[1]+'점';if(i===t15.length-1)b.className='last';bx.appendChild(b)});tr.appendChild(bx);
  var d0=t15[t15.length-2],dd=d0?Math.round((F.score-d0[1])*10)/10:0;tr.appendChild(el('span','k2',(dd>0?'▲ ':dd<0?'▼ ':'')+(dd?Math.abs(dd)+'점':'제자리')));w.appendChild(tr)}
 var A=F.area_scores||{};var on=[],nr=[];ORD.forEach(function(a){var x=A[a];if(!x)return;x.items.forEach(function(i){if(i.lv==='켜짐')on.push(SH[i.name]||i.name);else if(i.lv==='근접')nr.push(SH[i.name]||i.name)})});
 var why=el('p','why');why.innerHTML='켜진 불 <b>'+on.length+'개</b>'+(on.length?'('+on.join('·')+')':'')+'에 문턱 앞 지표를 가까운 만큼 더했습니다'+(nr.length?' — 근접: '+nr.join('·'):'')+'.'+(st?'<br><span class="ref">지난 1년 보통 '+st.med+'점 · 상위 20% '+st.p80+'점 · 최고 '+st.max[1]+'점('+md(st.max[0])+')</span>':'');w.appendChild(why);
 // 영역별 점수 막대(누르면 지표별 점수)
 var ar=el('div','ar');ORD.concat(Object.keys(A).filter(function(k){return ORD.indexOf(k)<0})).forEach(function(a){var x=A[a];if(!x)return;var p=x.max?x.score/x.max:0;var cc=p>=.8?'#b3261e':p>=.45?'#e07b16':p>0?'#c99a06':'#cfc8ba';
  var r=el('details','r');var sm=el('summary');sm.appendChild(el('b','',a));var br=el('span','bar');var i=el('i');i.style.width=Math.max(p>0?4:0,p*100)+'%';i.style.background=cc;br.appendChild(i);sm.appendChild(br);var v=el('span','v',(Math.round(x.score*10)/10)+'');v.style.color=cc;v.appendChild(el('small','','/'+x.max));sm.appendChild(v);
  var hit=x.items.filter(function(i){return i.pt>0});sm.appendChild(el('span','one',hit.length?hit.map(function(i){return (SH[i.name]||i.name)+' '+fv(i)+' '+i.lv}).join(' · '):'문턱에서 멉니다'));r.appendChild(sm);
  var ul=el('div','its');x.items.forEach(function(i){var q=el('p');var k=el('span','k k-'+({'켜짐':'on','근접':'nr','보통':'md','양호':'ok'}[i.lv]||'sf'),i.lv);q.appendChild(k);q.appendChild(el('b','',i.name));q.appendChild(el('span','vv',(i.note?i.note+' · 1달 '+(Math.round(i.val*100)/100)+'%':fv(i))+' (기준 '+(i.op==='<'?'< ':'≥ ')+i.th+(i.unit==='%p'?'%p':i.unit||'')+')'));q.appendChild(el('em','','+'+i.pt+(i.w!==1?' (무게 '+i.w+')':'')));ul.appendChild(q)});r.appendChild(ul);ar.appendChild(r)});w.appendChild(ar);
 w.appendChild(el('p','key','켜짐 = 무게 전부 · 근접(기준의 90%↑) 0.8 · 보통(80%↑) 0.4 · 양호(60%↑) 0.2 · 안전 0 — 무게를 곱해 더합니다. 줄을 누르면 지표별 점수가 펼쳐집니다.'));
 big.insertBefore(w,big.firstChild);var vw=document.getElementById('view');if(vw&&vw.compareDocumentPosition(big)&Node.DOCUMENT_POSITION_FOLLOWING)vw.before(big)}
function hist(){var hc=document.getElementById('hist-card');if(!hc||!F||!F.score_hist||hc.querySelector('.mm-sch'))return;var h=F.score_hist;if(h.length<20)return;var st=stats(h);
 var W=360,H=150,P=[6,24,18,6],mx=Math.max(F.score_max||12,8);mx=Math.max(9,Math.ceil(Math.max.apply(null,h.map(function(x){return x[1]}))+1));
 var X=function(i){return P[3]+i/(h.length-1)*(W-P[1]-P[3])},Y=function(v){return P[0]+(1-v/mx)*(H-P[0]-P[2])};
 var sv='<svg viewBox="0 0 '+W+' '+H+'" width="100%" role="img" aria-label="경고등 점수 1년 흐름">';
 BC.forEach(function(b,i){var e=Math.min(mx,(BC[i+1]||[mx])[0]);if(b[0]>=mx)return;sv+='<rect x="'+P[3]+'" y="'+Y(e)+'" width="'+(W-P[1]-P[3])+'" height="'+(Y(b[0])-Y(e))+'" fill="'+b[1]+'" opacity=".09"/><text x="'+(W-P[1]+3)+'" y="'+(Y((b[0]+e)/2)+3.5)+'" font-size="9.5" font-weight="700" fill="'+b[1]+'">'+b[2]+'</text>'});
 var pts=h.map(function(x,i){return X(i).toFixed(1)+','+Y(x[1]).toFixed(1)}).join(' ');sv+='<polyline points="'+pts+'" fill="none" stroke="#5f5a52" stroke-width="1.4" stroke-linejoin="round"/>';
 var mi=h.indexOf(st.max),L=h.length-1;sv+='<circle cx="'+X(mi)+'" cy="'+Y(st.max[1])+'" r="3" fill="#b3261e"/><text x="'+Math.min(X(mi),W-90)+'" y="'+(Y(st.max[1])-5)+'" font-size="9.5" font-weight="700" fill="#b3261e" text-anchor="middle">최고 '+st.max[1]+' ('+md(st.max[0])+')</text>';
 sv+='<circle cx="'+X(L)+'" cy="'+Y(h[L][1])+'" r="4" fill="'+col(h[L][1])+'" stroke="#fff" stroke-width="1.5"/>';
 var mo='';h.forEach(function(x,i){var m=x[0].slice(0,7);if(m!==mo){mo=m;if(+x[0].slice(5,7)%3===1||i===0)sv+='<text x="'+X(i)+'" y="'+(H-4)+'" font-size="9.5" fill="#9a948a">'+(+x[0].slice(5,7))+'월</text>'}});sv+='</svg>';
 var b=el('div','mm-sch');b.appendChild(el('h3','','점수로 본 1년'));var p=el('p','s');var now=h[L][1];var rk=h.filter(function(x){return x[1]>=now}).length;p.textContent='지금 '+now.toFixed(1)+'점은 지난 1년 '+h.length+'거래일 중 상위 '+Math.max(1,Math.round(rk/h.length*100))+'% 자리입니다. 보통 날은 '+st.med+'점 근처였습니다.';b.appendChild(p);var g=el('div','g');g.innerHTML=sv;b.appendChild(g);
 b.appendChild(el('p','s2','아래는 예전 방식(켜진 불 개수)과 나스닥100입니다.'));var h2=hc.querySelector('h2');if(h2)h2.textContent='1년 기록 · 경고등 점수와 나스닥100';(h2||hc.firstChild).after(b)}
function run(){try{card()}catch(e){}try{hist()}catch(e){}}
fetch('d/lights/fresh.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){F=j;var k=0;(function go(){run();if(++k<16)setTimeout(go,400)})();
 var lw=document.querySelector('.lw');if(lw&&window.MutationObserver){var t=null;new MutationObserver(function(){clearTimeout(t);t=setTimeout(run,120)}).observe(lw,{childList:true,subtree:true})}}).catch(function(){});
})();
