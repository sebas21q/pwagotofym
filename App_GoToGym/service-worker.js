// Versión del caché (cámbiala cuando hagas cambios grandes)
const CACHE_NAME = "gotogym-v2";

// Ruta base de tu app cuando la sirves con Live Server
// En tu caso la URL es algo como:
// http://127.0.0.1:5500/App_GoToGym/indexSeleccion.html
const APP_ROOT = "/App_GoToGym/";

// Archivos que quieres tener disponibles offline
const STATIC_ASSETS = [
  APP_ROOT,
  APP_ROOT + "index.html",
  APP_ROOT + "indexSeleccion.html",
  APP_ROOT + "estilos1.css",
  APP_ROOT + "estilos2.css",
  APP_ROOT + "globals1.css",
  APP_ROOT + "js/config.js",
  APP_ROOT + "js/main.js",
  APP_ROOT + "manifest.json",
  APP_ROOT + "public/images/recurso-14.png",
  APP_ROOT + "favicon.ico"
];

// Instalación: precache de recursos estáticos
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
});

// Activación: borrar cachés antiguos
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// Estrategia de fetch:
// - Navegación (HTML): network first con fallback a caché
// - Archivos estáticos: cache first con fallback a red
self.addEventListener("fetch", (event) => {
  const request = event.request;

  // No tocar peticiones que no sean GET (ejemplo: POST al backend)
  if (request.method !== "GET") {
    return;
  }

  // Navegación entre páginas (documentos HTML)
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(() => {
          // Si no hay red, intenta servir indexSeleccion o index
          return caches.match(APP_ROOT + "indexSeleccion.html")
            .then((cached) => cached || caches.match(APP_ROOT + "index.html"));
        })
    );
    return;
  }

  // Archivos estáticos: CSS, JS, imágenes, etc.
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(request).then((networkResponse) => {
        const copy = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        return networkResponse;
      });
    })
  );
});
