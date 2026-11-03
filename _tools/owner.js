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
 function tryPin(p,quiet){msg.textContent='여는 중…';return dec(p).then(function(h){ss(p);msg.textContent='';show(h);draft(p);ownTag();report()}).catch(function(e){
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
// 자동 초안 받은편지함(2026-11-02): 예약 작업은 비번 없이 공개키로만 잠가 d/notice_inbox.json에 넣고, 여기서 비번으로 개인키를 풀어 합침
function inbox(pin,t){var C=crypto.subtle;return Promise.all([fetch('d/notice_inbox.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():[]}).catch(function(){return []}),fetch('d/notice_key.enc.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})]).then(function(a){var L=a[0]||[],K=a[1];if(!L.length||!K)return t;
 return decJ(K,pin).then(function(pk){return C.importKey('pkcs8',ub(pk),{name:'RSA-OAEP',hash:'SHA-256'},false,['decrypt'])}).then(function(rk){
  return Promise.all(L.map(function(e){return C.decrypt({name:'RSA-OAEP'},rk,ub(e.k)).then(function(raw){return C.importKey('raw',raw,'AES-GCM',false,['decrypt'])}).then(function(ak){return C.decrypt({name:'AES-GCM',iv:ub(e.iv)},ak,ub(e.ct))}).then(function(b){return JSON.parse(new TextDecoder().decode(b))}).catch(function(){return null})}))}).then(function(M){
  var B;try{B=JSON.parse(t)}catch(e){B={drafts:[],cands:[]}}B.drafts=B.drafts||[];B.cands=B.cands||[];B.log=B.log||[];
  M.filter(Boolean).reverse().forEach(function(m){var x=m.item,k=m.kind;B.drafts=B.drafts.filter(function(y){return y.id!==x.id});B.cands=B.cands.filter(function(y){return y.id!==x.id});
   if(k==='draft')B.drafts.unshift(x);else if(k==='cand')B.cands.unshift(x);if(m.log)B.log.unshift(m.log)});B.log=B.log.slice(0,30);B.cands=B.cands.slice(0,8);return JSON.stringify(B)})}).catch(function(){return t})}
// ── 주인장만 울리는 알림(사용자 2026-11-03): 비번이 맞은 기기의 알림 구독에 '주인장' 표시(mm_owner=1)를 붙임
//    주인장 칸에 새 글이 올라오면 owner_push.yml이 이 표시가 있는 기기에만 보냄(지인 폰은 안 울림)
function ownTag(){try{localStorage.setItem('mm-owner','1')}catch(e){}var n=0;ownNote('🔔 주인장 알림 확인 중…',0);(function w(){var O=window.OneSignal;
 try{if(O&&O.User&&O.User.PushSubscription&&O.User.PushSubscription.id&&O.User.PushSubscription.optedIn!==false){O.User.addTag('mm_owner','1');ownNote('🔔 이 기기는 주인장 알림을 받습니다',1);return}}catch(e){}
 if(++n<16)setTimeout(w,500);else ownNote('🔕 주인장 알림 켜기 — 눌러 주세요',2)})()}
function ownNote(t,st){var b=document.querySelector('.mm-own-body');if(!b)return;var e=b.querySelector('.own-tagnote');
 if(!e){e=document.createElement('button');e.type='button';e.className='own-tagnote';b.insertBefore(e,b.firstChild);
  e.onclick=function(){if(e.dataset.st==='1'){ownTag();return}if(e.dataset.st==='0')return;
   if(!window.mmPushSub){ownNote('홈 화면에 추가한 멍터 앱에서 열어야 알림을 켤 수 있습니다',3);return}
   ownNote('🔔 알림 허용 창을 띄웁니다…',0);window.mmPushSub(function(ok){if(ok==='cant'){ownNote('아이폰은 홈 화면에 추가한 멍터 앱에서만 알림이 됩니다 — 앱으로 열어 주세요',3);return}if(ok===false){ownNote('🔕 알림이 허용되지 않았습니다 — 설정 › 알림에서 멍터를 켠 뒤 다시 눌러 주세요',2);return}setTimeout(ownTag,800)})}}
 e.textContent=t;e.dataset.st=String(st==null?1:st);e.classList.toggle('on',st===1);e.classList.toggle('off',st===2||st===3)}
// ── 배너에서 바로 공개 + 전체 알림(사용자 2026-11-03): 이 기기에 한 번 등록한 GitHub 열쇠로 d/notice.html을 올리고 push-notice를 실행
//    열쇠는 저장소에 올라가지 않고, 이 기기 브라우저에만 비번으로 잠가 둠(mm-own-gh)
var GH='https://api.github.com/repos/mung-mungi/mung-mung-market';
function encJ(txt,pin){var C=crypto.subtle,salt=crypto.getRandomValues(new Uint8Array(16)),iv=crypto.getRandomValues(new Uint8Array(12)),it=310000;
 return C.importKey('raw',new TextEncoder().encode(pin),'PBKDF2',false,['deriveKey']).then(function(k){return C.deriveKey({name:'PBKDF2',salt:salt,iterations:it,hash:'SHA-256'},k,{name:'AES-GCM',length:256},false,['encrypt'])})
 .then(function(key){return C.encrypt({name:'AES-GCM',iv:iv},key,new TextEncoder().encode(txt))}).then(function(ct){function b(u){u=new Uint8Array(u);var s='';for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s)}
  return {iter:it,salt:b(salt),iv:b(iv),ct:b(ct)}})}
function ghKey(pin){var j;try{j=JSON.parse(localStorage.getItem('mm-own-gh')||'null')}catch(e){}return j?decJ(j,pin):Promise.reject('nokey')}
function gh(tok,path,opt){opt=opt||{};opt.headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'};
 return fetch(GH+path,opt).then(function(r){if(r.status===204)return {};return r.json().then(function(j){if(!r.ok)throw (r.status+' '+(j.message||''));return j})})}
function b64u(s){var u=new TextEncoder().encode(s),o='';for(var i=0;i<u.length;i+=32768)o+=String.fromCharCode.apply(null,u.subarray(i,i+32768));return btoa(o)}
function sendUI(c,x,src,tt,pin){var btn=c.querySelector('.own-dr-send'),m=c.querySelector('.own-send-msg'),armed=false;
 fetch('d/notice.html?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.text()}).then(function(h){if(h.indexOf('data-id="'+(src.getAttribute('data-id')||x.id)+'"')>0&&/data-on="1"/.test(h)){btn.textContent='✅ 이미 공개됨';btn.disabled=true}}).catch(function(){});
 function keyForm(){m.innerHTML='<div class="own-key"><b>🔑 보내기 열쇠 등록 (기기마다 한 번)</b><p>GitHub → Settings → Developer settings → Fine-grained tokens에서 <b>mung-mung-market 저장소만</b> 고르고 권한 <b>Contents: Read and write</b>, <b>Actions: Read and write</b>로 만든 토큰을 붙여 넣으세요. 이 기기에만 비번으로 잠가 저장되고 저장소에는 올라가지 않습니다.</p><input type="password" autocomplete="off" placeholder="github_pat_…"><button>저장</button></div>';
  var i=m.querySelector('input');m.querySelector('button').onclick=function(){var v=i.value.trim();if(!/^(github_pat_|ghp_)/.test(v)){i.value='';i.placeholder='토큰 모양이 아닙니다';return}
   encJ(v,pin).then(function(j){try{localStorage.setItem('mm-own-gh',JSON.stringify(j))}catch(e){}m.textContent='🔑 등록됐습니다. 다시 눌러 보내세요.'})}}
 btn.onclick=function(){
  if(!armed){armed=true;btn.textContent='한 번 더 누르면 지인 전체에게 공개·알림';btn.classList.add('armed');setTimeout(function(){if(armed&&!btn.disabled){armed=false;btn.textContent='📢 공개 + 전체 알림 보내기';btn.classList.remove('armed')}},6000);return}
  armed=false;btn.disabled=true;btn.classList.remove('armed');btn.textContent='보내는 중…';
  ghKey(pin).then(function(tok){
   var now=new Date(Date.now()+9*3600e3).toISOString().slice(0,16)+'+09:00',html=x.html;
   html=/data-at="[^"]*"/.test(html)?html.replace(/data-at="[^"]*"/,'data-at="'+now+'"'):html.replace('<div id="mm-ntc-src"','<div id="mm-ntc-src" data-at="'+now+'"');
   var first=(src.querySelector('.ntc-c')||src.querySelector('.nc-new b')||{}).textContent||'';first=first.replace(/^[①②③④]\s*/,'').trim().slice(0,120)||'멍뭉 터미널 전달사항이 올라왔습니다.';
   m.textContent='① 배너 올리는 중…';
   function put(n){return gh(tok,'/contents/d/notice.html').then(function(f){return gh(tok,'/contents/d/notice.html',{method:'PUT',body:JSON.stringify({message:'전달사항 공개(주인장 칸에서): '+tt,content:b64u(html),sha:f.sha})})}).catch(function(e){if(n<2&&/^409/.test(String(e)))return put(n+1);throw e})}
   return put(0).then(function(){m.textContent='② 전체 알림 보내는 중…';return gh(tok,'/actions/workflows/push_notice.yml/dispatches',{method:'POST',body:JSON.stringify({ref:'main',inputs:{title:'📢 '+tt,msg:first,path:'index.html'}})})})
    .then(function(){btn.textContent='✅ 공개됨 · 알림 보냄';m.textContent='1~2분 뒤 사이트에 배너가 뜨고 알림이 갑니다.'})})
  .catch(function(e){btn.disabled=false;btn.textContent='📢 공개 + 전체 알림 보내기';if(e==='nokey'){keyForm();return}
   m.textContent='보내지 못했습니다: '+e+(/^40[13]/.test(String(e))?' — 열쇠 권한·기한을 확인하세요':'');if(/^401/.test(String(e))){try{localStorage.removeItem('mm-own-gh')}catch(_){}}})}}
// ── 작업 보고(사용자 2026-11-03): Claude가 단계마다 d/report/log.json에 한 줄씩 남기면 주인장 칸 맨 위에 '오늘 작업 보고'로 보여 줌
function report(){fetch('d/report/log.json?t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){
 var b=document.querySelector('.mm-own-body');if(!b||!j||!(j.items||[]).length)return;var old=b.querySelector('.own-rep');if(old)old.remove();
 var e=document.createElement('div');e.className='own-rep';
 e.innerHTML='<div class="own-rep-hd">🐾 작업 보고 <small>'+esc(j.date||'')+'</small></div>'+j.items.slice(-12).map(function(x){
  return '<div class="own-rep-r'+(/⚠/.test(x.s||'')?' warn':'')+'"><span class="t">'+esc(x.t||'')+'</span><span class="s">'+esc(x.s||'')+'</span><span class="m">'+esc(x.msg||'')+'</span></div>'}).join('')+
  (j.note?'<p class="own-rep-note">'+esc(j.note)+'</p>':'');
 var tn=b.querySelector('.own-tagnote');b.insertBefore(e,tn?tn.nextSibling:b.firstChild)}).catch(function(){})}
