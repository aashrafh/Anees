from datetime import datetime
import pandas as pd
import time_extract
import requests
import json
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta


def extract_time_location(tokens, tokens_verb_noun,ents):
    cities = pd.read_csv('Task_data/weather_cities.csv',encoding='utf-8')
    #if the text not a question then we have to generate a text if we agree or not
    #defaults
    location = "Cairo"#the location of GPS
    #extract features from text -> location & Time
    for ent,value in ents.items():
        if value == 'B-LOC':
            if ent in list(cities['Arabic Name']):
                location = cities[cities['Arabic Name'] == ent]['capital'].values[0]
            else:
                location = ent
            break
    edited_time, _, _ = time_extract.main(tokens, tokens_verb_noun,'weather')
    print(edited_time)
    now_time = datetime.now()
    if edited_time.month > now_time.month:
        return location , 10 , 10
    edited_time = edited_time - relativedelta(days=now_time.day,hours = now_time.hour)
    day = edited_time.day
    hour = edited_time.hour
    if edited_time.day > now_time.day:
        day = 0
    print(location , day , hour)
    return location , day , hour

def get_weather(city_name, day , hour):
    api_key = "acc2137340c0aeb19d563cf85cf78595"
    api_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric&lang=ar".format(city_name, api_key)

    response = requests.get(api_url)
    response_dict = response.json()
	
    index = math.ceil((day*24 + hour) / 3)
    if index > 39:
        index = 39
    print(index)
    weather = response_dict["list"][index]['weather'][0]["description"]
    temperature = round(response_dict["list"][index]["main"]["temp"])

    if response.status_code == 200:
        return str(temperature) + chr(176) +"C" + " الجو " + str(weather) + " درجة الحرارة "
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None
    
def main(tokens, tokens_verb_noun,ents):
    for ent in ents.keys():
        if ent in tokens:
            tokens.remove(ent)
    location , day , hour = extract_time_location(tokens, tokens_verb_noun,ents)
    return get_weather(location , day , hour)
