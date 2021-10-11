"""
    Requirements:
    Backend -> Notion https://github.com/jamalex/notion-py
"""

from notion.client import NotionClient

from .config import *

def execute(intent, entities):

    print('Test')
    client = NotionClient(token_v2=TOKEN)
    print(client)
    page = client.get_block("https://www.notion.so/Test-page-e7c0eefc4edf432683830cfc13326844")
    print('Test')

    print(f'Page title is {page.title}')