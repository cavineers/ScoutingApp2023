//cite: https://www.freecodecamp.org/news/build-a-pwa-from-scratch-with-html-css-and-javascript/

const cacheLocation = "scouting-app-4541";
const assets = [
    //base app caches
    "index.html",
    "help.html",
    "compselect.html",
    "js/darktheme.js",
    "js/index.js",
    "js/link-sw.js",
    "js/navbar.js",
    "js/overlay-menu.js",
    "css/base.css",
    "css/navbar.css",
    "css/overlay-menu.css",

    //images
    "img/icon/close_dark_32.png",
    "img/icon/close_dark_250.png",
    "img/icon/close_light_32.png",
    "img/icon/close_light_250.png",

    //comps/2023
    "comps/2023/scout.html",

];

self.addEventListener("install", installEvent => {
    installEvent.waitUntil( caches.open(cacheLocation).then(cache => { 
        cache.addAll(assets);
    }));
});

self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith( caches.match(fetchEvent.request).then(res => {
        return res || fetch(fetchEvent.request);
    }));
});