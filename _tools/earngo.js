// 실적 알림을 누르면 그 노트로(사용자 2026-11-12 '누르면 넘어가는 거 저번에도 문제') — p-earn.html#<노트 id>
// 노트는 DB에서 늦게 그려지므로 나올 때까지 기다렸다가 펼치고·화면 위로·잠깐 반짝임. 앱이 이미 열려 있으면 hashchange로 같은 동작
(function(){
  function go(){
    var id=(location.hash||'').slice(1);if(!/^[\w.-]+$/.test(id))return;var n=0;
    (function wait(){
      var a=document.getElementById(id);
      if(!a||a.tagName!=='ARTICLE'){if(++n<50)setTimeout(wait,300);return}
      if(a.hidden){var r=document.querySelector('#fc button,#fc .reset');if(r)r.click();a.hidden=false}
      if(a.classList.contains('fold')){a.classList.remove('fold');var s=a.querySelector('.sumrow');if(s){s.setAttribute('aria-expanded','true');var ar=s.querySelector('.ar');if(ar)ar.textContent='접기 ▴'}}
      setTimeout(function(){var y=a.getBoundingClientRect().top+scrollY-64;scrollTo({top:y<0?0:y,behavior:'smooth'});a.classList.add('mm-go-flash');setTimeout(function(){a.classList.remove('mm-go-flash')},2200)},n?250:600)
    })()
  }
  addEventListener('hashchange',go);
  if(document.readyState==='complete')go();else addEventListener('load',go);
})();
