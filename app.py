# libraries
from flask import Flask, render_template, url_for, redirect, abort
import time
import json
import requests
import os
# root files
from config import ProdConfig, DevConfig
from scripts import *
from env import *

# Initialize app
app = Flask(__name__)

# Configuration
app.config.from_object(DevConfig())
#api.config.from_object(ProdConfig())

'''
# Initialize dB
db = SQLAlchemy(api)
from models import *
'''

# Query API to dynamically generate site (used as global var)
areas = requests.get('https://skiforecast-api.herokuapp.com/api/v1/areas', auth=(userpass(), userpass())) #os.environ['API_User'], os.environ['API_KEY']
areas = areas.json()

@app.route("/", methods =['GET'])
def index():
    # Create list, pass to Jinja to generate dynamic links
    global areas
    resort_name_list = {}
    backcountry_name_list = {}
    for area in areas:
        if 'resort' == area["area_type"]:
            url = area["name"]
            name = create_header(area["name"])
            resort_name_list.update({url:name})
        elif 'backcountry' == area["area_type"]:
            url = area["name"]
            name = create_header(area["name"])
            backcountry_name_list.update({url:name})
    return render_template('index.html', title = 'Home - Will\'s Weather Forecast', 
                            backcountry_name_list = backcountry_name_list, resort_name_list = resort_name_list)

@app.route("/<area_name>", methods =['GET'])
def forecast(area_name):
    global areas
    # Generate page if it exists in API
    for area in areas:
        if str(area_name) == area["name"]:
            # Code graphs in here
            # Get str vars to pass to functions
            name = area["name"]
            area_type = area["area_type"]
            avalanche_forecast = area["avalanche_forecast"]
            coordinates = area["coordinates"]
            model_elevation = area["model_elevation"]
            # Call functions to get data
            avy_data = get_avy_forecast(avalanche_forecast)
            weather_data = get_current_weather(coordinates)
            # Create weather graphs
            forecast_plot = create_todays_graph(weather_data)
            historical_plot = create_todays_graph(weather_data)
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
                                    title = create_header(area["name"]) + ' - Will\'s Weather Forecast', 
                                    header = create_header(area["name"]), 
                                    forecast_plot = forecast_plot, 
                                    historical_plot = historical_plot, 
                                    summary = summary, 
                                    avy_danger = avy_danger, 
                                    avy_problems = avy_problems, 
                                    confidence = avy_data["confidence"], 
                                    date_issued = 'Date Issued: '+ avy_data["dateIssued"][:10], 
                                    elevation = model_elevation,)
    # Requested route doesn't exist in API
    else:
        abort (404)

# Run app
if __name__ == "__main__":
    app.run()