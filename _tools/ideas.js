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

function val(D){
  var it=D.items;$('take-chip').textContent=md(D.asof)+' 종가 기준';
  var cnt={};it.forEach(function(o){o.L.forEach(function(l){if(l.on)cnt[l.k]=(cnt[l.k]||0)+1})});
  var top=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a]});
  var hi=it.filter(function(o){return o.lights>=6});
  $('take-text').textContent='불 6개 이상 켜진 곳은 '+hi.map(function(o){return o.name+'('+o.lights+')'}).join('·')+'입니다. 요즘은 \''+top[0]+'\'('+cnt[top[0]]+'곳)과 \''+top[1]+'\'('+cnt[top[1]]+'곳) 불이 가장 많이 켜져 있어, 실적은 좋은데 주가가 빠져 있는 곳이 많은 장입니다.';
  tiles([['살펴본 종목',it.length+'곳','AI 밸류체인(지수 ETF 제외)'],['불 5개 이상',it.filter(function(o){return o.lights>=5}).length+'곳','7개 만점'],['가장 적게 켜진 불',top[top.length-1],cnt[top[top.length-1]]+'곳만 켜짐']]);
  var cats={};it.forEach(function(o){cats[o.cat]=(cats[o.cat]||0)+1});
  var CK=['전체'].concat(Object.keys(cats).sort(function(a,b){return cats[b]-cats[a]})),cat='전체',srt='l';
  $('cat').innerHTML=CK.map(function(c,i){return '<button type="button"'+(i?'':' class="on"')+' data-k="'+esc(c)+'">'+esc(c)+(i?' '+cats[c]:'')+'</button>'}).join('');
  $('cat').onclick=function(e){var b=e.target.closest('button');if(!b)return;[].forEach.call(this.children,function(x){x.classList.toggle('on',x===b)});cat=b.dataset.k;draw()};
  // 내 불 고르기 — 고른 불만 세어 줄 세움(사용자 2026-10-29). 고른 것은 이 휴대폰에만 기억
  var LK=it[0].L.map(function(l){return l.k});
  var PS=[['all','전체 7개',LK],['safe','안정형',['실적 탄력','같은 층 대비 싸다','목표가 오름세','수급 개선']],['risk','하이리스크·반등',['고점 대비 눌림','목표가 여력','고수 상향','실적 탄력']],['mom','모멘텀',['목표가 오름세','고수 상향','실적 탄력','수급 개선']]];
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
    +'<details class="iv-cut"'+(OPEN?' open':'')+'><summary>▸ 불마다 기준 바꾸기</summary>'+SEL.filter(function(k){return CUT[k]}).map(function(k){var c=CUT[k];return '<div class="iv-cr"><b>'+esc(k)+'</b><div class="iv-pills">'+c[0].map(function(v){return '<button type="button" data-c="'+esc(k)+'" data-v="'+v+'"'+(P[k]===v?' class="on"':'')+'>'+c[2](v)+'</button>'}).join('')+'</div></div>'}).join('')+'<button type="button" class="iv-reset" data-reset="1">기준 처음대로</button></details>'}
  $('pickbox').onclick=function(e){var b=e.target.closest('button');if(!b)return;
    if(b.dataset.reset){LK.forEach(function(k){if(CUT[k])P[k]=CUT[k][1]});saveP();pk();draw();return}
    if(b.dataset.c){P[b.dataset.c]=+b.dataset.v;saveP();pk();draw();return}
    if(b.dataset.p){SEL=PS.filter(function(p){return p[0]===b.dataset.p})[0][2].slice()}
    else{var k=b.dataset.l,i=SEL.indexOf(k);if(i>=0){if(SEL.length>1)SEL.splice(i,1)}else SEL.push(k)}
    save();pk();draw()};
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
fetch('d/ideas/'+(K==='p-value'?'value':'pros')+'.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(K==='p-value'?val:pros).catch(function(e){var t=$('take-text');if(t)t.textContent='자료를 불러오지 못했습니다.';console.error(e)});
})();
