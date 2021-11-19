import numpy as np

def encode(tokenizer: object, texts: list, texts_labels: list, max_len: int) -> tuple:
    """
        Encode a sequence of strings using the provided tokenizer.
        Returns an encoded ID and an attention mask

        Inputs: 
         - tokenizer:    tokenizer object from the PreTrainedTokenizer class
         - texts:        sequence of strings to be tokenized
         - texts_labels: word-level lables for the text sequences
         - max_len:      integer controling the maximum number of tokens to tokenize
        
        Outputs:
         - input_ids:      sequence of encoded tokens as a np array
         - attention_mask: sequence of attention masks as a np array
         - labels:         sequence of token-level labels as a np array
    """

    input = [__tokenize_and_preserve_labels(tokenizer, text, text_labels, max_len=max_len) for text, text_labels in zip(texts, texts_labels)]

    input_ids       = np.array([i[0] for i in input])
    attention_masks = np.array([i[1] for i in input])
    labels          = np.array([i[2] for i in input])
    
    return input_ids, attention_masks, labels

def encode_without_labels(tokenizer: object, texts: list, max_len: int) -> tuple:
    """
        Encode a sequence of strings using the provided tokenizer.
        Returns an encoded ID and an attention mask

        Inputs: 
         - tokenizer: tokenizer object from the PreTrainedTokenizer class
         - texts:     sequence of strings to be tokenized
         - max_len:   integer controling the maximum number of tokens to tokenize
        
        Outputs:
         - input_ids:      sequence of encoded tokens as a np array
         - attention_mask: sequence of attention masks as a np array
    """

    input = tokenizer(
        texts,
        max_length=max_len,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors='np'
    )

    return input['input_ids'], input['attention_mask']

def __tokenize_and_preserve_labels(tokenizer: object, text: str, text_labels: list, max_len: int) -> tuple:
    """
        Tokenize a sequence while preserving word-level labels

        Inputs:
         - tokenizer:   tokenizer object from huggingface
         - text:        prompt
         - text_labels: list of labels for each word in the prompt
         - max_len:     maximum length of a prompt after tokenization

        Outputs:
         - token_ids:      list token IDs for the input text
         - attention_mask: attention mask for the input text
         - labels:         list of token-level labels
    """

    tokenized_sequence = []
    labels = []
    attention_mask = []

    for word, label in zip(text.split(), text_labels):

        # tokenize the word
        tokenized_word = tokenizer.tokenize(word)
        n_tokens = len(tokenized_word)

        tokenized_sequence.extend(tokenized_word)

        labels.extend([label] * n_tokens)

    # add in the [CLS] and [SEP] tokens to mark the start and end
    tokenized_sequence.insert(0, '[CLS]')
    labels.insert(0, 0)

    tokenized_sequence.append('[SEP]')
    labels.append(0)

    attention_mask = [1] * len(tokenized_sequence)

    # pad the lists
    while len(tokenized_sequence) < max_len:
        tokenized_sequence.append('[PAD]')
        attention_mask.append(0)
        labels.append(0)

    # convert the tokens into token IDs
    token_ids = [tokenizer.convert_tokens_to_ids(token) for token in tokenized_sequence]

    return token_ids, attention_mask, labels