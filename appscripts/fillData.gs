/**
 * @param {number} teamNumber The number of the team to get data from.
 * @param {Array.<Array.<object>>} rows The rows to pull the team data from.
 */
function getTeamValues(teamNumber, rows) {
  var relevant = [];
  for (let row of rows) {
    if (row[0]==teamNumber) //
      relevant.push(row);

  }

  var data = [];
  for (let rel of relevant) {
    //cut out the match number, team number, and scouter name
    let val = rel.slice(3)
    //add match number to the front of the array (first column)
    val.unshift(rel[1]);
    data.push(val);

    //add pieces sum (insert total -> cubes -> cones: cones, cubes, total)
    const cones = val[1]+val[2]+val[3];
    const cubes = val[4]+val[5]+val[6];

    val.splice(7, 0, cones+cubes);
    val.splice(7, 0, cubes);
    val.splice(7, 0, cones);
  }
  return data;
}

/**
 * @param {number} tn1 The first team number in the alliance.
 * @param {number} tn2 The second team number in the alliance.
 * @param {number} tn3 The third team number in the alliance.
 * @param {Array.<Array.<object>>} rows The rows to pull the teams' data from.
 */
function getAllianceValues(tn1, tn2, tn3, rows) {
  var d1 = getTeamValues(tn1, rows);
  var d2 = getTeamValues(tn2, rows);
  var d3 = getTeamValues(tn3, rows);

  //TODO turn into alliance display data (use old sheets as reference/inspiration)
}