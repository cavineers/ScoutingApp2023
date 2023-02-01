function verifyInfo(inputs) {
    console.log(inputs.matchNumber)
    if (inputs.matchNumber < 1) {
        //TODO output error message to user
        console.error("Invalid match number.")
        return false;
    }
    else if ((inputs.teamNumber).toString().length < 3) {
        //TODO output error to user
        console.error("Invalid team number.")
        return false;
    }
    else if (!inputs.scouterName.trim()) {
        //TODO output error
        console.error("Enter your name (The name of the person scouting).");
        return false;
    }
    return true;
}

window.addEventListener("load", () => {
    let submitForm = document.getElementById("submitForm");
    submitForm.addEventListener("submit", (ev) => {
        ev.preventDefault();
        const found = document.getElementsByTagName("input");
        let inputs = {};
        for(let input of found)
            inputs[input.name] = input.type == "number" ? Number(input.value) : input.value;
        //verify info
        if (!verifyInfo(inputs))
            return;
        //save info
        localStorage.setItem("preliminaryData", JSON.stringify(inputs));
        
        window.location.href = "/comps/2023/auto.html";
    });
});