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
 // 한국: 대만처럼 네모칸(작은 월별 막대) 3열 — 반도체 수출·이번 달 잠정·메모리·시스템·SSD, 누르면 아래에 월별 표
 if(C.length){var mm={};M.forEach(function(r){mm[r.month]=r});C.sort(function(x,y){return x.month.localeCompare(y.month)});
  var pre=P.slice().sort(function(x,y){return (y.month||'').localeCompare(x.month||'')||((y.day_to||0)-(x.day_to||0))})[0];
  function svg(vals){var mx=Math.max.apply(null,vals.map(function(v){return Math.abs(v||0)}).concat([1]));var w=134,h=60,bw=w/vals.length;return '<svg width="100%" viewBox="0 0 '+w+' '+h+'"><line x1="0" x2="'+w+'" y1="'+(h-2)+'" y2="'+(h-2)+'" stroke="#e4e1d8"></line>'+vals.map(function(v,i){var hh=Math.max(2,Math.abs(v||0)/mx*(h-6));return '<rect x="'+(i*bw+1)+'" width="'+(bw-2)+'" y="'+(h-2-hh)+'" height="'+hh+'" rx="2" fill="'+((v||0)>=0?'#1a7f37':'#c62828')+'" opacity="'+(i===vals.length-1?.95:.55)+'"></rect>'}).join('')+'</svg>'}
  var last=C[C.length-1],lm=mm[last.month]||{};
  var items=[{n:'반도체 수출',r:'전체 · 월별',v:last.chip_yoy_pct,m:mlab(last.month)+' · '+n(last.chip_exports_usd_100m)+'억$',s:C.map(function(r){return r.chip_yoy_pct}),rows:C.map(function(r){return [r.month,r.chip_exports_usd_100m,r.chip_yoy_pct]})}];
  if(pre&&!C.some(function(r){return r.month===pre.month}))items.push({n:mlab(pre.month)+' 잠정',r:(pre.period||'')+' · 발표 '+(pre.released||'').slice(5).replace('-','/'),v:pre.chip_yoy_pct,m:n(pre.chip_exports_usd_100m)+'억$ · 반도체 비중 '+(pre.total_exports_usd_100m?(pre.chip_exports_usd_100m/pre.total_exports_usd_100m*100).toFixed(0)+'%':'—'),s:null,rows:null,pre:1});
  [['메모리','memory'],['시스템반도체','system'],['SSD','ssd']].forEach(function(o){var k1=o[1]+'_usd_100m',k2=o[1]+'_yoy_pct';items.push({n:o[0],r:'ICT 수출 · 월별',v:lm[k2],m:mlab(last.month)+' · '+n(lm[k1])+'억$',s:C.map(function(r){return (mm[r.month]||{})[k2]}),rows:C.map(function(r){var x=mm[r.month]||{};return [r.month,x[k1],x[k2]]})})});
  var s=document.createElement('section');s.className='sp-card';s.id='kr-table-card';
  s.innerHTML='<h3>한국 반도체 · 월별 수출</h3><p class="sub">삼성전자·SK하이닉스는 월매출을 내지 않아 매달 나오는 수출로 대신 봅니다. 막대 = 1년 전보다 몇 % 늘었나(12개월). 칸을 누르면 월별 숫자가 펼쳐집니다.</p><div class="sp-grid kr-grid">'+items.map(function(it,ix){return '<div class="sp-small kr-small'+(it.pre?' kr-pre':'')+'" role="button" tabindex="0" data-ix="'+ix+'"><div class="n">'+it.n+'</div><div class="r">'+it.r+'</div><div class="y '+((it.v||0)>=0?'up':'dn')+'">'+(it.v==null?'—':(it.v>=0?'+':'')+(+it.v).toFixed(1)+'%')+'</div><div class="m">'+it.m+'</div>'+(it.s?'<div class="kr-ch">'+svg(it.s.slice(-12))+'</div>':'<div class="kr-ch kr-note">월 중간 잠정치는 반도체 전체만 나옵니다</div>')+'</div>'}).join('')+'</div><div class="kr-detail" hidden></div>';
  tw.after(s);var det=s.querySelector('.kr-detail');
  s.querySelectorAll('.kr-small').forEach(function(b){b.addEventListener('click',function(){var it=items[+b.dataset.ix];var on=b.classList.contains('on');s.querySelectorAll('.kr-small').forEach(function(x){x.classList.remove('on')});if(on||!it.rows){det.hidden=true;return}b.classList.add('on');
   det.innerHTML='<p class="kr-dh">'+it.n+' · 월별</p><table class="sp-table"><thead><tr><th class="l">월</th><th>금액(억$)</th><th>전년 대비</th></tr></thead><tbody>'+it.rows.slice().reverse().map(function(r){return '<tr><td class="l">'+r[0].slice(2).replace('-','.')+'</td><td>'+n(r[1])+'</td><td class="'+((r[2]||0)>=0?'up':'dn')+'">'+(r[2]==null?'—':(r[2]>=0?'+':'')+(+r[2]).toFixed(1)+'%')+'</td></tr>'}).join('')+'</tbody></table>';det.hidden=false;det.scrollIntoView({block:'nearest',behavior:'smooth'})})})}
 var sub=document.getElementById('tw-table-sub');if(sub&&!/누르면/.test(sub.textContent))sub.textContent+=' 회사를 누르면 12개월 흐름이 펼쳐집니다.';
})})();
