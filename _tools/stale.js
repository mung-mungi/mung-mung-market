// 오래된 자료 경고 칩(사용자 2026-11-02) — 맨 위 날짜 칩의 기준일이 정해진 영업일 수보다 밀리면 '⚠ n영업일 전 자료'
// 페이지마다 허용치가 다름(주간·월간 자료는 넉넉히). 목록에 없는 페이지는 건드리지 않음.
(function(){
var LIM={'p-opt.html':2,'p-value.html':2,'p-pros.html':3,'p-econ.html':3,'p-fx.html':7,'p-insider.html':8,'p-capex.html':0,'p-short.html':0};
var F=location.pathname.split('/').pop()||'index.html',N=LIM[F];if(!N)return;
function pd(t){var y=new Date().getFullYear(),m,d,a;
 if(a=t.match(/(20\d\d)-(\d{1,2})-(\d{1,2})/)){y=+a[1];m=+a[2];d=+a[3]}
 else if(a=t.match(/(\d{1,2})월\s*(\d{1,2})일/)){m=+a[1];d=+a[2]}
 else if(a=t.match(/(?:^|[^\d.])(\d{1,2})\.(\d{1,2})(?![\d.])/)){m=+a[1];d=+a[2]}
 else return null;var x=new Date(y,m-1,d);if(x-new Date()>5*864e5)x=new Date(y-1,m-1,d);return x}
function wk(x){var g=x.getDay();return g>0&&g<6}
// 기대 기준일: 한국 시간으로 오늘 이전의 마지막 평일(미국 마감 기준)
function bdays(x){var e=new Date();e.setHours(0,0,0,0);e.setDate(e.getDate()-1);while(!wk(e))e.setDate(e.getDate()-1);var n=0,c=new Date(x);c.setHours(0,0,0,0);while(c<e){c.setDate(c.getDate()+1);if(wk(c))n++}return n}
function run(){var t=document.getElementById('take')||document.querySelector('.pg-take');var c=t&&t.querySelector('b.mm-chipx');if(!c)return false;if(c.nextElementSibling&&c.nextElementSibling.classList.contains('mm-stale'))return true;
 var x=pd(c.textContent);if(!x)return true;var n=bdays(x);if(n<N)return true;
 var s=document.createElement('span');s.className='mm-stale';s.textContent='⚠ '+n+'영업일 전 자료';s.title='자동 갱신이 밀렸습니다. 최신 값과 다를 수 있습니다.';c.after(s);if(s.offsetTop>c.offsetTop+6)s.style.marginLeft='0';return true}
var k=0;(function go(){var ok;try{ok=run()}catch(e){ok=false}if(++k<20&&!ok)setTimeout(go,400);else if(k<20)setTimeout(go,1500)})();
var st=document.createElement('style');st.textContent='.mm-stale{display:inline-block;margin:4px 0 4px 6px;vertical-align:middle;font:800 12.5px/1.5 -apple-system,"Apple SD Gothic Neo",sans-serif;color:#b3261e;background:#fbe8e5;border:1px solid #f1c2bb;border-radius:999px;padding:1px 10px}';document.head.appendChild(st);
})();
