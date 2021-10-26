from aurras.nlp.model import Model
from aurras.nlp.data_processing import generate_dataset

generate_dataset()

nlp_model = Model('dataset/intent_labels.json', 'dataset/entity_labels.json', build=True, debug=True)
nlp_model.train('dataset/train.pkl', epochs=2)
nlp_model.save_model('model/pretrained')