from .core.model import Model
from .core.data_processing import generate_dataset

# interactions
from .integrations.plugins import PluginManager

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
        self.nlp.save_model(Config.PRETRAINED_PATH)

    def build_dataset(self):
        """ Build a dataset based on the provided intents & entities """
        print('Generating a dataset...')

        generate_dataset(Config.DATASET_PATH, Config.SAMPLES_PER_INTENT, Config.ALLOW_DUPLICATE_SAMPLES)

    #* Interactions
    def get_classification(self, prompt: str) -> dict:
        """
            Get the classification of a single prompt

            Outputs:
             - classification: Classification json containing intent and extracted entities
        """

        classification = self.nlp.classify(prompt)

        return classification

    def ask(self, prompt: str) -> dict:
        """
            Pass a single prompt to Aurras

            Outputs:
             - response: Response json object
        """
        
        classification = self.nlp.classify(prompt, Config.PROMPT_PADDING)
        response = self.plugins.generate_response(classification['intent'], classification['entities'])

        return response

    def interact(self):
        """ Start a conversation with Aurras - text based """
        print('\n\n')
        print('Live interactive console loaded')

        while True:
            # get the user's prompt
            print('=> ', end='')
            prompt = input()

            if (prompt.lower() == 'exit'): # exit case
                break

            response = self.ask(prompt)
            print(response['response'])
            print('')

    def parse_speech(self, speech):
        """ 
            Parses an audio clip and extracts the speech

            Inputs: 
             - speech (Not yet decided)

            Outputs:
             - speech (path): Path to audio file
        """
        return

    def generate_speech(self, text: str):
        """ 
            Generate an audio clip of the provided text

            Inputs: 
             - text (string)

            Outputs:
             - speech (path): Path to audio file
        """
        return