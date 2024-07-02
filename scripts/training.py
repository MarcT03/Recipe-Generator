from sklearn.model_selection import train_test_split
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset


def train_model(recipes_df):
    X = recipes_df['ingredients'] + recipes_df['instructions']
    y = recipes_df['instructions']

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def tokenization(data):
        return tokenizer(data, return_tensors="pt", padding=True, truncation=True)
    
    train_encodings = tokenization(X_train.tolist())
    val_encodings = tokenization(X_val.tolist())