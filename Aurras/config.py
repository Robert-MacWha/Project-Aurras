class Config:
    # data
    DATASET_PATH = 'dataset'
    PLUGINS_PATH = 'Aurras/plugins'
    PROMPT_PADDING = 128
    SAMPLES_PER_INTENT = 512
    ALLOW_DUPLICATE_SAMPLES = False

    # model
    PRETRAINED_PATH = 'Aurras/core/model/pretrained'
    MODEL_NAME = 'distilbert-base-uncased'

    # training
    EPOCHS = 1