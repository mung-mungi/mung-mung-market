(function(){
  // 멍뭉 터미널: 누르는 곳마다 부드러운 '틱' 소리(소리 파일 없이 브라우저가 직접 만듦), 오른쪽 아래 🔊/🔇로 끄고 켬
  if (window.__tick) return; window.__tick = 1;
  var KEY = 'mm-tick-off', off = false, ctx = null;
  try { off = localStorage.getItem(KEY) === '1'; } catch (e) {}
  var SEL = 'a,button,summary,select,label,[role=button],[role=tab],[onclick],.pb-row,.pb-hc,.pb-tile,.cp,.item,tr[data-tk],input[type=checkbox],input[type=radio]';
  var buf = null;
  function ac(){
    if (!ctx) { var A = window.AudioContext || window.webkitAudioContext; if (!A) return null; ctx = new A(); }
    if (ctx.state !== 'running' && ctx.resume) ctx.resume();
    if (!buf) { // 짧은 '틱' = 25ms 잡음을 고음대만 걸러서(휴대폰 스피커에서도 잘 들림)
      var n = Math.floor(ctx.sampleRate * 0.025); buf = ctx.createBuffer(1, n, ctx.sampleRate); var d = buf.getChannelData(0);
      for (var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 4);
    }
    return ctx;
  }
  // 소리 종류: tap(기본 틱) · nav(페이지 이동, 조금 낮은 톡) · open(펼침, 올라가는 두 번 틱) · close(닫힘, 낮은 틱)
  var TONE = { tap: [[2300, 0.2, 0]], nav: [[1500, 0.22, 0]], open: [[2700, 0.18, 0]], close: [[1700, 0.16, 0]] };
  function tick(kind){
    if (off) return;
    try { if (navigator.vibrate) navigator.vibrate(6); } catch (e) {}  // 안드로이드만 살짝 진동(아이폰 웹은 진동 불가)
    try {
      var c = ac(); if (!c) return;
      (TONE[kind] || TONE.tap).forEach(function(x){
        var t = c.currentTime + 0.005 + x[2], s = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain();
        s.buffer = buf; f.type = 'bandpass'; f.frequency.value = x[0]; f.Q.value = 0.9; g.gain.value = x[1];
        s.connect(f); f.connect(g); g.connect(c.destination); s.start(t);
      });
    } catch (e) {}
  }
  // 아이폰·카톡 안 브라우저는 '누름이 끝난 뒤(click)'에만 소리를 허락하는 경우가 많아 click에서 냅니다
  var last = 0;
  function onTap(e){
    var el = e.target && e.target.closest ? e.target.closest(SEL) : null;
    if (!el || el.id === 'mm-snd' || el.disabled) return;
    var now = Date.now(); if (now - last < 120) return; last = now;
    var isNav = el.tagName === 'A' && el.href && !el.target && (function(){ try { var u = new URL(el.href, location.href); return u.origin === location.origin && u.pathname !== location.pathname; } catch (x) { return false; } })();
    var tog = el.hasAttribute('aria-expanded') ? 'aria-expanded' : el.hasAttribute('aria-pressed') && el.closest('[role=group]') == null ? 'aria-pressed' : null;
    if (isNav) tick('nav');
    else if (tog) { var before = el.getAttribute(tog); setTimeout(function(){ var after = el.getAttribute(tog); tick(after === before ? 'tap' : after === 'true' ? 'open' : 'close'); }, 0); }
    else if (el.tagName === 'SUMMARY') { var d = el.parentElement; setTimeout(function(){ tick(d && d.open ? 'open' : 'close'); }, 0); }
    else if (el.matches('tr, .pb-row')) { var wasOn = el.classList.contains('on'); setTimeout(function(){ tick(wasOn ? 'close' : 'open'); }, 0); }
    else tick('tap');
    // 다른 페이지로 넘어가는 링크는 소리가 끊기지 않게 0.07초 뒤에 이동
    if (el.tagName === 'A' && el.href && !el.target && !e.defaultPrevented && !e.metaKey && !e.ctrlKey && !e.shiftKey && e.button === 0) {
      var u = new URL(el.href, location.href);
      if (u.origin === location.origin && u.pathname !== location.pathname) { e.preventDefault(); setTimeout(function(){ location.href = el.href; }, 70); }
    }
  }
  document.addEventListener('click', onTap, true);
  ['touchend', 'pointerdown', 'keydown'].forEach(function(ev){ document.addEventListener(ev, function(){ try { if (!off) ac(); } catch (e) {} }, { capture: true, passive: true }); });
  // 누를 때 살짝 눌리는 느낌(움직임 줄이기 설정이면 생략)
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) {
    var st = document.createElement('style');
    st.textContent = '.mm-press{transform:scale(.975)!important;filter:brightness(.97);transition:transform .07s ease,filter .07s ease!important}tr.mm-press{transform:none!important}.item{box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 4px 0 rgba(30,22,8,.13),0 9px 20px rgba(30,22,8,.13)!important;transition:transform .1s ease,box-shadow .1s ease!important}.pb-chip,.pb-tdet .cp{box-shadow:0 3px 0 rgba(30,22,8,.16),0 4px 8px rgba(30,22,8,.10);transition:transform .1s ease,box-shadow .1s ease}.item.mm-press,.pb-chip.mm-press,.pb-tdet .cp.mm-press{transform:translateY(3px)!important;filter:none!important;box-shadow:0 1px 0 rgba(30,22,8,.14)!important}@media (hover:hover){.item:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,.75),0 4px 0 rgba(40,30,10,.08),0 10px 20px rgba(40,30,10,.10)!important}}tr.mm-press>td{background:rgba(154,98,0,.08)!important}.mm-rel{transition:transform .16s ease,filter .16s ease}';
    (document.head || document.documentElement).appendChild(st);
    var pressed = null;
    var rel = function(){ if (pressed) { var p = pressed; pressed = null; p.classList.remove('mm-press'); p.classList.add('mm-rel'); setTimeout(function(){ p.classList.remove('mm-rel'); }, 180); } };
    document.addEventListener('pointerdown', function(e){ var el = e.target && e.target.closest ? e.target.closest(SEL) : null; if (!el || el.id === 'mm-snd') return; rel(); pressed = el; el.classList.add('mm-press'); }, { capture: true, passive: true });
    ['pointerup', 'pointercancel', 'pointerleave', 'scroll'].forEach(function(ev){ document.addEventListener(ev, rel, { capture: true, passive: true }); });
  }
  function ui(){
    if (document.getElementById('mm-snd')) return;
    var b = document.createElement('button'); b.id = 'mm-snd'; b.type = 'button';
    var paint = function(){ b.textContent = off ? '🔇' : '🔊'; b.setAttribute('aria-label', off ? '누름 소리 켜기' : '누름 소리 끄기'); b.title = b.getAttribute('aria-label'); };
    b.style.cssText = 'position:fixed;z-index:50;right:calc(12px + env(safe-area-inset-right,0px));bottom:calc(12px + env(safe-area-inset-bottom,0px));width:36px;height:36px;border-radius:50%;border:1px solid rgba(0,0,0,.12);background:rgba(255,255,255,.92);box-shadow:0 2px 8px rgba(0,0,0,.12);font-size:16px;line-height:1;cursor:pointer;padding:0;opacity:.85';
    b.addEventListener('click', function(){ off = !off; try { localStorage.setItem(KEY, off ? '1' : '0'); } catch (e) {} paint(); if (!off) tick(); });
    paint(); document.body.appendChild(b);
  }
  if (document.body) ui(); else document.addEventListener('DOMContentLoaded', ui);
})();
