#imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import lxml
import re
import datetime
#graphing
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Band, Tabs, Panel
from bokeh.models.tools import HoverTool
from bokeh.resources import CDN
from bokeh.embed import file_html

def get_current_weather(coordinates):
    # Query SpotWX
    response = requests.get('https://spotwx.com/products/grib_index.php?model=gem_lam_continental&%s&tz=America/Vancouver&display=table' % coordinates).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text = re.compile("var aDataSet =")))
    # Regex parsing
    m = re.search(r'\[.*\](?= )', scripts)
    m = m.group(0)
    data = re.findall(r'\[(.*?)\]', m)
    df = []
    for sets in data:
        sets = sets.split('\',\'')
        for s in sets:
            s = s.replace('\'', '')
        df.append(sets)
    # Create df and drop unwanted colmuns
    df = pd.DataFrame(columns = ["DATETIME", "DATE", "TIME", "TMP", 
                    "DPT", "RH", "WS", "WD", "APCP", "CLOUD", 
                    "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP", 
                    "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX"], data = df)
    df = df.drop(columns=
                    ["DATETIME", "DPT", "RH", "APCP", 
                    "SLP", "PTYPE", "FQP", "IQP", 
                    "WS925", "WD925", "TMP850", 
                    "WS850", "WD850", "4LFTX"])
    # Correct data types from str input
    df["DATETIME"] = ''
    for i in range (0,len(df['TIME'])):
        df.at[i, 'WD'] = convert_compass(df.at[i, 'WD'])
        df.at[i, 'TMP'] = float(df.at[i, 'TMP'])
        df.at[i, 'WS'] = float(df.at[i, 'WS'])
        df.at[i, 'CLOUD'] = float(df.at[i, 'CLOUD'])
        df.at[i, 'RQP'] = float(df.at[i, 'RQP'])
        df.at[i, 'SQP'] = float(df.at[i, 'SQP'])
        df.at[i, 'SQP'] *= 10.0
        df.at[i, 'DATE'] = datetime.datetime.strptime(df.at[i, 'DATE'], '%Y/%m/%d').date()
        df.at[i, 'TIME'] = datetime.datetime.strptime(df.at[i, 'TIME'], '%H:%M').time()
        df.at[i, 'DATETIME'] = datetime.datetime.combine(df.at[i, 'DATE'], df.at[i, 'TIME'])
    return df

def get_averages_totals(df):
    # Default for precip is sum hourly
    rain = df['RQP'].iloc[-1]
    snow = df['SQP'].iloc[-1]
    # Average ws and tmp
    div = float(len(df['TMP']))
    tmp_tot = float(df[['TMP']].sum())
    temp = float(tmp_tot/div)
    temp = round(temp, 1)
    wind_tot = float(df[['WS']].sum())
    wind = float(wind_tot/div)
    wind = round(wind, 1)
    return rain, snow, temp, wind

def get_avy_forecast(avalanche_forecast):
    # Query Avcan API
    #response = requests.get('https://www.avalanche.ca/api/forecasts/%s.json' % avalanche_forecast)
    response = requests.get('https://www.avalanche.ca/api/bulletin-archive/2020-01-07/%s.json' % avalanche_forecast)
    data = response.json()
    return data

def convert_compass(direction):
    # Convert int into directional string
    if 22.5 <= int(direction) <= 67.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' NE'
    elif 67.5 <= int(direction) <= 112.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' E'
    elif 112.5 <= int(direction) <= 157.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' SE'
    elif 157.5 <= int(direction) <= 202.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' S'
    elif 202.5 <= int(direction) <= 247.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' SW'
    elif 247.5 <= int(direction) <= 292.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' W'
    elif 292.5 <= int(direction) <= 337.5:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' NW'
    else:
        direction = str(direction) + u'\N{DEGREE SIGN}' + ' N'
    return direction

def convert_elevtxt(elevation):
    # Convert text from API to human friendly
    elevation = elevation.lower()
    if elevation == 'alp':
        elevation = 'Alpine'
    elif elevation == 'tln':
        elevation = 'Treeline'
    elif elevation == 'btl':
        elevation = 'Below Treeline'
    return elevation

def create_header(header_name):
    # Change API data to human friendly titles
    header = header_name
    header = header.title()
    header = header.replace('-', ' ')
    return header

def get_avy_danger(avy_data):
    # Parse API data and create HTML strings to pass to Jinja
    danger_list = avy_data["dangerRatings"]
    date =[]
    # Write the 3 forecast days
    for danger_date in danger_list:
        string = '<h4>' + danger_date["date"][:10] + '</h4>'
        date.append(string)
    danger = []
    # Rename keys
    for dangers in danger_list:
        dangers['dangerRating']['Alpine'] = dangers['dangerRating'].pop('alp')
        dangers['dangerRating']['Treeline'] = dangers['dangerRating'].pop('tln')
        dangers['dangerRating']['Below Treeline'] = dangers['dangerRating'].pop('btl')
        danger.append(dangers['dangerRating'])
    return date, danger

