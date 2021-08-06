
#! disable tensorflow logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#! disable transformers logging
import transformers
transformers.logging.set_verbosity_error()

from transformers import DistilBertTokenizerFast
from ast import literal_eval
import tensorflow as tf
import pandas as pd
import json
import sys

from encodeTexts import encode, encode_without_labels
from intentClassificationModel import build_intent_classification_model, classify

#* hyperparameters
MODEL_NAME = 'distilbert-base-uncased'
MAX_LENGTH = 128
EPOCHS = 1
BATCH_SIZE = 16

#* create the tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

#* load in the dataset
df_train = pd.read_csv(open('./data/train.csv'), converters={'word_labels': literal_eval})
df_val   = pd.read_csv(open('./data/val.csv'),   converters={'word_labels': literal_eval})

intent_labels = json.load(open('./data/intent_labels.json'))
entity_labels = json.load(open('./data/entity_labels.json'))
intent_count = len(intent_labels)
entity_count = len(entity_labels)

# tokenize the dataset
x_train_ids, x_train_attention, y_train_entities = encode(
    tokenizer, 
    list(df_train['words']), 
    list(df_train['word_labels']),
    max_len=MAX_LENGTH
)

x_val_ids, x_val_attention, y_val_entities = encode(
    tokenizer, 
    list(df_val['words']), 
    list(df_val['word_labels']),   
    max_len=MAX_LENGTH
)

# convert the lables to one-hot arrays
y_train_intents = tf.one_hot(df_train['intent_label'].values, intent_count)
y_val_intents   = tf.one_hot(df_val  ['intent_label'].values, intent_count)

y_train_entities = tf.one_hot(y_train_entities, entity_count)
y_val_entities   = tf.one_hot(y_val_entities, entity_count)

#* build the model
model = build_intent_classification_model(intent_count, entity_count)

model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5),
              loss      = tf.keras.losses.CategoricalCrossentropy(),
              metrics   = [tf.keras.metrics.CategoricalAccuracy('categorical_accuracy')])

#* train the model
history = model.fit(
    x = [x_train_ids, x_train_attention],
    y = [y_train_intents, y_train_entities],
    epochs = EPOCHS,
    batch_size = BATCH_SIZE,
    verbose = 1
)

# save the model
model.save_weights('./models/model_weights') # load the pre-trained model by creating a compiled version of the model then calling model.load_weights('path/savefile')

#* test the model
while True:
    prompt = input(f'Enter a prompt in one of the following classes: {list(intent_labels.values())}: ')

    classification = classify(prompt, tokenizer, model, intent_labels, entity_labels)
    print(f'classification is: {classification}')