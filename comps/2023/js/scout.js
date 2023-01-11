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
     */

    constructor(element, type, gamePiece) {
        this.element = element;
        this.type = !type ? ScoreNode.nodeTypeFromClass(element) : type;
        this.gamePiece = Object.values(GamePiece).includes(gamePiece) ? gamePiece : null;
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
                if (scoreNode.gamePiece == null) {
                    scoreNode.gamePiece = GamePiece.Cone;
                    scoreNode.element.style.background = "#ff0";
                    scoreNode.element.style.borderColor = "#cc0";
                }
                else {
                    scoreNode.gamePiece = null;
                    scoreNode.element.style.background = "#777";
                    scoreNode.element.style.borderColor = "#777";
                }
                break;
            case NodeType.Cube:
                if (scoreNode.gamePiece == null) {
                    scoreNode.gamePiece = GamePiece.Cube;
                    scoreNode.element.style.background = "#b0f";
                    scoreNode.element.style.borderColor = "#80c";
                }
                else {
                    scoreNode.gamePiece = null;
                    scoreNode.element.style.background = "#777";
                    scoreNode.element.style.borderColor = "#777";
                }
                break;
        }
    });
}