window.addEventListener("load", (e) => {
    for (let element in document.getElementsByClassName("secret")) {
        element.onclick = (e) => {
            if (e.button != 0)
                return;

            //TODO make popup window to enter password
        }
    }
});