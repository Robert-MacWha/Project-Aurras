import os
import json
import random
import itertools
import glob
import pandas as pd
from pathlib import Path

def generate_dataset(dataset_path, samples_per_intent=512, duplicates=False):
    """
        Generate the dataset from .entity and .intent files in the dataset directory.

        Inputs:
         - dataset_path: path to the train.pkl output
         - samples_per_intent: number of samples to generate per intent
         - duplicates: allow duplicate prompts to fill the [samples_per_intent] quota
        
        Outputs:
         - entity_labels.json: JSON mapping to convert entity IDs into the plain-text entities
         - intent_labels.json: JSON mapping to convert intent IDs into the plain-text intents
         - samples.csv: Sample of the dataset, used for debugging
         - train.pkl: Full training dataset
    """

    if not os.path.isdir(dataset_path):
        print('Dataset directory does not exist')
        return

    # load data from file
    entity_files = glob.glob(f'{dataset_path}/*/entities/*.entity', recursive=True)
    intent_files = glob.glob(f'{dataset_path}/*/intents/*.intent', recursive=True)

    entities = {}
    entity_id = 1
    for file in entity_files:
        name = Path(file).stem
        samples = [(e.lower(), entity_id) for e in open(file).read().splitlines() if not e.startswith('#')]
        entities[name] = samples

        entity_id += 1

    intents = {}
    for file in intent_files:
        name = Path(file).stem
        samples = [i.lower() for i in open(file).read().splitlines() if not i.startswith('#')]
        intents[name] = samples

    # generate mapping for intents and entities
    intent_labels = {}
    entity_labels = {}

    x = 0
    for category in intents:
        intent_labels[x] = category
        x += 1

    x = 1 # entities start at 0 to make room for null entity
    for category in entities:
        entity_labels[x] = category
        x += 1

    # slot filling
    filled_prompts = {}
    for category in intents:
        filled_prompts[category] = []

        for sample in intents[category]:
            filled_prompts[category].append(
                [entities[word[1:-1]] if word.startswith('{') and word.endswith('}') else [(word, 0)] for word in sample.split()]
            )

    # permutation generation
    premutated_prompts = {}
    for category in filled_prompts:
        permutations = []

        for sample in filled_prompts[category]:
            permutations.extend(list(itertools.product(*sample)))

        premutated_prompts[category] = permutations

    # distribute entity labels to individual words
    generated_prompts = {}
    for category in premutated_prompts:             # intent categories
        category_prompts = []

        for sample in premutated_prompts[category]: # intent samples
            new_sample = []

            for word in sample:                     # individual words / entities
                if word[0] == '':                   # remove empty intents (mostly from prepend_request's null case)
                    continue

                new_sample.extend([(w, word[1]) for w in word[0].split()])

            category_prompts.append(new_sample)
        
        generated_prompts[category] = category_prompts

    # generate the dataset
    dataset = []

    for category in generated_prompts:

        # sample the category for prompts
        if not duplicates and len(generated_prompts[category]) < samples_per_intent:
            samples = generated_prompts[category]
            print(f'not enough "{category}" intents were generated from templates.  Limiting number of samples to {len(generated_prompts[category])}')
        else:
            samples = random.choices(generated_prompts[category], k=samples_per_intent)

        # convert the data into a json so pandas can read it
        for sample in range(len(samples)):

            dataset.append({
                'prompts':  ' '.join([w[0] for w in samples[sample]]),
                'prompt_intent': list(intent_labels.values()).index(category),
                'word_entities': [w[1] for w in samples[sample]]
            })

    # save the dataset
    df = pd.DataFrame(dataset)
    df.to_pickle(f'{dataset_path}/train.pkl')
    df.to_csv(f'{dataset_path}/train.csv')
    pd.DataFrame(dataset[::200]).to_csv(f'{dataset_path}/sample.csv', index=False)

    with open(f'{dataset_path}/intent_labels.json', 'w') as f:
        json.dump(intent_labels, f)
    
    with open(f'{dataset_path}/entity_labels.json', 'w') as f:
        json.dump(entity_labels, f)