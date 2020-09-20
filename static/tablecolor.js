const elevations = document.querySelectorAll(".elev");
const dangers = document.querySelectorAll(".danger");

elevations.forEach(function(elevation){
  switch(elevation.innerHTML){
    case 'Alpine':
      elevation.style.background = 'blue';
      break;
    case 'Treeline':
      elevation.style.background = 'green';
      break;
    case 'Below Treeline':
      elevation.style.background = 'brown';
      break;
  }
});

dangers.forEach(function(danger){
  switch(danger.innerHTML){
    case 'Extreme':
      danger.style.background = 'black';
      danger.style.color = "white";
      break;
    case 'High':
      danger.style.background = 'red';
      break;
    case 'Considerable':
      danger.style.background = 'orange';
      break;
    case 'Moderate':
      danger.style.background = 'yellow';
      break;
    case 'Low':
      danger.style.background = 'lime';
      break;
  }
});