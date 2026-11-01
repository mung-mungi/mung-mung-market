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
function dec(pin){return load().then(function(j){return decJ(j,pin)})}
function decJ(j,pin){return Promise.resolve().then(function(){var C=window.crypto&&crypto.subtle;if(!C)throw 'nocrypto';
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
  body.querySelectorAll('.own-card .own-hd').forEach(function(h){h.setAttribute('role','button');h.onclick=function(){h.parentNode.classList.toggle('own-on')}});
  body.querySelectorAll('.own-col').forEach(function(col){var m=col.querySelector('.own-col-more');if(!m)return;m.setAttribute('role','button');
   m.onclick=function(){var o=col.classList.toggle('own-col-open');m.textContent=o?'▲ 칼럼 접기':'▼ 칼럼 전체 펼치기';if(!o)col.scrollIntoView({block:'start',behavior:'smooth'})}})}
 function lock(){ss('');body.innerHTML='';c.className='mm-own';hd.querySelector('i').textContent='🔒';hd.querySelector('small').textContent='비밀번호로 열립니다';hd.querySelector('em').textContent='열기 ›';inp.value='';paint()}
 function tryPin(p,quiet){msg.textContent='여는 중…';return dec(p).then(function(h){ss(p);msg.textContent='';show(h);draft(p)}).catch(function(e){
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
// 🧪 검수 대기(속보 배너 키트, 2026-11-01) — d/notice_draft.enc.json(같은 비번)을 풀어 맨 위에: 초안(점수·이유·미리보기) + 후보(5~6점) + 점수 기준
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function scoreHtml(x,R){var sc=x.score||{},why=sc.why||{},h='<div class="own-sc"><div class="own-sc-top"><b>'+(x.total||0)+'</b><span>/10</span><em class="lv-'+esc(x.level)+'">'+esc(x.level)+'</em>'+(sc.force?'<i>⚡ '+esc(sc.force)+'</i>':'')+'</div>';
 (R||[]).forEach(function(r){var v=+sc[r[0]]||0;h+='<div class="own-sc-r"><span>'+esc(r[1])+'</span><s class="v'+v+'"><u></u><u></u></s><small>'+(why[r[0]]?esc(why[r[0]]):'')+'</small></div>'});
 return h+'</div>'}
function popup(tt,dt,inner){var p=document.createElement('div');p.className='mm-ntc-pop';
 p.innerHTML='<div class="mm-ntc-sheet"><div class="mm-ntc-top"><span class="chip">🧪 검수용 미리보기 · '+esc(dt)+'</span><span class="x" role="button" aria-label="닫기">✕</span></div><div class="mm-ntc-scroll"><h3></h3><div class="mm-ntcb"></div></div><div class="mm-ntc-bot"><button class="c">닫기</button></div></div>';
 p.querySelector('h3').textContent=tt;p.querySelector('.mm-ntcb').innerHTML=inner;
 function shut(){p.classList.remove('on');document.documentElement.classList.remove('mm-ntc-lock');setTimeout(function(){p.remove()},300)}
 p.querySelector('.x').onclick=shut;p.querySelector('.c').onclick=shut;p.addEventListener('click',function(e){if(e.target===p)shut()});
 document.body.appendChild(p);document.documentElement.classList.add('mm-ntc-lock');requestAnimationFrame(function(){p.classList.add('on')})}
function draft(pin){fetch('d/notice_draft.enc.json?t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){return decJ(j,pin)}).then(function(t){
 var body=document.querySelector('.mm-own-body');if(!body||body.querySelector('.own-draft'))return;
 var B;try{B=JSON.parse(t)}catch(e){B={drafts:[{title:'',html:t}],cands:[]}}
 var R=B.rubric||[],box=document.createElement('div');box.className='own-drafts';
 (B.drafts||[]).forEach(function(x){
  var w=document.createElement('div');w.innerHTML=x.html||'';var src=w.querySelector('#mm-ntc-src');if(!src)return;
  var tt=x.title||src.getAttribute('data-title')||'초안',dt=x.date||src.getAttribute('data-date')||'';
  var c=document.createElement('div');c.className='own-card own-test own-draft own-on';
  c.innerHTML='<div class="own-hd" role="button"><span class="own-dr-chip">🧪 검수 대기 · 배너 초안</span><span class="own-dr-at">'+esc(x.at||'')+' 작성</span><b></b></div><div class="own-b">'+scoreHtml(x,R)+
   '<div class="own-dr-btns"><button class="own-dr-pop">📱 배너로 띄워 보기</button><button class="own-dr-in">본문 펼치기 ▾</button></div><div class="own-dr-body mm-ntcb" hidden></div>'+
   '<p class="own-dr-how">괜찮으면 대화창에 <b>배너 공개</b>, 고칠 곳은 그대로 말해 주세요. 공개 전에는 주인장만 봅니다.</p></div>';
  c.querySelector('b').textContent=tt+(dt?' · '+dt:'');
  var bd=c.querySelector('.own-dr-body');bd.innerHTML=src.innerHTML;
  c.querySelector('.own-hd').onclick=function(){c.classList.toggle('own-on')};
  c.querySelector('.own-dr-in').onclick=function(){bd.hidden=!bd.hidden;this.textContent=bd.hidden?'본문 펼치기 ▾':'본문 접기 ▴'};
  c.querySelector('.own-dr-pop').onclick=function(){popup(tt,dt,src.innerHTML)};
  box.appendChild(c)});
 if((B.cands||[]).length){var c=document.createElement('div');c.className='own-card own-test own-draft own-cands own-on';
  var h='<div class="own-hd" role="button"><span class="own-dr-chip c">후보 '+B.cands.length+'건 · 5~6점</span><b>보시고 올리라고 하면 배너로 만듭니다</b></div><div class="own-b">';
  B.cands.forEach(function(x){h+='<details class="own-cd"><summary role="button"><em class="lv-'+esc(x.level)+'">'+(x.total||0)+'</em><span>'+esc(x.title)+'</span><i>'+esc(x.at||'')+'</i></summary>'+scoreHtml(x,R)+(x.note?'<p class="own-dr-how">'+esc(x.note)+'</p>':'')+'</details>'});
  c.innerHTML=h+'</div>';c.querySelector('.own-hd').onclick=function(){c.classList.toggle('own-on')};box.appendChild(c)}
 if(!box.children.length)return;
 var rb=document.createElement('details');rb.className='own-rule';
 rb.innerHTML='<summary role="button">▸ 배너 올리는 기준 · 점수표</summary><div><p><b>원칙</b> 오늘 안 보면 판단이 틀어질 일만 배너로. 7점 이상 초안, 5~6 후보, 4 이하 타임라인만.</p><p><b>무조건</b> '+(B.force||[]).map(esc).join(' · ')+'</p>'+
  R.map(function(r){return '<p><b>'+esc(r[1])+'</b> '+esc(r[2])+'</p>'}).join('')+'<p><b>피로 막기</b> 하루 최대 2개 · 같은 주제는 새 배너 대신 갱신 · 실적은 제외(판을 바꿀 때만) · 날짜 지나면 내림</p></div>';
 box.appendChild(rb);
 body.insertBefore(box,body.firstChild)}).catch(function(){})}
// 잠긴 상태에서도 '검수 대기 n건'만 표시(제목·내용은 잠금 안)
function badge(){fetch('d/notice_draft.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(m){
 var c=document.querySelector('.mm-own');if(!c||!m||!(m.n||m.c))return;var hd=c.querySelector('.mm-own-hd');if(!hd||hd.querySelector('.own-dr-badge'))return;
 var b=document.createElement('span');b.className='own-dr-badge';b.textContent='🧪 검수 대기 '+(m.n||0)+(m.c?' · 후보 '+m.c:'');hd.querySelector('span').appendChild(b)}).catch(function(){})}
var k=0;(function go(){if(mount()){badge();return}if(++k<20)setTimeout(go,300)})();
}catch(e){}})();
