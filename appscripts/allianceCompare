/**
 * @param {Array.<Array.<string>>} columns The array of columns to make vertical.
 * @returns {Array.<Array.<string>>} An array of columns where each column name from the columns array is in its own array.
 */
function columnsVertical(columns) {
  var rows = [];
  for (let column of columns[0])
    rows.push([column]);

  return rows;
}

function teamsAreUnique(t1, t2, t3) {
  const teams = [t1, t2, t3];
  for (let i = 0; i<3; i++) {
    if (teams[i] == teams[(i+1)%3] || teams[i] == teams[(i+2)%3])
      return false;
  }
  return true;
}

function allianceFill(t1, t2, t3, fromDate, toDate, rows) {
  if (!teamsAreUnique(t1, t2, t3)) return "Teams must be unique.";

  var relevant = [];
  const tAll = [t1, t2, t3];
  for (let row of rows) { //iter through rows
    if (tAll.includes(row[0]) && row[3] && dateInRange(row[3], fromDate, toDate))
      relevant.push(row);
  }

  var data = [];
  for (let i = 4; i<relevant[0].length; i++) { //iter through columns
    const avgs = getAverageValues(relevant, i);
    data.push([
      getFittingAverage(avgs.get(String(t1))),
      getFittingAverage(avgs.get(String(t2))),
      getFittingAverage(avgs.get(String(t3)))
    ]);
  }
  return data;
}