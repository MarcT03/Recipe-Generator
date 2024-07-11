import pandas as pd
from scripts.processing import preprocess

def combine_data():

    cleaned_df = pd.read_csv('data/cleaned_recipes.csv')
    new_df = pd.read_csv('data/foodrecipes.csv')

    combined_df = pd.concat([cleaned_df, new_df], ignore_index=True)

    combined_df = preprocess(combined_df)

    return combined_df

def save_combined(combined_df):
    combined_df.to_csv('data/combined_recipes.cvs', index = False)

def generate_recipes_txt(combines_df):
    with open('data/recipes.txt', 'w', encoding='utf-8') as f:
        for _, row in combined_df.iterrows():