//https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/

const currentTheme = localStorage.getItem("theme") || "light";

function setThemeDark() {
    for (let element in document.getElementsByClassName("light-theme")) {
        element.classList.remove("light-theme");
        element.classList.add("dark-theme");
        localStorage.setItem("theme", "dark");
    }
}

function setThemeLight() {
    for (let element in document.getElementsByClassName("dark-theme")) {
        element.classList.remove("dark-theme");
        element.classList.add("light-theme");
        localStorage.setItem("theme", "light");
    }
}

function toggleDarkTheme() {
    if (currentTheme == "light")
        setThemeDark();
    else
        setThemeLight();
}

window.addEventListener("load", () => {
    if (currentTheme == "light")
        setThemeLight();
    else
        setThemeDark();
});