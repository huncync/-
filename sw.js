// 앱(홈 화면 설치)용 서비스 워커.
// 페이지·스크립트는 항상 새 버전을 먼저 받아오고(날짜별 화면 전환·가격이 바로 반영되도록),
// 인터넷이 끊겼을 때만 저장해 둔 사본을 보여줍니다.
const CACHE = "malijul-v1";
const SHELL = [
  "./",
  "index.html",
  "style.css",
  "script.js",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return; // 신청서 전송(Formspree)은 건드리지 않음

  const url = new URL(req.url);
  const sameOrigin = url.origin === location.origin;
  const isFont = /fonts\.(googleapis|gstatic)\.com|cdn\.jsdelivr\.net/.test(url.host);
  if (!sameOrigin && !isFont) return;

  if (sameOrigin) {
    // 네트워크 우선 → 실패하면 저장본
    e.respondWith(
      fetch(req)
        .then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() =>
          caches.match(req, { ignoreSearch: true })
            .then((hit) => hit || (req.mode === "navigate" ? caches.match("index.html") : undefined))
        )
    );
  } else {
    // 글꼴은 바뀌지 않으니 저장본 우선
    e.respondWith(
      caches.match(req).then((hit) =>
        hit || fetch(req).then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return res;
        })
      )
    );
  }
});
