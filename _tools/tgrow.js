(function(){try{fetch('d/prices/prices.json?t='+Math.floor(Date.now()/3e5)).then(function(r){return r.ok?r.json():null}).then(function(P){if(!P)return;var m={};P.forEach(function(x){if(x.price!=null)m[String(x.name).trim()]=x.price});window.__mmPX=m;document.querySelectorAll('.rc-list .mk-row').forEach(function(r){var mm=r.querySelector('.mk-m');if(!mm||mm.querySelector('.mk-now'))return;var nmEl=r.querySelector('.mk-l b');if(!nmEl)return;var t=nmEl.cloneNode(true);t.querySelectorAll('i').forEach(function(i){i.remove()});var nm=t.textContent.trim();if(m[nm]==null)return;var q=document.createElement('small');q.className='mk-now';q.textContent='현재 $'+(m[nm]>=100?m[nm].toFixed(0):m[nm].toFixed(1));mm.appendChild(q)})}).catch(function(){})}catch(e){}})();
// 목표주가 최근 변경: 시세 보드 한 줄 카드 모양으로 (사용자 2026-10-29)
(function(){function fx(){document.querySelectorAll('.rc-list>li').forEach(li=>{if(li.dataset.mk)return;li.dataset.mk=1;
const g=s=>li.querySelector(s);const nm=g('.l0 .nm')?.textContent||'',bd=g('.l0 .bdg'),dt=g('.l0 .dt')?.textContent||'',isnew=!!g('.newb');
const l2=g('.l2');const fm=l2?.querySelector('.fm')?.textContent||'';const pt=l2?.querySelector('.pt')?.textContent||'';const sp=[...(l2?.children||[])];const op=sp.find(x=>!x.className&&x.tagName==='SPAN')?.textContent||'';const up=l2?.querySelector('.dt')?.textContent.replace('상승여력','여력')||'';
const cm=g('.cm');const dn=li.classList.contains('r-dn');const pct=(bd?.textContent.match(/[+\-−]\d+%/)||[''])[0];const kind=(bd?.textContent||'').replace(/[▲▼⬆⬇🡅🡇]/g,'').replace(/[+\-−]\d+%/,'').replace('목표가','').replace(/[·\s]+$/,'').split('·')[0].trim();
const [a,b]=pt.split('→').map(x=>x&&x.trim());
const row=document.createElement('div');row.className='mk-row';
/* 투자의견 변경 표시(사용자 2026-11-09 '의견은 좋아졌는데 목표가는 낮아지는 경우') */
const RK=x=>/강력매수|강력 매수/.test(x)?3:/매수|비중확대|아웃퍼폼|시장수익률 상회|긍정/.test(x)?2:/중립|보유|시장수익률|동일비중|홀드/.test(x)?1:/매도|비중축소|언더퍼폼/.test(x)?0:-1;
const [rf,rt]=op.includes('→')?op.split('→').map(x=>x.trim()):[null,op];const rd=rf&&RK(rf)>=0&&RK(rt)>=0?Math.sign(RK(rt)-RK(rf)):0;
const pv=parseFloat((pct||'0').replace('−','-'));const mix=rd&&pv&&Math.sign(pv)!==rd;
const opH=rd?`<i class="mk-rt ${rd>0?'up':'dn'}">의견 ${rd>0?'⬆':'⬇'} ${rf}→${rt}</i>`:(op||'');
if(rd)li.dataset.rt=rd>0?'up':'dn';
row.innerHTML=`<div class="mk-l"><b>${isnew?'<i class="mk-new">NEW</i>':''}${nm}${mix?`<i class="mk-mix">의견${rd>0?'↑':'↓'} 목표가${pv>0?'↑':'↓'}</i>`:''}</b><small>${fm} · ${opH} · ${dt}</small></div><div class="mk-m"><span class="mk-old">${a||''}</span><b>${b||''}</b></div><div class="mk-r ${dn?'dn':'up'}"><b>${pct}</b><small>${kind}</small></div><span class="mk-ch">›</span>`;
li.textContent='';li.appendChild(row);/* 현재가 한 줄(사용자 2026-11-09 '현재가도') — 시세 보드 자료 이름으로 찾음 */try{var PX=window.__mmPX;if(PX&&PX[nm.trim()]!=null){var mm=row.querySelector('.mk-m'),q=document.createElement('small');q.className='mk-now';var pv0=PX[nm.trim()],tg=parseFloat(String(b||'').replace(/[^\d.]/g,''));q.textContent='현재 $'+(pv0>=100?pv0.toFixed(0):pv0.toFixed(1));if(tg&&pv0){var gap=Math.round((tg/pv0-1)*100);q.title='목표가까지 '+(gap>0?'+':'')+gap+'%'}mm.appendChild(q)}}catch(e){}if(cm){cm.classList.add('mk-cm');li.appendChild(cm)}
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

// '의견 바뀐 것만' 버튼(사용자 2026-11-09)
(function(){var k=0;(function g(){var h=document.querySelector('#recent .rc-head'),ul=document.getElementById('recent-list');if(h&&ul&&!h.querySelector('.mk-rtf')){var b=document.createElement('button');b.type='button';b.className='fchip mk-rtf';b.textContent='의견 바뀐 것만';b.onclick=function(){var on=!ul.classList.contains('rt-only');if(on){var more=document.getElementById('recent-more');if(more&&!ul.classList.contains('open')&&more.offsetParent)more.click()}ul.classList.toggle('rt-only',on);b.setAttribute('aria-pressed',on)};var ref=h.querySelector('#recent-more-top');h.insertBefore(b,ref||null);return}if(++k<20)setTimeout(g,500)})()})();
