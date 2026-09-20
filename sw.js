/* AURISI service worker v50 - network-first (always latest), offline cache - original logo icons */
var CACHE = "aurisi-v50";
var ASSETS = ["./", "./index.html", "./AURISI.html", "./manifest.json", "./icon-192.png", "./icon-512.png", "./icon-maskable-512.png", "./apple-touch-icon.png"];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(ASSETS).catch(function () {}); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  var url;
  try { url = new URL(e.request.url); } catch (err) { return; }
  if (url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(function (res) {
      if (res && res.ok && res.type === "basic") {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(e.request, { ignoreSearch: true }).then(function (m) {
        if (m) return m;
        if (e.request.mode === "navigate") return caches.match("./AURISI.html");
        return new Response("Offline", { status: 503, statusText: "Offline" });
      });
    })
  );
});
