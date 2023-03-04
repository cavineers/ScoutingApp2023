function verifyInfo(inputs) {
    console.log(inputs.matchNumber)
    if (inputs.matchNumber < 1) {
        outputError("Invalid match number.");
        return false;
    }
    else if (inputs.teamNumber < 1) {
        outputError("Invalid team number.")
        return false;
    }
    else if (!inputs.scouterName.trim() || inputs.scouterName=="placeholder") {
        outputError("Enter your name (The name of the person scouting).");
        return false;
    }
    return true;
}

function outputError(message) {
  console.error(message);
  let errorOutput = document.getElementById("errorOutput");
  if (errorOutput==null) {
    const submitForm = document.getElementById("submitForm");
    if (submitForm==null) return; //nowhere to visibly output error to
    errorOutput = document.createElement("p");
    errorOutput.style.color = "#be0000";
    errorOutput.id = "errorOutput";
    submitForm.prepend(errorOutput);
  }
  errorOutput.innerHTML = message;
}

window.addEventListener("load", async () => {
  var namesResponse = await fetch("/comps/2023/names");
  /*An array containing all the country names in the world:*/
  var names = await namesResponse.json();
  /*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
  autocomplete(document.getElementById("name"), names);

  let submitForm = document.getElementById("submitForm");
  submitForm.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const found = document.getElementsByClassName("input");
      let inputs = {};
      for(let input of found)
          inputs[input.name] = input.type == "number" ? Number(input.value) : input.value;
      //verify info
      if (!verifyInfo(inputs))
          return;
      //save info
      localStorage.setItem("preliminaryData", JSON.stringify(inputs));
      window.location.href = "/comps/2023/prematch.html";
  });
});

function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

  /*An array containing all the names:*/
  /*
  var names = (
  "Abellano Jonah",
  "Avilla Anthony",
  "Baker Taryn",
  "Bechtel Logan",
  "Bell Laura",
  "Boomer Brett",
  "Bost James",
  "Bucht Lucas",
  "Ceryes Sadie",
  "Collins Brennen",
  "Comeau Dulcey",
  "Comeau Brady",
  "D'Amico Peter",
  "Davis Paul",
  "Davis Elijah",
  "Donyinah Jay",
  "Flynn Gavin",
  "Flynn Patrick",
  "Gardiner Andrew",
  "Gardiner Thomas",
  "Gash Nick",
  "Goodyear Jake",
  "Grant Chad",
  "Greenhill Kate",
  "Greensfelder Caden",
  "Grice Ashley",
  "Grice Thomas",
  "Ha Bryan",
  "Hayden Grant",
  "Haynes Reid",
  "Haynes Max",
  "Hecker Charles",
  "Henn Alex",
  "Herberich Eric",
  "Jablinske Sierra",
  "Kearney Matthew",
  "Kellam Kit",
  "Kelly Brody",
  "Lam Trystan",
  "Larson Evan",
  "Lawrence Kayley",
  "Levin Rosie",
  "Lisiewski Aubrie",
  "Maginnis Max",
  "Malta Maggie",
  "Malta Sam",
  "Marques Mateo",
  "McCabe Sean",
  "McManus Aiden",
  "Meacham Dylan",
  "Moore Addisyn",
  "Moore Savannah",
  "Moulta Ali Aliyah",
  "Obara Kate",
  "Phelps Andrew",
  "Phelps Jacob",
  "Richardson Kaleb",
  "Robinson Aeryn",
  "Russ Nolan",
  "Ryan Dakota",
  "Sayan Nicholas",
  "Snell Robert",
  "Stifflemire Grace",
  "Studgeon Matthew",
  "Tracy Daniel",
  "Tsampos Michael",
  "Webb Michael",
  "Yoshida Gabe");
  
  autocomplete(document.getElementById("name"), names);
  */