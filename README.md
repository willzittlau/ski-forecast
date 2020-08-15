# Ski/Weather Forecast app
**For a live demo of V1, please visit https://skiforecast.herokuapp.com/**

This is a personal weather forecast app I made to streamline the process when I'm looking at which areas to ski in the winter. 

It's written using Flask in python3, and deployed to Heroku. It queries its sister API to dynamically generate site contents. Bokeh is the graphing library, and is used along with Jinja and some jQuery to create the dynamic content. Add in some HTML for structure and the light amount of CSS is mainly from Pure-CSS. The page structures are built from SpotWX and Avalanche Canada data, so in the summer time the site will load empty/placeholder avalanche data, but the weather graphs should work year round.

V2 is in progress and will add two additional graphs of 3 and 7 day historical weather by integrating a mongoDB nosql database and a manager file which will addd the daily data. In scripts.py I'll add a function which will query and append the data and pass it to the graphing function. I'll also add a toggle switch between the 48H/3.5D forward forecast, and the 3/7D historical. Also, some improvements to the UI, especially on the landing page.

## Usage

Use this site as much as youd like!! :) message me if you want a specific area added.

## Limitations

This site queries SpotWX and Avalanche Canada to generate data. It may break if the structure of either of these sites changes. Currently it will only work for areas in Canada due to using Avalanche Canada avy forecast data.

## Contributing

Let me know any changes you'd want to see!

## License
[MIT](https://choosealicense.com/licenses/mit/) Free Usage
