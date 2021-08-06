
#! disable tensorflow logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#! disable transformers logging
import transformers
transformers.logging.set_verbosity_error()

#* imports
from intentClassificationModel import build_intent_classification_model, classify

import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy

from transformers import DistilBertTokenizer
import pandas as pd
import numpy as np
import json
import sys

#* hyperparameters
model_name = 'distilbert-base-uncased'

#* load in training data
df_train = pd.read_csv(open('./data/train.csv'))
df_val   = pd.read_csv(open('./data/val.csv'))

intent_labels = json.load(open('./data/intent_labels.json'))
entity_labels = json.load(open('./data/entity_labels.json'))
intent_count  = len(intent_labels)
entity_count  = len(entity_labels)

#* build the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained(model_name)

#* format training data
# inputs
prompts_train = df_train['words'].values
tokenized_train = tokenizer(prompts_train, padding='max_length', max_length=128, truncation=True, return_tensors='np')

prompts_val = df_val['words'].values
tokenized_val   = tokenizer(prompts_val  , padding='max_length', max_length=128, truncation=True, return_tensors='np')

# outputs
intent_train = np.array(df_train['intent_label'].values)
intent_val   = np.array(df_val  ['intent_label'].values)

#* build the model
model = build_intent_classification_model(intent_count, entity_count)

model.compile(optimizer=Adam(learning_rate=5e-5),
                loss=SparseCategoricalCrossentropy(from_logits=True),
                metrics=[SparseCategoricalAccuracy('categorical_accuracy')])

#* train the model
#! Model does not work with batch_size of higher than 16
history = model.fit(x=[tokenized_train['input_ids'], tokenized_train['attention_mask']], y=intent_train, epochs=1, batch_size=16)
# model.save('./models/model',save_format='tf')

#* test the model
validation_set = list(df_val['words'])

for v in validation_set:
    print(f"'{v}': {classify(v, tokenizer, model, intent_labels)}")