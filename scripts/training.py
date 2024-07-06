from sklearn.model_selection import train_test_split
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, EarlyStoppingCallback
import torch
from torch.utils.data import Dataset

class RecipeDataset(Dataset):
     
    def __init__(self, encodings):
        self.encodings = encodings
        
  
    def __len__(self):
        return len(self.encodings['input_ids'])
    
    def __getitem__(self, idx):
        item = {key: val[idx].clone().detach() for key, val in self.encodings.items()}
        item['labels'] = item['input_ids'].clone().detach()
        return item
   

    
def tokenization(data, tokenizer):
    return tokenizer(data, return_tensors="pt", padding=True, truncation=True, max_length=512)


def train_model(recipes_df):
    recipes_df['ingredients'] = recipes_df['ingredients'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    
    # Combine ingredients and instructions for tokenization
    recipes_df['combined'] = recipes_df.apply(lambda row: row['ingredients'] + ' ' + row['instructions'], axis=1)
    
    X = recipes_df['combined']
    y = recipes_df['instructions']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    tokenizer.pad_token = tokenizer.eos_token

    train_encodings = tokenization(X_train.tolist(), tokenizer)
    val_encodings = tokenization(X_val.tolist(), tokenizer)

    train_labels = tokenizer(y_train.tolist(), return_tensors="pt", padding=True, truncation=True)['input_ids']
    val_labels = tokenizer(y_val.tolist(), return_tensors="pt", padding=True, truncation=True)['input_ids']

    print(f"train_encodings shape: {train_encodings['input_ids'].shape}")
    print(f"train_labels shape: {train_labels.shape}")


    train_dataset = RecipeDataset(train_encodings)
    val_dataset = RecipeDataset(val_encodings)

    model = GPT2LMHeadModel.from_pretrained("gpt2")

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=50,
        per_device_eval_batch_size=8,
        per_device_train_batch_size=8,
        warmup_steps=500,
        weight_decay=.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=3,
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    trainer.train()

    print("Training Complete")