def get_avy_problems(avy_data):
    # Create html string to pass to jinja from API data
    problems_list = []
    problems_data = avy_data["problems"]
    # Write problem type and expected size
    for problem in problems_data:
        output_string = '<h4>' + problem["type"] + '</h4>' + '<p><b>Expected Size = </b>'
        for key, value in problem["expectedSize"].items():
            output_string += key.title() + ': ' + value + ', '
        # Write Likelihood and Aspects
        output_string += '<b>Likelihood = </b>' + problem["likelihood"] + '</p><p><b>Aspects = </b>'
        for aspect in problem["aspects"]:
            output_string += aspect + ', '
        # Write elevations
        output_string += '<b>Elevations = </b>'
        for elevation in problem["elevations"]:
            elevation = convert_elevtxt(elevation)
            output_string += elevation + ', '
        # Clean up final output string
        output_string = output_string[:-2]
        output_string += '</p><p>' + problem["comment"] + '</p>'
        problems_list.append(output_string)
    return problems_list

def daily_weather(coordinates):
    json.dumps()
    db.session.add
    db.session.commit()

def create_todays_graph(df):
    source = ColumnDataSource(df)

    p1 = figure(x_axis_type='datetime', plot_width=600, plot_height=300, toolbar_location=None)
    p1.title.text = '48H Temperature'
    p1.xaxis.axis_label = 'Date/Time'
    p1.yaxis.axis_label = 'Temperature \N{DEGREE SIGN}C'

    glyph_1 = p1.line(x= 'DATETIME', y='TMP',source=source, legend_label='Temperature', color='OrangeRed', line_width=1.5)
    glyph_1a = p1.scatter(x= 'DATETIME', y='TMP',source=source, line_color="darkRed", fill_color="OrangeRed", size=4)

    hover1 = HoverTool(renderers=[glyph_1], tooltips=[('\N{DEGREE SIGN}C', '@TMP')])
    p1.add_tools(hover1)

    tab1 = Panel(child=p1, title="Temperature")

    p2 = figure(x_axis_type='datetime', plot_width=600, plot_height=300, toolbar_location=None)
    p2.title.text = '48H Precipitation'
    p2.xaxis.axis_label = 'Date/Time'
    p2.yaxis.axis_label = 'Amount (mm/cm)'

    glyph_1 = p2.line(x= 'DATETIME', y='RQP',source=source, legend_label='Total Rain', color='blue', line_width=1.5)
    glyph_1a = p2.scatter(x= 'DATETIME', y='RQP',source=source, line_color="darkblue", fill_color="blue", size=4)
    glyph_2 = p2.line(x= 'DATETIME', y='SQP',source=source, legend_label='Total Snow', color='lightgrey', line_width=1.5)
    glyph_2a = p2.scatter(x= 'DATETIME', y='SQP',source=source, line_color="grey", fill_color="lightgrey", size=4)

    p2.varea(x='DATETIME', y1='SQP', source=source, color='WhiteSmoke', alpha=0.8)
    band = Band(base='DATETIME', upper='RQP', source=source, level='overlay', fill_alpha=0.3, fill_color='SkyBlue')
    p2.add_layout(band)

    hover2a = HoverTool(renderers=[glyph_1], tooltips=[('mm Rain', '@RQP')])
    hover2b = HoverTool(renderers=[glyph_2], tooltips=[('cm Snow', '@SQP')])
    p2.add_tools(hover2a, hover2b)

    tab2 = Panel(child=p2, title="Precipitation")

    p3 = figure(x_axis_type='datetime', plot_width=600, plot_height=300, toolbar_location=None)
    p3.title.text = '48H Wind/Cloud'
    p3.xaxis.axis_label = 'Date/Time'
    p3.yaxis.axis_label = 'Speed (km/h) / % Coverage'

    glyph_1 = p3.line(x= 'DATETIME', y='WS',source=source, legend_label='Wind Speed', color='green', line_width=1.5)
    glyph_1a = p3.scatter(x= 'DATETIME', y='WS',source=source, line_color="darkgreen", fill_color="green", size=4)
    glyph_2 = p3.line(x= 'DATETIME', y='CLOUD',source=source, legend_label='Cloud Cover', color='grey', line_width=1.5)
    glyph_2a = p3.scatter(x= 'DATETIME', y='CLOUD',source=source, line_color="darkgrey", fill_color="grey", size=4)

    band = Band(base='DATETIME', upper='CLOUD', source=source, level='underlay', fill_alpha=0.3, fill_color='lightgrey')
    p3.add_layout(band)

    hover3a = HoverTool(renderers=[glyph_1], tooltips=[('Wind Speed', '@WS'), ('Wind Direction', '@WD')])
    hover3b = HoverTool(renderers=[glyph_2], tooltips=[('% Coverage', '@CLOUD')])
    p3.add_tools(hover3a, hover3b)

    tab3 = Panel(child=p3, title="Wind/Cloud")

    plot = Tabs(tabs=[tab1, tab2 , tab3])

    html = file_html(plot, CDN)
    return html

df = get_current_weather("lat=62.11416&lon=-121.19238")