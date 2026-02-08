const CACHE_NAME = 'leonor-amor-cache-v1.0.1';
const urlsToCache = [
    '/',
    '/offline/',  // Cache the offline page for fallback
    '/static/css/styles.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/img/logo-light-192x192.png',
    '/static/img/logo-light-512x512.png',
    '/static/img/logo-dark-192x192.png',
    '/static/img/logo-dark-512x512.png',
    '/static/img/logo-light-180x180.png',
    '/static/img/logo-dark-180x180.png',
];

// Install event to cache essential assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

// Fetch event to serve cached assets
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                return response || fetch(event.request)
                    .then((networkResponse) => {
                        return caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse.clone());
                            return networkResponse;
                        });
                    })
                    .catch(() => {
                        // Fallback to offline.html when user is offline
                        return caches.match('/offline/');
                    });
            })
    );
});

// Activate event to clean up old caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
