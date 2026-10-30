// 휴대폰 알림 받기(사용자 2026-10-30) — 원시그널 웹 푸시. 메인 화면에만 '📈 실적 알림 받기' 카드
// 아이폰은 홈 화면에 추가한 앱에서만 됨(애플 규칙) → 그 밖에선 안내만. SDK는 버튼을 쓸 수 있는 기기에서만 불러옴(가볍게)
(function(){try{
if(!/\/(index\.html)?$/.test(location.pathname))return;
var APP='b81f8268-5aef-4a29-b2b8-2173248136a3',ua=navigator.userAgent;
var iOS=/iPhone|iPad|iPod/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
var standalone=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
var inApp=/KAKAOTALK|NAVER|Instagram|FBAN|FBAV|Line\//i.test(ua);
var can='serviceWorker' in navigator&&'PushManager' in window&&'Notification' in window&&!inApp&&(!iOS||standalone);
var card,sdk=null,mobile=/Android|iPhone|iPad|iPod/.test(ua)||iOS,android=/Android/.test(ua),BIP=null;
addEventListener('beforeinstallprompt',function(e){e.preventDefault();BIP=e;if(card&&card.classList.contains('inst'))inst()});
// ── 앱 설치 카드(사용자 2026-10-30): 카톡 → 사파리·크롬으로 넘김 / 안드로이드 → 설치 창 / 아이폰 사파리 → 화살표 안내
var HOME='https://mung-mungi.github.io/mung-mung-market/';
function inst(){if(!card)return;try{if(sessionStorage.getItem('mm-inst-x')){card.remove();card=null;return}}catch(e){} var kakao=/KAKAOTALK/i.test(ua),how=kakao?(iOS?'사파리로 열어 설치합니다':'크롬으로 열어 설치합니다'):inApp?'사파리·크롬에서 열면 설치할 수 있습니다':(iOS?'공유 → 홈 화면에 추가, 두 번이면 끝':(BIP?'버튼 한 번이면 홈 화면에 앱이 생깁니다':'메뉴 ⋮ → 홈 화면에 추가'));
 card.className='mm-push inst';card.innerHTML='<i><img src="img/icon192.png?v=2" alt=""></i><span><b>멍뭉 터미널 앱 설치</b><small>'+how+' · 설치하면 실적 알림도 받을 수 있습니다.</small></span><button type="button" class="mm-push-on">설치</button><button type="button" class="mm-push-x" aria-label="닫기">✕</button>';
 var bs=card.querySelectorAll('button');bs[1].onclick=function(){try{sessionStorage.setItem('mm-inst-x','1')}catch(e){}card.remove();card=null};
 bs[0].onclick=function(){
  if(kakao){if(android){location.href='intent://mung-mungi.github.io/mung-mung-market/#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url='+encodeURIComponent(HOME)+';end';setTimeout(function(){guide('app')},1500)}else{location.href='kakaotalk://web/openExternal?url='+encodeURIComponent(HOME)}return}
  if(BIP){BIP.prompt();BIP.userChoice.then(function(){BIP=null;inst()});return}
  guide(inApp?'app':iOS?'ios':/SamsungBrowser/.test(ua)?'sam':'and')}}
function guide(k){var o=document.createElement('div');o.className='mm-guide '+k;var ipad=/iPad/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
 var st=k==='ios'?['아래 <b>공유</b> 버튼 <em>⬆︎</em> 을 누르고','목록을 내려 <b>홈 화면에 추가</b>를 누른 뒤','오른쪽 위 <b>추가</b>를 누르면 끝입니다']:k==='and'?['오른쪽 위 <b>⋮ 메뉴</b>를 누르고','<b>홈 화면에 추가</b>(또는 앱 설치)를 누른 뒤','<b>설치</b>를 누르면 끝입니다']:k==='sam'?['아래 <b>≡ 메뉴</b>를 누르고','<b>현재 페이지 추가 → 홈 화면</b>을 누른 뒤','<b>추가</b>를 누르면 끝입니다']:['오른쪽 위(또는 아래) <b>⋮ 메뉴</b>에서','<b>다른 브라우저로 열기</b>(크롬·사파리·삼성 인터넷)를 누른 뒤','거기서 <b>앱 설치</b>를 다시 누릅니다'];
 o.innerHTML='<div class="g-box"><b class="g-t">홈 화면에 앱으로 설치하기</b><ol>'+st.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ol><button type="button">알겠습니다</button></div>'+(k==='ios'?'<div class="g-arrow'+(ipad?' top':'')+'">⬇︎</div>':'');
 o.onclick=function(e){if(e.target===o||e.target.tagName==='BUTTON')o.remove()};document.body.appendChild(o)}
function load(cb){if(sdk)return sdk.then(cb);sdk=new Promise(function(ok){window.OneSignalDeferred=window.OneSignalDeferred||[];
  var s=document.createElement('script');s.src='https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js';s.defer=true;document.head.appendChild(s);
  OneSignalDeferred.push(async function(OS){try{await OS.init({appId:APP,serviceWorkerPath:'mung-mung-market/OneSignalSDKWorker.js',serviceWorkerUpdaterPath:'mung-mung-market/OneSignalSDKUpdaterWorker.js',serviceWorkerParam:{scope:'/mung-mung-market/'},notifyButton:{enable:false}})}catch(e){}
   ok(OS);OS.User&&OS.User.PushSubscription&&OS.User.PushSubscription.addEventListener('change',function(){draw(OS)})})});return sdk.then(cb)}
function on(OS){try{if(Notification.permission!=='granted')return false;if(!OS||!OS.User||!OS.User.PushSubscription){return true}var o=OS.User.PushSubscription.optedIn;return o!==false||localStorage.getItem('mm-push-on')==='1'}catch(e){return false}}
// 켠 사람은 메인 맨 아래로(사용자 2026-10-30), 아직 안 켠 사람은 '새 실적' 띠 아래(위쪽)
function place(bottom){var sh=document.querySelector('p.sh');if(!sh||!card)return;var box=sh.parentElement,par=box.parentElement;
 if(bottom){if(card.parentElement!==par||card.nextElementSibling){par.appendChild(card)}card.classList.add('bot')}else if(card.nextElementSibling!==box&&!card.classList.contains('bot')){par.insertBefore(card,box)}}
function draw(OS){if(!card)return;
 if(mobile&&!standalone){inst();return}
 if(!can){  card.className='mm-push off';card.innerHTML='<i>🔔</i><span><b>실적·속보 알림</b><small>'+(inApp?'카톡 안에서는 알림을 받을 수 없습니다. 사파리·크롬에서 열어 홈 화면에 추가하면 켤 수 있습니다.':'홈 화면에 추가한 멍뭉 터미널 앱에서 켤 수 있습니다.')+'</small></span>';return}
 if(on(OS)){try{localStorage.setItem('mm-push-on','1')}catch(e){}card.className='mm-push done';place(true);card.innerHTML='<i>✓</i><span><b>실적 알림 켜짐</b><small>새 실적 노트와 중요한 속보가 오면 알려 드립니다.</small></span>';return}
 try{localStorage.removeItem('mm-push-on')}catch(e){}place(false);card.className='mm-push';card.innerHTML='<i>📈</i><span><b>실적 알림 받기</b><small>새 실적 노트와 중요한 속보만 휴대폰으로 알려 드립니다.</small></span><button type="button" class="mm-push-on">켜기</button>';
 card.querySelector('button').onclick=function(){this.textContent='…';sub(function(){draw(null);gate()})}}
// 알림 켜기(사용자 2026-10-30): 아이폰은 '누른 그 순간'에 허용 창을 띄워야 해서 휴대폰 기본 허용 창을 먼저 부르고, 허용되면 원시그널 등록
function sub(done){var pr;try{pr=Notification.permission==='granted'?Promise.resolve('granted'):Notification.requestPermission()}catch(e){pr=Promise.resolve(Notification.permission)}
 Promise.resolve(pr).then(function(r){if(Notification.permission!=='granted'){done(false);return}try{localStorage.setItem('mm-push-on','1')}catch(e){}
  load(function(OS){try{Promise.resolve(OS.User.PushSubscription.optIn()).catch(function(){}).then(function(){done(true,OS);setTimeout(function(){draw(OS)},800)})}catch(e){done(true)}});setTimeout(function(){done(true)},4000)})}
// 앱으로 열었는데 알림이 꺼져 있으면 아래에서 올라오는 배너(사용자 2026-10-30: '나중에' 없음 — 켤 때까지 앱 열 때마다, 거절한 사람은 열 때마다 설정 안내)
function gate(){var g=document.getElementById('mmpg');if(g)g.remove();if(!can||!standalone||Notification.permission==='granted')return;
 var today=new Date().toISOString().slice(0,10),den=Notification.permission==='denied';
 try{if(den&&sessionStorage.getItem('mm-gate-den'))return}catch(e){}
 g=document.createElement('div');g.id='mmpg';
 g.innerHTML='<div class="bx"><img class="ic" src="img/icon192.png?v=2" alt=""><h3>'+(den?'알림이 꺼져 있습니다':'🔔 알림을 켜 주세요')+'</h3>'+(den?'<p>아이폰 <b>설정 → 알림 → 멍뭉 터미널</b>에서<br>‘알림 허용’을 켜 주세요.</p><button type="button" class="go">알겠습니다</button>':'<p>새 실적·중요 속보만 바로 알려 드립니다.</p><button type="button" class="go">알림 켜기</button>')+'</div>';
 document.body.appendChild(g);var go=g.querySelector('.go'),lt=g.querySelector('.ltr');
 go.onclick=function(){if(den){try{sessionStorage.setItem('mm-gate-den','1')}catch(e){}g.remove();return}go.textContent='…';sub(function(ok){g.remove();if(!ok)gate()})};
}
function mount(){if(document.querySelector('.mm-push'))return true;var sh=document.querySelector('p.sh');if(!sh)return false;var box=sh.parentElement;
 card=document.createElement('div');var was=false;try{was=localStorage.getItem('mm-push-on')==='1'||Notification.permission==='granted'}catch(e){}if(was&&can)box.parentElement.appendChild(card);else box.parentElement.insertBefore(card,box);draw(null);
 if(can&&(Notification.permission==='granted'||standalone))load(draw);setTimeout(gate,1200);return true}
var n=0;(function go(){if(!mount()&&++n<40)setTimeout(go,250)})();
}catch(e){}})();
