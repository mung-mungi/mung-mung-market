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
  if(sg('mm-ntc-closed')===id||lg('mm-ntc-hide')===id+'|'+today())return;
  function open(){
    if(document.getElementById('mm-splash')){setTimeout(open,400);return}
    var p=document.createElement('div');p.className='mm-ntc-pop';
    p.innerHTML='<div class="mm-ntc-sheet"><div class="mm-ntc-top"><span class="chip">📌 전달사항 · '+dt+'</span><span class="x" role="button" aria-label="닫기">✕</span></div><div class="mm-ntc-scroll"><h3></h3><div class="mm-ntcb"></div></div><div class="mm-ntc-bot"><button class="d">오늘 하루 안 보기</button><button class="c">닫기</button></div></div>';
    p.querySelector('h3').textContent=tt;p.querySelector('.mm-ntcb').innerHTML=body;
    function shut(hide){ss('mm-ntc-closed',id);if(hide)ls('mm-ntc-hide',id+'|'+today());p.classList.remove('on');document.documentElement.classList.remove('mm-ntc-lock');setTimeout(function(){p.remove()},300)}
    p.querySelector('.x').addEventListener('click',function(){shut(false)});
    p.querySelector('.c').addEventListener('click',function(){shut(false)});
    p.querySelector('.d').addEventListener('click',function(){shut(true)});
    p.addEventListener('click',function(e){if(e.target===p)shut(false)});
    document.body.appendChild(p);document.documentElement.classList.add('mm-ntc-lock');
    requestAnimationFrame(function(){p.classList.add('on')})}
  setTimeout(open,300);
}).catch(function(){});
}catch(e){}})();
