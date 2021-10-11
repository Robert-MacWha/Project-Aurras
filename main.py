import logging
import json
from src.nlp.model import Model
from src.plugins.pluginmanager import PluginManager

# preperation
logging.basicConfig(filename="src/nlp/interact.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

nlp_model = Model('dataset/intent_labels.json', 'dataset/entity_labels.json', debug=False)
nlp_model.build_model()
nlp_model.load_model('src/nlp/model/pretrained')

plugin_manager = PluginManager()

print()

while True:

    # get the user's prompt
    print('=> ', end='')
    prompt = input()

    classification = nlp_model.classify(prompt)
    response = plugin_manager.generate_response(classification['intent'], classification['entities'])
    print(response['response'])