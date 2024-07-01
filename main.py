import torch
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.allrecipes.com/'
main_url = f'{base_url}/recipes-a-z-6735880'
headers = {'User-Agent': 'Mozilla/5.0'}

# Scrapes the main page
main_response = requests.get(main_url, headers=headers,timeout=30)
main_soup = BeautifulSoup(main_response.text, 'html.parser')

#Finds links to each category
category_links = [a['href'] for a in main_soup.find_all('a', class_='mntl-link-list__link type--dog-bold type--dog-link')]

recipes = []

for category_link in category_links:
    #Scrapes each category page
    category_url = category_link
    category_response = requests.get(category_url, headers=headers, timeout=30)

    if category_response.status_code == 200:
        category_soup = BeautifulSoup(category_response.text, 'html.parser')

        #Finds links for each recipe
        recipe_links = [a['href'] for a in category_soup.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card--image-top card card--no-image')]
        

        for recipe_link in recipe_links[:5]:
            #Scrapes each recipe
            recipe_url = recipe_link
            recipe_response = requests.get(recipe_url, headers=headers, timeout=30)
            
            if recipe_response.status_code == 200:
                recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')

                #Finds and extracts the details of the recipes
                title = recipe_soup.find('h1').text.strip()
                ingredients = [li.text.strip() for li in recipe_soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')]
                instructions = recipe_soup.find('div', class_='comp mm-recipes-steps__content mntl-sc-page mntl-block')

                recipes.append({
                    'title': title,
                    'ingredients': ', '.join(ingredients),
                    'instructions': instructions
                })
#Removes HTML elements from a .csv file
def clean_html(raw_html):
    if isinstance(raw_html, float):
        return ""
    soup = BeautifulSoup(raw_html,'html.parser')
    text = soup.get_text(separator=' ').strip()
    return ' '.join(text.split())

#Uses clean_html and transfers clean text from original csv to new csv
df = pd.read_csv('recipes.csv')
df['instructions'] = df['instructions'].apply(clean_html)
df.to_csv('cleaned_recipes.csv', index=False)

df = pd.DataFrame(recipes)
df.to_csv('recipes.csv', index = False)

df = pd.read_csv('cleaned_recipes.csv')
with open('recipes.txt', 'w', encoding='utf-8') as f:
    for _, row in df. iterrows():
        f.write(f"Title: {row['title']}\nIngredients: {row['ingredients']}\nInstructions: {row['instructions']}\n\n")

    