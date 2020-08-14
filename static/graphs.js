//Hide / Show Graphs button

function show_forecast() {
    var x = document.getElementById("48H");
    if (x.style.display === "none") {
        x.style.display = "block"; 
    } 
    else {
        x.style.display = "none";
    }
}

function show_historical() {
    var x = document.getElementById("72H");
    if (x.style.display === "none") {
        x.style.display = "block"; 
    } 
    else {
        x.style.display = "none";
    }
}