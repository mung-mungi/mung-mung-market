// 방금 들어온 소식(사용자 2026-11-02) — GitHub 자동 수집(30분마다, 크레딧 0)이 'newsq' 가지에 쌓는 외신·공식 발표 제목을 뉴스 페이지 맨 위에 바로 보여 줌.
// 원문 제목(영어) 그대로 + 한글 분류 칩 + '로이터 외 n곳 · n분 전'. Claude 정리(2시간마다)가 올림/버림 판정하면 여기서 빠지고 타임라인으로 감.
(function(){try{
var PG=(location.pathname.split('/').pop()||'').replace(/\.html$/,'');if(PG!=='p-policy'&&PG!=='p-tech')return;
var URL='https://raw.githubusercontent.com/mung-mungi/mung-mung-market/newsq/newsq.json';
var EMO={'이란 전쟁·유가':'🛢 이란·유가','연준·정책':'🏦 연준','반도체 수출통제':'🚫 수출통제','AI 정책':'⚖️ AI 정책','관세·무역':'📦 관세','한국 관련':'🇰🇷 한미','AI·테크':'💻 AI·테크','공식 발표':'📣 공식 발표'};
function ago(t){var m=Math.max(0,Math.round((Date.now()/1e3-t)/60));return m<60?m+'분 전':Math.floor(m/60)+'시간 '+(m%60)+'분 전'}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function draw(d){var take=document.getElementById('take');if(!take||!d||!d.items)return;
 var now=Date.now()/1e3,L=d.items.filter(function(x){if(x.state&&x.state!=='new')return false;if(!x.major)return false;if(!x.title||x.title.length<15||/^[-–—]/.test(x.title))return false;if(now-x.t>12*3600)return false;var tech=x.cats.indexOf('AI·테크')>=0;return PG==='p-tech'?tech:x.cats.some(function(c){return c!=='AI·테크'})});
 L.sort(function(a,b){return (b.t-a.t)});
 var box=document.querySelector('.nq');if(!box){box=el('section','nq nq-col');take.after(box)}box.textContent='';
 var h=el('div','nq-h');h.appendChild(el('span','dot'));h.appendChild(el('span','','굵직한 새 소식'));h.appendChild(el('span','s','30분마다 · 확인 '+ago(Date.parse(d.at)/1e3)));box.appendChild(h);
 box.appendChild(el('div','nq-sub','외신 여러 곳이 같이 다루거나 공식 발표·합의·공습·관세·대형 거래처럼 판을 바꿀 사건만 · 기계 번역(아래 회색은 원문)'));
 if(!L.length){box.appendChild(el('div','nq-sub','지난 12시간 굵직한 새 소식 없음'));return}
 L.slice(0,20).forEach(function(x,i){var a=el('a','nq-r'+(i>=5?' x':''));a.href=x.link;a.target='_blank';a.rel='noopener';
  var m=el('div','nq-m');(x.cats||[]).filter(function(c){return PG==='p-tech'||c!=='AI·테크'}).slice(0,2).forEach(function(c){m.appendChild(el('span','nq-c',EMO[c]||c))});
  if(now-x.t<3600)m.appendChild(el('span','new','NEW'));
  m.appendChild(el('span','',(x.wraps>1?'시황 '+x.wraps+'건 중 최신 · ':'')+x.media+(x.n>1?' 외 '+(x.n-1)+'곳':'')+(x.paywall?' (유료)':'')+' · '+ago(x.t)));a.appendChild(m);a.appendChild(el('div','nq-t',x.title_ko||x.title));if(x.title_ko)a.appendChild(el('div','nq-o',x.title));box.appendChild(a)});
 if(L.length>5){var b=el('button','nq-more','더 보기 '+(Math.min(L.length,20)-5)+'건 ▾');b.type='button';b.onclick=function(){var c=box.classList.toggle('nq-col');b.textContent=c?'더 보기 '+(Math.min(L.length,20)-5)+'건 ▾':'접기 ▴'};box.appendChild(b)}}
function load(){fetch(URL+'?t='+Math.floor(Date.now()/12e4)).then(function(r){return r.ok?r.json():null}).then(function(d){var k=0;(function t(){if(document.getElementById('take'))draw(d);else if(++k<30)setTimeout(t,300)})()}).catch(function(){})}
load();setInterval(load,5*60*1000);
}catch(e){}})();
