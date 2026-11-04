// 미국 중간선거 개표 지도(사용자 2026-11-04 — 오늘·내일만): 메인 맨 위 = 캠퍼스 지도 + 주별 개표 색(상원·하원 전환)
// 네오클라우드 페이지 = 기존 캠퍼스 지도의 '🗳 개표 현황' 버튼이 같은 색으로 칠함. 자료: d/election/live.json, 바탕: d/election/basemap.json
(function(){try{
var main=/\/(index\.html)?$/.test(location.pathname),neo=/p-neo\.html$/.test(location.pathname);if(!main&&!neo)return;
var css='.el-card{margin:10px 0 14px;background:#fff;border:1px solid #e3d6bd;border-radius:16px;padding:12px 12px 10px;box-shadow:0 3px 0 #ece2cc;color:#1d1a16}'+
'.el-card h2{font-size:18px;margin:0;line-height:1.35}.el-card .sub{font-size:12.5px;color:#6b6458;margin:2px 0 8px}'+
'.el-seat{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:0 0 8px}.el-seat>div{border:1px solid #eadfc8;border-radius:12px;padding:7px 9px}.el-seat .h{font-size:12.5px;font-weight:800;color:#6b6458}.el-seat .n{font-size:17px;font-weight:900;font-variant-numeric:tabular-nums}.el-seat .s{font-size:11.5px;color:#6b6458}'+
'.el-d{color:#2457a6}.el-r{color:#b8322a}'+
'.el-tabs{display:flex;gap:6px;margin:0 0 6px}.el-tabs button{flex:1;padding:8px 0;border-radius:999px;border:1px solid #d9cdb8;background:#fffaf2;box-shadow:0 2px 0 #e4d8c3;font:inherit;font-size:14px;font-weight:800;color:#5b5246}.el-tabs button.on{background:#1d1a16;color:#fff;border-color:#1d1a16;box-shadow:none}'+
'.el-svg svg{display:block;width:100%;height:auto}.el-svg .nat{fill:none;stroke:#8a7f6c;stroke-width:1}.el-svg .sts{fill:none;stroke:#fff;stroke-width:.8}'+
'.el-lg{display:flex;flex-wrap:wrap;gap:3px 10px;font-size:12px;color:#5b5246;margin:6px 0 2px}.el-lg i{display:inline-block;width:11px;height:11px;border-radius:3px;vertical-align:-1px;margin-right:3px}'+
'.el-top{font-size:13px;color:#4a4339;line-height:1.55;margin:4px 0 0}.el-top b{color:#1d1a16}.el-more{display:block;text-align:right;font-size:12.5px;font-weight:800;color:#2f5f7a;text-decoration:none;margin-top:4px}'+
'.cp-livenote{font-size:13.5px;color:#4a4339;margin:6px 2px 0;line-height:1.55}.cp-livenote b{color:#1d1a16}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function e(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var F={"AL":"01","AK":"02","AZ":"04","AR":"05","CA":"06","CO":"08","CT":"09","DE":"10","DC":"11","FL":"12","GA":"13","HI":"15","ID":"16","IL":"17","IN":"18","IA":"19","KS":"20","KY":"21","LA":"22","ME":"23","MD":"24","MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30","NE":"31","NV":"32","NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37","ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44","SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50","VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"},ID={};for(var k in F)ID[F[k]]=k;
var K={"VA":"버지니아","TX":"텍사스","CA":"캘리포니아","IL":"일리노이","GA":"조지아","OH":"오하이오","AZ":"애리조나","NY":"뉴욕","PA":"펜실베이니아","OR":"오리건","IN":"인디애나","FL":"플로리다","WA":"워싱턴","IA":"아이오와","NC":"노스캐롤라이나","MO":"미주리","MN":"미네소타","MI":"미시간","NV":"네바다","NJ":"뉴저지","TN":"테네시","CO":"콜로라도","MD":"메릴랜드","WI":"위스콘신","CT":"코네티컷"};
var C={Dw:'#2f62b5',Dl:'#a9c4ec',Rw:'#c0392b',Rl:'#f0b2aa',N:'#ece8df'};
// 주 하나의 상태: mode 's' = 상원(없으면 주지사), 'h' = 하원(주 안 확정 의석 많은 쪽)
function stat(x,mode){x=x||{};if(mode==='h'){var h=x.house||{},d=+h.D||0,r=+h.R||0,t=+h.total||0;if(!d&&!r)return{c:C.N,t:'하원 미정'};var p=d>r?'D':r>d?'R':'';var all=t&&d+r>=t;
  return{c:p?C[p+(all?'w':'l')]:'#d9d3c6',t:'하원 민주 '+d+' · 공화 '+r+(t?' / '+t+'석':'')+(all?' (전 의석 확정)':' (확정분)')}}
 if(x.lead!=='D'&&x.lead!=='R')return{c:C.N,t:(x.race||'')+' 미정'};return{c:C[x.lead+(x.called?'w':'l')],t:(x.race||'')+' '+(x.lead==='D'?'민주':'공화')+(x.called?' 확정':' 앞섬')}}
function lg(mode){return'<span><i style="background:'+C.Dw+'"></i>민주 확정</span><span><i style="background:'+C.Dl+'"></i>민주 '+(mode==='h'?'많음(일부 확정)':'앞섬')+'</span><span><i style="background:'+C.Rw+'"></i>공화 확정</span><span><i style="background:'+C.Rl+'"></i>공화 '+(mode==='h'?'많음(일부 확정)':'앞섬')+'</span><span><i style="background:'+C.N+'"></i>미정</span><span><i style="background:#e07b16;border-radius:50%"></i>데이터센터 캠퍼스</span>'}
function top(M,mode){return Object.keys(M).sort(function(a,b){return(M[b].dc||0)-(M[a].dc||0)}).slice(0,8).map(function(k){return'<b>'+(K[k]||k)+'</b> '+stat(M[k],mode).t.replace(/^\s+/,'')}).join(' · ')}
function seat(x,n){x=x||{};return'<div><div class="h">'+n+' (과반 '+e(x.needed)+')</div><div class="n"><span class="el-d">민주 '+e(x.D==null?'–':x.D)+'</span> · <span class="el-r">공화 '+e(x.R==null?'–':x.R)+'</span></div><div class="s">'+(x.called?'✅ AP 확정: '+e(x.called)+' 다수당':'다수당 미정')+'</div></div>'}
var J=fetch('d/election/live.json?t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()});
if(main)Promise.all([J,fetch('d/election/basemap.json',{cache:'force-cache'}).then(function(r){return r.json()})]).then(function(a){var j=a[0],B=a[1],M=(j.map||{}).states||{};
 if(j.ended||Date.now()>Date.parse('2026-11-06T12:00:00+09:00'))return;var mode='s';
 var box=document.createElement('section');box.className='el-card';box.id='election';
 var dots=B.dots.map(function(d){return d[3]==='none'?'<circle cx="'+d[0]+'" cy="'+d[1]+'" r="'+d[2]+'" fill="none" stroke="#16181a" stroke-width="1.5" stroke-dasharray="3 3" vector-effect="non-scaling-stroke"/>':'<circle cx="'+d[0]+'" cy="'+d[1]+'" r="'+d[2]+'" fill="'+d[3]+'" fill-opacity="'+d[5]+'" stroke="#fff" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'}).join('');
 var paths=Object.keys(B.states).map(function(id){return'<path data-id="'+id+'" d="'+B.states[id]+'"><title></title></path>'}).join('');
 box.innerHTML='<h2>🗳 미국 중간선거 개표 × 데이터센터 지도</h2><p class="sub">'+e(j.updated_label||'')+' · 10분마다 갱신 · AP 확정만 진하게, 예측·여론조사 없음</p>'+
  '<div class="el-seat">'+seat(j.senate,'상원')+seat(j.house,'하원')+'</div><div class="el-tabs"><button type="button" data-m="s" class="on">상원(없으면 주지사)</button><button type="button" data-m="h">하원</button></div>'+
  '<div class="el-svg"><svg viewBox="'+B.vb+'" role="img" aria-label="주별 개표와 데이터센터 캠퍼스"><g class="pol">'+paths+'</g><path class="sts" d="'+B.sts+'"/><path class="nat" d="'+B.nat+'"/><g>'+dots+'</g></svg></div>'+
  '<div class="el-lg"></div><p class="el-top"></p><a class="el-more" href="p-neo.html#cp-map">캠퍼스별 자세히 보기 ›</a>';
 function paint(){box.querySelectorAll('g.pol path').forEach(function(p){var k=ID[p.getAttribute('data-id')],s=stat(M[k],mode);p.setAttribute('fill',s.c);p.firstChild.textContent=(K[k]||k)+' · '+s.t});
  box.querySelector('.el-lg').innerHTML=lg(mode);box.querySelector('.el-top').innerHTML='데이터센터 많은 주: '+top(M,mode);
  box.querySelectorAll('.el-tabs button').forEach(function(b){b.classList.toggle('on',b.dataset.m===mode)})}
 box.querySelectorAll('.el-tabs button').forEach(function(b){b.onclick=function(){mode=b.dataset.m;paint()}});paint();
 var w=document.querySelector('.wrap')||document.body,h=w.querySelector('header,.mm-hero,.nl-rail');(h&&h.parentNode===w)?w.insertBefore(box,h.nextSibling):w.insertBefore(box,w.firstChild)}).catch(function(){});
if(neo)J.then(function(j){var M=(j.map||{}).states||{},n=0,mode='s';(function wait(){var ps=document.querySelectorAll('#cp-map g.pol path[data-id]');if(!ps.length){if(n++<60)setTimeout(wait,500);return}
 var b=document.getElementById('cp-pol'),pl=document.getElementById('cp-pleg');if(!b)return;var ln=document.createElement('div');ln.className='cp-livenote';ln.hidden=true;(pl||b).after(ln);
 function paint(){ps.forEach(function(p){var k=ID[p.getAttribute('data-id')],s=stat(M[k],mode);p.setAttribute('fill',s.c);var t=p.querySelector('title')||p.appendChild(document.createElementNS('http://www.w3.org/2000/svg','title'));t.textContent=(K[k]||k)+' · '+s.t});
  if(pl)pl.innerHTML=lg(mode).replace('데이터센터 캠퍼스','캠퍼스');ln.innerHTML='<div class="el-tabs"><button type="button" data-m="s"'+(mode==='s'?' class="on"':'')+'>상원(없으면 주지사)</button><button type="button" data-m="h"'+(mode==='h'?' class="on"':'')+'>하원</button></div><b>11월 중간선거 개표 · '+e(j.updated_label||'')+'</b><br>데이터센터 많은 주: '+top(M,mode);
  ln.querySelectorAll('button').forEach(function(x){x.onclick=function(){mode=x.dataset.m;paint()}})}
 var lab=function(){b.textContent=b.classList.contains('on')?'개표 지도 끄기':'🗳 개표 현황';ln.hidden=!b.classList.contains('on')};paint();lab();
 b.addEventListener('click',function(){setTimeout(lab,0)});if(/#cp-map|#election/.test(location.hash)&&!b.classList.contains('on'))b.click()})()}).catch(function(){});
}catch(_){}})();
