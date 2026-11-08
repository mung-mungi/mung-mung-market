// 환율 → '아시아 통화'(사용자 2026-11-09: 한국을 빼지 말고 아시아 반도체 흐름으로 같이 보자, 환율에 하나 더) — 원·대만달러·엔 세 칸 + 한 줄 해석 + 아시아 반도체 수출로 바로가기
(function(){
  if (!/p-fx\.html/.test(location.pathname)) return;
  function el(t, c, x){ var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function pct(a, b){ return b ? (a / b - 1) * 100 : null; }
  function back(rows, d, days){ var t = new Date(d); t.setDate(t.getDate() - days); var s = t.toISOString().slice(0, 10), r = null; rows.forEach(function(x){ if (x.date <= s) r = x; }); return r; }
  var R = null;
  function draw(){
    if (!R || document.querySelector('.fxa')) return !!document.querySelector('.fxa');
    var take = document.getElementById('take'); if (!take) return false;
    var L = R[R.length - 1], P = R[R.length - 2], M = back(R, L.date, 30);
    var C = [['원', 'usdkrw', '원/달러', 2], ['대만달러', 'usdtwd', '대만달러/달러', 3], ['엔', 'usdjpy', '엔/달러', 2]];
    var box = el('section', 'fxa'); var hd = el('div', 'fxa-h'); hd.appendChild(el('b', '', '아시아 통화 한눈에')); hd.appendChild(el('span', '', L.date.slice(5).replace('-', '.') + ' 기준 · 야후 종가')); box.appendChild(hd);
    var g = el('div', 'fxa-g'), str = [];
    C.forEach(function(c){ var v = L[c[1]]; if (v == null) return; var d1 = P && pct(v, P[c[1]]), m1 = M && pct(v, M[c[1]]);
      var t = el('div', 'fxa-t'); t.appendChild(el('small', '', c[0])); t.appendChild(el('b', '', v.toLocaleString('en-US', { maximumFractionDigits: c[3] })));
      var s = el('em', m1 > 0.3 ? 'w' : m1 < -0.3 ? 's' : '', m1 == null ? '' : '1달 ' + (m1 > 0 ? '+' : '') + m1.toFixed(1) + '% · ' + (m1 > 0.3 ? c[0] + ' 약세' : m1 < -0.3 ? c[0] + ' 강세' : '보합')); t.appendChild(s);
      if (d1 != null) t.appendChild(el('i', '', '하루 ' + (d1 > 0 ? '+' : '') + d1.toFixed(2) + '%'));
      g.appendChild(t); if (m1 != null && c[1] !== 'usdjpy') str.push(m1);
    });
    box.appendChild(g);
    var both = str.length === 2 ? (str[0] < -0.3 && str[1] < -0.3 ? 'in' : str[0] > 0.3 && str[1] > 0.3 ? 'out' : 'mix') : 'mix';
    var p = el('p', 'fxa-r'); p.appendChild(el('b', '', '지금 '));
    p.appendChild(document.createTextNode(both === 'in' ? '원·대만달러가 함께 강해졌습니다 — 하이닉스·삼성·TSMC 같은 아시아 반도체로 외국인 돈이 들어오는 쪽입니다.' : both === 'out' ? '원·대만달러가 함께 약해졌습니다 — 아시아 반도체에서 외국인 돈이 빠지는 쪽입니다(반도체 투매 때 자주 같이 나옴).' : '원·대만달러 방향이 엇갈립니다 — 한쪽 시장만의 사정일 가능성이 큽니다.'));
    box.appendChild(p);
    var a = el('a', 'fxa-go', '아시아 반도체 수출(TSMC·대만·한국 월별) 보기 ›'); a.href = 'p-supply.html'; box.appendChild(a);
    (take.closest('section,.card,.panel') || take).after(box); return true;
  }
  function title(){ document.querySelectorAll('h1 .m, .lw-mast *, header *').forEach(function(e){ if (e.children.length === 0 && e.textContent.trim() === '원·달러 환율') e.textContent = '아시아 통화'; }); }
  fetch('d/fx/usdkrw.json?t=' + Math.floor(Date.now() / 3e5)).then(function(r){ return r.ok ? r.json() : null; }).then(function(d){ if (!d || !d.length) return; R = d;
    var k = 0; (function go(){ var ok = false; try { title(); ok = draw(); } catch (e) {} if (++k < 30) setTimeout(go, ok ? 800 : 300); })(); }).catch(function(){});
})();
