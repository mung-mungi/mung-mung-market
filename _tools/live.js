(function(){
  // 미국 종목 차트를 열면 그 종목만 Finnhub로 실시간 시세를 받아 가격 칸을 바꿉니다(사용자 2026-10-29 지시).
  // 같은 종목은 1분 동안 다시 묻지 않습니다. 실패하면 저장값을 두고 '기준: 날짜 종가'를 붙입니다.
  if (window.__mmLive) return; window.__mmLive = 1;
  var KEY = 'dbh0f5hr01qjpoc3ltqgdbh0f5hr01qjpoc3ltr0', TTL = 60000, FRESH = 30 * 60000;
  var cache = {}, wait = {};
  function isUS(t){ return !!t && /^[A-Z][A-Z0-9.\-]{0,6}$/.test(t) && !/\.(KS|KQ|TW|TWO|T|HK|SS|SZ|L|PA|DE|AS)$/.test(t); }
  function load(t){ try { var x = JSON.parse(sessionStorage.getItem('fh:' + t) || 'null'); if (x && Date.now() - x.at < TTL) return x; } catch (e) {} return null; }
  function quote(t, cb){
    var c = cache[t] || load(t);
    if (c && Date.now() - c.at < TTL) { cb(c.q); return; }
    if (wait[t]) { wait[t].push(cb); return; } wait[t] = [cb];
    var done = function(q){ var e = { at: Date.now(), q: q }; cache[t] = e; try { sessionStorage.setItem('fh:' + t, JSON.stringify(e)); } catch (x) {} var l = wait[t]; delete wait[t]; l.forEach(function(f){ try { f(q); } catch (x) {} }); };
    var ctl = window.AbortController ? new AbortController() : null; var to = setTimeout(function(){ if (ctl) ctl.abort(); }, 6000);
    fetch('https://finnhub.io/api/v1/quote?symbol=' + encodeURIComponent(t.replace('-', '.')) + '&token=' + KEY, { cache: 'no-store', signal: ctl ? ctl.signal : undefined })
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(q){ clearTimeout(to); done(q && q.c > 0 && q.t ? q : null); })
      .catch(function(){ clearTimeout(to); done(null); });
  }
  function fmt(v){ return v >= 1000 ? v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : v.toFixed(2); }
  function kst(sec){ var d = new Date(sec * 1000 + 9 * 3600000); var p = function(n){ return (n < 10 ? '0' : '') + n; }; return (d.getUTCMonth() + 1) + '/' + d.getUTCDate() + ' ' + p(d.getUTCHours()) + ':' + p(d.getUTCMinutes()); }
  function pct(v){ return v == null ? '' : (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(2) + '%'; }
  function asofDate(){ var a = document.getElementById('asof'); var m = a && a.textContent.match(/(\d{1,2})월\s*(\d{1,2})일|(\d{1,2})[.\/](\d{1,2})/); return m ? (m[1] || m[3]) + '/' + (m[2] || m[4]) : ''; }
  // 한 자리(가격 칸 pr, 설명 칸 kd)에 결과 반영
  function apply(t, pr, kd, cur){
    if (!pr || pr.dataset.fh === t) return; pr.dataset.fh = t;
    var saved = pr.textContent, savedLive = /프리마켓|장중|애프터|데이장/.test(saved + (kd ? kd.textContent : ''));
    quote(t, function(q){
      if (!pr.isConnected) return;
      var fresh = q && Date.now() - q.t * 1000 < FRESH;
      if (q && (fresh || !savedLive)) {
        var lab = (fresh ? '' : '기준: ') + kst(q.t) + (fresh ? '' : ' 종가') + ' · ' + pct(q.dp);
        if (kd) { pr.textContent = fmt(q.c) + ' ' + cur; kd.textContent = lab; }
        else pr.textContent = fmt(q.c) + ' ' + cur + ' · ' + lab;
        pr.title = 'Finnhub 시세 · 1분마다 새로 받음';
        pr.classList.add('mm-fh');
      } else if (!savedLive) {
        var d = asofDate(); if (d && !kd) pr.textContent = saved + ' · 기준: ' + d + ' 종가';
      }
    });
  }
  function scan(){
    // 시세 보드: 펼친 종목 줄
    var det = document.querySelector('tr.pb-det');
    if (det) { var row = det.previousElementSibling, t = row && row.dataset.key, pr = det.querySelector('.hd .pr'); if (isUS(t) && pr && /USD/.test(pr.textContent)) apply(t, pr, null, 'USD'); }
    // 차트 길잡이: 고른 종목 카드
    document.querySelectorAll('span.tk').forEach(function(tk){
      var card = tk.parentElement; for (var i = 0; i < 3 && card && !card.querySelector('span.pr'); i++) card = card.parentElement;
      if (!card) return; var pr = card.querySelector('span.pr'), kd = card.querySelector('span.kind'), t = tk.textContent.trim();
      if (isUS(t) && pr && /USD/.test(pr.textContent)) apply(t, pr, kd, 'USD');
    });
  }
  var q = 0; function later(){ if (q) return; q = 1; setTimeout(function(){ q = 0; scan(); }, 120); }
  try { new MutationObserver(later).observe(document.documentElement, { subtree: true, childList: true }); } catch (e) {}
  document.addEventListener('DOMContentLoaded', scan); window.addEventListener('load', scan); setTimeout(scan, 1500);
  var st = document.createElement('style'); st.textContent = '.mm-fh{color:#1f7a3f!important}'; (document.head || document.documentElement).appendChild(st);
})();
