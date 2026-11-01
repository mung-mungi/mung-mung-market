// 정책·지정학 순서·일정 미리보기(사용자 2026-11-01): 오늘 한눈에 → 타임라인 → 다가오는 일정(3줄 + 펼치기) → 나머지
(function(){
function ord(){var tl=document.getElementById('tl-sec'),up=document.getElementById('up-sec'),ti=document.getElementById('tiles');if(!tl||!up||!ti)return;
 if(tl.compareDocumentPosition(ti)&Node.DOCUMENT_POSITION_FOLLOWING&&up.previousElementSibling===tl)return;ti.before(tl);ti.before(up)}
function fold(){var u=document.getElementById('up');if(!u)return;var it=[...u.querySelectorAll(':scope>.pg-upi')];var b=u.parentElement.querySelector('.mm-pf');
 if(it.length<=3){if(b)b.remove();u.classList.remove('mm-pfc');return}
 if(b&&b.dataset.n==it.length)return;if(b)b.remove();
 var open=u.classList.contains('mm-pfo');u.classList.add('mm-pfc');var h3=Math.round(it[2].getBoundingClientRect().bottom-u.getBoundingClientRect().top+2);if(h3<60)return;u.style.setProperty('--h3',h3+'px');
 b=document.createElement('button');b.type='button';b.className='mm-pf';b.dataset.n=it.length;
 var set=function(){b.textContent=u.classList.contains('mm-pfo')?'접기 ▴':'일정 '+(it.length-3)+'건 더 보기 ▾';u.style.maxHeight=u.classList.contains('mm-pfo')?u.scrollHeight+'px':'var(--h3)'};
 b.onclick=function(){u.classList.toggle('mm-pfo');set()};u.after(b);set()}
function run(){try{ord()}catch(e){}try{fold()}catch(e){}}
var k=0;(function go(){run();if(++k<15)setTimeout(go,400)})();
var u=document.getElementById('up');if(u&&window.MutationObserver){var t;new MutationObserver(function(){clearTimeout(t);t=setTimeout(run,100)}).observe(u,{childList:true})}
})();
// 맨 위 종합 3줄(사용자 2026-11-01) — 정책·지정학(d/policy)과 테크 행사(d/tech) 공용: 지금 판(사람이 쓴 headline) · 시장은(유가·금리·심리·경고등 자동) · 다음 관문(일정 자동, D-day)
(function(){var TECH=/p-tech/.test(location.pathname),D={};function j(u){return fetch(u+'?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
function md(d){var a=String(d).split('-');return (+a[1])+'/'+(+a[2])}
var WD=['일','월','화','수','목','금','토'];
function dd(d){var t=new Date(Date.now()+9*3600e3);var a=Date.UTC(t.getUTCFullYear(),t.getUTCMonth(),t.getUTCDate()),p=d.split('-'),b=Date.UTC(+p[0],+p[1]-1,+p[2]);return Math.round((b-a)/864e5)}
function wd(d){var p=d.split('-');return WD[new Date(Date.UTC(+p[0],+p[1]-1,+p[2])).getUTCDay()]}
function draw(){var t=document.querySelector('#take.pg-take');if(!t||!D.ev||t.querySelector('.pg3'))return;var hl=t.querySelector('[data-field=headline]');if(!hl||!hl.textContent.trim())return;
 var ul=document.createElement('ul');ul.className='pg3';
 function row(k,html,cls){var li=document.createElement('li');if(cls)li.className=cls;var i=document.createElement('i');i.textContent=k;li.appendChild(i);var s=document.createElement('span');s.innerHTML=html;li.appendChild(s);ul.appendChild(li);return li}
 var h=hl.textContent.trim();row('지금 판',h.replace(/</g,'&lt;'));
 var m=[];if(TECH&&D.st&&D.st.sectors){[['SOXX','반도체'],['XLK','기술']].forEach(function(a){var x=D.st.sectors.filter(function(z){return z.t===a[0]})[0];if(x)m.push('<b class="'+(x.d1<=-2?'hot':x.d1>=2?'up':'')+'">'+a[1]+' 하루 '+(x.d1>0?'+':'')+x.d1+'% · 1달 '+(x.m1>0?'+':'')+x.m1+'%</b>')})}
 if(!TECH&&D.oil&&D.oil.length){var w=D.oil[D.oil.length-1].wti;m.push('<b class="'+(w>=100?'hot':'')+'">WTI '+Math.round(w)+'달러</b>')}
 if(!TECH&&D.y&&D.y.length){var y=D.y[D.y.length-1];m.push('<b class="'+(y.us10y>=4.9?'hot':'')+'">10년물 '+y.us10y.toFixed(2)+'%</b>')}
 if(D.f&&D.f.fng){var s=Math.round(D.f.fng.score);m.push('<b class="'+(s<45?'cold':'')+'">공포·탐욕 '+s+(s<25?' 극단 공포':s<45?' 공포':s<55?' 중립':' 탐욕')+'</b>')}
 if(D.l&&D.l.stage)m.push('<a href="p-lights.html">경고등 '+D.l.stage+(D.l.score!=null?' '+D.l.score.toFixed(1)+'점':'')+' ›</a>');
 if(m.length)row('시장은',m.join('<em>·</em>'),'mk');
 var up=D.ev.filter(function(e){return e.date&&dd(e.date)>=0&&e.status!=='발생'}).sort(function(a,b){return a.date<b.date?-1:1}).slice(0,3);
 if(up.length){var r=row(TECH?'다음 행사':'다음 관문',up.map(function(e){var n=dd(e.date);return '<span class="gt"><em class="'+(n<=3?'soon':'')+'">'+(n===0?'오늘':'D-'+n)+'</em>'+md(e.date)+'('+wd(e.date)+') '+e.title.split(' — ')[0].replace(/</g,'&lt;')+'</span>'}).join(''),'gate');r.onclick=function(){var u=document.getElementById('up-sec');if(u)u.scrollIntoView({behavior:'smooth',block:'start'})}}
 hl.style.display='none';var o=t.querySelector('.tg3');if(o)o.style.display='none';t.classList.remove('tg-rows');t.appendChild(ul);t.classList.add('pg3-on')}
var B=TECH?'d/tech/':'d/policy/';Promise.all([j(B+'events.json'),j('d/lights/oil.json'),j('d/bond/yields_daily.json'),j('d/fng.json'),j('d/lights/fresh.json'),TECH?j('d/stress/stress.json'):null]).then(function(a){D={ev:a[0],oil:a[1],y:a[2],f:a[3],l:a[4],st:a[5]};var k=0;(function go(){try{draw()}catch(e){}if(++k<30)setTimeout(go,400)})();var tk=document.getElementById('take');if(tk&&window.MutationObserver)new MutationObserver(function(){if(!tk.querySelector('.pg3'))try{draw()}catch(e){}}).observe(tk,{childList:true})})})();
