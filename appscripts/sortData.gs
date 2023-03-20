/**
 * @param {string} columnName What column to sort the leaderboard by.
 * @param {string} sortBy How to merge the different rows of data into one spot in the leaderboard.
 * @param {Array.<Array.<string|number>>} rows The rows to pull the data from. Includes the columns.
 */
function sortData(columnName, sortBy, direction, rows) {
  /** @type {Array.<string>} */
  const columns = rows[0];
  rows = rows.slice(1);
  /** @type {number} */
  const colIndex = columns.indexOf(columnName);
  const sortMethod = SORT_METHODS[sortBy];
  if (sortMethod) {
    var sorted = sortMethod(rows, colIndex);
    if (direction=="DOWN")
      sorted.reverse();
    return sorted;
  }
  else
    throw new Error("Invalid Look Method\n Expected a sort method '"+"', '".concat(SORT_METHOD_NAMES)+"', got: "+sortBy);
}

//types for 3 functions below are as seen in sortData
function sortMax(rows, colIndex) {
  var maxed = new Map();
  for (let row of rows) {
    const num = String(row[0]);
    if (!maxed.has(num) || (row[colIndex] > maxed.get(num))) { //team number not in maxed or row value > maxed value
      maxed.set(num, row[colIndex]);
    }
  }
  
  var maxedArray = [];
  maxed.forEach((value, key) => {
    maxedArray.push([key, value]);
  });
  maxedArray.sort((a, b) => b[1]-a[1]);
  return maxedArray;
}

function sortMin(rows, colIndex) {
  var mined = new Map();
  for (let row of rows) {
    const num = String(row[0]);
    if (!mined.has(num) || (row[colIndex] < mined.get(num))) {
      mined.set(num, row[colIndex]);
    }
  }
  
  var minedArray = [];
  mined.forEach((value, key) => {
    minedArray.push([key, value]);
  });
  minedArray.sort((a, b) => b[1]-a[1]);
  return minedArray;
}

function sortAvg(rows, colIndex, doMax) {
  var avged = new Map();
  for (let row of rows) {
    const num = String(row[0]);
    if (avged.has(num))
      avged.get(num).push(row[colIndex]);
    else
      avged.set(num, [row[colIndex]]);

  }
  
  var avgedArray = [];
  avged.forEach((value, key) => {
    const rawAvg = value.reduce((a, b) => a + b)/value.length;
    avgedArray.push([key, parseFloat(rawAvg.toFixed(3))]);
  });
  avgedArray.sort((a, b) => b[1]-a[1]);
  return avgedArray;
}


const SORT_METHOD_NAMES = ["MAX", "MIN", "AVG"];

const SORT_METHODS = {
  MAX:sortMax,
  MIN:sortMin,
  AVG:sortAvg
}