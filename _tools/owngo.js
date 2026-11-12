// 주인장 보고 알림을 누르면 주인장 칸으로(사용자 2026-11-12) — index.html#own
(function(){
  function go(){if(!/^#own/.test(location.hash))return;var n=0;(function w(){var b=document.querySelector('.mm-own');if(!b){if(++n<40)setTimeout(w,300);return}
    if(!b.classList.contains('open')){var h=b.querySelector('[role=button],.own-hd,summary,h3');if(h)h.click()}
    function sc(){var y=b.getBoundingClientRect().top+scrollY-60;scrollTo({top:y<0?0:y,behavior:'smooth'})}setTimeout(sc,300);setTimeout(sc,1800)})()}
  addEventListener('hashchange',go);if(document.readyState==='complete')go();else addEventListener('load',go);
})();
