
#! TODO: fix the entity_labels file so it starts at 0 instead of 1 (because of the prepend_requests.um_entity file)
import os

class Entity:
    def __init__(self, file, name, id):
        content = open(file).read().splitlines()

        self.name = name
        self.samples = [c for c in content if not c.startswith('#')]

        self.labled_samples = []
        for s in self.samples:

            if (s.startswith('#')): # hashtags are used to denote comments
                continue

            self.labled_samples.append([(w, id) for w in s.split()])

def load_Entities(path):

    entity_lables = {}
    entities      = {}

    i = 1
    for filename in os.listdir(path):
        if filename.endswith('.entity'):

            entity_name = filename.removesuffix('.entity')
            entities[entity_name] = Entity(os.path.join(path, filename), entity_name, i)
            entity_lables[i] = entity_name

            i += 1

        elif filename.endswith('.um_entity'):

            entity_name = filename.removesuffix('.um_entity')
            entities[entity_name] = Entity(os.path.join(path, filename), entity_name, 0)

    return entities, entity_lables