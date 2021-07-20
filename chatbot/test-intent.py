import json

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

#? load the model and tokenizer
name = 'distilbert-base-uncased'
cache_dir = './models/One-hot Intent Classification - distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(cache_dir, local_files_only=True)

#? load the domains
with open('./data/domains.json') as f:
    domains = json.load(f)['domains']

while True:
    prompt = input()

    model_input = tokenizer(prompt, padding=True, truncation=True, return_tensors="pt")
    output = model(**model_input)
    print(output.logits.shape)

    predictions = torch.nn.functional.softmax(output.logits, dim=-1).detach().numpy()
    intent = predictions.argmax()
    confidence = predictions.max()

    print(f'Intent is {domains[intent]} with a confidence of {confidence}')