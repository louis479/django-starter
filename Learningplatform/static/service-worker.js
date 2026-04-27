self.addEventListener('install', function(event) {
    console.log('Service Worker Installed');
    // Cache resources here if needed
});

self.addEventListener('fetch', function(event) {
    // Basic fetch handler for offline capability
    event.respondWith(
        fetch(event.request).catch(function() {
            return new Response('Offline');
        })
    );
});