(function(){
// 페이지별: 짧은 제목 · 영문 머리말 · 멍뭉이 동작 · 숫자칸(값을 글에서 뽑거나, 없으면 아이콘)
var CFG={
 'p-earn':{t:'실적 결과',en:'EARNINGS',cat:'earn',ic:'📑',lb:'실적 노트'},
 'p-cal':{t:'실적 일정',en:'EARNINGS CALENDAR',cat:'cal',ic:'🗓️',lb:'이번 주'},
 'p-qtr':{t:'분기별 실적 추이',en:'QUARTERLY',cat:'earn',ic:'📈',lb:'분기'},
 'p-capex':{t:'빅테크 설비투자',en:'BIG TECH CAPEX',cat:'capex',ic:'🏗️',lb:'설비투자'},
 'p-targets':{t:'목표주가',en:'PRICE TARGETS',cat:'target',ic:'🎯',lb:'목표가',re:/상향\s*([\d,]+)\s*건/,rl:'1년 상향'},
 'p-opt':{t:'옵션 온도계',en:'OPTIONS',cat:'opt',ic:'🌡️',lb:'온도',re:/VIX\s*([\d.]+)/,rl:'VIX'},
 'p-lights':{t:'시장 경고등',en:'MARKET LIGHTS',cat:'lights',ic:'🚦',lb:'경고등',re:/불\s*(\d+)\s*\/\s*10/,rl:'/10 켜짐',body:1},
 'p-bond':{t:'채권·금리',en:'BONDS & RATES',cat:'fx',ic:'🏦',lb:'금리'},
 'p-fx':{t:'원·달러 환율',en:'USD / KRW',cat:'fx',ic:'💱',lb:'환율',re:/달러당\s*([\d,]+)/,rl:'원'},
 'p-brief':{t:'데일리 시황',en:'DAILY BRIEF',cat:'brief',ic:'📰',lb:'아침'},
 'p-econ':{t:'경제지표',en:'MACRO CALENDAR',cat:'cal',ic:'📊',lb:'지표'},
 'p-policy':{t:'주요 뉴스',en:'NEWS & POLICY',cat:'globe',ic:'🌐',lb:'뉴스'},
 'p-tech':{t:'AI·테크 뉴스',en:'AI & TECH NEWS',cat:'wafer',ic:'🎤',lb:'테크'},
 'p-supply':{t:'아시아 반도체 수출',en:'ASIA SUPPLY',cat:'wafer',ic:'🚢',lb:'수출'},
 'p-neo':{t:'네오클라우드 신용',en:'NEOCLOUD',cat:'magnify',ic:'☁️',lb:'신용'},
 'p-insider':{t:'내부자·기관 보유',en:'INSIDERS',cat:'magnify',ic:'🕵️',lb:'수급'},
 'p-short':{t:'공매도 추이',en:'SHORT INTEREST',cat:'magnify',ic:'🐻',lb:'공매도'},
 'p-trend':{t:'종목 차트',en:'STOCK CHART',cat:'trend',ic:'🧭',lb:'지지·저항'},
 'p-value':{t:'저평가 서치',en:'VALUE RADAR · 공사중',cat:'magnify',ic:'🔎',lb:'3관문'},
 'p-pros':{t:'고수 성적표',en:'PRO SCORECARD · 공사중',cat:'target',ic:'🏆',lb:'적중률'}
};
var key=(location.pathname.split('/').pop()||'').replace(/\.html$/,'');var C=CFG[key];if(!C)return;
function badge(c,side){
  if(!C.re){return}
  var src=C.body?document.body.innerText:(document.querySelector('.mm-take')||{}).textContent||'';var m=src&&src.match(C.re);
  if(m){side.innerHTML='<b></b><small></small>';side.firstChild.textContent=m[1];side.lastChild.textContent=C.rl;}
}
function run(){
  var c=document.querySelector('.mm-hero');if(!c||c.classList.contains('pb-hx'))return;
  var h=c.querySelector('h1.mm-h1');if(!h)return;
  if(!c.classList.contains('mm-hx')){
    c.classList.add('mm-hx');
    if(!h.title)h.title=h.textContent.trim();h.textContent=C.t;document.title=document.title||C.t;
    var eb=c.querySelector(':scope>.mm-eb');if(!eb){eb=document.createElement('p');eb.className='mm-eb';c.insertBefore(eb,h)}eb.textContent=C.en;
    var side=document.createElement('div');side.className='hx-side';side.setAttribute('aria-hidden','true');side.innerHTML='<b class="ic"></b><small></small>';side.firstChild.textContent=C.ic;side.lastChild.textContent=C.lb;c.insertBefore(side,c.firstChild);
    var img=document.createElement('img');img.className='hx-cat';img.alt='';img.setAttribute('aria-hidden','true');img.src='img/cat-'+C.cat+'.webp?v=1';img.onerror=function(){img.remove()};c.appendChild(img);
    var meta=document.createElement('p');meta.className='hx-meta';meta.innerHTML='<i></i>';h.after(meta);
  }
  var meta=c.querySelector(':scope>.hx-meta'),chip=c.querySelector(':scope>.mm-chip');
  if(chip&&meta){var sp=meta.querySelector('span');if(!sp){sp=document.createElement('span');meta.appendChild(sp)}var ct=chip.textContent.trim();if(sp.textContent!==ct)sp.textContent=ct}
  if(meta)meta.classList.toggle('hx-off',!meta.querySelector('span'));
  var tks=[].slice.call(c.querySelectorAll(':scope>.mm-take'));tks.forEach(function(t){c.after(t)});
  var all=[].slice.call(document.querySelectorAll('.mm-take'));if(all.length){var base=all.filter(function(t){return t.querySelector('.mm-chipx')})[0]||all[0];base.classList.add('hx-card');
    all.forEach(function(t){if(t===base)return;t.classList.remove('mm-take');t.classList.add('hx-sub');base.appendChild(t)});}
  var s=c.querySelector(':scope>.hx-side');if(s)badge(c,s);
}
run();document.addEventListener('DOMContentLoaded',run);window.addEventListener('load',run);[300,900,1600,2600,4000].forEach(function(t){setTimeout(run,t)});
})();