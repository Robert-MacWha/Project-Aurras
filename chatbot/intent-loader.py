from resources.entity import load_Entities
from resources.intent import load_Intents

import random
import pandas as pd
import json

train_count = 500
val_ratio   = 0.05
no_duplicates = True

def main():

    #* load in all entities and intents
    entities, entity_lables = load_Entities('./resources/data/entities')
    intents, intent_lables  = load_Intents('./resources/data/intents', entities)

    #* extract the specified number of training and testing samples
    intent_train = []
    intent_val   = []

    for i in intents:

        if (no_duplicates and len(intents[i].samples) < train_count):  # case for there being fewer samples than I'm trying to get.  This avoids there being duplicate samples in the training set which is bad
            train_samples = intents[i].samples
            intent_train += [intents[i].parse_line(s) for s in train_samples]
            print(f'INFO: Not enough {i} templates were provided.  Limiting the number of samples to {len(intents[i].samples)} to avoid duplicates')
        else:
            train_samples = random.choices(intents[i].samples, k=train_count)
            intent_train += [intents[i].parse_line(s) for s in train_samples]

        val_samples   = random.choices(intents[i].samples, k=int(train_count * val_ratio))
        intent_val   += [intents[i].parse_line(s) for s in val_samples]

    # convert data into pd.dataframe format
    df_train = pd.DataFrame(intent_train)
    df_val   = pd.DataFrame(intent_val)

    #* save all the extracted data
    df_train.to_pickle('./resources/data/train.pkl')
    df_val.to_pickle('./resources/data/val.pkl')

    with open ('./resources/data/intent_labels.json', 'w') as f:
        json.dump(intent_lables, f)

    with open ('./resources/data/entity_labels.json', 'w') as f:
        json.dump(entity_lables, f)

main()