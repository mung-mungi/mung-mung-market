// 실적 결과 > IR 서재 (사용자 2026-10-30) — 데이터는 d/ir/ir.json(새 정리는 items 맨 앞에 추가)
(function(){
var L={'연산칩':'NVDA AMD INTC','맞춤형 칩':'AVGO MRVL 2454','메모리·저장':'MU 000660 005930 SNDK WDC STX 285A SIMO 8299','파운드리':'TSM TSMC TSEM GFS','설계 SW':'CDNS SNPS',
'장비·후공정':'AMAT LRCX KLAC ASML TER CAMT FORM MKSI UCTT AMKR 8150','광통신':'LITE COHR AAOI AXTI FN GLW VIAV','연결·네트워크':'ALAB SMTC CRDO RMBS APH TEL ANET CSCO LUMN',
'서버':'CLS SMCI DELL','전력·냉각':'VRT GEV BE CAT','전력반도체':'NVTS ON MPWR TXN','전력 시공':'PWR FLR','네오클라우드':'CRWV NBIS IREN APLD CIFR','데이터센터 리츠':'EQIX DLR GDS',
'빅테크':'MSFT GOOGL GOOG AMZN META ORCL AAPL TSLA IBM','SW·보안':'NET PLTR PANW NOW'};
var T2L={};Object.keys(L).forEach(function(k){L[k].split(' ').forEach(function(t){T2L[t]=k})});
function layer(t){t=String(t||'').toUpperCase().replace(/\..*$/,'');return T2L[t]||'기타'}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function md(d){var m=String(d||'').match(/\d{4}-(\d\d)-(\d\d)/);return m?(+m[1])+'/'+(+m[2]):''}
var DATA=[],cur='전체',q='';
function build(){var main=document.querySelector('main');var find=document.getElementById('find');if(!main||!find||document.getElementById('irlib'))return false;
 var s=document.createElement('section');s.id='irlib';
 s.innerHTML='<div class="ir-h"><h2>📚 IR 서재</h2><span class="ir-n">0권</span></div>'+
 '<p class="ir-sub">회사가 직접 낸 실적 발표자료·어닝콜을 정리해 꽂아 둡니다 · 누르면 펼쳐집니다</p>'+
 '<details class="ir-how"><summary>▸ 이렇게 읽습니다 · 눌러서 펼치기</summary><p>위 실적 결과가 시장이 본 \'숫자 성적표\'라면, IR 서재는 회사가 그 숫자를 어떻게 설명했는지 모아 둔 곳입니다.<br>실적 결과 카드 이름 옆 <b>IR</b> 알약을 누르면 그 회사 정리로 바로 넘어옵니다.<br>분야 알약으로 같은 층 회사들의 설명을 나란히 비교해 볼 수 있습니다.</p></details>'+
 '<div class="ir-tool"><input class="ir-q" type="search" placeholder="회사·티커 찾기" aria-label="IR 서재 검색"></div>'+
 '<div class="ir-pills" role="group" aria-label="분야"></div><div class="ir-list"></div>';
 var anchor=(find.closest('section')&&find.closest('section').parentNode===main)?find.closest('section'):find;
 main.insertBefore(s,anchor);
 s.querySelector('.ir-q').addEventListener('input',function(e){q=e.target.value.trim().toLowerCase();render()});
 return true}
function pills(){var box=document.querySelector('#irlib .ir-pills');var have={};DATA.forEach(function(x){have[x._l]=(have[x._l]||0)+1});
 var ks=['전체'].concat(Object.keys(L).filter(function(k){return have[k]}),have['기타']?['기타']:[]);
 box.innerHTML='';ks.forEach(function(k){var b=document.createElement('button');b.type='button';b.textContent=k+(k==='전체'?' '+DATA.length:' '+have[k]);b.setAttribute('aria-pressed',k===cur);b.onclick=function(){cur=k;pills();render()};box.appendChild(b)});
 box.style.display=DATA.length?'':'none';document.querySelector('#irlib .ir-tool').style.display=DATA.length>4?'':'none'}
function lk(u,t,c){u=String(u||'');return /^https:\/\//.test(u)?'<a'+(c?' class="'+c+'"':'')+' href="'+esc(u)+'" target="_blank" rel="noopener">'+t+'</a>':''}

// 정리 글을 읽기 좋게(사용자 2026-10-30): 【제목】·━ 줄은 빼고, ★ 한 줄 핵심은 노란 상자, ▶는 소제목, ▪는 점 목록, 들여쓴 줄은 작은 보충 설명.
// 펼치면 '한 줄 핵심 + 첫 소제목(회사가 강조한 것)'까지만 먼저, 나머지(분기 숫자 등)는 '숫자·세부 전체 보기'로 접음
function fmt(ls){var o='',ul=false;function cl(){if(ul){o+='</ul>';ul=false}}
 ls.forEach(function(l){var t=l.replace(/\s+$/,''),u=t.replace(/^[\s　]+/,'');if(!u||/^[━─=]{3,}$/.test(u)||/^【.*】$/.test(u))return;
  if(/^★/.test(u)){cl();o+='<p class="ir-key">'+esc(u.replace(/^★\s*(한\s*줄\s*핵심\s*[:：]\s*)?/,''))+'</p>';return}
  if(/^▶/.test(u)){cl();o+='<h5 class="ir-h5">'+esc(u.replace(/^▶\s*/,''))+'</h5>';return}
  if(/^[▪•·\-]/.test(u)){if(!ul){o+='<ul class="ir-ul">';ul=true}o+='<li>'+esc(u.replace(/^[▪•·\-]\s*/,''))+'</li>';return}
  if(ul&&/^[\s　]{2,}/.test(t)){o=o.replace(/<\/li>$/,'<small>'+esc(u)+'</small></li>');return}
  cl();o+='<p class="ir-p">'+esc(u)+'</p>'});cl();return o}
function txt(b){b=String(b||'');var ls=b.split('\n'),hd=[],i,cut=-1;for(i=0;i<ls.length;i++){if(/^\s*▶/.test(ls[i]))hd.push(i);if(hd.length===2){cut=i;break}}
 if(cut<0||b.length<900)return '<div class="ir-txt">'+fmt(ls)+'</div>';
 return '<div class="ir-txt">'+fmt(ls.slice(0,cut))+'</div><details class="ir-rest"><summary>▾ 숫자·세부 전체 보기</summary><div class="ir-txt">'+fmt(ls.slice(cut))+'</div></details>'}
function card(x,i){var c=document.createElement('div');c.className='ir-c';c.id='ir-'+esc(x.id||i);c.dataset.tk=String(x.ticker||'').toUpperCase();
 var fresh=(Date.now()-new Date(x.date||0).getTime())<3*864e5;
 c.innerHTML='<button type="button" class="ir-row" aria-expanded="false"><div class="ir-l"><b>'+(fresh?'<i>최신</i>':'')+esc(x.name)+'</b><small>'+esc(x.ticker||'')+(x.q?' · '+esc(x.q):'')+(x.time?' · '+esc(x.time):'')+'</small>'+(x.title?'<span class="ir-t">'+esc(x.title)+'</span>':'')+'</div><div class="ir-r"><em>'+esc(x._l)+'</em><span class="ar">›</span></div></button>'+
 '<div class="ir-body"><div class="ir-top">'+(x.pdf_kr_site?'<button type="button" class="ir-pdf ir-main" data-u="'+esc(x.pdf_kr_site)+'" data-t="'+esc(x.name+' '+(x.q||'')+' 번역본')+'">📄 번역본</button>':x.pdf_kr?lk(x.pdf_kr,'📄 번역본','ir-main'):lk(x.pdf_orig,'📄 원문 PDF(한글)','ir-main'))+((x.pdf_kr_site||x.pdf_kr)?lk(x.pdf_orig,'원문 PDF'):'')+lk(x.pdf_slides,'슬라이드')+lk(x.src,'IR 원문 ↗')+'</div>'+txt(x.body)+'<div class="ir-foot"><button type="button" class="ir-up">접기 ▴</button><span>'+(x.by?'정리 · '+esc(x.by):'')+'</span></div></div>';
 var row=c.querySelector('.ir-row');function tog(){var on=c.classList.toggle('on');row.setAttribute('aria-expanded',on)}
 row.onclick=tog;var pb=c.querySelector('.ir-pdf');if(pb)pb.onclick=function(){view(pb.dataset.u,pb.dataset.t)};c.querySelector('.ir-up').onclick=function(){tog();var y=c.getBoundingClientRect().top+scrollY-80;if(c.getBoundingClientRect().top<0)scrollTo(0,y)};return c}

// PDF 보기 화면(사용자 2026-10-30): 사이트 안 번역본을 페이지 안에서 열고, 맨 위 '← 돌아가기'(휴대폰 뒤로가기로도 닫힘)
var PJ=null;function pdfjs(cb){if(window.pdfjsLib)return cb(window.pdfjsLib);if(PJ)return PJ.push(cb);PJ=[cb];var sc=document.createElement('script');sc.src='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
 sc.onload=function(){pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';PJ.forEach(function(f){f(pdfjsLib)});PJ=null};sc.onerror=function(){PJ.forEach(function(f){f(null)});PJ=null};document.head.appendChild(sc)}
function closeV(){var o=document.getElementById('ir-view');if(!o)return;o.remove();document.documentElement.classList.remove('ir-vopen')}
addEventListener('popstate',function(){if(document.getElementById('ir-view'))closeV()});
function view(u,t){closeV();var o=document.createElement('div');o.id='ir-view';
 o.innerHTML='<div class="iv-bar"><button type="button" class="iv-back">← 돌아가기</button><b></b><a target="_blank" rel="noopener">새 창 ↗</a></div><div class="iv-pages"><p class="iv-msg">불러오는 중…</p></div>';
 o.querySelector('b').textContent=t||'';o.querySelector('a').href=u;document.body.appendChild(o);document.documentElement.classList.add('ir-vopen');
 try{history.pushState({irv:1},'',location.href)}catch(e){}
 o.querySelector('.iv-back').onclick=function(){if(history.state&&history.state.irv)history.back();else closeV()};
 var box=o.querySelector('.iv-pages');
 pdfjs(function(L){if(!L){box.innerHTML='<p class="iv-msg">보기 화면을 못 불러왔습니다. 위 \'새 창\'으로 열어 주세요.</p>';return}
  L.getDocument(u).promise.then(function(doc){box.innerHTML='';var W=Math.min(box.clientWidth||innerWidth,900),dpr=Math.min(devicePixelRatio||1,2),n=0;
   (function next(){if(++n>doc.numPages||!document.getElementById('ir-view'))return;doc.getPage(n).then(function(pg){var v1=pg.getViewport({scale:1}),sc=W/v1.width,vp=pg.getViewport({scale:sc*dpr});
    var cv=document.createElement('canvas');cv.width=vp.width;cv.height=vp.height;cv.style.width=W+'px';box.appendChild(cv);pg.render({canvasContext:cv.getContext('2d'),viewport:vp}).promise.then(next)})})()
  }).catch(function(){box.innerHTML='<p class="iv-msg">PDF를 열지 못했습니다. 위 \'새 창\'으로 열어 주세요.</p>'})})}
function render(){var list=document.querySelector('#irlib .ir-list');if(!list)return;list.innerHTML='';list.classList.remove('open');list.style.removeProperty('--irh');var old=document.querySelector('#irlib .ir-more');if(old)old.remove();
 document.querySelector('#irlib .ir-n').textContent=DATA.length+'권';
 if(!DATA.length){list.innerHTML='<div class="ir-empty"><b>아직 꽂힌 자료가 없습니다</b>첫 IR 정리가 들어오면 최신순으로 여기에 쌓입니다.</div>';return}
 var v=DATA.filter(function(x){if(cur!=='전체'&&x._l!==cur)return false;if(!q)return true;return (x.name+' '+x.ticker+' '+(x.title||'')).toLowerCase().indexOf(q)>=0});
 if(!v.length){list.innerHTML='<div class="ir-empty">찾는 회사가 아직 서재에 없습니다.</div>';return}
 var lastD=null;v.forEach(function(x,i){if(x.date!==lastD){lastD=x.date;var h=document.createElement('div');h.className='ir-day';h.textContent=(md(x.date)||'날짜 미상')+' 발표';list.appendChild(h)}list.appendChild(card(x,i))});
 // 처음엔 4권만, 나머지는 펼치기(사용자 2026-10-30 — 스크롤 압박 줄이기)
 if(v.length>4){var cs=list.children,seen=0;[].forEach.call(cs,function(e){if(e.classList.contains('ir-c')){if(++seen>4)e.classList.add('ir-hid')}});
  [].forEach.call(cs,function(e){if(e.classList.contains('ir-day')){var nx=e.nextElementSibling;if(nx&&nx.classList.contains('ir-hid'))e.classList.add('ir-hid')}});
  var m=document.createElement('button');m.type='button';m.className='ir-more';var lb='▼ '+(v.length-4)+'권 더 펼치기';m.textContent=lb;
  m.onclick=function(){var o=list.classList.toggle('open');m.textContent=o?'▲ 접기':lb;if(!o){var s=document.getElementById('irlib');if(s&&s.getBoundingClientRect().top<0)scrollTo(0,s.getBoundingClientRect().top+scrollY-70)}};list.after(m)}}
function open(tk){tk=String(tk||'').toUpperCase();cur='전체';q='';var qi=document.querySelector('#irlib .ir-q');if(qi)qi.value='';pills();render();
 var c=[].slice.call(document.querySelectorAll('#irlib .ir-c')).find(function(x){return x.dataset.tk===tk});var s=document.getElementById('irlib');if(!s)return;
 if(c){document.querySelector('#irlib .ir-list').classList.add('open');if(!c.classList.contains('on'))c.querySelector('.ir-row').click();c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash')}
 if(c&&c.classList.contains('ir-hid')){var li=document.querySelector('#irlib .ir-list');li.classList.add('open');var mb=document.querySelector('#irlib .ir-more');if(mb)mb.textContent='▲ 접기'}var el=c||s;requestAnimationFrame(function(){scrollTo(0,el.getBoundingClientRect().top+scrollY-70)})}
window.mmIrOpen=open;
// 실적 결과 카드에 IR 알약
function badges(){if(!DATA.length)return;var by={};DATA.forEach(function(x){by[String(x.name).replace(/\s/g,'')]=x.ticker});
 document.querySelectorAll('article .mk-l>b').forEach(function(b){if(b.querySelector('.ir-go'))return;var a=b.closest('article');var nm=((a&&a.dataset.name)||'').split(' ')[0].replace(/\s/g,'');var tk=by[nm];if(!tk)return;
  var g=document.createElement('button');g.type='button';g.className='ir-go';g.textContent='IR';g.addEventListener('click',function(e){e.stopPropagation();e.preventDefault();open(tk)},true);b.appendChild(g)})}
function jump(){var hero=document.querySelector('header.mm-hero');if(!hero||document.querySelector('.ir-jump')||!DATA.length)return;var j=document.createElement('button');j.type='button';j.className='ir-jump';j.textContent='📚 IR 서재 '+DATA.length+'권 ›';j.onclick=function(){var s=document.getElementById('irlib');if(s)scrollTo(0,s.getBoundingClientRect().top+scrollY-70)};hero.after(j)}
function load(){fetch('d/ir/ir.json?v='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){DATA=(j.items||[]).filter(function(x){return x&&x.name}).map(function(x){x._l=layer(x.ticker);return x});
 var TO={'아시아':0,'장전':1,'장후':2};DATA.sort(function(a,b){return String(b.date||'').localeCompare(String(a.date||''))||((TO[a.time]==null?9:TO[a.time])-(TO[b.time]==null?9:TO[b.time]))});pills();render();jump();
 var k=0;(function bg(){try{badges()}catch(e){}if(++k<16)setTimeout(bg,500)})();
 if(location.hash==='#ir')setTimeout(function(){var s=document.getElementById('irlib');if(s)scrollTo(0,s.getBoundingClientRect().top+scrollY-70)},300)}).catch(function(){render()})}
var n=0;(function go(){if(build())load();else if(++n<30)setTimeout(go,300)})();
})();
