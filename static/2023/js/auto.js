window.addEventListener("load", () => {
    const nextButton = document.getElementById("nextButton");
    nextButton.addEventListener("click", (ev) => {
        if (ev.button != 0)
            return;
        
        //TODO get data gathered in page, put into localStorage, get from localStorage in qrscanner.html

        //go to next page
        window.location.href = "/comps/2023/scout.html";
    });
});