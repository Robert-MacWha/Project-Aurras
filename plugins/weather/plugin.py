"""
    Requirements:
    Natural time -> Python DateTime: https://github.com/alvinwan/timefhuman [pip install timefhuman]
    Fetching forecast -> https://openweathermap.org/bulk [key required]

"""
import logging
import requests
import datetime
from dateutil import parser
from timefhuman import timefhuman

from .config import *

def execute(intent, entities):

    # get the time for the forecast
    time = datetime.datetime.now()

    #? use specific datetime
    for e in entities:
        if e[0] == 'datetime':

            predicted_time = timefhuman(e[1], now=time)
            if predicted_time != []:
                time = predicted_time
            else:
                logging.error(f'Provided datetime "{entities["datetime"]}" could not be parsed')

            break

    time_delta = (time - datetime.datetime.now()).days
    if time_delta > 8:
        return { 'response': "Forecasts can't be predicted this far into the future" }

    # get the forecast from OpenWeatherMap
    request = f'https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude={EXCLUDE}&units={UNITS}&appid={KEY}'
    response = requests.get(request)

    x = response.json()
    temperature = x['daily'][time_delta]['temp']['max']
    weather = x['daily'][time_delta]['weather'][0]['description']

    return { 'response':f'On {time.strftime("%b %d")} it\'ll be {temperature} degrees with {weather}' }