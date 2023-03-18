/** @type {Array.<ScoreNode>} */
let scoreNodes = [];
/** @type {Array.<number>} */
let pickUps = []
/** @type {Array.<number>} */
let shelfPickUps = [];
/** @type {Array.<number>} */
let drops = [];
/** @type {Array.<number>} */
let defenses = [];


const SCORE_GRID_STORAGE = "scoreGrid";
const PICK_UPS_STORAGE = "pickUps";
const SHELF_PICK_UPS_STORAGE = "shelfPickUps";
const DROPS_STORAGE = "pieceDrops";
const DEFENSES_STORAGE = "defenses";
const CHARGE_STORAGE = "chargeState";
const AUTO_CHARGE_STORAGE = "autoChargeState";
const END_AUTO_STORAGE = "endAuto";
const COMMUNITY_EXIT_STORAGE = "communityExit";

const NodeType = {
    Cone: "cone",
    Cube: "cube",
    Hybrid: "hybrid"
};

const GamePiece = {
    Cone: "cone",
    Cube: "cube"
};

const UNSELECTED_COLOR = "#777";
const CONE_COLOR = "#ff0";
const CONE_BORDER_COLOR = "#cc0";
const CUBE_COLOR = "#b0f";
const CUBE_BORDER_COLOR = "#80c";

function getUTCNow() {
    let d = new Date();
    return d.getTime() + d.getTimezoneOffset()*60000; //60000 ms in 1 minute
}

class ScoreNode {

    /**
     * 
     * @param {Element} element Element to check the classList of.
     * @returns {string|null} The node type, or null if could not be determined.
     */

    static nodeTypeFromClass(element) {
        return element.classList.contains("node-cone") ? NodeType.Cone : element.classList.contains("node-cube") ? NodeType.Cube : element.classList.contains("node-hybrid") ? NodeType.Hybrid : null;
    }

    /**
     * 
     * @param {Element} element 
     * @param {string} type Type of score node.
     * @param {string|null} gamePiece Game piece that is in the node.
     * @param {object} history
     */

    constructor(element, type, gamePiece, history) {
        this.element = element;
        this.type = !type ? ScoreNode.nodeTypeFromClass(element) : type;
        this.gamePiece = Object.values(GamePiece).includes(gamePiece) ? gamePiece : null;
        this.history = history?history:{};
    }

    /**
     * Set the Score Node's Game Piece
     * @param {string|null} gamePiece 
     */
    setGamePiece(gamePiece) {
        this.gamePiece = gamePiece;
        this.history[getUTCNow()] = Object.values(GamePiece).includes(gamePiece) ? gamePiece : null;
        if (gamePiece==GamePiece.Cone) {
            this.element.style.background = CONE_COLOR;
            this.element.style.borderColor = CONE_BORDER_COLOR;
        }
        else if (gamePiece==GamePiece.Cube) {
            this.element.style.background = CUBE_COLOR;
            this.element.style.borderColor = CUBE_BORDER_COLOR;
        }
        else {
            this.element.style.background = UNSELECTED_COLOR;
            this.element.style.borderColor = UNSELECTED_COLOR;
        }
        localStorage.setItem(SCORE_GRID_STORAGE, JSON.stringify(scoreNodes));
    }
}


