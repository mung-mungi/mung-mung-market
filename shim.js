document.documentElement.setAttribute('data-theme','light'); /* 주간 모드 고정 */
/* 원본 대시보드 런타임(dash)을 통합본 안에서 흉내 내는 작은 틀. 자료는 d/<페이지>/<자료>.json에서 읽습니다. */
(function () {
  const cfg = window.__PAGE__ || { page: '', ds: [], params: {} };
  const store = {};
  const calcs = {};
  const order = [];
  const subs = [];
  let params = Object.assign({}, cfg.params || {});
  const defaults = Object.assign({}, cfg.params || {});
  cfg.ds.forEach((id) => { store[id] = { status: 'loading', data: [], columns: [], meta: [], message: '' }; });
  const colsOf = (rows) => { const s = []; (rows || []).slice(0, 50).forEach((r) => { if (r && typeof r === 'object') Object.keys(r).forEach((k) => { if (!s.includes(k)) s.push(k); }); }); return s; };
  function result(o) { return Object.assign({ refreshing: false }, o, { rows: o.data, value: o.data }); }
  function getCalc(id) {
    const c = calcs[id];
    if (c.cache) return c.cache;
    const ins = c.inputs.map((i) => (store[i] ? store[i] : calcs[i] ? getCalc(i) : { status: 'missing', data: [] }));
    const bad = ins.find((x) => x.status !== 'ok');
    if (bad) return result({ status: bad.status === 'error' ? 'error' : 'loading', data: [], columns: [], meta: [] });
    try {
      const out = c.fn.apply(null, ins.map((x) => x.data));
      c.cache = result({ status: 'ok', data: out, columns: Array.isArray(out) ? colsOf(out) : [], meta: [] });
    } catch (e) {
      console.error('calc', id, e);
      c.cache = result({ status: 'error', data: [], columns: [], meta: [], message: String(e && e.message) });
    }
    return c.cache;
  }
  function fire() {
    Object.values(calcs).forEach((c) => { c.cache = null; });
    subs.forEach((fn) => { try { fn(); } catch (e) { console.error(e); } });
  }
  const dash = {
    data(id) {
      if (store[id]) return result(store[id]);
      if (calcs[id]) return getCalc(id);
      return result({ status: 'missing', data: [], columns: [], meta: [] });
    },
    calc(id, o) { calcs[id] = { inputs: o.inputs || [], fn: o.fn, cache: null }; order.push(id); },
    loader() {},
    onData(fn) { subs.push(fn); try { fn(); } catch (e) { console.error(e); } },
    colors: ['var(--dc1)', 'var(--dc2)', 'var(--dc3)', 'var(--dc4)', 'var(--dc5)', 'var(--dc6)', 'var(--dc7)', 'var(--dc8)'],
    refresh() {},
    params() { return Object.assign({}, params); },
    setParams(p) { params = Object.assign({}, params, p); fire(); },
    resetParams() { params = Object.assign({}, defaults); fire(); },
    setLink(name) { try { history.replaceState(null, '', '#' + name); } catch (e) {} },
  };
  window.dash = dash;
  let t = null;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(fire, 150); });
  const bust = window.__SYNC__ ? '?v=' + window.__SYNC__ : '';
  Promise.all(cfg.ds.map((id) => fetch('d/' + cfg.page + '/' + id + '.json' + bust).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }).then((d) => {
    const rows = Array.isArray(d) ? d : d.rows || d.data || d;
    store[id] = { status: 'ok', data: rows, columns: Array.isArray(rows) ? colsOf(rows) : [], meta: [] };
  }).catch((e) => { store[id] = { status: 'error', data: [], columns: [], meta: [], message: String(e) }; }))).then(() => {
    const root = document.getElementById('dash-root'); if (root) root.removeAttribute('data-dash-state');
    fire();
    const named = location.hash && document.getElementById(location.hash.slice(1)); if (named) named.scrollIntoView();
  });
})();
/* 가독성: 한 덩어리에 ①②③이 이어 붙은 문단은 번호마다 줄을 바꿔 보여 줍니다(내용은 그대로). */
(function () {
  var NUM = /[①②③④⑤⑥⑦⑧⑨⑩]/, SPLIT = /(?=[①②③④⑤⑥⑦⑧⑨⑩])/;
  var BLOCK = { P:1, DIV:1, LI:1, UL:1, OL:1, TABLE:1, SECTION:1, ARTICLE:1, H1:1, H2:1, H3:1, H4:1, BR:0 };
  var SKIP = 'button,a,select,option,svg,script,style,textarea,input,label,nav';
  function fix(el) {
    var t = el.textContent || '';
    if (el._rdx === t) return;
    var m = t.match(/[①②③④⑤⑥⑦⑧⑨⑩]/g);
    if (!m || m.length < 2 || t.length < 30 || el.closest(SKIP)) { el._rdx = t; return; }
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [], seen = false;
    while (w.nextNode()) nodes.push(w.currentNode);
    nodes.forEach(function (n) {
      var s = n.textContent;
      if (n.parentElement && n.parentElement.closest(SKIP)) { if (s.trim()) seen = true; return; }
      var parts = s.split(SPLIT);
      if (!parts.some(function (p, i) { return NUM.test(p.charAt(0)) && (seen || i > 0); })) { if (s.trim()) seen = true; return; }
      var prev = n.previousSibling, f = document.createDocumentFragment();
      parts.forEach(function (p, i) {
        if (NUM.test(p.charAt(0)) && (seen || i > 0)) {
          if (!(i === 0 && prev && prev.nodeName === 'BR')) f.appendChild(document.createElement('br'));
          p = p.replace(/^\s+/, '');
        } else if (i < parts.length - 1) p = p.replace(/\s+$/, '');
        if (p) f.appendChild(document.createTextNode(p));
        if (p.trim()) seen = true;
      });
      n.parentNode.replaceChild(f, n);
    });
    el._rdx = el.textContent;
  }
  function run() {
    var els = document.querySelectorAll('p,li,td,dd,blockquote,div,span.sub');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], kids = el.children, block = false;
      for (var j = 0; j < kids.length; j++) if (BLOCK[kids[j].tagName]) { block = true; break; }
      if (!block) fix(el);
    }
  }
  var tm = null;
  function later() { clearTimeout(tm); tm = setTimeout(run, 250); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', later); else later();
  try { new MutationObserver(later).observe(document.documentElement, { childList: true, subtree: true, characterData: true }); } catch (e) {}
})();
/* 폰 화면(640px 이하)에서 카드 목록을 한 줄에 2개씩 놓습니다. 그래프 묶음(20rem 이상)은 그대로 한 줄. */
(function () {
  function run() {
    if (document.getElementById('two-col-css')) return;
    var sels = [];
    for (var i = 0; i < document.styleSheets.length; i++) {
      var rules; try { rules = document.styleSheets[i].cssRules; } catch (e) { continue; }
      if (!rules) continue;
      for (var j = 0; j < rules.length; j++) {
        var r = rules[j]; if (!r.style || !r.selectorText) continue;
        var g = r.style.gridTemplateColumns || ''; if (g.indexOf('repeat(auto-f') !== 0) continue;
        var m = g.match(/minmax\((?:min\(100%,\s*)?([\d.]+)(rem|px)/); if (!m) continue;
        var v = parseFloat(m[1]) * (m[2] === 'rem' ? 16 : 1);
        if (v > 150 && v <= 300) sels.push(r.selectorText);
      }
    }
    if (!sels.length) return;
    var st = document.createElement('style'); st.id = 'two-col-css';
    st.textContent = '@media (max-width:640px){' + sels.join(',') + '{grid-template-columns:repeat(2,minmax(0,1fr))!important}' +
      sels.map(function (s) { return s.split(',').map(function (x) { return x + '>*'; }).join(','); }).join(',') + '{min-width:0;overflow-wrap:anywhere}' +
      sels.map(function (s) { return s.split(',').map(function (x) { return x + ' .v'; }).join(','); }).join(',') + '{font-size:clamp(18px,6.4vw,28px)!important;line-height:1.15;overflow-wrap:anywhere}}';
    document.head.appendChild(st);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();

/* 위 이동 막대: 홈 버튼을 왼쪽에 고정 */
(function(){function run(){var a=document.querySelector('.ib a.home');if(!a)return;if(a.textContent.indexOf('통합본')>=0)a.textContent='⌂ 홈';
if(!document.getElementById('home-pin')){var st=document.createElement('style');st.id='home-pin';st.textContent='.ib a.home{position:sticky;left:0;z-index:3;box-shadow:-8px 0 0 5px var(--ib-bg,#f9f9f7),-22px 0 0 5px var(--ib-bg,#f9f9f7),9px 0 10px -8px rgba(0,0,0,.3)}';document.head.appendChild(st)}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();})();

/* 단락 제목 글씨 키우기(본문보다 한눈에 들어오게) */
(function(){function run(){if(document.getElementById('h-size'))return;var st=document.createElement('style');st.id='h-size';
st.textContent='#dash-root section > h2,#dash-root section > h3,#dash-root .card > h2,#dash-root .pg-sec > .k{font-size:clamp(19px,4.8vw,21px)!important;line-height:1.35!important}';document.head.appendChild(st)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();})();
