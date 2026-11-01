(function(){
  // 홈으로 가거나 '뒤로'일 때는 반대 방향(오른쪽으로 빠짐)
  window.addEventListener('pagereveal', function(e){
    if (!e.viewTransition) return;
    var back = false;
    try {
      var a = window.navigation && navigation.activation;
      if (a) { back = a.navigationType === 'traverse' && a.from && a.entry && a.entry.index < a.from.index; if (!back && /\/(index\.html)?$/.test(new URL(a.entry.url).pathname)) back = true; }
      else back = /\/(index\.html)?$/.test(location.pathname);
    } catch (x) {}
    if (back) { document.documentElement.classList.add('mm-back'); e.viewTransition.finished.finally(function(){ document.documentElement.classList.remove('mm-back'); }); }
  });
})();