window.addEventListener("load", () => {
    const selections = document.querySelectorAll(".node-cone, .node-cube, .node-hybrid");
    selections.forEach((selection) => {
        let node = new ScoreNode(selection);
        scoreNodes.push(node);
        setNodeClick(node);
    });

    //track button press times
    const pickedUpGround = document.getElementById("pickedUpGround");
    const pickedUpShelf = document.getElementById("pickedUpShelf");
    const pickUpAuto = document.getElementById("pickUpAuto");
    const pickedUpShelfAuto = document.getElementById("pickedUpShelfAuto");
    const dropPiece = document.getElementById("dropPiece");
    const dropPieceAuto = document.getElementById("dropPieceAuto");
    const markDefense = document.getElementById("markDefense");
    const passesMidLineAuto = document.getElementById("passesMidLineAuto");
    if (!localStorage.getItem(COMMUNITY_EXIT_STORAGE))
        localStorage.setItem(COMMUNITY_EXIT_STORAGE, "null");

    setMarkTime(pickedUpGround, PICK_UPS_STORAGE, pickUps);
    setMarkTime(pickUpAuto, PICK_UPS_STORAGE, pickUps);
    setMarkTime(pickedUpShelf, SHELF_PICK_UPS_STORAGE, shelfPickUps);
    setMarkTime(pickedUpShelfAuto, SHELF_PICK_UPS_STORAGE, shelfPickUps);
    setMarkTime(dropPiece, DROPS_STORAGE, drops);
    setMarkTime(dropPieceAuto, DROPS_STORAGE, drops);
    setMarkTime(markDefense, DEFENSES_STORAGE, defenses);

    passesMidLineAuto.addEventListener("click", (ev)=>{
        if (ev.button!=0) return;
        localStorage.setItem(COMMUNITY_EXIT_STORAGE, getUTCNow());
    })

    //end auto button
    switchAuto();
    const endAutoButton = document.getElementById("endAuto");
    endAutoButton.addEventListener("click", (ev) => {
        const chargeOff = document.getElementById("chargeOffAuto");
        const chargeDocked = document.getElementById("chargeDockedAuto");
        const chargeEngaged = document.getElementById("chargeEngagedAuto");
        const state = chargeEngaged.checked ? chargeEngaged.value :
                      chargeDocked.checked ? chargeDocked.value :
                      chargeOff.value;
        localStorage.setItem(AUTO_CHARGE_STORAGE, JSON.stringify(state))
        localStorage.setItem(END_AUTO_STORAGE, JSON.stringify(getUTCNow()));
        switchTele();
    });

    //next button
    const nextButton = document.getElementById("nextButton");
    nextButton.addEventListener("click", (ev) => {
        if (ev.button != 0)
            return;
        
        const chargeOff = document.getElementById("chargeOff");
        const chargeDocked = document.getElementById("chargeDocked");
        const chargeEngaged = document.getElementById("chargeEngaged");
        const state = chargeEngaged.checked ? chargeEngaged.value :
                      chargeDocked.checked ? chargeDocked.value :
                      chargeOff.value;

        //save
        localStorage.setItem(CHARGE_STORAGE, JSON.stringify(state));
        //redundant save
        localStorage.setItem(SCORE_GRID_STORAGE, JSON.stringify(scoreNodes));
        localStorage.setItem(PICK_UPS_STORAGE, JSON.stringify(pickUps));
        localStorage.setItem(SHELF_PICK_UPS_STORAGE, JSON.stringify(shelfPickUps));
        localStorage.setItem(DROPS_STORAGE, JSON.stringify(drops));
        localStorage.setItem(DEFENSES_STORAGE, JSON.stringify(defenses));

        //go to result.html
        window.location.href = "/comps/2023/result.html";
    });

});

function setMarkTime(element, storageKey, array) {
    element.addEventListener("click", (ev) => {
        if (ev.button != 0)
            return;

        array.push(getUTCNow());
        localStorage.setItem(storageKey, JSON.stringify(array));
    });
}

/**
 * 
 * @param {number} col The column that the score node is on (start at 0)
 * @param {number} row The row that the score node is on (start at 0)
 * @returns {number} The index in the list scoreNodes that the scoreNode in the specified column and row is at.
 */
function coordinatesToIndex(col, row) {
    return row*9+col;
}

/**
 * @param {ScoreNode} scoreNode
 */
function setNodeClick(scoreNode) {
    scoreNode.element.addEventListener("click", (e) => {
        switch(scoreNode.type) {
            case NodeType.Cone:
                if (scoreNode.gamePiece == null)
                    scoreNode.setGamePiece(GamePiece.Cone);
                else
                    scoreNode.setGamePiece(null);
                break;
            case NodeType.Cube:
                if (scoreNode.gamePiece == null)
                    scoreNode.setGamePiece(GamePiece.Cube);
                else
                    scoreNode.setGamePiece(null);
                break;
            case NodeType.Hybrid:
                //define popup menu, get menu element
                if (scoreNode.gamePiece == null) {
                    let menuContainer = addMenu(null, "50%", "fit-content");
                    let menu = menuContainer.children[1];
                    menu.style.alignItems = "center";

                    //define button
                    let coneButton = document.createElement("button");
                    //set button style
                    coneButton.classList.add("node-cone_button");
                    coneButton.style.background = CONE_COLOR;
                    coneButton.style.borderColor = CONE_BORDER_COLOR;
                    //set button click event
                    coneButton.addEventListener("click", (ev) => {
                        if (ev.button != 0)
                            return;
                        scoreNode.setGamePiece(GamePiece.Cone);
                        menuContainer.remove();
                    });

                    //define button
                    let cubeButton = document.createElement("button")
                    //set button style
                    cubeButton.classList.add("node-cube_button");
                    cubeButton.style.background = CUBE_COLOR;
                    cubeButton.style.borderColor = CUBE_BORDER_COLOR;
                    cubeButton.addEventListener("click", (ev) => {
                        if (ev.button != 0)
                            return;
                        scoreNode.setGamePiece(GamePiece.Cube);
                        menuContainer.remove();
                    });

                    menu.appendChild(coneButton);
                    menu.appendChild(cubeButton);
                }
                else
                    scoreNode.setGamePiece(null);
                break;
        }
    });
}

let autoState = true;

function switchTele() {
    for (let elm of document.getElementsByClassName("auto"))
        elm.hidden = true;
    for (let elm of document.getElementsByClassName("tele"))
        elm.hidden = false;
}

function switchAuto() {
    for (let elm of document.getElementsByClassName("auto"))
        elm.hidden = false;
    for (let elm of document.getElementsByClassName("tele"))
        elm.hidden = true;
}

function toggleAutoTele() {
    autoState = !autoState;
    if (autoState)
        switchAuto();
    else
        switchTele();

}