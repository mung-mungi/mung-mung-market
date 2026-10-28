(function(){
  // 홈 '오늘 한눈에' 숫자 4개를 5분 시세 갱신(live/market.json) 값으로 바꿈 — 사용자 2026-10-29 지시. 페이지를 열어 둔 동안 5분마다 다시 읽음
  var MAP = [[/나스닥/, 'nasdaq'], [/반도체|SOX/, 'sox'], [/10년/, 'us10y'], [/WTI|유가/, 'wti']];
  function f2(v){ return v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function sg(v, u){ return (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(u === 'bp' ? 0 : 2) + (u || '%'); }
  function paint(d){
    var st = document.querySelectorAll('.stats .stat'); if (!st.length || !d || !d.items) return false;
    st.forEach(function(s){
      var k = s.querySelector('.k'), n = s.querySelector('.n'); if (!k || !n) return;
      var key = null; MAP.forEach(function(m){ if (!key && m[0].test(k.textContent)) key = m[1]; }); var it = key && d.items[key]; if (!it) return;
      var txt, cls = '';
      if (it.kind === 'pct') { txt = sg(it.chg); cls = it.chg > 0 ? 'up' : it.chg < 0 ? 'dn' : ''; }
      else if (it.kind === 'lvl') { txt = it.v.toFixed(2) + '%'; if (it.pc) txt += ' <small>' + sg((it.v - it.pc) * 100, 'bp') + '</small>'; }
      else { txt = '$' + it.v.toFixed(1); if (it.chg != null) txt += ' <small>' + sg(it.chg, '%').replace(/\.(\d)\d%/, '.$1%') + '</small>'; }
      n.innerHTML = txt; n.classList.remove('up', 'dn'); if (cls) n.classList.add(cls);
    });
    var box = document.querySelector('.stats'), cap = document.getElementById('mkt-cap');
    if (!cap) { cap = document.createElement('div'); cap.id = 'mkt-cap'; box.after(cap); }
    cap.textContent = '● 숫자 ' + d.label + ' 기준 · 5분마다 새로';
    return true;
  }
  var last = null;
  function load(){ fetch('live/market.json?t=' + Date.now(), { cache: 'no-store' }).then(function(r){ return r.ok ? r.json() : null; }).then(function(d){ if (d) { last = d; paint(d); } }).catch(function(){}); }
  try { new MutationObserver(function(){ if (last && !document.getElementById('mkt-cap')) paint(last); }).observe(document.documentElement, { subtree: true, childList: true }); } catch (e) {}
  var st = document.createElement('style'); st.textContent = '#mkt-cap{font:600 11.5px/1.4 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif;color:#2f9a4c;padding:5px 12px 7px;text-align:right;background:color-mix(in srgb,var(--panel-2,#f1f0ec) 55%,var(--panel,#fff))}.stats .stat .n small{font-size:.62em;font-weight:600;color:var(--muted,#6f6d68);margin-left:2px}';
  (document.head || document.documentElement).appendChild(st);
  load(); setInterval(load, 300000); document.addEventListener('visibilitychange', function(){ if (!document.hidden) load(); });
})();
