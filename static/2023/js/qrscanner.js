const version = "1.0";

function buildQRContents() {
  let contents = {}
  contents["version"] = version;
  contents["contentType"] = "match"; //as opposed to contentType="pit"
  //get home data
  contents["preliminaryData"] = JSON.parse(localStorage.getItem("preliminaryData"));
  //get prematch data
  
  //get scout data
  //scoreGrid: just array of ScoreNode.history    =   [ScoreNode, ScoreNode, ...] -> [ScoreNode.history, ...]
  contents["scoreGrid"] = trimScoreGrid(JSON.parse(localStorage.getItem("scoreGrid")));
  contents["pickUps"] = JSON.parse(localStorage.getItem("pickUps"));
  contents["pieceDrops"] = JSON.parse(localStorage.getItem("pieceDrops"));
  contents["defenses"] = JSON.parse(localStorage.getItem("defenses"));
  contents["chargeState"] = JSON.parse(localStorage.getItem("chargeState"));
  contents["endAuto"] = JSON.parse(localStorage.getItem("endAuto"))
  //get result data
  contents["comments"] = JSON.parse(localStorage.getItem("comments"));
  //get navigation timestamps
  contents["navStamps"] = JSON.parse(localStorage.getItem("navStamps"));
  return JSON.stringify(contents);
}

/** @param {Array.<ScoreNode>} array */
function trimScoreGrid(array) {
  const histories = array.map((scoreNode) => scoreNode.history);
  let rtv = {};
  //store only the indexes that have values
  for (let i in histories) {
    if (Object.keys(histories[i]).length > 0)
      rtv[i] = histories[i];
  }
  return rtv;
}


function gencode() {
  new QRCode(document.getElementById("qr"), {text:buildQRContents()});
}