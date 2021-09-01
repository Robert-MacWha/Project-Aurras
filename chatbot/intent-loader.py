from entity import load_Entities
from intent import load_Intents

import random
import pandas as pd
import json

#* load in all entities and intents
entities, entity_lables = load_Entities('./data/entities')
intents, intent_lables  = load_Intents('./data/intents', entities)

#* extract the specified number of training and testing samples
train_count = 256
val_ratio   = 0.05

intent_train = []
intent_val   = []

for i in intents:
    train_samples = random.choices(intents[i].samples, k=train_count)
    intent_train += [intents[i].parse_line(s) for s in train_samples]

    val_samples   = random.choices(intents[i].samples, k=int(train_count * val_ratio))
    intent_val   += [intents[i].parse_line(s) for s in val_samples]

# convert data into pd.dataframe format
df_train = pd.DataFrame(intent_train)
df_val   = pd.DataFrame(intent_val)

#* save all the extracted data
df_train.to_csv('./data/train.csv')
df_val.to_csv('./data/val.csv')

with open ('./data/intent_labels.json', 'w') as f:
    json.dump(intent_lables, f)

with open ('./data/entity_labels.json', 'w') as f:
    json.dump(entity_lables, f)