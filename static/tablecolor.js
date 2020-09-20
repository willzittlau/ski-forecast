document.addEventListener("DOMContentLoaded", function () {

  const elevations = document.querySelectorAll(".elev");
  const dangers = document.querySelectorAll(".danger");

  elevations.forEach(function (elevation) {
    switch (elevation.innerHTML) {
      case " Alpine ":
        elevation.style.background = "AliceBlue";
        break;
      case " Treeline ":
        elevation.style.background = "#c1d831";
        break;
      case " Below Treeline ":
        elevation.style.background = "SeaGreen";
        break;
    }
  });

  dangers.forEach(function (danger) {
    switch (danger.innerHTML) {
      case " 5:Extreme ":
        danger.style.background = "black";
        danger.style.color = "white";
        break;
      case " 4:High ":
        danger.style.background = "red";
        break;
      case " 3:Considerable ":
        danger.style.background = "orange";
        break;
      case " 2:Moderate ":
        danger.style.background = "yellow";
        break;
      case " 1:Low ":
        danger.style.background = "green";
        break;
      default:
        danger.style.background = "white";
    }
  });
});
