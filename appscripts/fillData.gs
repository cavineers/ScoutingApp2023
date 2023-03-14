function myFunction(teamNumber, rows) {
  var relevant = [];
  for (let row of rows) {
    if (row[0]==teamNumber)
      relevant.push(row);

  }


  var data = [];
  for (let rel of relevant) {
    let val = rel.slice(3)
    val.unshift(rel[1]);
    data.push(val);
    
  }
  return data;

}