// 시장 경고등: 맨 위 바로가기 칩 + 주제가 바뀌는 곳마다 구분띠(사용자 2026-11-02)
(function(){
var L=[['mm-semi','반도체·기술'],['big','경고등 점수'],['mm-sector','돈은 어디로'],['area-card','영역별 상세'],['mm-emo','투자자 심리'],['mm-sys','금융 시스템'],['hist-card','1년 기록']];
var N='①②③④⑤⑥⑦⑧';
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
function jump(id){var b=document.querySelector('[data-mmband="'+id+'"]')||document.getElementById(id);if(!b)return;scrollTo({top:b.getBoundingClientRect().top+scrollY-8,behavior:'smooth'})}
function run(){var have=L.filter(function(a){var e=document.getElementById(a[0]);return e&&e.offsetParent!==null});if(have.length<3)return false;
 have.forEach(function(a,i){var e=document.getElementById(a[0]);var b=document.querySelector('[data-mmband="'+a[0]+'"]');var lab=N[i]+' '+a[1];
  if(b&&b.nextElementSibling===e&&b.textContent===lab)return;if(b)b.remove();b=el('div','mm-band');b.dataset.mmband=a[0];b.appendChild(el('span','',lab));e.before(b)});
 var hero=document.querySelector('.mm-st-hero');var j=document.querySelector('.mm-jump');var sig=have.map(function(a){return a[0]}).join(',');
 if(hero&&(!j||j.dataset.sig!==sig)){if(j)j.remove();j=el('nav','mm-jump');j.dataset.sig=sig;j.setAttribute('aria-label','바로가기');
  have.forEach(function(a,i){var x=el('a','',N[i]+' '+a[1]);x.href='#'+a[0];x.onclick=function(ev){ev.preventDefault();jump(a[0])};j.appendChild(x)});hero.appendChild(j)}
 return true}
var k=0;(function go(){try{run()}catch(e){}if(++k<30)setTimeout(go,500)})();
})();
