let toggleDarkThemeButton;

window.addEventListener("load", () => {
    for (let element in document.getElementsByClassName("secret")) {
        element.onclick = (e) => {
            if (e.button != 0) //if not left click
                return;

            //TODO make popup window to enter password
        }
    }

    toggleDarkThemeButton = document.getElementById("toggle_darkmode");
    toggleDarkThemeButton.onclick = (e) => {
        if (e.button != 0)
            return;

        toggleDarkTheme();
        toggleDarkThemeButton.innerHTML = `${currentTheme[0].toUpperCase()+currentTheme.substring(1)} Mode`;
    }

});