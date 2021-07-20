import json
import sys

#? load the prompts & domains
with open('./data/data_formated.json') as f:
    prompts = json.load(f)

with open('./data/domains.json') as f:
    domains = json.load(f)['domains']

#? generate the dataset
"""
    each datapoint contains a prompt, a domain, and a binary classification of whether the domain is correct
"""

dataset = {}

# loop over the train, test, and val data
for g in prompts:

    # create the dataset array
    dataset[g] = {'data': []}

    for p in prompts[g]:

                # add the prompt and its one-hot label
        dataset[g]['data'].append({
            'prompt': str(p['prompt']),
            'label': domains.index(p['intent'])
        })

#? save the dataset as three files - train, test, and val
json.dump(dataset['train'], open('./data/train.json', 'w'))
json.dump(dataset['test'], open('./data/test.json', 'w'))
json.dump(dataset['val'], open('./data/val.json', 'w'))