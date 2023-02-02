/** @returns {Promise<Array.<string>>} */
async function getAssets() {
    let response = await fetch("/assets");
    if (!response.ok) {
        console.error("Failed to get asset list.");
        return [];
    }
    return await response.json()
}

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
let assets;

self.addEventListener("install", async (installEvent) => {
    assets = await getAssets();
    const cache = await caches.open(cacheLocation);
    cache.addAll(assets);
});

//Network then cache method: https://stackoverflow.com/a/70216365
self.addEventListener("fetch", (event) => {
    event.respondWith(async function() {
        var path = event.request.url.split(self.location.hostname)[1].slice(1); //https://stackoverflow.com/a/11898963
        try {
            if (navigator.onLine || !caches.has(path))
                return await fetch(event.request);
            throw new Error("Skip to cache");
        }
        catch (err) {
            return caches.match(path);
        }
    }());
  });

console.log("Registered service worker");