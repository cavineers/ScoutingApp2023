function collectData() {
    let contents = {};
    contents["contentType"] = "match"; //as opposed to contentType="pit"
    //get home data
    contents["preliminaryData"] = JSON.parse(localStorage.getItem("preliminaryData"));
    //get prematch data
    contents["startPiece"] = JSON.parse(localStorage.getItem("startPiece"));
    contents["roboPos"] = JSON.parse(localStorage.getItem("roboPos"));
    contents["pieceLayout"] = JSON.parse(localStorage.getItem("pieceLayout"));
    //get scout data
    //scoreGrid: just array of ScoreNode.history    =   [ScoreNode, ScoreNode, ...] -> [ScoreNode.history, ...]
    contents["scoreGrid"] = trimScoreGrid(JSON.parse(localStorage.getItem("scoreGrid")));
    contents["pickUps"] = JSON.parse(localStorage.getItem("pickUps"));
    contents["shelfPickUps"] = JSON.parse(localStorage.getItem("shelfPickUps"));
    contents["pieceDrops"] = JSON.parse(localStorage.getItem("pieceDrops"));
    contents["defenses"] = JSON.parse(localStorage.getItem("defenses"));
    contents["autoChargeState"] = JSON.parse(localStorage.getItem("autoChargeState"));
    contents["chargeState"] = JSON.parse(localStorage.getItem("chargeState"));
    contents["endAuto"] = JSON.parse(localStorage.getItem("endAuto"));
    //get result data
    contents["comments"] = JSON.parse(localStorage.getItem("comments"));
    //get navigation timestamps
    contents["navStamps"] = JSON.parse(localStorage.getItem("navStamps"));
    return JSON.stringify(contents);
}

window.addEventListener("load", () => {
    const finishButton = document.getElementById("finishButton");
    finishButton.addEventListener("click", async (ev) => {
        if (ev.button != 0)
            return;
        //TODO add any more comments, or change to set string to localStorage instead of array
        localStorage.setItem("comments", JSON.stringify([document.getElementById("commentarea1").value]));
        const data = new FormData();
        data.set("data", JSON.stringify(collectData()));
        await fetch("/comps/2023/upload", {
            method:"POST",
            body: data
          });
        window.location.href = "/comps/2023/home.html";
    })
});

/** @param {Array.<ScoreNode>} array */
function trimScoreGrid(array) {
    if (array==null || !array) return [];
    const histories = array.map((scoreNode) => scoreNode.history);
    console.log(histories);
    let rtv = {};
    //store only the indexes that have values
    for (let i in histories) {
      if (Object.keys(histories[i]).length > 0)
        rtv[i] = histories[i];
    }
    return rtv;
  }