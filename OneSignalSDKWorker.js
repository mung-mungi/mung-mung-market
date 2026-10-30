importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");
// 홈 화면 아이콘 배지(사용자 2026-10-30) — 알림이 올 때마다 숫자 +1, 앱을 열면 페이지가 지움
self.addEventListener('push', function (e) {
  if (!self.navigator || !self.navigator.setAppBadge) return;
  e.waitUntil(caches.open('mm-badge').then(function (c) {
    return c.match('n').then(function (r) { return r ? r.text() : '0'; }).then(function (t) {
      var n = (parseInt(t, 10) || 0) + 1;
      return c.put('n', new Response(String(n))).then(function () { return self.navigator.setAppBadge(n); });
    });
  }).catch(function () {}));
});
