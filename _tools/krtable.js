// 아시아 반도체 수출: 대만 월매출표처럼 '한국 월별 수출표' 추가(사용자 2026-10-29) — 한국 회사는 월매출을 내지 않아 월별 수출로 대신 봄
(function(){if(document.getElementById('kr-table-card'))return;var tw=document.getElementById('tw-table-card');if(!tw)return;
function j(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.ok?r.json():[]}).catch(function(){return []})}
function rows(d){return Array.isArray(d)?d:(d&&d.rows)||[]}
function pc(v){if(v==null||isNaN(v))return '<td class="mu">—</td>';return '<td class="'+(v>=0?'up':'dn')+'">'+(v>=0?'+':'')+(+v).toFixed(1)+'%</td>'}
function n(v){return v==null||isNaN(v)?'—':(+v).toLocaleString('en-US',{maximumFractionDigits:1})}
Promise.all([j('d/supply/kr_chip_exports.json'),j('d/supply/kr_memory_exports.json'),j('d/supply/kr_prelim.json')]).then(function(a){var C=rows(a[0]),M=rows(a[1]),P=rows(a[2]);if(!C.length)return;
 var mm={};M.forEach(function(r){mm[r.month]=r});C.sort(function(x,y){return y.month.localeCompare(x.month)});
 var pre=P.slice().sort(function(x,y){return (y.month||'').localeCompare(x.month||'')||((y.day_to||0)-(x.day_to||0))})[0];
 var tr='';if(pre&&!C.some(function(r){return r.month===pre.month})){tr+='<tr class="kr-pre"><td class="l"><b>'+(+pre.month.slice(5))+'월</b><small>'+(pre.period||'').replace(/^\d+월\s*/,'')+' 잠정</small></td><td>'+n(pre.chip_exports_usd_100m)+'</td>'+pc(pre.chip_yoy_pct)+'<td class="mu">—</td><td class="mu">—</td><td class="mu">—</td></tr>'}
 C.forEach(function(r){var m=mm[r.month]||{};tr+='<tr><td class="l"><b>'+r.month.slice(2).replace('-','.')+'</b></td><td>'+n(r.chip_exports_usd_100m)+'</td>'+pc(r.chip_yoy_pct)+pc(m.memory_yoy_pct)+pc(m.system_yoy_pct)+pc(m.ssd_yoy_pct)+'</tr>'});
 var s=document.createElement('section');s.className='sp-card';s.id='kr-table-card';
 s.innerHTML='<h3>최근 월 수출표 · 한국 반도체</h3><p class="sub">삼성전자·SK하이닉스는 월매출을 내지 않아, 매달 나오는 반도체 수출로 대신 봅니다(억 달러, 전년 대비 %).</p><div class="sp-tbox"><table class="sp-table" id="kr-table"><thead><tr><th class="l">월</th><th>반도체 수출</th><th>전년 대비</th><th>메모리</th><th>시스템</th><th>SSD</th></tr></thead><tbody>'+tr+'</tbody></table></div>';
 tw.after(s)})})();
