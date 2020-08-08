# libraries
from flask import Flask, render_template, url_for, redirect, abort
import time
import json
import requests
import traceback
from werkzeug.wsgi import ClosingIterator
# root files
from scripts import *
from env import *

class AfterResponse:
    def __init__(self, app=None):
        self.callbacks = []
        if app:
            self.init_app(app)

    def __call__(self, callback):
        self.callbacks.append(callback)
        return callback

    def init_app(self, app):
        # install extension
        app.after_response = self

        # install middleware
        app.wsgi_app = AfterResponseMiddleware(app.wsgi_app, self)

    def flush(self): 
        for fn in self.callbacks:
            try:
                fn()
            except Exception:
                traceback.print_exc()

class AfterResponseMiddleware:
    def __init__(self, application, after_response_ext):
        self.application = application
        self.after_response_ext = after_response_ext

    def __call__(self, environ, start_response):
        iterator = self.application(environ, start_response)
        try:
            return ClosingIterator(iterator, [self.after_response_ext.flush])
        except Exception:
            traceback.print_exc()
            return iterator

app = Flask(__name__)
AfterResponse(app)

# Query API to dynamically generate site (used as global var)
areas = requests.get('https://skiforecast-api.herokuapp.com/api/v1/areas', auth=(userpass(), userpass())) #os.environ['API_User'], os.environ['API_KEY']
areas = areas.json()

@app.route("/", methods =['GET'])
def index():
    # Create list, pass to Jinja to generate dynamic links
    global areas
    name_list = []
    for area in areas:
        name_list.append(area["name"])
    return render_template('index.html', title = 'Home - Will\'s Weather Forecast', name_list = name_list)

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
            #
            # Create avalanche info
            #
            # Create forecast summary for end of page
            summary = ("<h3>Highlights:</h3>" + avy_data["highlights"] + 
                        "<h3>Avalanche Summary:</h3>" + avy_data["avalancheSummary"] + 
                        "<h3>Snowpack Summary:</h3>" + avy_data["snowpackSummary"] + 
                        "<h3>Forecast Region Summary:</h3>" + avy_data["weatherForecast"] )
            # Return template and vars to pass to Jinja
            return render_template('forecast.html', 
                                    title = create_header(area["name"]) + ' - Will\'s Weather Forecast', 
                                    header = create_header(area["name"]), 
                                    summary = summary, 
                                    )
    # Requested route doesn't exist in API
    else:
        abort (404)

@app.route("/test", methods =['GET'])
def test():
    refresh = 0
    data = ''
    @app.after_response
    def after():
        data= ''
        refresh = 0
        time.sleep(5)
        data = 'hello again'
        refresh = 1
        with app.app_context(), app.test_request_context():
            return render_template('index.html', data=data, refresh=refresh)
    return render_template('index.html', data = data, refresh = refresh)

# Run app
if __name__ == "__main__":
    app.run(debug=True)