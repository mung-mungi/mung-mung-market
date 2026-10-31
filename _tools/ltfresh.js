// 시장 경고등: 자동 한 줄(숫자로 매 갱신마다 다시 씀) + 멈춘 값 날짜 칩(사용자 2026-10-31). 자료 d/lights/fresh.json
(function(){try{
fetch('d/lights/fresh.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json()}).then(function(F){
  if(!F||!F.line)return;
  var md=function(s){return s?(+s.slice(5,7))+'/'+(+s.slice(8,10)):''};
  function paint(){
    var v=document.getElementById('view');
    if(v&&!document.getElementById('lt-auto')){
      var b=document.createElement('div');b.id='lt-auto';b.className='lt-auto';
      b.innerHTML='<span class="lt-k">자동 한 줄 · 숫자 기준</span><b></b>'+(F.stale&&F.stale.length?'<small></small>':'');
      b.querySelector('b').textContent=F.line;
      if(F.stale&&F.stale.length)b.querySelector('small').textContent='⚠ 받지 못해 이전 값을 쓰는 지표: '+F.stale.join(' · ');
      v.parentElement.insertBefore(b,v);
      // 손으로 쓴 관점에는 쓴 날짜가 이미 있음 → 자동 줄과 구분되게 표시만
      v.classList.add('lt-hand');
    }
    var it=F.items||{};
    Object.keys(it).forEach(function(k){var x=it[k];if(!x.stale)return;
      [].forEach.call(document.querySelectorAll('#areas li'),function(li){var n=li.querySelector('b');
        if(!n||n.textContent.trim()!==x.name||li.querySelector('.lt-stale'))return;
        var c=document.createElement('span');c.className='lt-stale';c.textContent='⚠ '+md(x.src)+' 값';
        var now=li.querySelector('.l-now');(now||n).insertAdjacentElement('afterend',c)})});
  }
  var n=0,t=setInterval(function(){paint();if(++n>20)clearInterval(t)},500);paint();
}).catch(function(){});
}catch(e){}})();
