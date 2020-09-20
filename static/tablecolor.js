const elevations = document.querySelectorAll(".elev");
console.log(elevations)
const dangers = document.querySelectorAll(".danger");

elevations.forEach(function(elevation){
  console.log(elevation);
  switch(elevation.innerHTML){
    case ' Alpine ':
      elevation.style.background = 'AliceBlue';
      break;
    case ' Treeline ':
      elevation.style.background = '#c1d831';
      break;
    case ' Below Treeline ':
      elevation.style.background = 'SeaGreen';
      break;
  }
});

dangers.forEach(function(danger){
  switch(danger.innerHTML){
    case ' Extreme ':
      danger.style.background = 'black';
      danger.style.color = "white";
      break;
    case ' High ':
      danger.style.background = 'red';
      break;
    case ' Considerable ':
      danger.style.background = 'orange';
      break;
    case ' Moderate ':
      danger.style.background = 'yellow';
      break;
    case ' Low ':
      danger.style.background = 'green';
      break;
    default:
      danger.style.background = 'white';
  }
});