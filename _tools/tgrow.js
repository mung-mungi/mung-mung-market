// 목표주가 최근 변경: 시세 보드 한 줄 카드 모양으로 (사용자 2026-10-29)
(function(){function fx(){document.querySelectorAll('.rc-list>li').forEach(li=>{if(li.dataset.mk)return;li.dataset.mk=1;
const g=s=>li.querySelector(s);const nm=g('.l0 .nm')?.textContent||'',bd=g('.l0 .bdg'),dt=g('.l0 .dt')?.textContent||'',isnew=!!g('.newb');
const l2=g('.l2');const fm=l2?.querySelector('.fm')?.textContent||'';const pt=l2?.querySelector('.pt')?.textContent||'';const sp=[...(l2?.children||[])];const op=sp.find(x=>!x.className&&x.tagName==='SPAN')?.textContent||'';const up=l2?.querySelector('.dt')?.textContent.replace('상승여력','여력')||'';
const cm=g('.cm');const dn=li.classList.contains('r-dn');const pct=(bd?.textContent.match(/[+\-−]\d+%/)||[''])[0];const kind=(bd?.textContent||'').replace(/[▲▼⬆⬇🡅🡇]/g,'').replace(/[+\-−]\d+%/,'').replace('목표가','').replace(/[·\s]+$/,'').split('·')[0].trim();
const [a,b]=pt.split('→').map(x=>x&&x.trim());
const row=document.createElement('div');row.className='mk-row';
row.innerHTML=`<div class="mk-l"><b>${isnew?'<i class="mk-new">NEW</i>':''}${nm}</b><small>${fm} · ${op} · ${dt}</small></div><div class="mk-m"><span class="mk-old">${a||''}</span><b>${b||''}</b></div><div class="mk-r ${dn?'dn':'up'}"><b>${pct}</b><small>${kind}</small></div><span class="mk-ch">›</span>`;
li.textContent='';li.appendChild(row);if(cm){cm.classList.add('mk-cm');li.appendChild(cm)}
li.addEventListener('click',()=>li.classList.toggle('mk-open'));
})}
var k=0;(function go(){fx();if(!document.__tgmo){var l=document.getElementById('recent');if(l){document.__tgmo=1;new MutationObserver(function(){fx()}).observe(l,{childList:true,subtree:true})}}if(++k<10)setTimeout(go,500)})()})();

// 목표주가 순서: 최근 변경 → 기관별 목표가(코멘트) 블록 → 목표가 vs 현재가 → 평균 추세 → 찾기·지도·요약 (사용자 2026-10-29)
function __tgord(){
(function(){var w=document.querySelector('.pt-wrap'),rc=document.getElementById('recent');if(!w||!rc||w.dataset.ord)return;w.dataset.ord=1;
var $=function(i){return document.getElementById(i)};
var det=$('detail'),ctrl=det&&det.nextElementSibling,chips=$('chips'),tk=$('tk-sec');
var after=rc;[det,ctrl,chips,tk,$('vsprice'),$('trend'),$('overview')].forEach(function(e){if(e){after.after(e);after=e}});
var firm=$('firm-card'),lines=$('lines-card'),log=$('log-card'),mon=$('month-card');
if(tk&&firm&&lines){lines.before(firm);if(log)lines.after(log);if(mon&&log)log.after(mon)}
if(det)det.textContent='기관별 목표가 · 종목 고르기';
var nav=document.querySelector('.pt-nav');if(nav){var L=[['#recent','최근 변경'],['#detail','기관별 목표가'],['#vsprice','목표가 vs 현재가'],['#trend','평균 추세'],['#heat-card','상향 지도'],['#find-card','종목 찾기']];nav.innerHTML=L.map(function(x){return '<a href="'+x[0]+'">'+x[1]+'</a>'}).join('')}
})();
}
var __k=0;(function g(){try{__tgord()}catch(e){}if(++__k<8&&!(document.querySelector('.pt-wrap')||{dataset:{}}).dataset.ord)setTimeout(g,400)})();
