""" GENERAL SETTINGS """
NAME = 'NOTION'    # name of the plugin.  Used mostly in debugging
PRIORITY = 0         # priority of the plugin - how it compets with other plugins sharing the same intents
ACCEPTED_INTENTS = [ # list of all intents this plugin reacts to
    'get_todos',
    'create_todo'
]

""" PLUGIN SETTINGS """
DAILY_UPDATE_ID = '8ad6e805247c4861bce7883dd1cc6330'

from .token import TOKEN