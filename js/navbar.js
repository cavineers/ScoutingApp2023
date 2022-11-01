let toggleDarkThemeButton;

window.addEventListener("load", () => {
    toggleDarkThemeButton = document.getElementById("toggle_darkmode");
    toggleDarkThemeButton.onclick = (e) => {
        if (e.button != 0)
            return;

        toggleDarkTheme();
        setThemeButtonText();
    }
    setThemeButtonText(); //set initial text
    
});

//update button text to match with theme
function setThemeButtonText() {
    var text = {"light":"Dark Mode","dark":"Light Mode"}[currentTheme] || "Light Mode"; //map light to Dark Mode and dark to Light Mode, else Light Mode
    toggleDarkThemeButton.innerText = text;
}
