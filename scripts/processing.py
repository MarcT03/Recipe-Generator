import pandas as pd
import os
from scripts.datascraper import recipe_scraper

def preprocess(df):
    df.dropna(subset=['ingredients, instructions'], inplace=True)
    df['ingredients'] = df['ingredients'].apply(lambda x: x.lower().split())
    df['instructions'] = df['instructions'].apply(lambda x: x.lower())
    return df

def load_data():
    if os.path.exists('cleaned_recipes.csv'):
        return pd.read_csv('cleaned_recipes.csv')
    else:
        return recipe_scraper()