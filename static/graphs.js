//Hide / Show Graphs button

function toggle_forecast() {
  var x = document.getElementById("weathergraph");
  if (x.innerHTML === `
  <h3>48H Forecast (GEM-LAM, 2.5km res)</h3> 
  {{HRDPS_plot | safe}} 
  <p>Model elevation: {{HRDPS_elevation}}</p>
  `) {
    x.innerHTML === `
    <h3>3.5 Day Forecast (NAM, 12km res)</h3>
    {{NAM_plot | safe}}
    <p>Model elevation: {{NAM_elevation}}</p>
    `;
  } else {
    x.innerHTML = `
    <h3>48H Forecast (GEM-LAM, 2.5km res)</h3> 
    {{HRDPS_plot | safe}} 
    <p>Model elevation: {{HRDPS_elevation}}</p>
    `;
  }
}

function show_historical() {
  var x = document.getElementById("72H");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
