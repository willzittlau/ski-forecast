//Hide / Show Graphs button

function toggle_HRDPS() {
    var x = document.getElementById("48H");
    if (x.style.display === "none") {
        x.style.display = "block"; 
    } 
    else {
        x.style.display = "none";
    }
}

function toggle_NAM() {
    var y = document.getElementById("72H");
    if (x.style.display === "block") {
        x.style.display = "none"; 
    } 
    else {
        x.style.display = "block";
    }
}

/*
function show_historical() {
    var x = document.getElementById("72H");
    if (x.style.display === "none") {
        x.style.display = "block"; 
    } 
    else {
        x.style.display = "none";
    }
}
*/