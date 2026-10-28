// 아시아 반도체 수출: 대만 월매출표·한국 월별 수출표를 같은 한 줄 카드로, 누르면 자세히(사용자 2026-10-29)
(function(){if(document.getElementById('kr-table-card'))return;var tw=document.getElementById('tw-table-card');if(!tw)return;
function j(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.ok?r.json():[]}).catch(function(){return []})}
function rows(d){return Array.isArray(d)?d:(d&&d.rows)||[]}
function n(v,d){return v==null||isNaN(v)?'—':(+v).toLocaleString('en-US',{maximumFractionDigits:d==null?1:d})}
function p(v){return v==null||isNaN(v)?'<span class="mu">—</span>':'<span class="'+(v>=0?'up':'dn')+'">'+(v>=0?'+':'')+(+v).toFixed(1)+'%</span>'}
function mlab(m){return (+m.slice(5))+'월'}
function bars(list){var mx=Math.max.apply(null,list.map(function(x){return Math.abs(x.v||0)}).concat([1]));return '<div class="ar-bars">'+list.map(function(x){var h=Math.max(3,Math.round(Math.abs(x.v||0)/mx*40));return '<span title="'+x.k+' '+(x.v==null?'—':x.v.toFixed(1)+'%')+'"><i class="'+((x.v||0)>=0?'up':'dn')+'" style="height:'+h+'px"></i><em>'+x.k+'</em></span>'}).join('')+'</div>'}
function row(o){return '<div class="ar-row" role="button" tabindex="0"><div class="ar-l"><b>'+o.name+'</b><small>'+o.sub+'</small></div><div class="ar-m"><small>'+o.mk+'</small><b>'+o.mv+'</b></div><div class="ar-r"><b>'+o.r+'</b><small>'+o.rs+'</small></div><span class="ar-ch">›</span></div><div class="ar-x">'+o.x+'</div>'}
function wire(box){box.querySelectorAll('.ar-row').forEach(function(r){r.addEventListener('click',function(){r.parentElement.classList.toggle('op')})})}
function wrap(h){var d=document.createElement('div');d.className='ar-list';d.innerHTML=h.map(function(x){return '<div class="ar-it">'+x+'</div>'}).join('');wire(d);return d}
Promise.all([j('d/supply/kr_chip_exports.json'),j('d/supply/kr_memory_exports.json'),j('d/supply/kr_prelim.json'),j('d/supply/tw_revenue.json')]).then(function(a){
 var C=rows(a[0]),M=rows(a[1]),P=rows(a[2]),T=rows(a[3]);
 // 대만
 if(T.length){var by={};T.forEach(function(r){(by[r.company]=by[r.company]||[]).push(r)});var cos=Object.keys(by).map(function(k){var l=by[k].sort(function(x,y){return x.month.localeCompare(y.month)});return l}).sort(function(x,y){return (x[0].order||0)-(y[0].order||0)});
  var H=cos.map(function(l){var z=l[l.length-1];var last12=l.slice(-12);
   var x=bars(last12.map(function(r){return {k:mlab(r.month),v:r.yoy_pct}}))+'<div class="ar-kv"><span>전월 대비 '+p(z.mom_pct)+'</span><span>매출 '+n(z.revenue_ntd_100m)+'억 대만달러</span><span>12개월 중 최고 '+(z.revenue_ntd_100m>=Math.max.apply(null,last12.map(function(r){return r.revenue_ntd_100m||0}))?'<b class="up">이번 달</b>':'아님')+'</span></div><p class="ar-cap">막대 = 달마다 1년 전보다 몇 % 늘었나</p>';
   return row({name:z.company,sub:z.role+' · '+mlab(z.month),mk:'매출(억 NT$)',mv:n(z.revenue_ntd_100m,0),r:p(z.yoy_pct),rs:'전년 대비',x:x})});
  var t=tw.querySelector('.sp-tbox');if(t){t.classList.add('ar-hide');t.after(wrap(H))}}
 // 한국
 if(C.length){var mm={};M.forEach(function(r){mm[r.month]=r});C.sort(function(x,y){return y.month.localeCompare(x.month)});
  var pre=P.slice().sort(function(x,y){return (y.month||'').localeCompare(x.month||'')||((y.day_to||0)-(x.day_to||0))})[0];var H2=[];
  if(pre&&!C.some(function(r){return r.month===pre.month}))H2.push(row({name:mlab(pre.month)+' <i class="ar-pre">잠정</i>',sub:(pre.period||'')+' · 발표 '+(pre.released||'').slice(5).replace('-','/'),mk:'반도체 수출',mv:n(pre.chip_exports_usd_100m)+'억$',r:p(pre.chip_yoy_pct),rs:'전년 대비',x:'<div class="ar-kv"><span>전체 수출 '+n(pre.total_exports_usd_100m)+'억$</span><span>반도체 비중 '+(pre.total_exports_usd_100m?(pre.chip_exports_usd_100m/pre.total_exports_usd_100m*100).toFixed(0)+'%':'—')+'</span><span>조업일수 '+(pre.workdays||'—')+'일(작년 '+(pre.workdays_prev||'—')+'일)</span></div><p class="ar-cap">월 중간 잠정치는 반도체 전체만 나옵니다.</p>'}));
  C.forEach(function(r){var m=mm[r.month]||{};H2.push(row({name:r.month.slice(2).replace('-','.'),sub:'메모리 '+(m.memory_yoy_pct!=null?(m.memory_yoy_pct>=0?'+':'')+m.memory_yoy_pct.toFixed(0)+'%':'—'),mk:'반도체 수출',mv:n(r.chip_exports_usd_100m)+'억$',r:p(r.chip_yoy_pct),rs:'전년 대비',
   x:'<div class="ar-grid"><div><small>메모리</small><b>'+n(m.memory_usd_100m)+'억$</b>'+p(m.memory_yoy_pct)+'</div><div><small>시스템반도체</small><b>'+n(m.system_usd_100m)+'억$</b>'+p(m.system_yoy_pct)+'</div><div><small>SSD</small><b>'+n(m.ssd_usd_100m)+'억$</b>'+p(m.ssd_yoy_pct)+'</div></div><div class="ar-kv"><span>전체 수출 '+n(r.total_exports_usd_100m)+'억$</span><span>반도체 비중 '+(r.total_exports_usd_100m?(r.chip_exports_usd_100m/r.total_exports_usd_100m*100).toFixed(0)+'%':'—')+'</span></div>'}))});
  var s=document.createElement('section');s.className='sp-card';s.id='kr-table-card';s.innerHTML='<h3>최근 월 수출표 · 한국 반도체</h3><p class="sub">삼성전자·SK하이닉스는 월매출을 내지 않아 매달 나오는 반도체 수출로 대신 봅니다. 줄을 누르면 메모리·시스템·SSD가 펼쳐집니다.</p>';
  var L=wrap(H2);L.classList.add('ar-long');s.appendChild(L);tw.after(s)}
 var sub=document.getElementById('tw-table-sub');if(sub&&!/누르면/.test(sub.textContent))sub.textContent+=' 회사를 누르면 12개월 흐름이 펼쳐집니다.';
})})();
