//cite: https://www.freecodecamp.org/news/build-a-pwa-from-scratch-with-html-css-and-javascript/

class CacheSettings {
    /**
     * Settings for caching and loading an asset.
     * @param {boolean} doCache Whether or not to cache the asset. true by default.
     * @param {boolean} prioritizeCache If the asset should be checked for in cache first instead of network. false by default.
     */
    constructor(doCache, prioritizeCache) {
        this.doCache = doCache==null||doCache==undefined?true:doCache?true:false;
        this.prioritizeCache = prioritizeCache?true:false;
    }

    /**
     * Get the asset path (url) that the CacheSettings are for.
     * @returns {string|undefined}
     */
    getAssetPath() {
        if ("assetPath" in this)
            return this.assetPath;
        for (let path in assets) {
            if (Object.is(assets[path], this)) {
                this.assetPath = path;
                return path;
            }
        }
    }

    /**
     * Cache the asset.
     * @param {string} path The path of the asset to cache. Calls getAssetPath by default.
     * @param {} cacheFile The cache file to write into. Opens up file at cacheLoction by default.
     * @returns {Promise<...>}
     */
    cache(path, cacheFile) {
        return (cacheFile||caches.open(cacheLocation)).then((cache) => {
            let cachePath = path||this.getAssetPath();
            if (cachePath) {
                try {
                    cache.add(cachePath);
                    
                }
                catch(err) {
                    console.error("Asset could not be cached:", err);
                }
            }
            else
                console.error("Failed to cache asset, could not identify asset path.");
        });
    }
}

const cacheLocation = "scouting-app-4541";
//define assets
const assets = {
    "manifest.json":new CacheSettings(),

    //navbar template
    "navbar.html": new CacheSettings(true, true),

    //base app caches
    "index.html": new CacheSettings(),
    "help.html": new CacheSettings(),
    "compselect.html": new CacheSettings(),
    "js/darktheme.js": new CacheSettings(),
    "js/link-sw.js": new CacheSettings(),
    "js/navbar.js": new CacheSettings(),
    "js/overlay-menu.js": new CacheSettings(),
    "css/base.css": new CacheSettings(),
    "css/navbar.css": new CacheSettings(),
    "css/overlay-menu.css": new CacheSettings(),

    //images
    "img/icon/close_dark_32.png": new CacheSettings(true, true),
    "img/icon/close_dark_250.png": new CacheSettings(true, true),
    "img/icon/close_light_32.png": new CacheSettings(true, true),
    "img/icon/close_light_250.png": new CacheSettings(true, true),
    "img/icon/robotics_cavs_icon_536.png": new CacheSettings(true, true),

    //comps/2023
    "comps/2023/scout.html": new CacheSettings(),

};

self.addEventListener("install", (installEvent) => {
    const cachePromise = caches.open(cacheLocation);
    //for each asset, cache if doCache
    for (let name in assets) {
        let cacheSet = assets[name];
        if (cacheSet.doCache)
            installEvent.waitUntil(cacheSet.cache(name), cachePromise);
    }
});

//Network then cache method: https://stackoverflow.com/a/70216365
self.addEventListener('fetch', (event) => {
    event.respondWith(async function() {
        var path = event.request.url.split(self.location.hostname)[1].slice(1); //https://stackoverflow.com/a/11898963
        if (self.location.port)
            path = path.slice(self.location.port.length+1); //get rid of port and slash after it
        
        const cacheSet = assets[path];
        //if asset is set to not cache, fetch
        if (!cacheSet.doCache && self.navigator.onLine)
            return await fetch(event.request);
        //else if asset prioritizes cache
        else if (cacheSet.prioritizeCache && self.navigator.onLine) {
            //if asset is cached, respond with cached asset
            if (caches.has(path))
                return caches.match(event.request);  
            //else, fetch and cache the response
            else { 
                const response = await fetch(event.request);
                caches.open(cacheLocation).then((cache) => {
                    cache.put(event.request, response);
                });
                return response;
            }
        }
        //else, try to fetch, fall back on cache
        else {
            try { return await fetch(event.request, ); }
            catch (err) { return caches.match(event.request); }
        }
    }());
});

console.log("Registered service worker");