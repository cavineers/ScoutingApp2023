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

  const tAll_S = [String(t1), String(t2), String(t3)];
  var data = [];
  for (let i = 4; i<relevant[0].length; i++) { //iter through columns
    const avgs = getAverageValues(relevant, i);
    for (let t of tAll_S) if(!avgs.has(t)) return `Team ${t} did not compete within the specified date range.`;
    data.push([
      getFittingAverage(avgs.get(String(t1))),
      getFittingAverage(avgs.get(String(t2))),
      getFittingAverage(avgs.get(String(t3)))
    ]);
  }
  return data;
}

function teamFill(number, fromDate, toDate, rows) {
  var relevant = [];
  for (let row of rows) { //iter through rows
    if (row[0]==number && row[3] && dateInRange(row[3], fromDate, toDate))
      relevant.push(row);
  }

  if(relevant.length==0) return `Team ${number} did not compete within the specified date range.`;

  var data = [];
  for (let i = 4; i<relevant[0].length; i++) { //iter through columns
    const avgs = getAverageValues(relevant, i);
    data.push([
      getFittingAverage(avgs.get(String(number)))
    ]);
  }
  return data;

}

function getAllianceAverage(v1, v2, v3) {
  return getFittingAverage([v1, v2, v3]);
}