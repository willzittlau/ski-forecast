# imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import lxml
import re
import datetime
from datetime import timedelta
# graphing
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Band, Tabs, Panel, LinearAxis, Range1d, Legend
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.tools import HoverTool, ResetTool, ZoomInTool, ZoomOutTool, PanTool
from bokeh.resources import CDN
from bokeh.embed import file_html

def get_map_coordinates(coordinates):
    lat = coordinates[4:12]
    lon = coordinates[17:]
    map_coordinates = lat + ',' + lon
    src = 'https://maps.google.com/maps?width=100%%25&amp;height=500&amp;hl=en&amp;q=%s&amp;t=p&amp;z=12&amp;ie=UTF8&amp;iwloc=B&amp;output=embed' % map_coordinates
    return src

def get_HRDPS_weather(coordinates, tz_info):
    # Query SpotWX
    response = requests.get(
        'https://spotwx.com/products/grib_index.php?model=gem_lam_continental&%s&tz=%s&display=table' % (coordinates, tz_info)).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text=re.compile("var aDataSet =")))
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
    df = pd.DataFrame(columns=["DATETIME", "DATE", "TIME", "TMP",
                               "DPT", "RH", "WS", "WD", "APCP", "CLOUD",
                               "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP",
                               "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX"], data=df)
    # Correct data types from str input
    df["DATETIME"] = ''
    for i in range(0, len(df['TIME'])):
        df.at[i, 'WD'] = convert_compass(df.at[i, 'WD'])
        df.at[i, 'TMP'] = float(df.at[i, 'TMP'])
        df.at[i, 'WS'] = float(df.at[i, 'WS'])
        df.at[i, 'CLOUD'] = float(df.at[i, 'CLOUD'])
        df.at[i, 'RQP'] = float(df.at[i, 'RQP'])
        df.at[i, 'SQP'] = float(df.at[i, 'SQP'])
        df.at[i, 'FQP'] = float(df.at[i, 'FQP'])
        df.at[i, 'IQP'] = float(df.at[i, 'IQP'])
        df.at[i, 'DATE'] = datetime.datetime.strptime(
            df.at[i, 'DATE'], '%Y/%m/%d').date()
        df.at[i, 'TIME'] = datetime.datetime.strptime(
            df.at[i, 'TIME'], '%H:%M').time()
        df.at[i, 'DATETIME'] = datetime.datetime.combine(
            df.at[i, 'DATE'], df.at[i, 'TIME'])
    return df

def get_GFS_weather(coordinates, tz_info):
    # Query SpotWX
    response = requests.get(
        'https://spotwx.com/products/grib_index.php?model=gfs_pgrb2_0p25_f&%s&tz=%s&display=table' % (coordinates, tz_info)).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text=re.compile("var aDataSet =")))
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
    df = pd.DataFrame(columns=["DATETIME", "DATE", "TIME", "TMP",
                               "RH", "WS", "WD", "APCP", "CLOUD",
                               "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP",
                               "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX", "HGT_0C_DB"], data=df)
    # Correct data types from str input
    df["DATETIME"] = ''
    df.at[0, 'CLOUD'] = '0'
    for i in range(0, len(df['TIME'])):
        df.at[i, 'WD'] = convert_compass(df.at[i, 'WD'])
        df.at[i, 'TMP'] = float(df.at[i, 'TMP'])
        df.at[i, 'WS'] = float(df.at[i, 'WS'])
        df.at[i, 'CLOUD'] = float(df.at[i, 'CLOUD'])
        df.at[i, 'RQP'] = float(df.at[i, 'RQP'])
        df.at[i, 'SQP'] = float(df.at[i, 'SQP'])
        df.at[i, 'FQP'] = float(df.at[i, 'FQP'])
        df.at[i, 'IQP'] = float(df.at[i, 'IQP'])
        df.at[i, 'HGT_0C_DB'] = int(df.at[i, 'HGT_0C_DB'].replace("'", ""))
        df.at[i, 'DATE'] = datetime.datetime.strptime(
            df.at[i, 'DATE'], '%Y/%m/%d').date()
        df.at[i, 'TIME'] = datetime.datetime.strptime(
            df.at[i, 'TIME'], '%H:%M').time()
        df.at[i, 'DATETIME'] = datetime.datetime.combine(
            df.at[i, 'DATE'], df.at[i, 'TIME'])
    return df

