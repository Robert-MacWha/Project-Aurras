from .config import *

#TODO: Allow plugins to ask the users questions
#TODO: Allow plugins to send back non-natural language, and convert it on the fly

# function called when this plugin is executed
def execute(intent, entities):
    """
        The function called when this plugin is executed

        Inputs:
         - intent: Stringified intent
         - entities: Dictionary containing stringified entities and their content

        Outputs:
         - command: Dictionary containing the plugin's responce in natural language
    """

    return { 'response':'This plugin was excecuted!' }