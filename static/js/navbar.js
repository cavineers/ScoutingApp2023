let toggleDarkThemeButton;

//update button text to match with theme
function setThemeButtonText() {
    var text = {"light":"Dark Mode","dark":"Light Mode"}[currentTheme] || "Light Mode"; //map light to Dark Mode and dark to Light Mode, else Light Mode
    toggleDarkThemeButton.innerText = text;
}

function checkDataAccess() {
    var popup = addMenu(null, "30%", "30%");

    //create menu content container
    var popupContent = document.createElement("div");
    popupContent.style.marginLeft = "2%";
    popupContent.style.marginTop = "2%"

    //create prompt
    var prompt = document.createElement("label");
    prompt.innerHTML = "Password:\t";

    //create output area
    var popupOutput = document.createElement("p");


    //create input for password
    var popupInput = document.createElement("input");
    popupInput.type = "password";

    //create verify button
    var verifyButton = document.createElement("button");
    verifyButton.innerHTML = "Verify";
    verifyButton.onclick = (e) => {
        if (e.button != 0)
            return;

        //TODO verify server-side
        if (popupInput.value == (!![]+[])[(+[])]+'w'+([]+[]+[][[]])[(+!+[]+((+!+[])+(+!+[])))]+(![]+[])[((+!+[])+(+!+[]))]+([]+[]+([]).constructor)[(+[+!+[]+[+[]+[+[]]]])/((+!+[])+(+!+[]))/((+!+[])+(+!+[]))-(+!+[])]+([]+[]+[][[]])[(+!+[]+((+!+[])+(+!+[])))]+(!![]+[])[(+[])]+'h'+([]+[]+[][[]])[(+[+!+[]+[+[]]])/((+!+[])+(+!+[]))]+(!![]+[])[(+!+[])]+(!![]+[])[(+[])]+(([]).constructor.name)[(+!+[])+(+!+[]+((+!+[])+(+!+[])))]+([]+[]+[][[]])[(+!+[]+((+!+[])+(+!+[])))]+([]+[]+[][[]])[(+[+!+[]+[+[]]])/((+!+[])+(+!+[]))]+(typeof ([]+[]))[(+[+!+[]+[+[]]])/((+!+[])+(+!+[]))]+'h'+(!![]+[])[(+[])]+(![]+[])[(+!+[])]+(typeof +[])[((+!+[])+(+!+[]))])
            window.location = "/data.html";
        else {
            popupOutput.style.color = "#990000";
            popupOutput.innerHTML = "Invalid Password";
            popupInput.value = "";
        }
    }


    //add elements to menu
    var menu = popup.children[1]; //children[0] is clickable background that closes popup, children[1] is the menu
    menu.appendChild(popupContent);
    popupContent.appendChild(popupOutput);
    popupContent.appendChild(prompt);
    popupContent.appendChild(document.createElement("br"));
    popupContent.appendChild(popupInput);
    popupContent.appendChild(document.createElement("br"));
    popupContent.appendChild(verifyButton);

    return false;
}