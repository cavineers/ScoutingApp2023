let pieceLayout = [null, null, null];
const pieceOrder = ["cone", "cube", null];

const UNSELECTED_COLOR = "#777";
const CONE_COLOR = "#ff0";
const CONE_BORDER_COLOR = "#cc0";
const CUBE_COLOR = "#b0f";
const CUBE_BORDER_COLOR = "#80c";

window.addEventListener("load", () => {
    const nextButton = document.getElementById("nextButton");
    nextButton.addEventListener("click", (ev) => {
        if (ev.button != 0)
            return;
        //startPiece: startNone|startCube|startCone
        //roboPos: left|mid|right
        localStorage.setItem("pieceLayout", JSON.stringify(pieceLayout));
        for (let input of document.getElementsByTagName("input")) {
            if (input.type == "radio" && !input.checked) continue;
            localStorage.setItem(input.name, JSON.stringify(input.value));
        }

        //go to next page
        window.location.href = "/comps/2023/scout.html";
    });

    let buttons = document.getElementsByClassName("node-hybrid");
    for (let i = 0; i<buttons.length; i++) {
        buttons[i].addEventListener("click", (ev) => {
            if (ev.button!=0) return;
            pieceLayout[i] = pieceOrder[(pieceOrder.indexOf(pieceLayout[i])+1)%pieceOrder.length];
            switch(pieceLayout[i]) {
                case "cone":
                    buttons[i].style.background = CONE_COLOR;
                    buttons[i].style.borderColor = CONE_BORDER_COLOR;
                    break;
                case "cube":
                    buttons[i].style.background = CUBE_COLOR;
                    buttons[i].style.borderColor = CUBE_BORDER_COLOR;
                    break;
                default:
                    buttons[i].style.background = UNSELECTED_COLOR;
                    buttons[i].style.borderColor = UNSELECTED_COLOR;
                    break;
            }
        });
    }
});