(function(){
var K=window.__IDEA__;
function $(i){return document.getElementById(i)}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function sg(x,d){if(x==null||isNaN(x))return '—';var a=Math.abs(x).toFixed(d==null?0:d);return (x>0?'+':x<0?'−':'')+a}
function cls(x){return x==null?'iv-0':x>0?'iv-up':x<0?'iv-dn':'iv-0'}
function md(d){var p=String(d).split('-');return (+p[1])+'.'+(+p[2])}
function num(v){return v==null?'—':Math.round(v).toLocaleString('ko-KR')}
function usd(v){var a=Math.abs(v);return (v<0?'−':'')+(a>=1e8?(a/1e8).toFixed(a>=1e9?0:1)+'억$':(a/1e4).toFixed(0)+'만$')}
function seg(el,opts,cur,cb){el.innerHTML=opts.map(function(o){return '<button type="button" data-k="'+o[0]+'"'+(o[0]===cur?' class="on"':'')+'>'+o[1]+'</button>'}).join('');
  el.onclick=function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(el.children,function(x){x.classList.toggle('on',x===b)});cb(b.dataset.k)}}
function tog(el){el.addEventListener('click',function(e){var h=e.target.closest('.iv-hd');if(h)h.parentElement.classList.toggle('open')})}
function tiles(a){$('tiles').innerHTML=a.map(function(t){return '<div class="in-tile"><span class="k">'+t[0]+'</span><span class="v">'+t[1]+'</span><span class="s">'+t[2]+'</span></div>'}).join('')}
function row(nm,sub,mid,big,body){return '<div class="iv-row"><button type="button" class="iv-hd"><span class="iv-nm"><b>'+nm+'</b><small>'+sub+'</small></span><span class="iv-mid">'+mid+'</span><span class="iv-big">'+big+'</span></button><div class="iv-bd">'+body+'</div></div>'}
function more(el,html,n0){if(html.length<=n0){el.innerHTML=html.join('');return}
  el.innerHTML=html.slice(0,n0).join('')+'<button type="button" class="iv-more">▼ 아래로 '+(html.length-n0)+'곳 더</button>';
  el.querySelector('.iv-more').onclick=function(){el.innerHTML=html.join('')}}

function val(D,G){
  var it=D.items;
  // 사슬 확인·재무 체력 불(관문 자료에서) — 사용자 2026-10-29
  if(G&&G.items)it.forEach(function(o){var g=G.items[o.ticker];if(!g||o.L.some(function(l){return l.k==='사슬 확인'}))return;
    var cv=g.chain;o.L.push({k:'사슬 확인',on:cv.v==='AI 확인',v:cv.v+' · 같은 층 '+cv.peers+'곳 중 '+cv.pbeat+'곳 매출 상회'+(cv.pyoy!=null?' · 층 매출 성장 '+cv.pyoy+'%':'')+(cv.ai?' · AI 관점 '+cv.ai:'')});
    o.L.push({k:'재무 체력',on:g.fin.v==='A'||g.fin.v==='B',v:'재무 등급 '+g.fin.v+(g.fin.why.length?' · '+g.fin.why.slice(0,3).join(' · '):'')});
    o.lights=o.L.filter(function(l){return l.on}).length});$('take-chip').textContent=md(D.asof)+' 종가 기준';
  var cnt={};it.forEach(function(o){o.L.forEach(function(l){if(l.on)cnt[l.k]=(cnt[l.k]||0)+1})});
  var top=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a]});
  var hi=it.filter(function(o){return o.lights>=6});
  $('take-text').textContent='불 6개 이상 켜진 곳은 '+hi.map(function(o){return o.name+'('+o.lights+')'}).join('·')+'입니다. 요즘은 \''+top[0]+'\'('+cnt[top[0]]+'곳)과 \''+top[1]+'\'('+cnt[top[1]]+'곳) 불이 가장 많이 켜져 있어, 실적은 좋은데 주가가 빠져 있는 곳이 많은 장입니다.';
  tiles([['살펴본 종목',it.length+'곳','AI 밸류체인(지수 ETF 제외)'],['불 5개 이상',it.filter(function(o){return o.lights>=5}).length+'곳',it[0].L.length+'개 만점'],['가장 적게 켜진 불',top[top.length-1],cnt[top[top.length-1]]+'곳만 켜짐']]);
  var cats={};it.forEach(function(o){cats[o.cat]=(cats[o.cat]||0)+1});
  var CK=['전체'].concat(Object.keys(cats).sort(function(a,b){return cats[b]-cats[a]})),cat='전체',srt='l';
  $('cat').innerHTML=CK.map(function(c,i){return '<button type="button"'+(i?'':' class="on"')+' data-k="'+esc(c)+'">'+esc(c)+(i?' '+cats[c]:'')+'</button>'}).join('');
  $('cat').onclick=function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(this.children,function(x){x.classList.toggle('on',x===b)});cat=b.dataset.k;draw()};
  // 내 불 고르기 — 고른 불만 세어 줄 세움(사용자 2026-10-29). 고른 것은 이 휴대폰에만 기억
  var LK=it[0].L.map(function(l){return l.k});
  var PS=[['all','전체 '+LK.length+'개',LK],['safe','안정형',['사슬 확인','재무 체력','실적 탄력','같은 층 대비 싸다','목표가 오름세']],['risk','하이리스크·반등',['고점 대비 눌림','목표가 여력','고수 상향','실적 탄력']],['mom','모멘텀',['사슬 확인','목표가 오름세','고수 상향','실적 탄력','수급 개선']]];
  var SEL;try{SEL=JSON.parse(localStorage.getItem('mm-val-pick')||'null')}catch(e){}
  if(!Array.isArray(SEL)||!SEL.length)SEL=LK.slice();
  function save(){try{localStorage.setItem('mm-val-pick',JSON.stringify(SEL))}catch(e){}}
  // 불마다 기준도 직접(사용자 2026-10-29) — 원래 숫자(r)로 휴대폰에서 다시 판정
  var CUT={'목표가 여력':[[10,20,30,50],20,function(v){return '+'+v+'% 이상'}],'같은 층 대비 싸다':[[0,10,20,30],10,function(v){return v?'가운데값보다 '+v+'%↓':'가운데값 아래'}],
   '실적 탄력':[[0,15,30,50],15,function(v){return '상회+전년비 '+v+'%↑'}],'고점 대비 눌림':[[10,15,25,40],15,function(v){return '고점 −'+v+'% 이하'}],
   '목표가 오름세':[[1,2,4],2,function(v){return '상향 '+v+'건↑'}],'고수 상향':[[5,10,20],10,function(v){return '상위 '+v+'곳'}],'수급 개선':[[1,2],1,function(v){return '신호 '+v+'개↑'}]};
  var P={};try{P=JSON.parse(localStorage.getItem('mm-val-cut')||'{}')||{}}catch(e){P={}}
  LK.forEach(function(k){if(CUT[k]&&CUT[k][0].indexOf(P[k])<0)P[k]=CUT[k][1]});
  function saveP(){try{localStorage.setItem('mm-val-cut',JSON.stringify(P))}catch(e){}}
  function lit(l){var r=l.r,v=P[l.k];if(r==null||!CUT[l.k])return !!l.on;switch(l.k){
    case '목표가 여력':return r>=v;case '같은 층 대비 싸다':return r.f<r.m*(1-v/100);case '실적 탄력':return !!r.b&&r.y!=null&&r.y>=v;
    case '고점 대비 눌림':return r<=-v;case '목표가 오름세':return r.u>=v&&r.u>r.d*2;case '고수 상향':return r.some(function(z){return z[1]<=v});case '수급 개선':return r>=v}return !!l.on}
  function vtxt(l){if(l.k==='고수 상향'&&Array.isArray(l.r)){var a=l.r.filter(function(z){return z[1]<=P[l.k]});return a.length?'적중률 상위 '+a.map(function(z){return z[0]+'('+z[1]+'위)'}).join(', ')+' 상향':'최근 60일 상위 '+P[l.k]+'곳 상향 없음'}return l.v}
  function pk(){var pb=$('pickbox');var same=function(a){return a.length===SEL.length&&a.every(function(x){return SEL.indexOf(x)>=0})};
    pb.innerHTML='<p class="iv-pk-t">내 불 고르기<small>고른 불만 셉니다</small></p><div class="iv-pills iv-ps">'+PS.map(function(p){return '<button type="button" data-p="'+p[0]+'"'+(same(p[2])?' class="on"':'')+'>'+p[1]+'</button>'}).join('')+'</div><div class="iv-pills iv-lp">'+LK.map(function(k){return '<button type="button" data-l="'+esc(k)+'"'+(SEL.indexOf(k)>=0?' class="on"':'')+'>'+esc(k)+'</button>'}).join('')+'</div>'
    +'<div class="iv-info" id="linfo"'+(LAST?'':' hidden')+'>'+(LAST?info(LAST):'')+'</div>'
    +'<details class="iv-cut"'+(OPEN?' open':'')+'><summary>▸ 불마다 기준 바꾸기</summary>'+SEL.filter(function(k){return CUT[k]}).map(function(k){var c=CUT[k];return '<div class="iv-cr"><b>'+esc(k)+'</b><div class="iv-pills">'+c[0].map(function(v){return '<button type="button" data-c="'+esc(k)+'" data-v="'+v+'"'+(P[k]===v?' class="on"':'')+'>'+c[2](v)+'</button>'}).join('')+'</div></div>'}).join('')+'<button type="button" class="iv-reset" data-reset="1">기준 처음대로</button></details>'}
  $('pickbox').onclick=function(e){var b=e.target.closest('button');if(!b)return;
    if(b.dataset.reset){LK.forEach(function(k){if(CUT[k])P[k]=CUT[k][1]});saveP();pk();draw();return}
    if(b.dataset.c){P[b.dataset.c]=+b.dataset.v;saveP();pk();draw();return}
    if(b.dataset.p){SEL=PS.filter(function(p){return p[0]===b.dataset.p})[0][2].slice()}
    else{var k=b.dataset.l,i=SEL.indexOf(k);LAST=k;if(i>=0){if(SEL.length>1)SEL.splice(i,1)}else SEL.push(k)}
    save();pk();draw()};
  // 불을 누르면 그 불이 뭘 보는지 + 지금 몇 곳 켜졌는지(사용자 2026-10-29)
  var LAST='';var IX={'목표가 여력':'증권사 평균 목표가가 지금 주가보다 얼마나 위에 있는지 봅니다.','같은 층 대비 싸다':'선행 PER을 같은 층(예: 메모리끼리) 가운데값과 비교합니다.','실적 탄력':'가장 최근 분기 매출이 예상보다 높고 전년보다 크게 늘었는지 봅니다.',
   '고점 대비 눌림':'1년 최고가에서 얼마나 내려와 있는지 봅니다. 떨어지는 칼일 수 있어 사슬·실적 불과 함께 보는 게 좋습니다.','목표가 오름세':'최근 60일 증권사 목표가 상향이 하향보다 충분히 많은지 봅니다.','고수 상향':'고수 성적표의 적중률 상위 증권사가 최근 60일 안에 올렸는지 봅니다.',
   '수급 개선':'공매도 잔고 감소·기관 보유 비중 증가·내부자 순매수 가운데 몇 개가 보이는지 셉니다.','사슬 확인':'AI 돈이 이 종목의 층(동료 실적)과 이 종목 자신(실적·AI 판정)까지 내려왔는지 봅니다. 우리 사슬 관점의 출발점입니다.','재무 체력':'몸값·성장·이익률·현금흐름·빚을 묶은 재무 등급이 A·B인지 봅니다. 시장가치를 받쳐 줄 체력이 있는지입니다.'};
  function info(k){var n=it.filter(function(o){return o.L.some(function(l){return l.k===k&&lit(l)})}).length,on=SEL.indexOf(k)>=0;
    return '<b>'+esc(k)+(on?' 켬':' 끔')+'</b> · '+esc(IX[k]||'')+(CUT[k]?' 지금 기준 '+CUT[k][2](P[k])+'.':'')+' '+it.length+'곳 중 <b>'+n+'곳</b> 켜짐.'}
  var OPEN=0;$('pickbox').addEventListener('toggle',function(e){if(e.target.classList&&e.target.classList.contains('iv-cut'))OPEN=e.target.open?1:0},true);
  pk();
  seg($('sort'),[['l','불 개수'],['u','목표가 여력'],['p','싼 순(PER)'],['d','많이 빠진 순']],'l',function(k){srt=k;draw()});
  tog($('list'));
  function draw(){
    function sc(o){return o.L.filter(function(l){return lit(l)&&SEL.indexOf(l.k)>=0}).length}
    var a=it.filter(function(o){return cat==='전체'||o.cat===cat}).slice();
    var nz=function(v,d){return v==null||v<=0?d:v};
    a.sort(srt==='u'?function(x,y){return (y.up==null?-1e9:y.up)-(x.up==null?-1e9:x.up)}:srt==='p'?function(x,y){return nz(x.fpe,1e9)-nz(y.fpe,1e9)}:srt==='d'?function(x,y){return (x.dd==null?0:x.dd)-(y.dd==null?0:y.dd)}:function(x,y){return sc(y)-sc(x)||(y.up||-1e9)-(x.up||-1e9)});
    var html=a.map(function(o){
      var dots='<span class="iv-dots">'+o.L.map(function(l){var s=SEL.indexOf(l.k)>=0;return '<i class="'+(lit(l)?'on':'')+(s?'':' x')+'"></i>'}).join('')+'</span>';
      var mid=dots+'<b>'+sc(o)+'</b>/'+SEL.length+'<small>'+(o.fpe&&o.fpe>0?'선행 PER '+o.fpe.toFixed(1)+'배':'PER —')+'</small>';
      var big='<span class="'+cls(o.up)+'">'+sg(o.up)+'%</span><small>목표가까지</small>';
      var body=o.L.map(function(l){var on=lit(l);return '<div class="iv-lt'+(on?'':' off')+(SEL.indexOf(l.k)>=0?'':' ns')+'"><i>'+(on?'🟡':'⚪')+'</i><b>'+esc(l.k)+(CUT[l.k]?' <small style="font-weight:600;color:#a39d90">('+CUT[l.k][2](P[l.k])+')</small>':'')+'</b><span>'+esc(vtxt(l))+'</span></div>'}).join('');
      body+='<p class="iv-note">3개월 주가 '+sg(o.m3,1)+'% · 증권사 의견 매수 '+(o.n_buy==null?'—':o.n_buy)+' · 중립 '+(o.n_hold==null?'—':o.n_hold)+' · 매도 '+(o.n_sell==null?'—':o.n_sell)+'</p>';
      if(o.m3!=null&&o.m3<=-30)body+='<p class="iv-warn">⚠ 3개월 새 '+sg(o.m3,0)+'% — 빠진 이유(실적·가이던스·업황)를 먼저 확인할 자리입니다.</p>';
      return row(esc(o.name),esc(o.cat)+' · '+esc(o.ticker),mid,big,body)});
    more($('list'),html,25);
  }
  draw();
}

