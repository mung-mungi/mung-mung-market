// 시장 경고등 점수제(사용자 2026-11-01, 안 A) — 자료 d/lights/fresh.json(lights_fresh.py가 계산)
// 켜짐 = 무게 전부 · 근접 0.8 · 보통 0.4 · 양호 0.2 · 안전 0 을 무게에 곱해 더한 점수(만점 12)로 단계를 정함.
// 큰 카드(#big)를 점수 카드로 바꾸고, 1년 기록 칸 맨 위에 점수 흐름 그래프를 붙임.
(function(){
var F=null;window.__MM_EXP_SET=1;
var EXP={
semi_design:['엔비디아·AMD·브로드컴 평균 주가가 1년 최고점에서 얼마나 내려왔나입니다. 30% 넘게 빠지면 켜집니다 — AI 칩 수요에 대한 의심이 커졌다는 뜻입니다.','p-prices.html','시세 보드에서 보기'],
semi_mem:['마이크론·SK하이닉스가 1년 최고점에서 얼마나 내려왔나입니다. 메모리는 가격이 출렁이는 업종이라 AI 수요 변화를 가장 먼저 탑니다.','p-prices.html','시세 보드에서 보기'],
semi_fab:['TSMC·어플라이드·램리서치 — 칩을 만드는 공장과 장비 회사들입니다. 여기가 빠지면 내년 설비투자가 줄 걱정이 커진 것입니다.','p-prices.html','시세 보드에서 보기'],
semi_net:['아리스타·코히어런트 — 데이터센터 안 서버를 잇는 네트워크·광통신 회사입니다.','p-prices.html','시세 보드에서 보기'],
semi_pwr:['버티브·GE버노바 — 데이터센터 전력·냉각 장비 회사입니다. AI 공장 건설 속도를 보여 줍니다.','p-prices.html','시세 보드에서 보기'],
semi_neo:['코어위브·네비우스 — 빚을 내 GPU를 사서 빌려주는 회사들이라 변동이 커서 문턱을 45%로 높게 잡았습니다. 여기가 빠지면 AI 인프라 돈줄이 불안하다는 신호입니다.','p-neo.html','네오클라우드에서 보기'],
soxday:['필라델피아 반도체 지수가 최근 5거래일 중 하루에 가장 크게 빠진 폭입니다. 5% 넘게 하루에 빠지면 켜집니다.','p-lights.html#mm-semi','반도체·기술 한눈에'],
oil:['WTI 유가가 최근 한 달 동안 얼마나 올랐나입니다. 15% 넘게 급등하면 물가·금리를 다시 자극할 수 있어 켜집니다.','p-policy.html','주요 뉴스에서 보기'],
oil_lvl:['지금 유가가 지난 1년 평균보다 얼마나 높은가입니다. 14% 넘게 높으면 켜집니다 — 비싼 기름값이 오래가는지 봅니다.','p-policy.html','주요 뉴스에서 보기'],
oil_bw:['국제 유가(브렌트)와 미국 내륙 유가(WTI)의 차이입니다. 중동·해상 위험이 커지면 브렌트만 더 올라 차이가 벌어집니다. 평소 3~4달러, 8달러 넘으면 켜집니다.','p-policy.html','주요 뉴스에서 보기'],
ovx:['원유 옵션으로 본 유가의 ‘공포지수’입니다. 전쟁 소식에 유가가 위아래로 크게 흔들릴수록 올라갑니다. 60 넘으면 켜집니다.','p-policy.html','주요 뉴스에서 보기'],
ng:['천연가스 값이 한 달 동안 얼마나 올랐나입니다. 데이터센터 전기값과 이어져 있어 30% 넘게 급등하면 켜집니다.',null],
y10:['미국 10년 국채 금리입니다. 5%를 넘으면 주식의 매력이 줄고 기업 대출 이자가 비싸져 켜집니다.','p-bond.html','채권 온도계에서 보기'],
why:['금리가 왜 움직였는지 봅니다. 물가 걱정이 아니라 ‘나라 빚·수급’ 때문에 금리가 오르면(실질금리 상승) 주식에 더 나쁜 신호라 켜집니다.','p-bond.html','채권 온도계에서 보기'],
y30:['미국 30년 국채 금리입니다. 5.5%를 넘으면 정부 빚 부담 걱정이 커졌다는 뜻이라 켜집니다.','p-bond.html','채권 온도계에서 보기'],
auc:['미 국채 입찰에서 사려는 사람이 적었던(부진) 횟수입니다. 최근에 2번 이상 잇따르면 켜집니다.','p-bond.html','채권 온도계에서 보기'],
hy:['신용이 낮은 회사들(하이일드)이 국채보다 이자를 얼마나 더 내는지입니다. 4.5%p 넘으면 돈 빌리기가 어려워졌다는 뜻이라 켜집니다.','p-bond.html','채권 온도계에서 보기'],
ig:['우량 회사(투자등급)가 국채보다 이자를 얼마나 더 내는지입니다. 1.5%p 넘으면 큰 회사들도 돈줄이 빡빡해졌다는 뜻입니다. 지금처럼 1% 아래면 아주 편한 상태입니다.','p-bond.html','채권 온도계에서 보기'],
ccc:['가장 신용이 낮은 회사들(CCC 등급)이 국채보다 이자를 얼마나 더 내는지입니다. 약한 회사부터 먼저 아파서 위기 초기에 먼저 오릅니다. 14%p 넘으면 켜집니다.','p-bond.html','채권 온도계에서 보기'],
bdc:['사모신용 회사(BDC) 주가가 1년 최고점에서 얼마나 내려왔나입니다. 데이터센터 건설에 돈을 빌려주는 곳이라 15% 넘게 빠지면 켜집니다.',null],
mmf:['미국 MMF(현금처럼 쓰는 펀드) 잔고가 4주 동안 얼마나 늘었나입니다. MMF는 이자가 붙어 평소에도 천천히 늘어나므로, 4주에 3% 넘게 갑자기 몰릴 때(2020년 3월·2023년 3월처럼)만 ‘겁먹고 현금으로 숨는’ 신호로 봅니다.',null],
vix:['앞으로 한 달 S&P 500이 얼마나 출렁일지 옵션 가격으로 본 공포지수입니다. 20 넘으면 켜집니다.','p-opt.html#vix-card','옵션 온도계에서 보기'],
term:['지금 불안(VIX)을 3개월 뒤 불안(VIX3M)으로 나눈 값입니다. 1을 넘으면 ‘지금 당장이 더 무섭다’는 뜻이라 켜집니다.','p-opt.html#term-card','옵션 온도계에서 보기'],
pc:['하락에 거는 옵션(풋)이 상승에 거는 옵션(콜)보다 얼마나 많이 거래됐나입니다. 0.9 넘으면 보험을 많이 산 것이라 켜집니다.','p-opt.html#pc-card','옵션 온도계에서 보기'],
vvix:['VIX 자체가 얼마나 출렁일지 본 값(공포의 공포)입니다. 115 넘으면 시장이 불안 그 자체에 예민해졌다는 뜻이라 켜집니다.','p-opt.html','옵션 온도계에서 보기']};window.__MM_EXP=EXP;

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
 var why=el('p','why');why.innerHTML='켜진 불 <b>'+on.length+'개</b>'+(on.length?(F.ver===2?' — '+ORD.concat(Object.keys(A).filter(function(k){return ORD.indexOf(k)<0})).map(function(a){var x=A[a];if(!x)return'';var n=x.items.filter(function(i){return i.lv==='켜짐'}).length;return n?a+' '+n+'/'+x.items.length:''}).filter(Boolean).join(' · ')+' ':'('+on.join('·')+')'):'')+'에 문턱 앞 지표를 가까운 만큼 더했습니다'+(nr.length?' — 근접: '+nr.join('·'):'')+'.'+(st?'<br><span class="ref">지난 1년 보통 '+st.med+'점 · 상위 20% '+st.p80+'점 · 최고 '+st.max[1]+'점('+md(st.max[0])+')</span>':'');w.appendChild(why);/* 총평(사용자 2026-11-09 — 시장 전체 단계와 반도체만 가진 사람이 느끼는 것이 다를 때 오해 없게) */if(F.review&&F.review.head){var rv=el('details','mm-rv');var rs=el('summary');rs.appendChild(el('b','','📝 총평'));rs.appendChild(el('span','',F.review.head));rs.appendChild(el('i','','펼치기'));rv.appendChild(rs);(F.review.body||[]).forEach(function(t){rv.appendChild(el('p','',t))});if(F.review.by_area){var ch=el('div','rv-ch');ch.appendChild(el('small','','영역만 놓고 본 단계'));Object.keys(F.review.by_area).forEach(function(a){var t=F.review.by_area[a],c=el('span','',a+' '+t);var b=BC.filter(function(x){return x[2]===t})[0];if(b){c.style.borderColor=b[1];c.style.color=b[1]}ch.appendChild(c)});rv.appendChild(ch)}w.appendChild(rv)}
 // 영역별 점수 막대(누르면 지표별 점수)
 var ar=el('div','ar');ORD.concat(Object.keys(A).filter(function(k){return ORD.indexOf(k)<0})).forEach(function(a){var x=A[a];if(!x)return;var p=x.max?x.score/x.max:0;var cc=p>=.8?'#b3261e':p>=.45?'#e07b16':p>0?'#c99a06':'#cfc8ba';
  var r=el('details','r');var sm=el('summary');sm.appendChild(el('b','',a));var br=el('span','bar');var i=el('i');i.style.width=Math.max(p>0?4:0,p*100)+'%';i.style.background=cc;br.appendChild(i);sm.appendChild(br);var v=el('span','v',(Math.round(x.score*10)/10)+'');v.style.color=cc;v.appendChild(el('small','','/'+x.max));sm.appendChild(v);
  var hit=x.items.filter(function(i){return i.pt>0});sm.appendChild(el('span','one',hit.length?hit.map(function(i){return (SH[i.name]||i.name)+' '+fv(i)+' '+i.lv}).join(' · '):'문턱에서 멉니다'));r.appendChild(sm);
  var ul=el('div','its');x.items.forEach(function(i){var q=el('p');var k=el('span','k k-'+({'켜짐':'on','근접':'nr','보통':'md','양호':'ok'}[i.lv]||'sf'),i.lv);q.appendChild(k);q.appendChild(el('b','',i.name));q.appendChild(el('span','vv',(i.note?i.note+' · 1달 '+(Math.round(i.val*100)/100)+'%':fv(i))+(i.pctl!=null?' · 10년 중 '+Math.round(i.pctl)+'% 자리 (켜짐 ≥ '+(Math.round(i.th*100)/100)+(i.unit==='%p'?'%p':i.unit||'')+')':' (기준 '+(i.op==='<'?'< ':'≥ ')+i.th+(i.unit==='%p'?'%p':i.unit||'')+')')));q.appendChild(el('em','','+'+i.pt+(i.w!==1&&i.w!==.5?' (무게 '+i.w+')':'')));ul.appendChild(q);/* 지표 줄을 누르면 쉬운 설명 + 자세히 볼 페이지(사용자 2026-11-09) */var ex=EXP[i.id];if(ex){q.classList.add('can');q.setAttribute('role','button');var dd=el('div','ex');dd.appendChild(el('span','',ex[0]));if(ex[1]){var a=el('a','',(ex[2]||'자세히 보기')+' ›');a.href=ex[1];a.addEventListener('click',function(e){e.stopPropagation()});dd.appendChild(a)}dd.hidden=true;q.after(dd);q.addEventListener('click',function(e){e.stopPropagation();dd.hidden=!dd.hidden;q.classList.toggle('op',!dd.hidden)})}});r.appendChild(ul);ar.appendChild(r)});w.appendChild(ar);
 w.appendChild(el('p','key',F.ver===2?(F.ver3?'지표마다 지난 10년 중 몇 % 자리인지 봅니다 — 70% 자리 아래(평소)는 0점, 드물수록 99% 자리 1점까지 계속 올라갑니다(93% 자리부터 켜짐). 금리 수준·연준 스프레드처럼 10년 비교가 맞지 않는 지표는 문턱 가까이(88%↑) 와야 점수가 붙습니다. 5개 영역을 똑같이 20%씩 평균해 10점으로 바꿉니다. 줄을 누르면 지표별 설명이 펼쳐집니다.':'영역마다 불을 켜짐 1 · 근접(기준의 90%↑) 0.8 · 보통(80%↑) 0.4 · 양호(60%↑) 0.2 · 안전 0으로 매겨 얼마나 찼는지(0~100%)를 내고, 5개 영역을 똑같이 20%씩 평균해 10점으로 바꿉니다. 줄을 누르면 지표별 점수가 펼쳐집니다.'):'켜짐 = 무게 전부 · 근접(기준의 90%↑) 0.8 · 보통(80%↑) 0.4 · 양호(60%↑) 0.2 · 안전 0 — 무게를 곱해 더합니다. 줄을 누르면 지표별 점수가 펼쳐집니다.'));
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
fetch('d/lights/fresh.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){F=j;/* 경고등 2판(사용자 2026-11-09): 단계 문턱을 자료에서 받음 */if(j&&j.bands&&j.bands.length===5){var CC=['#2e9d5b','#c99a06','#e07b16','#c8501c','#b3261e'];BC=j.bands.map(function(b,i){return[b[0],CC[i],b[1]]})}var k=0;(function go(){run();if(++k<16)setTimeout(go,400)})();
 var lw=document.querySelector('.lw');if(lw&&window.MutationObserver){var t=null;new MutationObserver(function(){clearTimeout(t);t=setTimeout(run,120)}).observe(lw,{childList:true,subtree:true})}}).catch(function(){});
})();
