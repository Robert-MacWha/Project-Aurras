import logging
from src.nlp.data_processing import generate_dataset
from src.nlp.model import Model

logging.basicConfig(filename="src/nlp/train.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

generate_dataset()

nlp_model = Model('dataset/intent_labels.json', 'dataset/entity_labels.json', build=True, debug=True)
nlp_model.train('dataset/train.pkl', epochs=2)
nlp_model.save_model('src/nlp/model/pretrained')