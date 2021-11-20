""" GENERAL SETTINGS """
NAME = 'DATETIME'        # name of the plugin.  Used mostly in debugging
PRIORITY = 0         # priority of the plugin - how it compets with other plugins sharing the same intents
ACCEPTED_INTENTS = [ # list of all intents this plugin reacts to
    'get_date',
    'get_time'
]

""" PLUGIN SETTINGS """
DATE_FORMAT = '%B %d'
TIME_FORMAT = '%H:%M'