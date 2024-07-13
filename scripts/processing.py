import pandas as pd
import os
from scripts.datascraper import recipe_scraper

def preprocess(df):
    initial_length = len(df)
    df.dropna(subset=['ingredients', 'instructions'], inplace=True)
    after_dropna = len(df)
    df['ingredients'] = df['ingredients'].apply(lambda x: x.lower().split(',') if isinstance(x, str) else x)
    df['instructions'] = df['instructions'].apply(lambda x: x.lower() if isinstance(x, str) else x)
    print(f"Initial number of samples: {initial_length}")
    print(f"After dropna number of samples: {after_dropna}")
    return df

def load_data():
    if os.path.exists('data/combined_recipes.csv'):
        df = pd.read_csv('data/combined_recipes.csv')
        print(f"Loaded {len(df)} recipes from combined_recipes.csv")
    else:
        raise FileNotFoundError("combined_recipes.csv not found.")
    return df