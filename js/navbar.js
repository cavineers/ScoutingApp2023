let toggleDarkThemeButton;

//update button text to match with theme
function setThemeButtonText() {
    var text = {"light":"Dark Mode","dark":"Light Mode"}[currentTheme] || "Light Mode"; //map light to Dark Mode and dark to Light Mode, else Light Mode
    toggleDarkThemeButton.innerText = text;
}

/**
 * Fetches, sets up, and inserts navbar into the page
 * @param {string} dir
 * @returns {Promise<any>}
 */
function fetchNavbar(dir) {
    if (!dir) dir = "";
    return fetch(dir+"navbar.html").then((response) => { //get navbar template
        return response.text().then((text) => { //get navbar template text
            //insert navbar at start of body

            console.log(text);
            console.log(text.replace(/\{dir\}/g, dir));
            document.body.insertAdjacentHTML("afterbegin", text.replace(/\{dir\}/g, dir));

            //setup dark/light theme button
            toggleDarkThemeButton = document.getElementById("toggle_darkmode");
            toggleDarkThemeButton.onclick = (e) => {
                if (e.button != 0)
                    return;

                toggleDarkTheme();
                setThemeButtonText();
            }
            setThemeButtonText(); //set button initial text
        });
    })
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

        //check password (ideally this wouldn't be verified client-side)
        if (popupInput.value == (!![]+[])[(+[])]+'w'+([]+[]+[][[]])[(+!+[]+((+!+[])+(+!+[])))]+(![]+[])[((+!+[])+(+!+[]))]+([]+[]+([]).constructor)[(+[+!+[]+[+[]+[+[]]]])/((+!+[])+(+!+[]))/((+!+[])+(+!+[]))-(+!+[])]+([]+[]+[][[]])[(+!+[]+((+!+[])+(+!+[])))]+(!![]+[])[(+[])]+'h'+([]+[]+[][[]])[(+[+!+[]+[+[]]])/((+!+[])+(+!+[]))]+(!![]+[])[(+!+[])]+(!![]+[])[(+[])]+(([]).constructor.name)[(+!+[])+(+!+[]+((+!+[])+(+!+[])))]+([]+[]+[][[]])[(+!+[]+((+!+[])+(+!+[])))]+([]+[]+[][[]])[(+[+!+[]+[+[]]])/((+!+[])+(+!+[]))]+(typeof ([]+[]))[(+[+!+[]+[+[]]])/((+!+[])+(+!+[]))]+'h'+(!![]+[])[(+[])]+(![]+[])[(+!+[])]+(typeof +[])[((+!+[])+(+!+[]))])
            window.location = ""; //TODO go to data page (/data.html or something)
        else {
            popupOutput.style.color = "#990000";
            popupOutput.innerHTML = "Invalid Password";
            popupInput.value = "";
        }
    }


    //add elements to menu
    var menu = popup.children[0];
    menu.appendChild(popupContent);
    popupContent.appendChild(popupOutput);
    popupContent.appendChild(prompt);
    popupContent.appendChild(document.createElement("br"));
    popupContent.appendChild(popupInput);
    popupContent.appendChild(document.createElement("br"));
    popupContent.appendChild(verifyButton);

    return false;
}