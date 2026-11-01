// 메인 맨 아래 '주인장 자료'(사용자 2026-11-01) — 비번(4자리)으로 여는 개인 검토함. 내용은 d/owner.enc.json(암호문)만 올라가 있고,
// 브라우저에서 비번으로 풀어 보여 줌. 주인장이 보고 골라서 전달사항 등으로 올리는 용도.
(function(){try{
if(!/\/(index\.html)?$/.test(location.pathname))return;
var K='mm-own-pin';
function sg(){try{return sessionStorage.getItem(K)||''}catch(e){return ''}}
function ss(v){try{if(v)sessionStorage.setItem(K,v);else sessionStorage.removeItem(K)}catch(e){}}
function ub(s){var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
var J=null;
function load(){return J?Promise.resolve(J):fetch('d/owner.enc.json?t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){J=j;return j})}
function dec(pin){return load().then(function(j){var C=window.crypto&&crypto.subtle;if(!C)throw 'nocrypto';
  return C.importKey('raw',new TextEncoder().encode(pin),'PBKDF2',false,['deriveKey']).then(function(k){
   return C.deriveKey({name:'PBKDF2',salt:ub(j.salt),iterations:j.iter,hash:'SHA-256'},k,{name:'AES-GCM',length:256},false,['decrypt'])}).then(function(key){
   return C.decrypt({name:'AES-GCM',iv:ub(j.iv)},key,ub(j.ct))}).then(function(b){return new TextDecoder().decode(b)})})}
function mount(){
 if(document.querySelector('.mm-own'))return true;
 var ft=document.querySelector('footer.foot');if(!ft)return false;
 var c=document.createElement('section');c.className='mm-own';
 c.innerHTML='<div class="mm-own-hd" role="button"><i>🔒</i><span><b>주인장 자료</b><small>비밀번호로 열립니다</small></span><em>열기 ›</em></div>'+
  '<div class="mm-own-lock"><p>비밀번호 4자리</p><div class="mm-own-dots"><s></s><s></s><s></s><s></s></div>'+
  '<input class="mm-own-in" type="password" inputmode="numeric" pattern="[0-9]*" maxlength="4" autocomplete="off" aria-label="비밀번호"><div class="mm-own-msg"></div></div>'+
  '<div class="mm-own-body"></div>';
 ft.parentNode.insertBefore(c,ft);
 var hd=c.querySelector('.mm-own-hd'),inp=c.querySelector('.mm-own-in'),msg=c.querySelector('.mm-own-msg'),body=c.querySelector('.mm-own-body'),dots=c.querySelectorAll('.mm-own-dots s');
 function paint(){var n=inp.value.length;dots.forEach(function(d,i){d.className=i<n?'on':''})}
 function show(html){var w=document.createElement('div');w.innerHTML=html;var src=w.querySelector('#mm-own-src');
  body.innerHTML=src?src.innerHTML:html;c.className='mm-own open unl';
  hd.querySelector('i').textContent='🔓';hd.querySelector('small').textContent=(src&&src.getAttribute('data-date')?src.getAttribute('data-date')+' 정리 · ':'')+'보고 골라서 올립니다';hd.querySelector('em').textContent='잠그기';
  body.querySelectorAll('.own-card .own-hd').forEach(function(h){h.setAttribute('role','button');h.onclick=function(){h.parentNode.classList.toggle('own-on')}})}
 function lock(){ss('');body.innerHTML='';c.className='mm-own';hd.querySelector('i').textContent='🔒';hd.querySelector('small').textContent='비밀번호로 열립니다';hd.querySelector('em').textContent='열기 ›';inp.value='';paint()}
 function tryPin(p,quiet){msg.textContent='여는 중…';return dec(p).then(function(h){ss(p);msg.textContent='';show(h)}).catch(function(e){
   if(quiet){ss('');msg.textContent='';return}
   msg.textContent=e==='nocrypto'?'이 브라우저에서는 열 수 없습니다':'비밀번호가 다릅니다';inp.value='';paint();
   var l=c.querySelector('.mm-own-lock');l.classList.remove('sh');void l.offsetWidth;l.classList.add('sh')})}
 hd.onclick=function(){if(c.classList.contains('unl')){lock();return}
  if(c.classList.contains('open')){c.className='mm-own';return}
  c.className='mm-own open';setTimeout(function(){try{inp.focus()}catch(e){}},60)};
 c.querySelector('.mm-own-dots').onclick=function(){try{inp.focus()}catch(e){}};
 inp.addEventListener('input',function(){inp.value=inp.value.replace(/\D/g,'').slice(0,4);paint();msg.textContent='';if(inp.value.length===4){inp.blur();tryPin(inp.value)}});
 var p=sg();if(p)tryPin(p,true);
 return true}
var k=0;(function go(){if(mount())return;if(++k<20)setTimeout(go,300)})();
}catch(e){}})();
