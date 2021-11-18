from .aurras.core.model import Model
from .aurras.core.data_processing import generate_dataset

# interactions
from .aurras.integrations.plugins import PluginManager

from .config import Config

class Aurras:

    """ PUBLIC """
    def __init__(self):
        """ Initialize all integration classes & prepare Aurras for general use """
        print('Initializing Aurras...')

        self.plugins = PluginManager(Config.PLUGINS_PATH)

    def load(self):
        """ Load in a pre-trained NLP model """
        print('Loading Aurras...')

        intent_label_path = f'{Config.DATASET_PATH}/intent_labels.json'
        entity_label_path = f'{Config.DATASET_PATH}/entity_labels.json'

        self.nlp = Model(intent_label_path, entity_label_path, Config.PROMPT_PADDING)
        self.nlp.build_model(Config.MODEL_NAME)
        self.nlp.load_model(Config.PRETRAINED_PATH, Config.MODEL_NAME)

    def build(self):
        """ Build & train Aurras' NLP model """
        print('Building Aurras...')

        intent_label_path = f'{Config.DATASET_PATH}/intent_labels.json'
        entity_label_path = f'{Config.DATASET_PATH}/entity_labels.json'
        dataset_path = f'{Config.DATASET_PATH}/train.pkl'

        self.nlp = Model(intent_label_path, entity_label_path, Config.PROMPT_PADDING)
        self.nlp.build_model(Config.MODEL_NAME)
        self.nlp.train(dataset_path, epochs=Config.EPOCHS)
        self.nlp.save_model('model/pretrained')

    def build_dataset(self):
        """ Build a dataset based on the provided intents & entities """
        print('Generating a dataset...')

        generate_dataset(Config.DATASET_PATH)

    #* Interactions
    def ask(self, prompt):
        """
            Pass a single prompt to Aurras

            Outputs:
             - response (json): Response object
        """
        
        classification = self.nlp.classify(prompt)
        response = self.plugins.generate_response(classification['intent'], classification['entities'])

        return response

    def interact(self):
        """ Start a conversation with Aurras - text based """
        print('Live interactive console loaded')

        while True:
            # get the user's prompt
            print('=> ', end='')
            prompt = input()

            if (prompt.lower() == 'exit'): # exit case
                break

            classification = self.nlp.classify(prompt)
            response = self.plugins.generate_response(classification['intent'], classification['entities'])
            print(response['response'])

    def parse_speech(self, speech):
        return

    def generate_speech(self, text):
        """ 
            Generate an audio clip of the provided text

            Inputs: 
             - text (string)

            Outputs:
             - speech (path): Path to audio file
        """
        return