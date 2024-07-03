import pandas as pd
import os
from scripts.datascraper import recipe_scraper

def preprocess(df):
    df.dropna(subset=['ingredients', 'instructions'], inplace=True)
    df['ingredients'] = df['ingredients'].apply(lambda x: x.lower().split(',') if isinstance(x, str) else x)
    df['instructions'] = df['instructions'].apply(lambda x: x.lower() if isinstance(x, str) else x)
    return df

def load_data():
    if os.path.exists('data/cleaned_recipes.csv'):
        return pd.read_csv('data/cleaned_recipes.csv')
    else:
        return recipe_scraper()