function pros(D){
  var R=D.rank;$('take-chip').textContent=md(D.asof)+' 기준 · 3개월 채점';
  var t=R.slice(0,3);
  $('take-text').textContent='지난 1년 의견 가운데 3개월이 지난 '+num(D.scored)+'건을 실제 주가로 채점했습니다. 종합 1위는 '+t[0].firm+'(적중 '+t[0].hit+'% · 평균 '+sg(t[0].avg,1)+'%p), 2위 '+t[1].firm+', 3위 '+t[2].firm+'입니다. 상위 10곳은 최근 45일 동안 '+D.recent.length+'건을 올렸습니다.';
  var bh=R.slice().sort(function(a,b){return b.hit-a.hit||b.n-a.n})[0];
  tiles([['채점한 의견',num(D.scored)+'건','3개월 지난 상향·하향·신규'],['순위 오른 곳',R.length+'곳','채점 '+D.min_calls+'건 이상 · 전체 '+D.firms_total+'곳'],['적중률 최고',bh.hit+'%',bh.firm+' · '+bh.n+'건']]);
  var srt='s';seg($('rsort'),[['s','종합'],['h','적중률'],['a','평균 초과'],['n','건수']],'s',function(k){srt=k;drawR()});tog($('rank'));
  function drawR(){var a=R.slice();a.sort(srt==='h'?function(x,y){return y.hit-x.hit||y.n-x.n}:srt==='a'?function(x,y){return y.avg-x.avg}:srt==='n'?function(x,y){return y.n-x.n}:function(x,y){return x.rank-y.rank});
    var html=a.map(function(r){
      var nm='<span class="iv-rk'+(r.rank<=3?' t3':'')+'">'+r.rank+'</span>'+esc(r.firm)+'<span class="iv-st">'+'★★★★★'.slice(0,r.stars)+'</span>';
      var mid='적중 <b>'+r.hit+'%</b><small>'+r.n+'건 채점</small>';
      var big='<span class="'+cls(r.avg)+'">'+sg(r.avg,1)+'</span><small>평균 초과 %p</small>';
      var b='<div class="iv-lt"><i>⏱</i><b>1개월 적중률 '+(r.hit1==null?'—':r.hit1+'%')+'</b><span>1개월이 지난 '+r.n1+'건 기준</span></div>';
      b+='<div class="iv-lt"><i>📏</i><b>가운데값 '+sg(r.med,1)+'%p</b><span>평균이 몇 건의 대박에 끌려간 건 아닌지 보는 값</span></div>';
      b+='<div class="iv-lt"><i>🗂</i><b>다룬 종목 '+r.cover+'곳 · 낸 의견 '+r.calls+'건</b><span>3개월이 아직 안 지난 최근 의견 포함</span></div>';
      if(r.best)b+='<div class="iv-lt"><i>🎯</i><b>최고 적중: '+esc(r.best.name)+' '+sg(r.best.x,1)+'%p</b><span>'+md(r.best.date)+' '+esc(r.best.type)+' 의견 → 3개월 뒤 나스닥100 대비</span></div>';
      return row(nm,esc(r.firm_en),mid,big,b)});
    more($('rank'),html,15)}
  drawR();
  var rc=D.recent.map(function(e){var pt=e.pt_from&&e.pt_to?num(e.pt_from)+'→'+num(e.pt_to):(e.rating||'');
    return row(esc(e.name),md(e.date)+' · '+esc(e.firm)+'('+e.rank+'위) · '+esc(e.type)+(e.rating?' · '+esc(e.rating):''),'<b>'+pt+'</b><small>목표가</small>','<span class="'+cls(e.since)+'">'+sg(e.since,1)+'%</span><small>그 뒤 주가</small>',
      '<p class="iv-note">'+esc(e.firm)+'는 종합 '+e.rank+'위입니다. '+(e.pt_from&&e.pt_to?'목표가를 '+num(e.pt_from)+'에서 '+num(e.pt_to)+'('+sg((e.pt_to/e.pt_from-1)*100,0)+'%)로 올렸습니다.':'투자의견을 올렸습니다.')+'</p>')});
  tog($('recent'));more($('recent'),rc,10);
  var bt='l';seg($('btab'),[['l','레오폴드 펀드'],['i','기관 보유 변화'],['s','내부자 순매수']],'l',function(k){bt=k;drawB()});tog($('big'));
  function drawB(){var h;
    if(bt==='l')h=D.leopold.map(function(x){return row(esc(x.name),esc(x.q)+' · '+esc(x.ticker),'<b>'+usd(x.value_bn*1e9)+'</b><small>보유 금액</small>','<span class="iv-0">'+x.pct.toFixed(1)+'%</span><small>포트 비중</small>','<p class="iv-note">직전 분기 대비 '+esc(x.change)+'. AI 인프라에 집중 투자하는 상황인식(Situational Awareness, 레오폴드 아셴브레너) 펀드의 13F 공시 기준입니다.</p>')});
    else if(bt==='i')h=D.inst.map(function(x){return row(esc(x.name),esc(x.cat),'<b>'+num(x.holders)+'곳</b><small>보유 기관 '+sg(x.chg)+'곳</small>','<span class="'+cls(x.own_chg)+'">'+sg(x.own_chg,1)+'</span><small>지분율 %p</small>','<p class="iv-note">'+esc(x.q)+' 말 기준 기관 지분율 '+x.own.toFixed(1)+'%. 보유 기관 수는 대체로 늘어나는 게 보통이라, 지분율이 줄어든 곳이 더 눈에 띄는 신호입니다.</p>')});
    else h=D.insider.map(function(x){var n=x.buy-x.sell;return row(esc(x.name),esc(x.ticker),'매수 <b>'+x.nb+'</b> · 매도 <b>'+x.ns+'</b><small>최근 60일 건수</small>','<span class="'+cls(n)+'">'+usd(n)+'</span><small>순매수</small>','<p class="iv-note">매수 '+usd(x.buy)+' · 매도 '+usd(x.sell)+'. 임원 매도는 보수·세금 때문에 늘 많아서, 드문 매수가 더 의미 있는 신호입니다.</p>')});
    more($('big'),h.length?h:['<p class="iv-empty">자료가 없습니다.</p>'],12)}
  drawB();
}
function get(n){return fetch('d/ideas/'+n+'.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()})}
if(K==='p-value'){Promise.all([get('value'),get('gates').catch(function(){return null})]).then(function(a){val(a[0],a[1]);if(a[1]){my(a[1]);heat(a[1])}tabs()}).catch(function(e){var t=$('take-text');if(t)t.textContent='자료를 불러오지 못했습니다.';console.error(e)})}
else get('pros').then(pros).catch(function(e){var t=$('take-text');if(t)t.textContent='자료를 불러오지 못했습니다.';console.error(e)});

// 탭(사용자 2026-10-29) — 종목 찾기 / 내 종목 점검 / 반도체 온도판, 마지막 탭은 이 휴대폰에 기억
function tabs(){var T=$('tabs');if(!T)return;var cur='find';try{cur=(location.hash.slice(1))||localStorage.getItem('mm-val-tab')||'find'}catch(e){}
  function go(k){if(!$('t-'+k))k='find';[].forEach.call(T.children,function(b){b.classList.toggle('on',b.dataset.t===k)});['find','my','heat'].forEach(function(x){var el=$('t-'+x);if(el)el.hidden=x!==k});try{localStorage.setItem('mm-val-tab',k);history.replaceState(null,'','#'+k)}catch(e){}}
  T.onclick=function(e){var b=e.target.closest('button');if(!b)return;go(b.dataset.t);var y=T.getBoundingClientRect().top+scrollY-8;if(scrollY>y)scrollTo(0,y)};go(cur)}
var GCL={chain:{3:'ok',2:'mid',1:'no'},fin:{3:'ok',2:'mid',1:'no',0:''},spot:{4:'ok',3:'mid',2:'mid',1:'no'},wind:{3:'ok',2:'mid',1:'no'}};
var GX={chain:'같은 층 동료들이 최근 실적에서 매출을 잘 넘기고 있는지(상회 비율)와 층 매출 성장, 그리고 이 종목 자신의 실적·AI 판정을 함께 봅니다. 층과 종목 둘 다 확인되면 \'AI 확인\', 한쪽만이면 \'확인 중\'입니다.',
 fin:'선행 PER(같은 층 대비), 성장 대비 PER, EPS 서프라이즈, 매출 성장에 미국 증권거래위원회(SEC) 공식 재무의 영업이익률·잉여현금흐름·순부채를 더해 등급을 냅니다. 해외 상장사는 앞의 4가지만 씁니다.',
 spot:'200일선 아래면 \'추세 아래\', 고점 근처·RSI 70 이상이면 \'고점 근처\', 고점 대비 −15% 이하·RSI 40 이하·50일선 근처면 \'눌림 자리\'입니다. 10년 채점에서 자리만으로는 3개월 성과가 크게 갈리지 않아, 사슬·재무 다음에 봅니다.',
 wind:'같은 층 종목 가운데 50일선 위 비율과 이 종목 위치로 \'층 전체 조정\'인지 \'나 홀로 약세\'인지 구분합니다. 공매도·목표가·내부자 흐름도 함께 봅니다.'};
var GN={chain:'① 사슬',fin:'② 재무',spot:'③ 자리',wind:'바람'};
function lines(g){var c=g.chain,f=g.fin,s=g.spot,w=g.wind;
  return {chain:'같은 층 '+c.peers+'곳 중 '+c.pbeat+'곳 최근 매출 상회'+(c.pyoy!=null?' · 층 매출 성장 가운데값 전년비 '+sg(c.pyoy)+'%':'')+' · 이 종목 '+(c.yoy!=null?'전년비 '+sg(c.yoy,0)+'%':'이번 분기 자료 대기')+(c.ai?' · AI 관점 '+c.ai:''),
   fin:(f.why.length?f.why.join(' · '):'자료 부족')+(f.health?'':(FINON?' · 이익률·현금흐름·빚: SEC 자료 없음(해외 상장 등)':' · 이익률·현금흐름·빚은 SEC 공식 자료 연결 후 표시')),
   spot:'1년 고점 대비 '+sg(s.dd,0)+'% · 50일선('+num(s.m50)+') 대비 '+sg(s.v50,1)+'% · 200일선('+num(s.m200)+') 대비 '+sg(s.v200,1)+'% · RSI '+(s.rsi==null?'—':s.rsi),
   wind:'층 '+w.ln+'곳 중 '+w.a50+'곳 50일선 위 · 이 종목 50일선 '+(w.me50?'위':'아래')+(w.si!=null?' · 공매도 잔고 '+sg(w.si,1)+'%':'')+' · 목표가 60일 상향 '+w.up60+' · 하향 '+w.dn60+(w.ins?' · 내부자 순'+(w.ins>0?'매수 ':'매도 ')+usd(Math.abs(w.ins)):'')}}
function card(t,g){var L=lines(g),k=['chain','fin','spot','wind'];
  return '<div class="iv-mc" data-t="'+t+'"><div class="iv-mh"><b>'+esc(g.name)+'</b><small>'+esc(g.cat)+' · '+num(g.price)+(g.cur&&g.cur!=='USD'?' '+g.cur:'')+'</small></div>'
   +'<div class="iv-gate">'+k.map(function(x){return '<button type="button" data-g="'+x+'" class="'+(GCL[x][g[x].lv]||'')+'"><small>'+GN[x]+'</small><b>'+esc(g[x].v)+'</b></button>'}).join('')+'</div>'
   +'<div class="iv-gx" hidden></div><p class="iv-vd'+(g.stop?' stop':'')+'">'+esc(g.vd)+'</p>'
   +k.map(function(x){return '<div class="iv-ln" data-l="'+x+'"><b>'+GN[x]+'</b><span>'+esc(L[x])+'</span></div>'}).join('')+'</div>'}
var FINON=false;
function my(G){FINON=!!G.fin_asof;var S=[];try{S=JSON.parse(localStorage.getItem('mm-my')||'[]')||[]}catch(e){}S=S.filter(function(t){return G.items[t]});
  var open=0,qy='';function save(){try{localStorage.setItem('mm-my',JSON.stringify(S))}catch(e){}}
  function opts(){var cats={};Object.keys(G.items).forEach(function(t){var g=G.items[t];if(qy&&(g.name+t).toLowerCase().indexOf(qy.toLowerCase())<0)return;(cats[g.cat]=cats[g.cat]||[]).push(t)});
    return Object.keys(cats).map(function(c){return '<p>'+esc(c)+'</p>'+cats[c].map(function(t){return '<button type="button" data-a="'+t+'"'+(S.indexOf(t)>=0?' class="on"':'')+'>'+esc(G.items[t].name)+'</button>'}).join('')}).join('')||'<p>찾는 종목이 없습니다.</p>'}
  function head(){$('mypick').innerHTML='<div class="iv-chips">'+S.map(function(t){return '<button type="button" data-x="'+t+'">'+esc(G.items[t].name)+' ✕</button>'}).join('')+'<button type="button" class="add" data-o="1">'+(open?'닫기':'＋ 종목 추가')+'</button></div>'
    +(open?'<div class="iv-find"><input id="myq" placeholder="종목 이름 검색" value="'+esc(qy)+'"><div class="iv-opts" id="myopts">'+opts()+'</div></div>':'')}
  function body(){$('mylist').innerHTML=S.length?S.map(function(t){return card(t,G.items[t])}).join(''):'<p class="iv-empty">＋ 종목 추가로 담은 종목이나 관심 종목을 고르면 여기에 관문 점검이 나옵니다. 예: 마이크론, 셀레스티카, 엔비디아</p>'}
  $('mypick').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
    if(b.dataset.o){open=!open;head();var q=$('myq');if(q)q.focus();return}
    if(b.dataset.x){S.splice(S.indexOf(b.dataset.x),1);save();head();body();return}
    if(b.dataset.a){var i=S.indexOf(b.dataset.a);if(i>=0)S.splice(i,1);else S.push(b.dataset.a);save();var y=$('myopts')&&$('myopts').scrollTop;head();if($('myopts'))$('myopts').scrollTop=y;body()}});
  $('mypick').addEventListener('input',function(e){if(e.target.id!=='myq')return;qy=e.target.value;$('myopts').innerHTML=opts()});
  $('mylist').addEventListener('click',function(e){var b=e.target.closest('.iv-gate button');if(!b)return;var c=b.closest('.iv-mc'),x=b.dataset.g,gx=c.querySelector('.iv-gx'),was=b.classList.contains('sel');
    [].forEach.call(c.querySelectorAll('.iv-gate button'),function(z){z.classList.remove('sel')});[].forEach.call(c.querySelectorAll('.iv-ln'),function(z){z.classList.toggle('hl',!was&&z.dataset.l===x)});
    if(was){gx.hidden=true;return}b.classList.add('sel');gx.hidden=false;gx.innerHTML='<b>'+GN[x]+'은 이렇게 봅니다</b><br>'+esc(GX[x])});
  head();body()}
