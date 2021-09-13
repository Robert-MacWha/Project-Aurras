
#! disable tensorflow logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#! disable transformers logging
import transformers
transformers.logging.set_verbosity_error()

from transformers import DistilBertTokenizerFast
import json

from resources.intentClassificationModel import build_intent_classification_model, classify

#* hyperparameters
MODEL_NAME = 'distilbert-base-uncased'
MODEL_WEIGHTS_PATH = './resources/models/model_weights'

def main():

    #* load in intent and entity labels
    intent_labels = json.load(open('./resources/data/intent_labels.json'))
    entity_labels = json.load(open('./resources/data/entity_labels.json'))
    intent_count = len(intent_labels)
    entity_count = len(entity_labels)

    #* load in the model
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    model = build_intent_classification_model(intent_count, entity_count, plot=False)

    try:
        model.load_weights(MODEL_WEIGHTS_PATH)

    except:
        raise Exception('Model not found.  Run intent-classifier.py before running this script.  If that does not work confirm that the MODEL_WEIGHTS_PATH is correct.')

    #* interact with the model

    print('')
    print('Loaded intents: ')

    for i in intent_labels.values():
        print(f' - {i}')

    print('')
    print('======================')
    print(' Interact with Aurras ')
    print('======================')

    while True:
        prompt = input(f'=> ')

        classification = classify(prompt, tokenizer, model, intent_labels, entity_labels)
        print(f'classification is: {classification}')

main()