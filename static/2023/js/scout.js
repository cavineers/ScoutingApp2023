let scoreNodes = [];

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
        this.history[new Date().getTime()] = Object.values(GamePiece).includes(gamePiece) ? gamePiece : null;
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
        localStorage.setItem("scoreGrid", JSON.stringify(scoreNodes));
    }
}


window.addEventListener("load", () => {
    var selections = document.querySelectorAll(".node-cone, .node-cube, .node-hybrid");
    selections.forEach((selection) => {
        let node = new ScoreNode(selection);
        scoreNodes.push(node);
        setNodeClick(node);
    });
});


/**
 * 
 * @param {number} col The column that the score node is on (start at 0)
 * @param {number} row The row that the score node is on (start at 0)
 * @returns {number} The index in the list scoreNodes that the scoreNode in the specified column and row is at.
 */
function coordinatesToIndex(col, row) {
    return row*9+col;
}

function indexToCoordinates(index) {
    return; //TODO math :)
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
                    let menuContainer = addMenu(null, "20%", "fit-content");
                    let menu = menuContainer.children[1];
                    menu.style.textAlign = "center";

                    //define button
                    let coneButton = document.createElement("button");
                    //set button style
                    coneButton.classList.add("node-cone");
                    coneButton.style.background = CONE_COLOR;
                    coneButton.style.borderColor = CONE_BORDER_COLOR;
                    coneButton.style.marginRight = "4%";
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
                    cubeButton.classList.add("node-cube");
                    cubeButton.style.background = CUBE_COLOR;
                    cubeButton.style.borderColor = CUBE_BORDER_COLOR;
                    cubeButton.style.marginLeft = "4%";
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