//Hide / Show Graphs button
var counter = 'start';

function toggle_graph() {
    var x = document.getElementById("48H");
    var y = document.getElementById("72H");
    var z = document.getElementById("10D");
    if (counter === 'start'){
        x.style.display = "none"; 
        y.style.display = "block";
        z.style.display = "none";
        counter =2;
    }
    else if (counter === 0) {
        x.style.display = "block"; 
        y.style.display = "none";
        z.style.display = "none";
        counter += 1;
    }
    else if (counter === 1){
        x.style.display = "none"; 
        y.style.display = "block";
        z.style.display = "none";
        counter +=1;
    }
    else if (counter === 2){
        x.style.display = "none"; 
        y.style.display = "none";
        z.style.display = "block";
        counter = 0;
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