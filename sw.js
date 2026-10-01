/* My Lesson Diary service worker v2.5.0 */
const CACHE_NAME = 'mylesson-v250';
const APP_SHELL = [
  './', './index.html', './privacy.html', './terms.html', './styles.css',
  './manifest.webmanifest', './favicon.ico', './favicon-16x16.png', './favicon-32x32.png',
  './apple-touch-icon.png', './android-chrome-192x192.png', './android-chrome-512x512.png',
  './maskable-icon-512x512.png', './logo.png', './logo.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)));
  // Do not skipWaiting automatically. Keeping the old worker alive until all
  // existing tabs close prevents a running page from mixing old JS with a new cache.
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys
        .filter((key) => key.startsWith('mylesson-') && key !== CACHE_NAME)
        .map((key) => caches.delete(key))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (req.mode === 'navigate' || req.destination === 'document') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.put(req, copy)));
          }
          return res;
        })
        .catch(() => caches.match(req).then((hit) => hit || caches.match('./index.html')))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      const fresh = fetch(req).then((res) => {
        if (res && res.ok) {
          event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.put(req, res.clone())));
        }
        return res;
      }).catch(() => cached);
      return cached || fresh;
    })
  );
});
