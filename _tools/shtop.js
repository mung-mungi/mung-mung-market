// 공매도 추이 '오늘 한눈에'(사용자 2026-11-02 "실시간 트래킹이 안 되니 후행지표 — 지나고 보면 더 정확해지는 보조지표로")
// 비어 보이던 오늘 한눈에(#take, 3줄 나누기가 안 맞아 빈 상자) 자리에: '확인용 보조지표' 칩 + 자료 날짜(잔고는 2주마다·늦게 공개) + 3줄(많이 쌓인 곳 · 요즘 몰리는 곳 · 확인 신호) + 위쪽 바로가기 알약.
// 자료는 페이지가 이미 불러온 dash.data('si'·'sv'·'px')를 그대로 씀(추가로 받지 않음).
(function(){if(!/p-short\.html/.test(location.pathname))return;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function md(d){var a=String(d).split('-');return (+a[1])+'/'+(+a[2])}
function D(k){try{var r=window.dash&&dash.data(k);return r&&r.status==='ok'?r.data:null}catch(e){return null}}
function calc(){var si=D('si'),sv=D('sv'),px=D('px');if(!si||!sv||!px)return null;
 var nm={},sd='',vd='';si.forEach(function(r){nm[r.ticker]=r.name;if(r.date>sd)sd=r.date});
 var EX={'레오폴드 보유':1,'섹터·시장':1},OKT={},LT={};si.forEach(function(r){if(r.pct_float!=null&&(!LT[r.ticker]||r.date>LT[r.ticker].date))LT[r.ticker]=r});var cur=Object.keys(LT).map(function(k){return LT[k]}).filter(function(r){return !EX[r.layer]});cur.forEach(function(r){OKT[r.ticker]=1}); // 종목마다 최신 잔고, 밸류체인 종목만(페이지 기본 탭과 같게) // 밸류체인 종목만(페이지 기본 탭과 같게)
 var top=cur.slice().sort(function(a,b){return b.pct_float-a.pct_float}).slice(0,3);
 var by={};sv.forEach(function(r){if(r.ratio==null||!OKT[r.ticker])return;(by[r.ticker]=by[r.ticker]||[]).push(r);if(r.date>vd)vd=r.date});
 var dv=[];Object.keys(by).forEach(function(t){var a=by[t].sort(function(x,y){return x.date<y.date?-1:1});if(a.length<30||a[a.length-1].date!==vd)return;
  var l5=a.slice(-5),y=a.slice(-250),m5=l5.reduce(function(s,r){return s+r.ratio},0)/l5.length,my=y.reduce(function(s,r){return s+r.ratio},0)/y.length;dv.push({t:t,d:m5-my,m5:m5})});
 var pp={};px.forEach(function(r){(pp[r.ticker]=pp[r.ticker]||[]).push(r)});
 function ch(t){var a=(pp[t]||[]).sort(function(x,y){return x.date<y.date?-1:1});if(a.length<11)return null;return (a[a.length-1].close/a[a.length-11].close-1)*100}
 var hot=dv.slice().sort(function(a,b){return b.d-a.d}).slice(0,3);
 var push=dv.filter(function(x){var c=ch(x.t);return c!=null&&c<=-5&&x.d>=5}).map(function(x){x.c=ch(x.t);return x}).sort(function(a,b){return a.c-b.c});
 var cover=cur.filter(function(r){var c=ch(r.ticker);r.c=c;return r.pct_float>=10&&c!=null&&c>=5}).sort(function(a,b){return b.c-a.c});
 return {sd:sd,vd:vd,nm:nm,top:top,hot:hot,push:push,cover:cover}}
function f1(v){return (Math.round(v*10)/10).toFixed(1)}
// 맨 위 두 줄·전체 흐름은 페이지가 원래 쓴 #take 문장(굵은 글씨)을 그대로 씀 — 아래 그래프 숫자와 똑같게
function orig(t){return [].filter.call(t.querySelectorAll('b'),function(b){return !b.closest('.mm-sh')}).map(function(b){return b.textContent.trim()})}
function draw(){var t=document.getElementById('take');if(!t)return;var O=orig(t);if(O.length<2)return;var card=t.closest('section,.card,article')||t;var w=t.querySelector('.mm-sh');var C=calc();if(!C)return;
 var key=C.sd+C.vd+O.join('|');if(w&&w.dataset.k===key)return;if(!w){w=el('div','mm-sh');t.appendChild(w)}w.dataset.k=key;w.textContent='';t.classList.add('mm-sh-src');
 var hd=el('div','mm-sh-hd');hd.appendChild(el('span','tag','⏱ 확인용 보조지표'));hd.appendChild(el('span','dt','잔고 '+md(C.sd)+' 기준 · 일별 '+md(C.vd)+'까지'));w.appendChild(hd);w.appendChild(el('p','mm-sh-note','실시간 신호가 아닙니다 — 잔고는 2주에 한 번, 약 8거래일 늦게 나옵니다. 주가가 움직인 뒤 "숏 때문이었나"를 확인하는 데 씁니다.'));
 // 경고 상자(사용자 2026-11-09 '경고 문자 하나 쓰자' — 연 5천만 원 추적 비용 없이는 실시간이 어려운 참고자료, 후행·단일지표 금지)
 var wn=document.querySelector('.mm-shwarn');if(!wn){wn=el('div','mm-shwarn');card.parentNode.insertBefore(wn,card)}wn.textContent='';wn.appendChild(el('b','','⚠ 참고용 자료입니다'));wn.appendChild(el('p','','실시간 공매도 추적은 연 5천만 원 수준의 유료 자료가 있어야 가능합니다. 이 페이지는 공개 자료로 만들어 실시간 추적이 어렵습니다.'));wn.appendChild(el('p','','지난 흐름을 보는 후행 지표로만 쓰고, 이 숫자 하나로 판단하면 안 됩니다. (지금 잔고 '+md(C.sd)+' 기준)'));
 var N=function(t){return C.nm[t]||t};
 var rows=[['많이 쌓인 곳',O[0].replace(/,\s*/g,' · ')+' — 유통 주식 중 숏 비율'],
  ['요즘 몰리는 곳',O[1].replace(/,\s*/g,' · ')+' — 최근 5일 공매도 비중, 평소 대비']];
 if(O[2]&&O[3])rows.push(['전체 흐름','지난 집계보다 숏이 '+O[2]+' · '+O[3]+(/(되사|거둬)/.test(t.textContent)?' → 숏을 거둬들이는 쪽':'')]);
 rows=rows.concat([
  ['확인 신호',(C.push.length?'숏이 하락을 미는 곳 '+C.push.length+'곳('+C.push.slice(0,3).map(function(x){return N(x.t)+' '+f1(x.c)+'%'}).join(' · ')+')':'숏이 하락을 미는 곳 없음')+' / '+(C.cover.length?'되사기(숏 청산) 반등 후보 '+C.cover.slice(0,3).map(function(r){return N(r.ticker)+' +'+f1(r.c)+'%'}).join(' · '):'되사기 반등 후보 없음')]]);
 var ul=el('ul','mm-sh-rows');rows.forEach(function(r){var li=el('li');li.appendChild(el('span','lb',r[0]));li.appendChild(el('span','',r[1]));ul.appendChild(li)});w.appendChild(ul);
 jump(card)}
var J=[[/^하락 베팅이 많이/,'많이 쌓인 종목'],[/^요즘 숏이 몰리는/,'요즘 몰리는 종목'],['detail-card','종목 추이'],['flow-card','큰손 흐름'],['etf-si-card','반도체 ETF']];
function find(k){if(typeof k==='string'){var e=document.getElementById(k);return e&&e.offsetParent!==null?e:null}var h=[].find.call(document.querySelectorAll('h2,h3'),function(x){return x.offsetParent!==null&&k.test(x.textContent.trim())});return h&&(h.closest('section,.card,article')||h)}
function jump(card){var have=J.map(function(a){return [find(a[0]),a[1],a[0]]}).filter(function(a){return a[0]});var nav=document.querySelector('.mm-shj'),sig=have.map(function(a){return a[1]}).join(',');
 if(nav&&nav.dataset.sig===sig&&nav.previousElementSibling===card)return;if(nav)nav.remove();if(have.length<2)return;
 nav=el('nav','mm-shj');nav.dataset.sig=sig;have.forEach(function(a){var x=el('a','',a[1]);x.href='#';x.setAttribute('role','button');x.onclick=function(e){e.preventDefault();var t=find(a[2]);if(t)scrollTo({top:t.getBoundingClientRect().top+scrollY-10,behavior:'smooth'})};nav.appendChild(x)});card.after(nav)}
var k=0;(function go(){try{draw()}catch(e){}if(++k<40)setTimeout(go,500)})();
try{new MutationObserver(function(){try{draw()}catch(e){}}).observe(document.body,{childList:true,subtree:true})}catch(e){}
})();
