#? following https://github.com/m2dsupsdlclass/lectures-labs/blob/master/labs/06_deep_nlp/Transformers_Joint_Intent_Classification_Slot_Filling_rendered.ipynb

import os
import itertools
import sys

class Intent:
    def __init__(self, file, name, entities):
        content = open(file).read().splitlines()

        self.name = name
        self.samples = []

        # loop over each template intent
        for c in content:

            if (c.startswith('#')): # hashtags are used to denote comments
                continue
            
            # populate the template intent with each possible variation
            subsections = c.split()
            for i, s in enumerate(subsections):

                if s.startswith('{'):
                    
                    try:
                        entity_name = s[1:-1]
                        entity_samples = entities[entity_name].labled_samples

                        subsections[i] = entity_samples
                    
                    except:
                        print(f'FATAL ERROR: Entity {s[1:-1]} in intent {file} does not exist')
                        print(f' - Script failed on intent "{c}"')
                        sys.exit()

                else:
                    subsections[i] = [[(s, 0)]]

            samples = itertools.product(*subsections)
            for s in samples:
                sample = []
                for p in s:
                    sample += p

                self.samples.append(sample)

    def parse_line(self, line):
        intent_label = self.name
        words = [i[0] for i in line]
        word_labels = [i[1] for i in line]
        
        return {
            'intent_label': intent_label,
            'words':  ' '.join(words).lower(),
            'word_labels': word_labels
        }

def load_Intents(path, entities):

    intents       = {}
    intent_lables = {}
    
    i = 0
    for filename in os.listdir(path):
        if filename.endswith('.intent'):

            intent_name = filename.removesuffix('.intent')
            intents[intent_name] = Intent(os.path.join(path, filename), i, entities)
            intent_lables[i] = intent_name

            i += 1
    
    return intents, intent_lables