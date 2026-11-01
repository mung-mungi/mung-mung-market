(function(){
function run(){
  var h=null,hs=document.querySelectorAll('h1');
  for(var i=0;i<hs.length;i++){if(!hs[i].closest('.ib,.bn')){h=hs[i];break}}
  if(!h)return;var c=h.parentElement;if(!c||c===document.body)return;
  c.classList.add('mm-hero');h.classList.add('mm-h1');
  for(var k=c.firstElementChild;k;k=k.nextElementSibling){
    if(k===h||/^(META|SCRIPT|STYLE|LINK)$/.test(k.tagName))continue;
    var s=(k.className&&k.className.baseVal===undefined?k.className:'')+' '+k.id;
    k.classList.remove('mm-eb','mm-chip','mm-take','mm-x');
    if(/eyebrow|(^|[\s-])eb(\s|$)/.test(s))k.classList.add('mm-eb');
    else if(/take|chg/.test(s)){
      var t=(k.textContent||'').replace(/\s+/g,'');
      if(/chg/.test(s)&&(t===''||t==='—'))k.classList.add('mm-x');else{
        k.classList.add('mm-take');var f=k.firstElementChild;
        var n=k.firstChild;while(n&&n.nodeType===3&&!n.textContent.trim())n=n.nextSibling;if(f&&n===f&&(f.tagName==='B'||/chip|dl/.test(f.className||'')))f.classList.add('mm-chipx');}
    }
    else if(/date|chip|asof/.test(s))k.classList.add('mm-chip');
    else k.classList.add('mm-x');
  }
  var vs=document.querySelectorAll('[class*="-tile"]>.v');for(var j=0;j<vs.length;j++){var tx=(vs[j].textContent||'').trim();vs[j].classList.toggle('mm-vtxt',tx!==''&&!/^[\s+\-−~—]*[\d.]/.test(tx)&&tx!=='—')}
  var w=c.parentElement;
  if(w&&!document.querySelector('.mm-foot')){var p=document.createElement('p');p.className='mm-foot';p.textContent='참고용 정보이며 매수·매도 권유가 아닙니다.';w.appendChild(p)}
}
run();document.addEventListener('DOMContentLoaded',run);window.addEventListener('load',run);setTimeout(run,800);setTimeout(run,2500);
})();