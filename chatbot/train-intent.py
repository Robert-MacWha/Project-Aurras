from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, TrainingArguments, Trainer

#? load the model and tokenizer
name = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(name, num_labels=150)

# define the tokenizer function
def tokenize_function(example):
    return tokenizer(example["prompt"], truncation=True)

#? load the dataset
data_raw = load_dataset('json', field='data', data_files={
    'train': './data/train.json',
    'test': './data/test.json',
    'validate': './data/val.json'
})

#? tokenize the dataset
data_tokenized = data_raw.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

#? setup the trainer
args = TrainingArguments(
    f"One-hot Intent Classification - {name}",
    report_to='wandb',
    num_train_epochs=5,
    save_strategy='no'
)

trainer = Trainer(
    model,
    args,
    train_dataset=data_tokenized['train'],
    eval_dataset=data_tokenized['validate'],
    data_collator=data_collator,
    tokenizer=tokenizer
)

trainer.train()

model.save_pretrained(f'./models/One-hot Intent Classification - {name}')