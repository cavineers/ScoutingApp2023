
if ("serviceWorker" in navigator) {
    window.addEventListener("load", async () => {
        if (!(await navigator.serviceWorker.getRegistration()))
            navigator.serviceWorker.register("/sw.js");
    });

}