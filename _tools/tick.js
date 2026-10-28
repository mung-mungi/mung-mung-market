(function(){
  // 멍뭉 터미널: 누르는 곳마다 부드러운 '틱' 소리(소리 파일 없이 브라우저가 직접 만듦), 오른쪽 아래 🔊/🔇로 끄고 켬
  if (window.__tick) return; window.__tick = 1;
  var KEY = 'mm-tick-off', off = false, ctx = null;
  try { off = localStorage.getItem(KEY) === '1'; } catch (e) {}
  var SEL = 'a,button,summary,select,label,[role=button],[role=tab],[onclick],.pb-row,.pb-hc,.pb-tile,.cp,.item,tr[data-tk],input[type=checkbox],input[type=radio]';
  function tick(){
    if (off) return;
    try {
      if (!ctx) { var A = window.AudioContext || window.webkitAudioContext; if (!A) return; ctx = new A(); }
      if (ctx.state === 'suspended') ctx.resume();
      var t = ctx.currentTime, o = ctx.createOscillator(), g = ctx.createGain(), f = ctx.createBiquadFilter();
      o.type = 'triangle'; o.frequency.setValueAtTime(1500, t); o.frequency.exponentialRampToValueAtTime(700, t + 0.03);
      f.type = 'lowpass'; f.frequency.value = 3200;
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.06, t + 0.004); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.045);
      o.connect(f); f.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + 0.05);
    } catch (e) {}
  }
  document.addEventListener('pointerdown', function(e){
    var el = e.target && e.target.closest ? e.target.closest(SEL) : null;
    if (!el || el.id === 'mm-snd' || el.disabled) return;
    tick();
  }, true);
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
