// 미국 중간선거 개표판(사용자 2026-11-04 — 오늘·내일만): 메인 맨 위 한 줄 띠 + 네오클라우드 페이지 맨 위 상세 판
// 자료: d/election/live.json (Claude가 30분~2시간마다 갱신). ended가 true이거나 11/6 이후면 메인 띠는 숨김
(function(){try{
var main=/\/(index\.html)?$/.test(location.pathname),neo=/p-neo\.html$/.test(location.pathname);if(!main&&!neo)return;
var css='.el-band{display:block;margin:10px 0 12px;padding:11px 14px;border-radius:14px;background:#fff;border:1px solid #e3d6bd;border-left:5px solid #2f5f7a;box-shadow:0 3px 0 #ece2cc;color:#1d1a16;text-decoration:none;-webkit-tap-highlight-color:transparent}'+
'.el-band:active{transform:translateY(1px);box-shadow:none}.el-band b{font-weight:900}.el-band .k{font-size:12.5px;color:#6b6458;font-weight:700}.el-band .t{font-size:15.5px;line-height:1.45;margin-top:2px}.el-band .go{float:right;font-size:12.5px;color:#2f5f7a;font-weight:800}'+
'.el-wrap{margin:12px 0 18px;background:#fff;border:1px solid #e3d6bd;border-radius:16px;padding:14px 14px 10px;box-shadow:0 3px 0 #ece2cc;color:#1d1a16}'+
'.el-wrap h2{font-size:20px;margin:0 0 2px}.el-sub{font-size:12.5px;color:#6b6458;margin:0 0 10px}'+
'.el-seat{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 12px}.el-seat>div{border:1px solid #eadfc8;border-radius:12px;padding:9px 10px}'+
'.el-seat .h{font-size:13px;font-weight:800;color:#6b6458}.el-seat .n{font-size:20px;font-weight:900;font-variant-numeric:tabular-nums;margin:2px 0}.el-seat .d{color:#2457a6}.el-seat .r{color:#b8322a}.el-seat .s{font-size:12px;color:#6b6458}'+
'.el-sec{border-top:1px dashed #e3d6bd;padding:10px 0 4px}.el-sec h3{font-size:16px;margin:0 0 6px}'+
'.el-row{padding:7px 0;border-top:1px solid #f1eadb;font-size:14px;line-height:1.5}.el-row:first-of-type{border-top:0}.el-row .st{font-weight:800}.el-row .pill{display:inline-block;font-size:11.5px;font-weight:800;padding:1px 7px;border-radius:999px;background:#f1ece1;color:#5b5246;margin-left:4px}'+
'.el-row .pill.won{background:#e7f2e8;color:#2d6a3a}.el-row .q{display:block;color:#5b5246;font-size:13px;margin-top:2px}.el-row a{color:#2f5f7a}'+
'.el-note{font-size:12px;color:#8a7f6c;margin:8px 0 2px}.el-fold{display:block;margin:6px auto 0;padding:6px 14px;border:1px solid #e0d2b4;border-radius:999px;background:#fff;font:inherit;font-size:13px;font-weight:800;color:#5b5246}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function e(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function seat(x){if(!x)return'집계 전';var s='<span class="d">민주 '+e(x.D==null?'–':x.D)+'</span> · <span class="r">공화 '+e(x.R==null?'–':x.R)+'</span>';if(x.other)s+=' · 기타 '+e(x.other);return s}
function call(x){return x&&x.called?('✅ AP 확정: '+e(x.called)+' 다수당'):'다수당 미정'}
fetch('d/election/live.json?t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){
 var over=j.ended||Date.now()>Date.parse('2026-11-06T00:00:00+09:00');
 if(main){if(over)return;var w=document.querySelector('.wrap')||document.body;var a=document.createElement('a');a.className='el-band';a.href='p-neo.html#election';
  a.innerHTML='<span class="go">자세히 ›</span><span class="k">🗳 미국 중간선거 개표 중 · '+e(j.updated_label||'')+'</span><div class="t">하원 '+seat(j.house)+' ('+call(j.house)+')<br>상원 '+seat(j.senate)+' ('+call(j.senate)+')</div>';
  var h=w.querySelector('header,.mm-hero,.nl-rail');(h&&h.parentNode===w)?w.insertBefore(a,h.nextSibling):w.insertBefore(a,w.firstChild);return}
 var box=document.createElement('section');box.id='election';box.className='el-wrap';
 var h='<h2>🗳 선거와 데이터센터 — 개표 상황</h2><p class="el-sub">'+e(j.updated_label||'')+' · 출처 AP 등 확인된 확정 발표만, 예측·여론조사는 넣지 않습니다</p>'+
  '<div class="el-seat"><div><div class="h">하원 (과반 '+e((j.house||{}).needed||218)+')</div><div class="n">'+seat(j.house)+'</div><div class="s">'+call(j.house)+'</div></div>'+
  '<div><div class="h">상원 (과반 '+e((j.senate||{}).needed||51)+')</div><div class="n">'+seat(j.senate)+'</div><div class="s">'+call(j.senate)+'</div></div></div>';
 function sec(t,rows,f){if(!rows||!rows.length)return'';return'<div class="el-sec"><h3>'+t+'</h3>'+rows.map(f).join('')+'</div>'}
 h+=sec('데이터센터 많은 주의 핵심 선거',j.dc_races,function(r){return'<div class="el-row"><span class="st">'+e(r.state)+' · '+e(r.race)+'</span><span class="pill'+(r.winner?' won':'')+'">'+e(r.winner?('당선: '+r.winner):(r.status||'개표 중'))+'</span>'+
  (r.candidates||[]).map(function(c){return'<span class="q">'+e(c.name)+(c.party?' ('+e(c.party)+')':'')+' — '+e(c.dc_stance||'데이터센터 관련 확인된 발언 없음')+(c.src?' <a href="'+e(c.src)+'" target="_blank" rel="noopener">출처</a>':'')+'</span>'}).join('')+'</div>'});
 h+=sec('데이터센터 규제를 말해 온 인물 — 자리 변화',j.movers,function(m){return'<div class="el-row"><span class="st">'+e(m.name)+'</span> <span class="pill'+(m.result?' won':'')+'">'+e(m.result||'개표 중')+'</span><span class="q">'+e(m.role||'')+' — '+e(m.stance||'')+(m.src?' <a href="'+e(m.src)+'" target="_blank" rel="noopener">출처</a>':'')+'</span></div>'});
 h+=sec('지역 주민투표 · 데이터센터 제한',j.measures,function(m){return'<div class="el-row"><span class="st">'+e(m.place)+'</span> <span class="pill'+(m.result?' won':'')+'">'+e(m.result||'개표 중')+'</span><span class="q">'+e(m.what||'')+(m.src?' <a href="'+e(m.src)+'" target="_blank" rel="noopener">출처</a>':'')+'</span></div>'});
 if(j.market)h+='<div class="el-sec"><h3>투자자에게 어떤 변수인가</h3><div class="el-row">'+e(j.market)+'</div></div>';
 h+='<p class="el-note">'+e(j.note||'양당 같은 기준으로 확인된 발언·결과만 싣습니다. 11/5까지 운영 후 내려갑니다.')+'</p>';
 box.innerHTML=h;var root=document.querySelector('.wrap,main')||document.body;var hh=root.querySelector('.mm-hero,header,h1');
 if(hh&&hh.parentNode===root)root.insertBefore(box,hh.nextSibling);else root.insertBefore(box,root.firstChild);
 if(location.hash==='#election')setTimeout(function(){box.scrollIntoView({block:'start'})},300)}).catch(function(){})}catch(_){}})();
