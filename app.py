# libraries
from flask import Flask, render_template, url_for, redirect, abort
import time
import json
import requests
import os
import random
# root files
from scripts import *
# from env import *

# Initialize app
app = Flask(__name__)

# Query API to dynamically generate site
areas = requests.get('https://skiforecast-api.herokuapp.com/api/v1/areas', auth=(os.environ['API_User'], os.environ['API_KEY'])) #(userpass(), userpass()))
areas = areas.json()

@app.route("/", methods =['GET'])
def index():
    # Query API to dynamically generate site
    areas = requests.get('https://skiforecast-api.herokuapp.com/api/v1/areas', auth=(os.environ['API_User'], os.environ['API_KEY'])) #(userpass(), userpass()))
    areas = areas.json()
    # Create list, pass to Jinja to generate dynamic links
    resort_name_list = {}
    backcountry_name_list = {}
    rand = random.randint(0, (len(areas)-1))
    rand_url = areas[rand]["name"]
    for area in areas:
        if 'resort' == area["area_type"]:
            url = area["name"]
            name = create_header(area["name"])
            resort_name_list.update({url:name})
        elif 'backcountry' == area["area_type"]:
            url = area["name"]
            name = create_header(area["name"])
            backcountry_name_list.update({url:name})
    return render_template('index.html', title = 'Home - Will\'s Ski Forecast', 
                            backcountry_name_list = backcountry_name_list, resort_name_list = resort_name_list, rand_url=rand_url)

@app.route("/<area_name>", methods =['GET'])
def forecast(area_name):
    # Query API to dynamically generate site
    areas = requests.get('https://skiforecast-api.herokuapp.com/api/v1/areas', auth=(os.environ['API_User'], os.environ['API_KEY'])) #(userpass(), userpass()))
    areas = areas.json()
    # Generate page if it exists in API
    for area in areas:
        if str(area_name) == area["name"]:
            # Code graphs in here
            # Get str vars to pass to functions
            name = area["name"]
            area_type = area["area_type"]
            avalanche_forecast = area["avalanche_forecast"]
            coordinates = area["coordinates"]
            tz_info = area["tz_info"]
            NAM_elevation = area["NAM_elevation"]
            HRDPS_elevation = area["HRDPS_elevation"]
            # Call functions to get data
            map_coordinates = get_map_coordinates(coordinates)
            avy_data = get_avy_forecast(avalanche_forecast)
            weather_data = get_HRDPS_weather(coordinates, tz_info)
            NAM_data = get_NAM_weather(coordinates, tz_info)
            # Create weather graphs
            HRDPS_plot = create_HRDPS_graph(weather_data)
            NAM_plot = create_NAM_graph(NAM_data)
            # Create avalanche info
            avy_danger = get_avy_danger(avy_data)
            avy_problems = get_avy_problems(avy_data)
            # Create forecast summary for end of page
            summary = []
            summary.append("<h3>Highlights:</h3>" + avy_data["highlights"])
            summary.append("<h3>Avalanche Summary:</h3>" + avy_data["avalancheSummary"])
            summary.append("<h3>Snowpack Summary:</h3>" + avy_data["snowpackSummary"])
            summary.append("<h3>Regional Summary:</h3>" + avy_data["weatherForecast"])
            # Return template and vars to pass to Jinja
            return render_template('forecast.html', 
                                    title = create_header(area["name"]) + ' - Will\'s Ski Forecast', 
                                    header = create_header(area["name"]), 
                                    map_coordinates = map_coordinates,
                                    HRDPS_plot = HRDPS_plot, 
                                    NAM_plot = NAM_plot, 
                                    summary = summary, 
                                    avy_danger = avy_danger, 
                                    avy_problems = avy_problems, 
                                    confidence = avy_data["confidence"], 
                                    date_issued = 'Date Issued: '+ avy_data["dateIssued"][:10], 
                                    NAM_elevation = NAM_elevation,
                                    HRDPS_elevation = HRDPS_elevation,)
    # Requested route doesn't exist in API
    else:
        abort (404)

# Run app
if __name__ == "__main__":
    app.run()