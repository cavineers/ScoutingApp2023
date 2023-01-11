let scoreNodes = [];

const NodeType = {
    Cone: Symbol("cone"),
    Cube: Symbol("cube"),
    Hybrid: Symbol("hybrid")
};

const GamePiece = {
    Cone: Symbol("cone"),
    Cube: Symbol("cube")
};

class ScoreNode {

    /**
     * 
     * @param {Element} element Element to check the classList of.
     * @returns {NodeType|null} The node type, or null if could not be determined.
     */

    static nodeTypeFromClass(element) {
        return element.classList.contains("node-cone") ? NodeType.Cone : element.classList.contains("node-cube") ? NodeType.Cube : element.classList.contains("node-hybrid") ? NodeType.Hybrid : null;
    }

    /**
     * 
     * @param {NodeType} type Type of score node.
     * @param {GamePiece} gamePiece Game piece that is in the node.
     */

    constructor(type, gamePiece) {
        this.type = type instanceof Element ? nodeTypeFromClass(type) : type;
        this.gamePiece = !(gamePiece instanceof GamePiece) ? null : gamePiece;
    }
}


window.addEventListener("load", () => {
    var selections = document.querySelectorAll(".node-cone, .node-cube, .node-hybrid");
    selections.forEach((selection) => {
        scoreNodes.push(new ScoreNode(selection));
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


function setNodeClick(element, scoreNode) {
    element.addEventListener("click", (e) => {
        switch(scoreNode.type) {
            case ScoreNode.Cone:
                break;
            case ScoreNode.Cube:
                break;
            case ScoreNode.Hybrid:
                break;
        }
    });
}
