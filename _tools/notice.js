// 메인 전달사항(사용자 2026-10-31) — 들어오면 전체 화면 공지로 한 번(✕·오늘 하루 안 보기), 닫으면 메인에 접힌 한 줄로 남김.
// 내용은 d/notice.html 한 곳만 고치면 됨(data-id를 바꾸면 다시 띄움, data-on="0"이면 내림)
(function(){try{
if(!/\/(index\.html)?$/.test(location.pathname))return;
function today(){var d=new Date(Date.now()+9*3600e3);return d.toISOString().slice(0,10)}
function lg(k){try{return localStorage.getItem(k)||''}catch(e){return ''}}
function ls(k,v){try{localStorage.setItem(k,v)}catch(e){}}
function sg(k){try{return sessionStorage.getItem(k)||''}catch(e){return ''}}
function ss(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}
fetch('d/notice.html?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.text()}).then(function(h){
  var w=document.createElement('div');w.innerHTML=h;var src=w.querySelector('#mm-ntc-src');
  if(!src||src.getAttribute('data-on')!=='1')return;
  // 하루 지나면 배너에서 뺌(사용자 2026-11-03) — data-at(올린 시각, ISO)이 있으면 그 시각부터 24시간, 없으면 data-date(M.D) 한국 정오 기준 24시간
  var at=src.getAttribute('data-at'),t0=at?Date.parse(at):NaN;
  if(isNaN(t0)){var m=/^(\d{1,2})\.(\d{1,2})/.exec(src.getAttribute('data-date')||'');if(m){var y=new Date(Date.now()+9*3600e3).getUTCFullYear(),mo=+m[1];if(mo>new Date(Date.now()+9*3600e3).getUTCMonth()+2)y--;t0=Date.UTC(y,mo-1,+m[2],3,0)}}
  if(!isNaN(t0)&&Date.now()-t0>24*3600e3)return;
  var id=src.getAttribute('data-id')||'',dt=src.getAttribute('data-date')||'',tt=src.getAttribute('data-title')||'전달사항',body=src.innerHTML;
  // 1) 메인 접힌 한 줄
  var card=document.createElement('div');card.className='mm-ntc';
  card.innerHTML='<div class="mm-ntc-hd" role="button"><span class="chip">📌 전달사항 · '+dt+'</span><b></b><em>펼치기 ▾</em></div><div class="mm-ntcb"></div>';
  card.querySelector('b').textContent=tt;card.querySelector('.mm-ntcb').innerHTML=body;
  card.querySelector('.mm-ntc-hd').addEventListener('click',function(){var o=card.classList.toggle('open');card.querySelector('em').textContent=o?'접기 ▴':'펼치기 ▾'});
  function place(){
    var sh=document.querySelector('p.sh');if(!sh)return false;var box=sh.parentElement;
    var ref=document.querySelector('.mm-earnnew')||document.querySelector('.mm-push:not(.bot)')||box;
    if(ref.parentElement!==box.parentElement)ref=box;
    if(card.nextElementSibling!==ref||card.parentElement!==ref.parentElement)ref.parentElement.insertBefore(card,ref);
    return true}
  var n=0,t=setInterval(function(){place();if(++n>15)clearInterval(t)},700);place();
  // 2) 전체 화면 공지 — 이번 창에서 닫았거나 '오늘 하루 안 보기'면 안 띄움
  // 알림을 눌러 들어오면(#ntc) 닫았던 적이 있어도 다시 띄움 · 앱이 이미 열려 있으면 hashchange로 다시 띄움(사용자 2026-11-12 '알림 눌렀는데 이동 안 함')
  var forced=/^#ntc/.test(location.hash);
  addEventListener('hashchange',function(){if(/^#ntc/.test(location.hash)&&!document.querySelector('.mm-ntc-pop'))open()});
  if(!forced&&(sg('mm-ntc-closed')===id||lg('mm-ntc-hide')===id+'|'+today()))return;
  function open(){
    if(document.getElementById('mm-splash')){setTimeout(open,400);return}
    var p=document.createElement('div');p.className='mm-ntc-pop';
    p.innerHTML='<div class="mm-ntc-sheet"><div class="mm-ntc-top"><span class="chip">📌 전달사항 · '+dt+'</span><span class="x" role="button" aria-label="닫기">✕</span></div><div class="mm-ntc-scroll"><h3></h3><div class="mm-ntcb"></div></div><div class="mm-ntc-bot"><button class="d">오늘 하루 안 보기</button><button class="c">닫기</button></div></div>';
    p.querySelector('h3').textContent=tt;p.querySelector('.mm-ntcb').innerHTML=body;
    function shut(hide){try{if(/^#ntc/.test(location.hash))history.replaceState(null,'',location.pathname+location.search)}catch(e){}ss('mm-ntc-closed',id);if(hide)ls('mm-ntc-hide',id+'|'+today());p.classList.remove('on');document.documentElement.classList.remove('mm-ntc-lock');setTimeout(function(){p.remove()},300)}
    p.querySelector('.x').addEventListener('click',function(){shut(false)});
    p.querySelector('.c').addEventListener('click',function(){shut(false)});
    p.querySelector('.d').addEventListener('click',function(){shut(true)});
    p.addEventListener('click',function(e){if(e.target===p)shut(false)});
    document.body.appendChild(p);document.documentElement.classList.add('mm-ntc-lock');
    requestAnimationFrame(function(){p.classList.add('on')})}
  setTimeout(open,300);
}).catch(function(){});
}catch(e){}})();