function heat(G){var X=G.soxx;
  var vd=X.v200>0?(X.v50<0?'큰 추세(200일선)는 위, 짧은 추세(50일선)는 아래. 상승 추세 안에서 쉬어 가는 자리입니다.':'큰 추세·짧은 추세 모두 위. 오름세가 이어지는 자리입니다.'):'200일선 아래. 큰 추세가 꺾인 자리라 섹터째 담기는 신중할 때입니다.';
  vd+=' 지난 1년 가장 깊었던 눌림은 '+md(X.worst_d)+' '+sg(X.worst,0)+'%였고, 지금은 '+sg(X.dd,0)+'%입니다. 우리 추적 종목 '+X.bn+'곳 중 '+X.breadth+'곳만 50일선 위에 있습니다.';
  $('soxx').innerHTML='<h3>반도체 지수(SOXX)</h3><p class="sub">섹터째로 담을지 볼 때의 지수 자리입니다.</p><div class="iv-sx">'
   +[['200일선 대비',X.v200],['50일선 대비',X.v50],['1년 고점 대비',X.dd]].map(function(a){return '<div><small>'+a[0]+'</small><b class="'+cls(a[1])+'">'+sg(a[1],1)+'%</b></div>'}).join('')
   +'<div><small>RSI(14)</small><b>'+X.rsi+'</b></div><div><small>3개월</small><b class="'+cls(X.m3)+'">'+sg(X.m3,1)+'%</b></div><div><small>자리</small><b>'+esc(X.spot)+'</b></div></div>'
   +'<div class="iv-lights">'+X.L.map(function(l,i){return '<span'+(X.on[i]?' class="on"':'')+'>'+(X.on[i]?'● ':'○ ')+esc(l)+'</span>'}).join('')+'</div>'
   +'<p class="iv-vd">불 '+X.lights+'/'+X.L.length+' 켜짐 · '+esc(vd)+'</p>';
  var LS=Object.keys(G.layers).map(function(c){var L=G.layers[c];L.c=c;return L}).sort(function(a,b){return b.lv-a.lv||(b.m3||0)-(a.m3||0)});
  $('layers').innerHTML='<h3>사슬 층별 온도판</h3><p class="sub">층마다 \'실적(AI 확인)\'과 \'주가 흐름\'을 함께 봅니다. 실적은 좋은데 주가가 식은 층이 사슬 관점의 관심 자리입니다. 줄을 누르면 층 안 종목의 관문이 펼쳐집니다.</p>'
   +'<div class="iv-lrh"><span>층 · 최근 실적 상회</span><span>매출 성장</span><span>3개월</span><span>온도</span></div>'
   +LS.map(function(L){var ai=Object.keys(L.ai||{}).map(function(k){return k+L.ai[k]}).join('·')||'—';
     var mem=Object.keys(G.items).filter(function(t){return G.items[t].cat===L.c}).map(function(t){var g=G.items[t];return '<div><b>'+esc(g.name)+'</b><span>'+esc(g.chain.v)+' · 재무 '+esc(g.fin.v)+' · '+esc(g.spot.v)+'</span></div>'}).join('');
     return '<button type="button" class="iv-lr"><span class="n"><b>'+esc(L.c)+'</b><small>상회 '+L.beat+'/'+L.rep+' · AI '+ai+' · 50일선 위 '+L.a50+'/'+L.n+'</small></span><span class="c">'+(L.yoy==null?'—':sg(L.yoy)+'%')+'</span><span class="c '+cls(L.m3)+'">'+sg(L.m3,1)+'%</span><span class="c"><span class="iv-st iv-s'+L.lv+'">'+esc(L.temp)+'</span></span></button><div class="iv-mem">'+mem+'</div>'}).join('')
   +'<p class="iv-note">매출 성장은 층별 최근 분기 전년비 가운데값 · AI는 실적 결과 페이지의 AI 관점 판정 수입니다.</p>';
  $('layers').onclick=function(e){var b=e.target.closest('.iv-lr');if(b)b.nextElementSibling.classList.toggle('open')};
  var B=G.bt,ORD=['눌림 자리','보통','고점 근처','추세 아래'];
  function tb(o){return '<table class="iv-bt"><tr><th>자리</th><th>건수</th><th>평균</th><th>가운데값</th><th>이긴 비율</th></tr>'+ORD.filter(function(k){return o[k]}).map(function(k){var r=o[k];return '<tr><td>'+k+'</td><td>'+num(r.n)+'</td><td class="'+cls(r.avg)+'">'+sg(r.avg,1)+'%p</td><td class="'+cls(r.med)+'">'+sg(r.med,1)+'%p</td><td>'+r.hit+'%</td></tr>'}).join('')+'</table>'}
  var hs=ORD.filter(function(k){return B.stocks[k]}).map(function(k){return B.stocks[k].hit}),sp=Math.max.apply(null,hs)-Math.min.apply(null,hs);
  $('bt').innerHTML='<h3>자리 규칙 10년 채점</h3><p class="sub">‘자리’ 판정이 실제로 의미가 있었나 거꾸로 확인했습니다. 지난 10년 매달 말 각 종목의 자리를 판정하고, 3개월 뒤 나스닥100보다 얼마나 더 갔는지 셌습니다.</p>'
   +'<p class="iv-pk-t" style="margin-top:6px">추적 종목 전체</p>'+tb(B.stocks)+'<p class="iv-pk-t">반도체 지수(SOXX)</p>'+tb(B.soxx)
   +'<p class="iv-vd">'+(sp<8?'자리만으로는 3개월 성과가 거의 갈리지 않았습니다(이긴 비율 '+Math.min.apply(null,hs)+'~'+Math.max.apply(null,hs)+'%). 그래서 이 페이지는 자리를 맨 마지막 관문으로 둡니다. 사슬·재무가 먼저입니다.':'자리 단계에 따라 3개월 성과 차이가 뚜렷했습니다.')+' 평균이 가운데값보다 큰 건 몇몇 크게 오른 종목 덕분입니다.</p>'
   +'<p class="iv-note">'+esc(B.note)+' · 지금 추적 중인 종목으로 과거를 본 것이라 성적이 실제보다 좋게 나오는 쪽입니다(살아남은 종목만 보는 편향).</p>'}
})();
