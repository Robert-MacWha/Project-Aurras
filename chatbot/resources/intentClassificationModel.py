import tensorflow as tf
from transformers import TFDistilBertModel

from resources.encodeTexts import encode_without_labels

# TODO: Allow text to be passed into the model and use a custom layer to apply tokenization
# TODO: Allow inputs of variable length (IE not everything needs to be of length 128) to reduce memory costs
def build_intent_classification_model(intent_class_count, entity_class_count, max_len=128, model_name='distilbert-base-uncased', random_seed=42, plot=True):

    """
        Builds the intent and sequence classification model with keras' model API.

        Inputs:
         - intent_class_count: The dimensionality of the intent classification
         - entity_class_count: The dimensionality of the entity classification
         - max_len: Integer controling the maximum number of encoded tokens in a given sequence  
         - model_name: The name of the specific strand of distilbert to use
         - random_seed: The selected random seed for reproducible results

        Outputs:
         - model: a compiled tf.keras.Model with classification layers on top of the pre-trained transformer architecture
    """

    # define a weight initializer to ensure reproducibility
    weight_initializer = tf.keras.initializers.GlorotNormal(seed=random_seed)

    # define the transformer
    transformer = TFDistilBertModel.from_pretrained(model_name)

    # define input layers
    input_ids_layer = tf.keras.layers.Input(
        shape=(max_len,),
        name='input_ids',
        dtype='int32',
    )

    input_attention_layer = tf.keras.layers.Input(
        shape=(max_len,),
        name='input_attention',
        dtype='int32',
    )

    # define the transformer layer
    last_hidden_state = transformer([input_ids_layer, input_attention_layer])[0] # (batch_size, sequence_length, hidden_size=768)

    # the slot-filling layer needs to cover the entire range of the hidden state
    entity_output = tf.keras.layers.Dense(
        256,
        activation='relu',
        kernel_initializer=weight_initializer,
        kernel_constraint=None,
        bias_initializer='zeros'
    )(last_hidden_state)

    entity_output = tf.keras.layers.Dense(
        entity_class_count,
        activation='softmax',
        kernel_initializer=weight_initializer,
        kernel_constraint=None,
        bias_initializer='zeros',
        name='entity_output'
    )(entity_output)

    # the cls token contains a condensed representation of the entire last_hidden_state tensor
    cls_token = last_hidden_state[:, 0, :]

    intent_output = tf.keras.layers.Dense(
        intent_class_count,
        activation='softmax',
        kernel_initializer=weight_initializer,
        kernel_constraint=None,
        bias_initializer='zeros',
        name='intent_output'
    )(cls_token)

    # define the model
    model = tf.keras.Model([input_ids_layer, input_attention_layer], [intent_output, entity_output])

    if plot:
        tf.keras.utils.plot_model(model, to_file='intent_classifier.png', show_shapes=True, show_layer_names=True)

    return model

def classify(text, tokenizer, model, intent_labels, entity_labels):
    """
        Classify a single text prompt

        Inputs:
         - text: String text prompt to classify
         - tokenizer: The pre-made tokenizer
         - intent_lables: A dictionary of lables and text-representations

        Outputs:
         - label: the label for the text
    """

    input = encode_without_labels(tokenizer, text)
    model_output = model(input)

    intent_classification = model_output[0]
    intent_id = intent_classification.numpy().argmax(axis=1)[0]
    
    entity_classifications = model_output[1]
    entity_ids = entity_classifications.numpy().argmax(axis=2)

    info = decode_prediction(tokenizer, input[0][0], intent_labels, entity_labels, intent_id, entity_ids[0])
    
    return info 

def decode_prediction(tokenizer, input_ids, intent_labels, entity_labels, intent_id, entity_ids):

    info = {'intent': intent_labels[str(intent_id)], 'entities': []}

    current_entity = []
    current_entity_label = -1

    # loop over each token and add it to the info dict if it's been labled
    for i in range(len(input_ids)):

        token_id = input_ids[i]
        token_label = entity_ids[i]

        if token_label == current_entity_label: # more of the current entity
            current_entity.append(token_id)
        else: 
            
            # the entity is done - add it to the info dict
            if current_entity_label != -1:
                info['entities'].append((entity_labels[str(current_entity_label)], tokenizer.decode(current_entity)))
                current_entity_label = -1
            
            if token_label != 0: # a new entity
                current_entity_label = token_label
                current_entity = [token_id]

    return info