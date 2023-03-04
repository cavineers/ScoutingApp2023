let navStamps = JSON.parse(localStorage.getItem("navStamps") || "{}");
let navTime = new Date();

window.addEventListener("load", () => {
    const pnames = location.pathname.split("/");
    const fname = pnames[pnames.length-1];
    if (!(fname in navStamps))
        navStamps[fname] = navTime.getTime() + navTime.getTimezoneOffset() * 60000;
    localStorage.setItem("navStamps", JSON.stringify(navStamps));
});