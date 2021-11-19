import logging
import os
import glob
from os.path import isfile
from importlib import import_module

class PluginManager:

    plugins = []

    def __init__(self, plugin_path: str):
        """ 
            Load all modules into an array so they can be used when required

            Inputs:
             - plugin_path: Local path to the plugins directory
        """
        if not os.path.isdir(plugin_path):
            logging.error('Dataset directory does not exist')
            return

        plugin_paths = glob.glob(f'{plugin_path}/*/plugin.py')
        plugin_paths = [f for f in plugin_paths if isfile(f)]

        for path in plugin_paths:
            basename, extension = os.path.splitext(path)
            import_location = basename.replace("\\", ".")
            import_location = import_location.replace("/", ".")

            #? code partially from https://stackoverflow.com/questions/13598035/importing-a-module-when-the-module-name-is-in-a-variable
            try:
                plugin = import_module(import_location)
            except Exception as e:
                print(f'Could not load plugin {import_location}')
                return

            self.plugins.append(plugin)

    def generate_response(self, intent: str, entities: dict) -> dict:
        """
            Execute all plugins

            Inputs:
            - intent:   stringified intent provided by the NLP module
            - entities: dictionary of stringified entities provided by the NLP module

            Outputs:
            - response: Dictionary containing the plugin's responce in natural language
        """

        # select all plugins which react to this intent
        active_plugins = [p for p in self.plugins if intent in p.ACCEPTED_INTENTS]

        if len(active_plugins) == 0:
            return {'response': f'Your intent was {intent} and entities were {entities}'}

        # select the plugin with the highest priority.  If multiple plugins share the same priority, the first one is selected
        active_plugin = active_plugins[0]
        for p in active_plugins:
            if p != active_plugin:
                if p.PRIORITY > active_plugin.PRIORITY:
                    active_plugin = p

        # execute the selected plugin and return its response
        response = {'response': f'an error occurred while trying to execute the {p.NAME} plugin'}
        try:
            response = active_plugin.execute(intent, entities)
        except:
            print(active_plugin.__name__)

        return response