function draft(pin){fetch('d/notice_draft.enc.json?t='+Date.now(),{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){return decJ(j,pin)}).then(function(t){return inbox(pin,t)}).then(function(t){
 var body=document.querySelector('.mm-own-body');if(!body||body.querySelector('.own-draft'))return;
 var B;try{B=JSON.parse(t)}catch(e){B={drafts:[{title:'',html:t}],cands:[]}}
 var R=B.rubric||[],box=document.createElement('div');box.className='own-drafts';
 (B.drafts||[]).forEach(function(x){
  var w=document.createElement('div');w.innerHTML=x.html||'';var src=w.querySelector('#mm-ntc-src');if(!src)return;
  var tt=x.title||src.getAttribute('data-title')||'초안',dt=x.date||src.getAttribute('data-date')||'';
  var c=document.createElement('div');c.className='own-card own-test own-draft';
  c.innerHTML='<div class="own-hd" role="button"><span class="own-dr-chip">🧪 검수 대기 · 배너 초안</span><span class="own-dr-at">'+esc(x.at||'')+' 작성</span><b></b></div><div class="own-b">'+scoreHtml(x,R)+
   '<div class="own-dr-btns"><button class="own-dr-pop">📱 배너로 띄워 보기</button><button class="own-dr-in">본문 펼치기 ▾</button></div><div class="own-dr-body mm-ntcb" hidden></div>'+
   '<div class="own-send"><button class="own-dr-send">📢 공개 + 전체 알림 보내기</button><div class="own-send-msg"></div></div>'+
   '<p class="own-dr-how">여기서 바로 보내거나, 대화창에 <b>배너 공개</b>라고 해도 됩니다. 고칠 곳은 대화창에 말해 주세요. 공개 전에는 주인장만 봅니다.</p><button type="button" class="own-fold">접기 ▴</button></div>';
  c.querySelector('b').textContent=tt+(dt?' · '+dt:'');
  var bd=c.querySelector('.own-dr-body');bd.innerHTML=src.innerHTML;
  c.querySelector('.own-hd').onclick=function(){c.classList.toggle('own-on')};
  c.querySelector('.own-fold').onclick=function(){c.classList.remove('own-on');c.scrollIntoView({block:'nearest',behavior:'smooth'})};
  c.querySelector('.own-dr-in').onclick=function(){bd.hidden=!bd.hidden;this.textContent=bd.hidden?'본문 펼치기 ▾':'본문 접기 ▴'};
  c.querySelector('.own-dr-pop').onclick=function(){popup(tt,dt,src.innerHTML)};
  sendUI(c,x,src,tt,pin);
  box.appendChild(c)});
 if((B.cands||[]).length){var c=document.createElement('div');c.className='own-card own-test own-draft own-cands';
  var h='<div class="own-hd" role="button"><span class="own-dr-chip c">후보 '+B.cands.length+'건 · 5~6점</span><b>보시고 올리라고 하면 배너로 만듭니다</b></div><div class="own-b">';
  B.cands.forEach(function(x){h+='<details class="own-cd"><summary role="button"><em class="lv-'+esc(x.level)+'">'+(x.total||0)+'</em><span>'+esc(x.title)+'</span><i>'+esc(x.at||'')+'</i></summary>'+scoreHtml(x,R)+(x.note?'<p class="own-dr-how">'+esc(x.note)+'</p>':'')+'</details>'});
  c.innerHTML=h+'</div>';c.querySelector('.own-hd').onclick=function(){c.classList.toggle('own-on')};box.appendChild(c)}
 if((B.log||[]).length){var lg=document.createElement('details');lg.className='own-rule own-log';
  lg.innerHTML='<summary role="button">▸ 판정 기록 · 최근 '+B.log.length+'건 (시험 기간: 너무 자주 울리는지 보기)</summary><div>'+B.log.map(function(x){return '<p><b>'+esc(x.at)+'</b> '+(x.total||0)+'점 · '+esc(x.act)+' — '+esc(x.title)+(x.note?' <small>('+esc(x.note)+')</small>':'')+'</p>'}).join('')+'</div>';
  box.appendChild(lg)}
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
