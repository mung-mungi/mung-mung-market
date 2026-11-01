// 유튜브 새 영상 배너(사용자 2026-11-02) — 자료 d/yt.json(Actions yt.yml이 30분마다 채널 RSS 확인)
// 메인 헤드라인 카드 바로 아래, 올라온 지 48시간 안 + 아직 안 닫은 영상만. 누르면 유튜브로, ✕면 그 영상은 다시 안 뜸
(function(){
if(!/\/(index\.html)?$/.test(location.pathname))return;
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function ago(t){var h=(Date.now()-t)/36e5;return h<1?'방금':h<24?Math.floor(h)+'시간 전':Math.floor(h/24)+'일 전'}
function put(v){if(document.querySelector('.mm-yt'))return true;var h=document.querySelector('header.bn');var hl=h&&h.nextElementSibling;if(!hl)return false;
 var a=document.createElement('a');a.className='mm-yt';a.href=v.url;a.target='_blank';a.rel='noopener';
 a.innerHTML='<span class="th"><img alt="" decoding="async"><i>▶</i></span><span class="tx"><small></small><b></b></span><button class="x" aria-label="닫기">✕</button>';
 a.querySelector('img').src=v.thumb;a.querySelector('small').textContent=(v.short?'새 쇼츠':'새 시황 영상')+' · '+ago(Date.parse(v.published));a.querySelector('b').textContent=v.title;
 a.addEventListener('click',function(){ls('mm_yt_seen',v.id)});
 a.querySelector('.x').onclick=function(e){e.preventDefault();e.stopPropagation();ls('mm_yt_seen',v.id);a.classList.add('bye');setTimeout(function(){a.remove()},250)};
 hl.after(a);return true}
fetch('d/yt.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(j){if(!j||!j.items||!j.items.length)return;
 var v=j.items.filter(function(x){return !x.short})[0]||j.items[0];var t=Date.parse(v.published);if(!t||Date.now()-t>48*36e5||ls('mm_yt_seen')===v.id)return;
 var k=0;(function go(){if(!put(v)&&++k<20)setTimeout(go,400)})()}).catch(function(){});
})();
