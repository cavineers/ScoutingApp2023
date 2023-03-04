//cite: https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/

let currentTheme = localStorage.getItem("theme") || "dark";

function setThemeDark() {
    console.log("Set Dark");
    //iterate through all elements with light-theme class found by querySelector
    var elements = document.querySelectorAll(".light-theme");
    if (elements == null || elements == undefined)
        return;
    NodeList.prototype.forEach.call(elements, (element) => {
        element.classList.remove("light-theme");
        element.classList.add("dark-theme");

    });
    currentTheme = "dark";
    localStorage.setItem("theme", currentTheme);
}

function setThemeLight() {
    console.log("Set Light");
    var elements = document.querySelectorAll(".dark-theme");
    if (elements == null || elements == undefined)
        return;
    NodeList.prototype.forEach.call(elements, (element) => {
        element.classList.remove("dark-theme");
        element.classList.add("light-theme");
        
    });
    currentTheme = "light";
    localStorage.setItem("theme", currentTheme);
}

function toggleTheme() {
    if (currentTheme == "light")
        setThemeDark();
    else
        setThemeLight();
}

function getThemeName() {
    return currentTheme == "dark" ? "dark-theme" : "light-theme";
}

function setTheme() {
    if (currentTheme == "light")
        setThemeLight();
    else
        setThemeDark();
}

window.addEventListener("load", () => {
    setTheme();
    const toggleButton = document.getElementById("toggle_darkmode");
    if (toggleButton==null) return;
    toggleButton.addEventListener("click", (ev) => {
        if (ev.button != 0)
            return;
        toggleTheme();
        toggleButton.innerText = currentTheme == "light" ? "Light Mode" : "Dark Mode";
    });
});