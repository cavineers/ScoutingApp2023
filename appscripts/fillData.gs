/**
 * @param {number} teamNumber The number of the team to get data from.
 * @param {string} fromDate
 * @param {string} toDate
 * @param {Array.<Array.<object>>} rows The rows to pull the team data from.
 */
function getTeamValues(teamNumber, fromDate, toDate, rows) {
  var relevant = [];
  for (let row of rows) {
    if (row[0]==teamNumber && row[3] && dateInRange(row[3], fromDate, toDate))
      relevant.push(row);

  }

  var data = [];
  for (let rel of relevant) {
    //cut out the match number, team number, scouter name, and date
    let val = rel.slice(4);
    //add match number to the front of the array (first column)
    val.unshift(rel[1]);
    data.push(val);
  }
  return data;
}

/**
 * @param {Array.<number>|string} dateValue
 * @param {Array.<number>|string} fromDate
 * @param {Array.<number>|string} toDate
 */
function dateInRange(dateValue, fromDate, toDate) {
  dateValue = parseDateString(dateValue);
  fromDate = parseDateString(fromDate);
  if (toDate != "LATEST")
    toDate = parseDateString(toDate);
  const inBack = dateValue[0] > fromDate[0] || (dateValue[0]==fromDate[0] && dateValue[1] >= fromDate[1]);
  const inFront = toDate == "LATEST" || (dateValue[0] < toDate[0] || (dateValue[0]==toDate[0] && dateValue[1] <= toDate[1]));
  return inBack&inFront;
}

/**
 * @param {string} dateString
 * @returns {Array.<number>}
 */
function parseDateString(dateString) {
  if (typeof dateString != "string") return dateString;
  var dateArray = dateString.split("/", 2);
  for (let i = 0; i<dateArray.length; i++) dateArray[i] = Number(dateArray[i]);
  return dateArray;
}