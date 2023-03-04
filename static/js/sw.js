/** @returns {Promise<Array.<string>>} */
async function getAssets() {
    let response = await fetch("/assets");
    if (!response.ok) {
        console.error("Failed to get asset list.");
        return [];
    }
    return await response.json()
}

async function ping() {
    try {
        return (await fetch("/ping")).ok;
    }
    catch { return false; }
}
async function updateConnectionStatus() {
    const next = navigator.onLine ? await ping() : false;
    if (connectionStatus != next)
        console.log(`Connection status: ${connectionStatus} -> ${next}`);
    connectionStatus = next;
}
let connectionStatus = navigator.onLine;
let _interval = null;

const CONNECTION_STATUS_INTERVAL = 3000; //ms
const cacheLocation = "scouting-app-4541";

//define assets
let assets = [];

self.addEventListener("install", async (event) => {
    if (!_interval)
        _interval = setInterval(updateConnectionStatus, CONNECTION_STATUS_INTERVAL);
    assets = await getAssets();
    const cache = await caches.open(cacheLocation);
    cache.addAll(assets);
});

async function getResponse(request) {
    try {
        if (connectionStatus) {
            const response = await fetch(request);
            for (let url of assets) {
                if (request.url.split("?")[0].endsWith(url)) {
                    (await caches.open(cacheLocation)).put(request, response.clone());
                    break;
                }
            }
            return response;
        }
    }
    catch (error) { console.error(error); }

    const cached = await caches.match(request.url);
    if (cached)
        return cached;
    return new Response("Network error happened", {
        status: 408,
        headers: { "Content-Type": "text/plain" },
    });
}

//Network then cache method: https://stackoverflow.com/a/70216365
self.addEventListener("fetch", (event) => {
    if (!_interval)
        _interval = setInterval(updateConnectionStatus, CONNECTION_STATUS_INTERVAL);
    event.respondWith(getResponse(event.request));
});

console.log("Registered service worker");