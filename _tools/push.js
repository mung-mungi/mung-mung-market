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
function on(OS){try{return Notification.permission==='granted'&&OS&&OS.User.PushSubscription.optedIn}catch(e){return false}}
function draw(OS){if(!card)return;
 if(!can){card.className='mm-push off';card.innerHTML='<i>🔔</i><span><b>실적·속보 알림</b><small>'+(inApp?'카톡 안에서는 알림을 받을 수 없습니다. 사파리·크롬에서 열어 홈 화면에 추가하면 켤 수 있습니다.':'홈 화면에 추가한 멍뭉 터미널 앱에서 켤 수 있습니다.')+'</small></span>';return}
 if(on(OS)){card.className='mm-push done';card.innerHTML='<i>✓</i><span><b>실적 알림 켜짐</b><small>새 실적 노트와 중요한 속보가 오면 알려 드립니다.</small></span><button type="button" class="mm-push-off">끄기</button>';
  card.querySelector('button').onclick=function(){OS.User.PushSubscription.optOut().then(function(){draw(OS)})};return}
 card.className='mm-push';card.innerHTML='<i>📈</i><span><b>실적 알림 받기</b><small>새 실적 노트와 중요한 속보만 휴대폰으로 알려 드립니다.</small></span><button type="button" class="mm-push-on">켜기</button>';
 card.querySelector('button').onclick=function(){var b=this;b.textContent='…';load(function(OS){var p=Notification.permission==='granted'?OS.User.PushSubscription.optIn():OS.Notifications.requestPermission();
  Promise.resolve(p).then(function(){if(Notification.permission==='granted'&&!OS.User.PushSubscription.optedIn)return OS.User.PushSubscription.optIn()}).catch(function(){}).then(function(){setTimeout(function(){draw(OS)},800)})})}}
function mount(){if(document.querySelector('.mm-push'))return true;var sh=document.querySelector('p.sh');if(!sh)return false;var box=sh.parentElement;
 card=document.createElement('div');box.parentElement.insertBefore(card,box);draw(null);
 if(can&&Notification.permission==='granted')load(draw);return true}
var n=0;(function go(){if(!mount()&&++n<40)setTimeout(go,250)})();
}catch(e){}})();
