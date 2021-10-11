from logging import Logger
import json
import requests

#! DON'T DO THIS!  Just wait for the library to come out

class NotionDatabase:

    base_url = 'https://api.notion.com/v1/databases/'
    headers = {
        'Authorization': 'Bearer ' + '<token>',
        'Notion-Version': '2021-08-16',
        'Content-Type': 'application/json'
    }

    daily_template = [
        {
            'type': 'heading_2',
            'heading_2': {
                'text': [{
                        'type': 'text', 
                        'text': {'content': 'Daily Tasks'},
                        'annotations': {'color': 'yellow_background'}
                    }],
            },
        },
        {
            'type': 'to_do',
            'to_do': {
                'text': [{'type': 'text', 'text': {'content': 'Test todo'}}],
                'checked': False
            }
        },
        {
            'type': 'paragraph',
            'paragraph': { 'text': [{'type': 'text', 'text': {'content': ''}}] }
        },
        {
            'type': 'heading_2',
            'heading_2': {
                'text': [{
                        'type': 'text', 
                        'text': {'content': 'Daily Journal'},
                        'annotations': {'color': 'yellow_background'}
                    }],
            },
        },
        {
            'type': 'paragraph',
            'paragraph': {
                'text': [
                    {'type': 'text', 'text': {'content': 'What am I grateful for?\n\n'}, 'annotations': {'bold': True}},
                    {'type': 'text', 'text': {'content': 'What did I achieve today?\n\n'}, 'annotations': {'bold': True}},
                    {'type': 'text', 'text': {'content': 'How am I feeling today?\n'}, 'annotations': {'bold': True}},
                ]
            }
        }
    ]

    def __init__(self, token, database_id):

        '''
            Form a connection with a notion database for daily updates.  In its current form this only works for my template style
            Inputs:
             - token: Integration's secret token
             - database_id: The database's id: found in the database's url (https://developers.notion.com/docs/getting-started)
        '''

        self.token = token
        self.database_id = database_id
        self.headers['Authorization'] = 'Bearer ' + token

        self.url = f'{self.base_url}{self.database_id}/query'

        # test the database url
        res = requests.request('POST', self.url, headers=self.headers)

        if res.status_code != 200:
            Logger.error(f'Notion Database Error: Responce code {res.status_code} returned.  Check your token and database_id')
            return

        # load the database
        raw_database = json.loads(res.text)

        with open ('test.json', 'w') as file:
            json.dump(raw_database, file, sort_keys=True, indent=4)

        self.clean_database(raw_database)

    def get_day(self, date):
        '''
            Return a notion block for a single day
            Input:
             - date: wanted day, in format %Y-%m-%d
        '''

        database_res = requests.request('POST', self.url, headers=self.headers)
        database_res = self.clean_database(json.loads(database_res.text))

        for i in database_res:
            if i['date'] == date:
                return i
        
        # create a new day and return it
        url = f'https://api.notion.com/v1/pages'

        new_page_data = {
            'parent': {'database_id': self.database_id },
            'properties': {
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': '_____Test date_____'
                            }
                        }
                    ]
                },
                'Actual Date': {
                    'date': {
                        'start': date
                    },
                },
            },
            'children': self.daily_template
        }

        data = json.dumps(new_page_data)
        res = requests.request('POST', url, headers=self.headers, data=data)
        
        print(res.status_code)
        print(res.text)

    # private
    def clean_database(self, raw_database):
        '''
            Clean up a raw database response and remove most of the non-necessary data
            Inputs:
             - raw_database: database loaded from a post request
        '''

        database = []
        for result in raw_database['results']:
            try:
                database.append({
                    'name': result['properties']['Name']['title'][0]['text']['content'],
                    'id': result['id'],
                    'date': result['properties']['Actual Date']['date']['start']
                })

            except:
                print('failed to load row')

        return database