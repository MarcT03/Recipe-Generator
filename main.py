import os
from scripts.processing import load_data, preprocess
from scripts.training import train_model
from scripts.evaluate import evaluate

if __name__ == "__main__":
    recipes_df = load_data()
    recipes_df = preprocess(recipes_df)
    
    train_model(recipes_df)

    evaluate()
    

