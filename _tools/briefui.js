/* 데일리 시황 통일 양식(사용자 2026-11-02) — 맨 위 오늘 카드 날짜 줄, 출처 매체 알약, 공포·탐욕 설명 접기 */
(function(){
var WD=['일','월','화','수','목','금','토'];
function kst(){var n=new Date(Date.now()+9*36e5);return n}
function top(){
  var t=document.getElementById('take');if(!t||!t.classList.contains('np'))return;
  var ms=t.querySelector('.np-mast>span');if(ms&&ms.textContent!=='오늘의 시황')ms.textContent='오늘의 시황';var em=t.querySelector('.np-mast>em');if(em&&em.querySelector('br'))em.textContent='AI 밸류체인 · 아침판';
  if(t.querySelector('.mm-td'))return;
  var ln=t.querySelector('.np-line span');if(!ln)return;
  var m=/(\d{1,2})\.(\d{1,2})/.exec(ln.textContent);if(!m)return;
  var now=kst(),y=now.getUTCFullYear(),mo=+m[1],d=+m[2];if(mo>now.getUTCMonth()+2)y--;
  var u=Date.UTC(y,mo-1,d),wd=new Date(u).getUTCDay(),t0=Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate()),k=Math.round((t0-u)/864e5);
  var e=document.createElement('div');e.className='mm-td';
  e.innerHTML='<span class="mm-dd-n"></span><span class="mm-dd-w"></span><span class="mm-dd-s">한국 아침 발행</span><span class="mm-dd-r"></span>';
  e.children[0].textContent=mo+'.'+String(d).padStart(2,'0');
  e.children[1].textContent=WD[wd];if(wd===6)e.children[1].classList.add('sat');if(wd===0)e.children[1].classList.add('sun');
  var r=e.children[3];r.textContent=k<=0?'오늘 아침':k===1?'어제':k+'일 전';r.classList.add(k<=0?'now':k>=2?'old':'x');
  var hd=t.querySelector('.np-hd');t.insertBefore(e,hd||t.firstChild.nextSibling);
}
function src(){
  document.querySelectorAll('#days a[href^="http"]:not(.mm-src)').forEach(function(a){
    var tx=(a.textContent||'').trim();if(!/^https?:\/\//.test(tx))return;
    var h;try{h=new URL(a.href).hostname.replace(/^www\./,'')}catch(e){return}
    a.textContent='🔗 '+h;a.classList.add('mm-src');a.title=a.href;
  });
}
function fg(){
  document.querySelectorAll('.mm-fg-cap').forEach(function(c){
    var b=c.previousElementSibling;if(b&&b.classList.contains('mm-fgx'))return;
    b=document.createElement('button');b.type='button';b.className='mm-fgx';b.textContent='▸ 이렇게 읽습니다 · 눌러서 펼치기';
    b.onclick=function(){var o=b.classList.toggle('op');b.textContent=o?'▾ 이렇게 읽습니다 · 접기':'▸ 이렇게 읽습니다 · 눌러서 펼치기'};
    c.parentNode.insertBefore(b,c);
  });
}
function all(){top();src();fg()}
var k=0;(function go(){all();['take','days'].forEach(function(id){var el=document.getElementById(id);if(el&&!el.__bui){el.__bui=1;new MutationObserver(all).observe(el,{childList:true,subtree:true})}});if(++k<16)setTimeout(go,500)})();
})();
