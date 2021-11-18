"""
    Requirements:
    Natural time -> Python DateTime: https://github.com/alvinwan/timefhuman [pip install timefhuman]
    Fetching forecast -> https://openweathermap.org/bulk [key required]

"""
import logging
import requests
import datetime
from timefhuman import timefhuman

from .config import *
from.key import KEY

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
        return { 'response': "Forecasts can't be predicted this far into the future" } #! break point - can't predict more than 7 days ahead

    # get the forecast from OpenWeatherMap
    request = f'https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude={EXCLUDE}&units={UNITS}&appid={KEY}'
    res = requests.get(request)


    x = res.json()
    temperature = round(x['daily'][time_delta]['temp']['day'])
    weather = x['daily'][time_delta]['weather'][0]['description']

    if time_delta == 0: # special case for today
        response = { 'response':f'Today is is {temperature} degrees with {weather}' }
    else:
        response = { 'response':f'On {time.strftime(DATE_FORMAT)} it\'ll be {temperature} degrees with {weather}' }

    return response