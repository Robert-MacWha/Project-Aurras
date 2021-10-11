import logging
import os
import glob
from os.path import isfile
from importlib import import_module

logging.getLogger(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class PluginManager:

    PLUGIN_PATH = 'plugins'
    plugins = []

    def __init__(self):
        """ Load all modules into an array so they can be used """
        if not os.path.isdir(self.PLUGIN_PATH):
            logging.error('Dataset directory does not exist')
            return

        plugin_paths = glob.glob('plugins/*/plugin.py')
        plugin_paths = [f for f in plugin_paths if isfile(f)]

        for path in plugin_paths:
            basename, extension = os.path.splitext(path)
            import_location = basename.replace("\\", ".")

            #? code partially from https://stackoverflow.com/questions/13598035/importing-a-module-when-the-module-name-is-in-a-variable
            try:
                plugin = import_module(import_location)
            except:
                logger.error(f'Could not load plugin {basename}')
                return

            self.plugins.append(plugin)
            logger.info(f'Loaded plugin {plugin.NAME}')

    def generate_response(self, intent, entities):
        """
            Execute all plugins

            Inputs:
            - intent: stringified intent provided by the NLP module
            - entities: dictionary of stringified entities provided by the NLP module

            Outputs:
            - response: Dictionary containing the plugin's responce in natural language
        """

        # select all plugins which react to this intent
        active_plugins = [p for p in self.plugins if intent in p.ACCEPTED_INTENTS]

        if len(active_plugins) == 0:
            logger.warning(f'No plugin found for intent {intent}')
            return

        # select the plugin with the highest priority.  If multiple plugins share the same priority, the first one is selected
        active_plugin = active_plugins[0]
        for p in active_plugins:
            if p != active_plugin:
                if p.PRIORITY > active_plugin.PRIORITY:
                    active_plugin = p
                elif p.PRIORITY == active_plugin.PRIORITY:
                    logger.info(f'Multiple plugins have tried to claim this intent.  Plugin {p.NAME} was ignored')

        # execute the selected plugin and return its response
        response = {'response': f'an error occurred while trying to execute the {p.NAME} plugin'}
        try:
            response = active_plugin.execute(intent, entities)
        except:
            logger.warn(f'Could not execute plugin {active_plugin.__name__}')

        return response