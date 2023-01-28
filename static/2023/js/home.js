window.addEventListener("load", () => {
    let submitForm = document.getElementById("submitForm");
    if(submitForm != null)
    submitForm.addEventListener("submit", (ev) => {
        ev.preventDefault();
        const found = document.getElementsByTagName("input");
            let inputs = {};
            for(let input of found)
                inputs[input.name] = input.type == "number" ? Number(input.value) : input.value;
                localStorage.setItem("preliminaryData", JSON.stringify(inputs));
                console.log(inputs);
                window.location.href = "/comps/2023/scout.html";
    });
});