import pandas as pd
import os
from scripts.processing import preprocess
from ast import literal_eval
import re

def generate_new_dataset():

    new_df = pd.read_csv('data/foodrecipes.csv')

    print("Raw New Dataset (First 5 Rows):")
    print(new_df.head())

    new_df = new_df[['Name', 'RecipeIngredientParts', 'RecipeInstructions']]
    new_df.rename(columns={
        'Name': 'title',
        'RecipeIngredientParts': 'ingredients',
        'RecipeInstructions': 'instructions'
    }, inplace=True)


    
    def parse_recipe(expr):
        try: 
            return re.findall(r'"(.*?)"', expr)
        except(ValueError, SyntaxError):
            return ''
        
    new_df['ingredients'] = new_df['ingredients'].apply(parse_recipe)
    new_df['ingredients'] = new_df['ingredients'].apply(lambda x: ', '.join(x) if isinstance(x,list) else '')
    

    new_df['instructions'] = new_df['instructions'].apply(parse_recipe)
    new_df['instructions'] = new_df['instructions'].apply(lambda x: ', '.join(x) if isinstance(x,list) else '')
    

    print("Transformed New Dataset (First 5 rows):")
    print(new_df.head())

    return new_df

def combine_data():

    cleaned_df = pd.read_csv('data/cleaned_recipes.csv')
    new_df = generate_new_dataset()

    combined_df = pd.concat([cleaned_df, new_df], ignore_index=True)

    combined_df = preprocess(combined_df)

    print("Combined Dataset (First 5 rows): ")
    print(combined_df.head())

    return combined_df

def save_combined(combined_df):
    combined_df.to_csv('data/combined_recipes.csv', index = False)

def generate_recipes_txt(combined_df):
    with open('data/recipes.txt', 'w', encoding='utf-8') as f:
        for _, row in combined_df.iterrows():
            f.write(f"Title: {row['title']}\n")
            f.write(f"Ingredients: {row['ingredients']}\n")
            f.write(f"Instructions: {row['instructions']}\n\n")


if __name__ == "__main__":
    # Run the functions to debug
    combined_df = combine_data()
    save_combined(combined_df)
    generate_recipes_txt(combined_df)