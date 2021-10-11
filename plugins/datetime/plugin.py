import datetime

from .config import *

def execute(intent, entities):

    now = datetime.datetime.now()

    if intent == 'get_date':
        date = now.strftime(DATE_FORMAT)
    else:
        date = now.strftime(TIME_FORMAT)

    # remove leading zeros
    date = date.replace(' 0', ' ')

    return { 'response': f'It\'s {date}' }