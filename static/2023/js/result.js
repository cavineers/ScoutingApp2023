window.addEventListener("load", () => {
    const finishButton = document.getElementById("finishButton");
    finishButton.addEventListener("click", (ev) => {
        if (ev.button != 0)
            return;
        //TODO add any more comments, or change to set string to localStorage instead of array
        localStorage.setItem("comments", JSON.stringify([document.getElementById("commentarea1").value]));
        
        window.location.href = "/comps/2023/qrscanner.html";
    })
});