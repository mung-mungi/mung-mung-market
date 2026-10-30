// 휴대폰 알림 받기(사용자 2026-10-30) — 원시그널 웹 푸시. 메인 화면에만 '📈 실적 알림 받기' 카드
// 아이폰은 홈 화면에 추가한 앱에서만 됨(애플 규칙) → 그 밖에선 안내만. SDK는 버튼을 쓸 수 있는 기기에서만 불러옴(가볍게)
(function(){try{
if(!/\/(index\.html)?$/.test(location.pathname))return;
var APP='b81f8268-5aef-4a29-b2b8-2173248136a3',ua=navigator.userAgent;
var iOS=/iPhone|iPad|iPod/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
var standalone=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
var inApp=/KAKAOTALK|NAVER|Instagram|FBAN|FBAV|Line\//i.test(ua);
var can='serviceWorker' in navigator&&'PushManager' in window&&'Notification' in window&&!inApp&&(!iOS||standalone);
var card,sdk=null;
function load(cb){if(sdk)return sdk.then(cb);sdk=new Promise(function(ok){window.OneSignalDeferred=window.OneSignalDeferred||[];
  var s=document.createElement('script');s.src='https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js';s.defer=true;document.head.appendChild(s);
  OneSignalDeferred.push(async function(OS){try{await OS.init({appId:APP,serviceWorkerPath:'mung-mung-market/OneSignalSDKWorker.js',serviceWorkerUpdaterPath:'mung-mung-market/OneSignalSDKUpdaterWorker.js',serviceWorkerParam:{scope:'/mung-mung-market/'},notifyButton:{enable:false}})}catch(e){}
   ok(OS);OS.User&&OS.User.PushSubscription&&OS.User.PushSubscription.addEventListener('change',function(){draw(OS)})})});return sdk.then(cb)}
function on(OS){try{if(Notification.permission!=='granted')return false;if(!OS||!OS.User||!OS.User.PushSubscription){return true}var o=OS.User.PushSubscription.optedIn;return o!==false||localStorage.getItem('mm-push-on')==='1'}catch(e){return false}}
// 켠 사람은 메인 맨 아래로(사용자 2026-10-30), 아직 안 켠 사람은 '새 실적' 띠 아래(위쪽)
function place(bottom){var sh=document.querySelector('p.sh');if(!sh||!card)return;var box=sh.parentElement,par=box.parentElement;
 if(bottom){if(card.parentElement!==par||card.nextElementSibling){par.appendChild(card)}card.classList.add('bot')}else if(card.nextElementSibling!==box&&!card.classList.contains('bot')){par.insertBefore(card,box)}}
function draw(OS){if(!card)return;
 if(!can){try{if(localStorage.getItem('mm-push-x')){card.remove();card=null;return}}catch(e){}
  card.className='mm-push off';card.innerHTML='<i>🔔</i><span><b>실적·속보 알림</b><small>'+(inApp?'카톡 안에서는 알림을 받을 수 없습니다. 사파리·크롬에서 열어 홈 화면에 추가하면 켤 수 있습니다.':'홈 화면에 추가한 멍뭉 터미널 앱에서 켤 수 있습니다.')+'</small></span><button type="button" class="mm-push-x" aria-label="닫기">✕</button>';
  card.querySelector('button').onclick=function(){try{localStorage.setItem('mm-push-x','1')}catch(e){}card.remove();card=null};return}
 if(on(OS)){try{localStorage.setItem('mm-push-on','1')}catch(e){}card.className='mm-push done';place(true);card.innerHTML='<i>✓</i><span><b>실적 알림 켜짐</b><small>새 실적 노트와 중요한 속보가 오면 알려 드립니다.</small></span><button type="button" class="mm-push-off">끄기</button>';
  card.querySelector('button').onclick=function(){if(!OS){load(function(O){O.User.PushSubscription.optOut().then(function(){draw(O)})});return}OS.User.PushSubscription.optOut().then(function(){draw(OS)})};return}
 try{localStorage.removeItem('mm-push-on')}catch(e){}place(false);card.className='mm-push';card.innerHTML='<i>📈</i><span><b>실적 알림 받기</b><small>새 실적 노트와 중요한 속보만 휴대폰으로 알려 드립니다.</small></span><button type="button" class="mm-push-on">켜기</button>';
 card.querySelector('button').onclick=function(){var b=this;b.textContent='…';if(Notification.permission!=='granted'&&Notification.requestPermission&&!sdk){}setTimeout(function(){draw(null)},9000);load(function(OS){var p=Notification.permission==='granted'?OS.User.PushSubscription.optIn():OS.Notifications.requestPermission();
  Promise.resolve(p).then(function(){if(Notification.permission==='granted'&&!OS.User.PushSubscription.optedIn)return OS.User.PushSubscription.optIn()}).catch(function(){}).then(function(){if(Notification.permission==='granted'){try{localStorage.setItem('mm-push-on','1')}catch(e){}}setTimeout(function(){draw(OS)},800)})})}}
function mount(){if(document.querySelector('.mm-push'))return true;var sh=document.querySelector('p.sh');if(!sh)return false;var box=sh.parentElement;
 card=document.createElement('div');var was=false;try{was=localStorage.getItem('mm-push-on')==='1'||Notification.permission==='granted'}catch(e){}if(was&&can)box.parentElement.appendChild(card);else box.parentElement.insertBefore(card,box);draw(null);
 if(can&&Notification.permission==='granted')load(draw);return true}
var n=0;(function go(){if(!mount()&&++n<40)setTimeout(go,250)})();
}catch(e){}})();