def get_NAM_weather(coordinates, tz_info):
    # Query SpotWX
    response = requests.get(
        'https://spotwx.com/products/grib_index.php?model=nam_awphys&%s&tz=%s&display=table' % (coordinates, tz_info)).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text=re.compile("var aDataSet =")))
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
    df = pd.DataFrame(columns=["DATETIME", "DATE", "TIME", "TMP",
                               "DPT", "RH", "WS", "WD", "WG", "APCP", "CLOUD",
                               "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP",
                               "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX", "HGT_0C_DB", "HGT_0C_WB"], data=df)
    # Correct data types from str input
    df["DATETIME"] = ''
    for i in range(0, len(df['DATETIME'])):
        df.at[i, 'WD'] = convert_compass(df.at[i, 'WD'])
        df.at[i, 'TMP'] = float(df.at[i, 'TMP'])
        df.at[i, 'WS'] = float(df.at[i, 'WS'])
        df.at[i, 'WG'] = float(df.at[i, 'WG'])
        df.at[i, 'CLOUD'] = float(df.at[i, 'CLOUD'])
        df.at[i, 'RQP'] = float(df.at[i, 'RQP'])
        df.at[i, 'SQP'] = float(df.at[i, 'SQP'])
        df.at[i, 'FQP'] = float(df.at[i, 'FQP'])
        df.at[i, 'IQP'] = float(df.at[i, 'IQP'])
        df.at[i, 'HGT_0C_DB'] = int(df.at[i, 'HGT_0C_DB'])
        df.at[i, 'DATE'] = datetime.datetime.strptime(
            df.at[i, 'DATE'], '%Y/%m/%d').date()
        df.at[i, 'TIME'] = datetime.datetime.strptime(
            df.at[i, 'TIME'], '%H:%M').time()
        df.at[i, 'DATETIME'] = datetime.datetime.combine(
            df.at[i, 'DATE'], df.at[i, 'TIME'])
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
    response = requests.get(
        'https://www.avalanche.ca/api/forecasts/%s.json' % avalanche_forecast)  # prod
    # response = requests.get('https://www.avalanche.ca/api/bulletin-archive/2020-01-07/%s.json' % avalanche_forecast) #testing
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

def correct_date(dateString):
    wrongDate = datetime.date.fromisoformat(dateString)
    newDate = wrongDate - timedelta(days=1)
    return newDate

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
    date = []
    # Write the 3 forecast days
    for danger_date in danger_list:
        if avy_data['region'] == 'glacier':
            string = '<h4>' + danger_date["date"][:10] + '</h4>'
            date.append(string)
        else:
            forecastDate = str(correct_date(danger_date["date"][:10]))
            string = '<h4>' + forecastDate + '</h4>'
            date.append(string)
    danger = []
    # Rename keys
    for dangers in danger_list:
        dangers['dangerRating']['Alpine'] = dangers['dangerRating'].pop('alp')
        dangers['dangerRating']['Treeline'] = dangers['dangerRating'].pop(
            'tln')
        dangers['dangerRating']['Below Treeline'] = dangers['dangerRating'].pop(
            'btl')
        danger.append(dangers['dangerRating'])
    return date, danger

def get_avy_problems(avy_data):
    # Create html string to pass to jinja from API data
    problems_list = []
    problems_data = avy_data["problems"]
    # Write problem type and expected size
    for problem in problems_data:
        output_string = '<h4><u>' + \
            problem["type"] + '</u></h4>' + '<p><b>Expected Size = </b>'
        for key, value in problem["expectedSize"].items():
            output_string += key.title() + ': ' + value + ', '
        # Write Likelihood and Aspects
        output_string += '<b>Likelihood = </b>' + \
            problem["likelihood"] + '</p><p><b>Aspects = </b>'
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

