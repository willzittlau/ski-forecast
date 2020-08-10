from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import lxml
import re
import datetime

def get_current_weather(coordinates):
    response = requests.get('https://spotwx.com/products/grib_index.php?model=gem_lam_continental&%s&tz=America/Vancouver&display=table' % coordinates).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text = re.compile("var aDataSet =")))
    m = re.search(r'\[.*\](?= )', scripts)
    m = m.group(0)
    data = re.findall(r'\[(.*?)\]', m)
    df = []
    for sets in data:
        sets = sets.split('\',\'')
        for s in sets:
            s = s.replace('\'', '')
        df.append(sets)
    df = pd.DataFrame(columns = ["DATETIME", "DATE", "TIME", "TMP", 
                    "DPT", "RH", "WS", "WD", "APCP", "CLOUD", 
                    "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP", 
                    "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX"], data = df)
    df = df.drop(columns=
                    ["DATETIME", "DPT", "RH", "APCP", 
                    "SLP", "PTYPE", "FQP", "IQP", 
                    "WS925", "WD925", "TMP850", 
                    "WS850", "WD850", "4LFTX"])
    return df

def get_avy_forecast(avalanche_forecast):
    #response = requests.get('https://www.avalanche.ca/api/forecasts/%s.json' % avalanche_forecast)
    response = requests.get('https://www.avalanche.ca/api/bulletin-archive/2020-01-07/%s.json' % avalanche_forecast)
    data = response.json()
    return data

def convert_compass(direction):
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
    elevation = elevation.lower()
    if elevation == 'alp':
        elevation = 'Alpine'
    elif elevation == 'tln':
        elevation = 'Treeline'
    elif elevation == 'btl':
        elevation = 'Below Treeline'
    return elevation

def create_header(header_name):
    header = header_name
    header = header.title()
    header = header.replace('-', ' ')
    return header

def get_avy_danger(avy_data):
    danger_list = avy_data["dangerRatings"]
    date =[]
    for danger_date in danger_list:
        string = '<h4>' + danger_date["date"][:10] + '</h4>'
        date.append(string)
    danger = []
    for dangers in danger_list:
        dangers['dangerRating']['Alpine'] = dangers['dangerRating'].pop('alp')
        dangers['dangerRating']['Treeline'] = dangers['dangerRating'].pop('tln')
        dangers['dangerRating']['Below Treeline'] = dangers['dangerRating'].pop('btl')
        danger.append(dangers['dangerRating'])
    return date, danger

def get_avy_problems(avy_data):
    problems_list = []
    problems_data = avy_data["problems"]
    for problem in problems_data:
        output_string = '<h4>' + problem["type"] + '</h4>' + '<p><b>Expected Size = </b>'
        for key, value in problem["expectedSize"].items():
            output_string += key.title() + ': ' + value + ', '
        output_string += '<b>Likelihood = </b>' + problem["likelihood"] + '</p><p><b>Aspects = </b>'
        for aspect in problem["aspects"]:
            output_string += aspect + ', '
        output_string += '<b>Elevations = </b>'
        for elevation in problem["elevations"]:
            elevation = convert_elevtxt(elevation)
            print(elevation)
            output_string += elevation + ', '
        output_string = output_string[:-2]
        output_string += '</p><p>' + problem["comment"] + '</p>'
        problems_list.append(output_string)
    return problems_list

def daily_weather(coordinates):
    json.dumps()
    db.session.add
    db.session.commit()