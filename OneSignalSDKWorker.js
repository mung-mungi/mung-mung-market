// 알림 누르면 그 내용으로 바로 이동(사용자 2026-11-04 — 앱이 이미 열려 있으면 그 화면만 앞으로 나오고 알림 주소로 안 가던 문제)
// 원시그널 처리보다 먼저 받아서: 열린 앱 창이 있으면 그 창을 알림 주소로 옮기고, 없으면 새로 엶. 주소는 푸시 자료(custom.u)에서 찾음
// 새 판이 열린 앱을 닫을 때까지 기다리지 않고 바로 적용(이게 없으면 앱을 완전히 닫기 전까지 옛 처리 방식이 계속 씀)
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
var MM_SITE = 'https://mung-mungi.github.io/mung-mung-market/';
function mmFind(o, d) {
  if (!o || d > 5) return '';
  if (typeof o === 'string') { try { if (o.indexOf(MM_SITE) === 0) return o; if (o.charAt(0) === '{') return mmFind(JSON.parse(o), d + 1); } catch (e) {} return ''; }
  if (typeof o !== 'object') return '';
  var ks = ['u', 'url', 'launchURL', 'launchUrl'];
  for (var i = 0; i < ks.length; i++) { var v = o[ks[i]]; if (typeof v === 'string' && v.indexOf(MM_SITE) === 0) return v; }
  for (var k in o) { var r = mmFind(o[k], d + 1); if (r) return r; }
  return '';
}
self.addEventListener('push', function (e) {
  try { var u = mmFind(e.data && e.data.json(), 0); if (u) e.waitUntil(caches.open('mm-go').then(function (c) { return c.put('last', new Response(u)); })); } catch (x) {}
});
self.addEventListener('notificationclick', function (e) {
  var n = e.notification, u = mmFind(n && n.data, 0);
  e.stopImmediatePropagation(); n.close();
  e.waitUntil((u ? Promise.resolve(u) : caches.open('mm-go').then(function (c) { return c.match('last'); }).then(function (r) { return r ? r.text() : MM_SITE; }).catch(function () { return MM_SITE; }))
    .then(function (url) {
      return self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (cs) {
        var w = null;
        for (var i = 0; i < cs.length; i++) { if (cs[i].url.indexOf(MM_SITE) === 0) { w = cs[i]; if (cs[i].focused) break; } }
        if (!w) return self.clients.openWindow(url);
        try { w.postMessage({ mmGo: url }); } catch (x) {}
        return w.focus().then(function (f) { var c = f || w; return c.navigate ? c.navigate(url).catch(function () {}) : null; }).catch(function () {});
      });
    }));
});
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