def create_HRDPS_graph(df):
    source = ColumnDataSource(df)
    # create plot 1
    p1 = figure(x_axis_type='datetime', plot_width=600, plot_height=400, toolbar_location='above', sizing_mode='scale_width')
    p1.title.text = '48H Temperature'
    p1.xaxis.axis_label = 'Date/Time'
    p1.yaxis.axis_label = 'Temperature \N{DEGREE SIGN}C'
    # add lines
    glyph_1 = p1.line(x='DATETIME', y='TMP', source=source, color='OrangeRed', line_width=1.5)
    glyph_1a = p1.scatter(x='DATETIME', y='TMP', source=source, line_color="darkRed", fill_color="OrangeRed", size=4)
    # tools
    hover1 = HoverTool(renderers=[glyph_1], tooltips=[('\N{DEGREE SIGN}C', '@TMP'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    p1.tools = [ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    p1.toolbar.logo = None
    p1.toolbar.active_drag = None
    p1.toolbar.active_scroll = None
    p1.toolbar.active_tap = None
    p1.add_tools(hover1)
    # legend 1
    legend = Legend(items=[("Temp", [glyph_1, glyph_1a])], location="center", orientation="horizontal")
    p1.add_layout(legend, 'below')
    # create tab from plot
    tab1 = Panel(child=p1, title="Temperature")
    # create plot 2
    p2 = figure(x_axis_type='datetime', plot_width=600, plot_height=400, toolbar_location='above', sizing_mode='scale_width')
    p2.title.text = '48H Precipitation'
    p2.xaxis.axis_label = 'Date/Time'
    p2.yaxis.axis_label = 'Amount (mm/cm)'
    # Add lines
    glyph_1 = p2.line(x='DATETIME', y='RQP', source=source, color='blue', line_width=1.5)
    glyph_1a = p2.scatter(x='DATETIME', y='RQP', source=source, line_color="darkblue", fill_color="blue", size=4)
    glyph_2 = p2.line(x='DATETIME', y='SQP', source=source, color='lavender', line_width=1.5)
    glyph_2a = p2.scatter(x='DATETIME', y='SQP', source=source, line_color="lightsteelblue", fill_color="lavender", size=4)
    p2.varea(x='DATETIME', y1='SQP', source=source, color='GhostWhite', alpha=0.5)
    band = Band(base='DATETIME', upper='RQP', source=source, level='overlay', fill_alpha=0.3, fill_color='SkyBlue')
    p2.add_layout(band)
    # tools
    hover2a = HoverTool(renderers=[glyph_1], tooltips=[('mm Rain', '@RQP'), ('mm Freezing Rain', '@FQP'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    hover2b = HoverTool(renderers=[glyph_2], tooltips=[('cm Snow', '@SQP'), ('mm Ice/Hail', '@IQP'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    p2.tools = [ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    p2.toolbar.logo = None
    p2.toolbar.active_drag = None
    p2.toolbar.active_scroll = None
    p2.toolbar.active_tap = None
    p2.add_tools(hover2a, hover2b)
    # legend 2
    legend = Legend(items=[("Rain", [glyph_1, glyph_1a]), ("Snow", [glyph_2, glyph_2a])], location="center", orientation="horizontal")
    p2.add_layout(legend, 'below')
    # Create tab from plot
    tab2 = Panel(child=p2, title="Precipitation")
    # create plot 3
    p3 = figure(x_axis_type='datetime', plot_width=600, plot_height=400, toolbar_location='above', sizing_mode='scale_width')
    p3.title.text = '48H Wind/Cloud'
    p3.xaxis.axis_label = 'Date/Time'
    p3.yaxis.axis_label = 'Speed (km/h) / % Coverage'
    # Add lines
    glyph_1 = p3.line(x='DATETIME', y='WS', source=source, color='green', line_width=1.5)
    glyph_1a = p3.scatter(x='DATETIME', y='WS', source=source, line_color="darkgreen", fill_color="green", size=4)
    glyph_2 = p3.line(x='DATETIME', y='CLOUD', source=source, color='grey', line_width=1.5)
    glyph_2a = p3.scatter(x='DATETIME', y='CLOUD', source=source, line_color="darkgrey", fill_color="grey", size=4)
    band = Band(base='DATETIME', upper='CLOUD', source=source, level='underlay', fill_alpha=0.3, fill_color='lightgrey')
    p3.add_layout(band)
    # tools
    hover3a = HoverTool(renderers=[glyph_1], tooltips=[('Wind Speed', '@WS'), ('Wind Direction', '@WD'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    hover3b = HoverTool(renderers=[glyph_2], tooltips=[('% Coverage', '@CLOUD'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    p3.tools = [ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    p3.toolbar.logo = None
    p3.toolbar.active_drag = None
    p3.toolbar.active_scroll = None
    p3.toolbar.active_tap = None
    p3.add_tools(hover3a, hover3b)
    # legend 3
    legend = Legend(items=[("Wind", [glyph_1, glyph_1a]), ("Cloud", [glyph_2, glyph_2a])], location="center", orientation="horizontal")
    p3.add_layout(legend, 'below')
    # Create tab from plot
    tab3 = Panel(child=p3, title="Wind/Cloud")
    # merge to final plot
    plot = Tabs(tabs=[tab1, tab2, tab3])
    # return graph
    html = file_html(plot, CDN)
    return html

def create_NAM_graph(df):
    source = ColumnDataSource(df)
    # Create plot 1
    y_overlimit = 0.05
    p1 = figure(x_axis_type='datetime', plot_width=600, plot_height=400, toolbar_location='above', sizing_mode='scale_width')
    if len(df) > 65:
        p1.title.text = '10 Day Temperature'
    else:
        p1.title.text = '3.5 Day Temperature'
    p1.xaxis.axis_label = 'Date/Time'
    p1.yaxis.axis_label = 'Temperature \N{DEGREE SIGN}C'
    # add lines
    glyph_1 = p1.line(x='DATETIME', y='TMP', source=source, color='OrangeRed', line_width=1.5)
    glyph_1a = p1.scatter(x='DATETIME', y='TMP', source=source, line_color="darkRed", fill_color="OrangeRed", size=4)
    p1.y_range = Range1d(df['TMP'].min() * (1 - y_overlimit), df['TMP'].max() * (1 + y_overlimit))
    # SECOND AXIS
    y_column2_range = "HGT_0C_DB" + "_range"
    p1.extra_y_ranges = {y_column2_range: Range1d(start=df['HGT_0C_DB'].min() * (1 - y_overlimit), end=df['HGT_0C_DB'].max() * (1 + y_overlimit))}
    p1.add_layout(LinearAxis(y_range_name=y_column2_range, axis_label='Elevation (m)'), "right")
    # add lines
    glyph_2 = p1.line(x='DATETIME', y="HGT_0C_DB", source=source, line_width=1.5, y_range_name=y_column2_range, color="gold")
    glyph_2a = p1.scatter(x='DATETIME', y='HGT_0C_DB', source=source, y_range_name=y_column2_range, line_color="goldenrod", fill_color="gold", size=4)
    # tools
    hover1a = HoverTool(renderers=[glyph_1], tooltips=[('\N{DEGREE SIGN}C', '@TMP'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    hover1b = HoverTool(renderers=[glyph_2], tooltips=[('m', '@HGT_0C_DB'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    p1.tools = [ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    p1.toolbar.logo = None
    p1.toolbar.active_drag = None
    p1.toolbar.active_scroll = None
    p1.toolbar.active_tap = None
    p1.add_tools(hover1a, hover1b)
    # legend 1
    legend = Legend(items=[("Temp", [glyph_1, glyph_1a]), ("Frz Lvl", [glyph_2, glyph_2a])], location="center", orientation="horizontal")
    p1.add_layout(legend, 'below')
    # create tab from plot
    tab1 = Panel(child=p1, title="Temperature")
    # create plot 2
    p2 = figure(x_axis_type='datetime', plot_width=600, plot_height=400, toolbar_location='above', sizing_mode='scale_width')
    if len(df) > 65:
        p2.title.text = '10 Day Precipitation'
    else:
        p2.title.text = '3.5 Day Precipitation'
    p2.xaxis.axis_label = 'Date/Time'
    p2.yaxis.axis_label = 'Amount (mm/cm)'
    # add lines
    glyph_1 = p2.line(x='DATETIME', y='RQP', source=source, color='blue', line_width=1.5)
    glyph_1a = p2.scatter(x='DATETIME', y='RQP', source=source, line_color="darkblue", fill_color="blue", size=4)
    glyph_2 = p2.line(x='DATETIME', y='SQP', source=source, color='lavender', line_width=1.5)
    glyph_2a = p2.scatter(x='DATETIME', y='SQP', source=source, line_color="lightsteelblue", fill_color="lavender", size=4)
    p2.varea(x='DATETIME', y1='SQP', source=source, color='GhostWhite', alpha=0.5)
    band = Band(base='DATETIME', upper='RQP', source=source, level='overlay', fill_alpha=0.3, fill_color='SkyBlue')
    p2.add_layout(band)
    # tools
    hover2a = HoverTool(renderers=[glyph_1], tooltips=[('mm Rain', '@RQP'), ('mm Freezing Rain', '@FQP'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    hover2b = HoverTool(renderers=[glyph_2], tooltips=[('cm Snow', '@SQP'), ('mm Ice/Hail', '@IQP'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    p2.tools = [ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    p2.toolbar.logo = None
    p2.toolbar.active_drag = None
    p2.toolbar.active_scroll = None
    p2.toolbar.active_tap = None
    p2.add_tools(hover2a, hover2b)
    # legend 2
    legend = Legend(items=[("Rain", [glyph_1, glyph_1a]), ("Snow", [glyph_2, glyph_2a])], location="center", orientation="horizontal")
    p2.add_layout(legend, 'below')
    # create tab from plot
    tab2 = Panel(child=p2, title="Precipitation")
    # plot 3
    p3 = figure(x_axis_type='datetime', plot_width=600, plot_height=400, toolbar_location='above', sizing_mode='scale_width')
    if len(df) > 65:
        p1.title.text = '10 Day Wind/Cloud'
    else:
        p1.title.text = '3.5 Day Wind/Cloud'
    p3.xaxis.axis_label = 'Date/Time'
    p3.yaxis.axis_label = 'Speed (km/h) / % Coverage'
    # add lines
    glyph_1 = p3.line(x='DATETIME', y='WS', source=source, color='green', line_width=1.5)
    glyph_1a = p3.scatter(x='DATETIME', y='WS', source=source, line_color="darkgreen", fill_color="green", size=4)
    glyph_2 = p3.line(x='DATETIME', y='CLOUD', source=source, color='grey', line_width=1.5)
    glyph_2a = p3.scatter(x='DATETIME', y='CLOUD', source=source, line_color="darkgrey", fill_color="grey", size=4)
    band = Band(base='DATETIME', upper='CLOUD', source=source, level='underlay', fill_alpha=0.3, fill_color='lightgrey')
    p3.add_layout(band)
    # tools
    hover3a = HoverTool(renderers=[glyph_1], tooltips=[('Wind Speed', '@WS'), ('Wind Direction', '@WD'), ('Gusts', '@WG'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    hover3b = HoverTool(renderers=[glyph_2], tooltips=[('% Coverage', '@CLOUD'), ('Time', '@DATETIME{%F %T}')], formatters={'@DATETIME': 'datetime'}, mode='vline')
    p3.toolbar.logo = None
    p3.tools = [ZoomInTool(), ZoomOutTool(), PanTool(), ResetTool()]
    p3.toolbar.active_drag = None
    p3.toolbar.active_scroll = None
    p3.toolbar.active_tap = None
    p3.add_tools(hover3a, hover3b)
    # legend 3
    legend = Legend(items=[("Wind", [glyph_1, glyph_1a]), ("Cloud", [glyph_2, glyph_2a])], location="center", orientation="horizontal")
    p3.add_layout(legend, 'below')
    # tab from plot
    tab3 = Panel(child=p3, title="Wind/Cloud")
    # merge tabs into one plot
    plot = Tabs(tabs=[tab1, tab2, tab3])
    # return plot
    html = file_html(plot, CDN)
    return html

get_GFS_weather('lat=49.76125&lon=-123.02319', 'America/Vancouver')