from torch import nn
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.allrecipes.com/'
main_url = f'{base_url}/recipes-a-z-6735880'
headers = {'User-Agent': 'Mozilla/5.0'}

main_response = requests.get(main_url, headers=headers,timeout=10)
main_soup = BeautifulSoup(main_response.text, 'html.parser')

category_links = [a['href'] for a in main_soup.find_all('a', class_='mntl-link-list__link type--dog-bold type--dog-link')]

recipes = []

for category_link in category_links:
    category_url = category_link
    category_response = requests.get(category_url, headers=headers, timeout=10)

    if category_response.status_code == 200:
        category_soup = BeautifulSoup(category_response.text, 'html.parser')

        recipe_links = [a['href'] for a in category_soup.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card--image-top card card--no-image')]
        

        for recipe_link in recipe_links[:5]:
            recipe_url = recipe_link
            recipe_response = requests.get(recipe_url, headers=headers, timeout=10)
            
            if recipe_response.status_code == 200:
                recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')

                title = recipe_soup.find('h1').text.strip()
                ingredients = [li.text.strip() for li in recipe_soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')]
                instructions = recipe_soup.find('div', class_='comp mm-recipes-steps__content mntl-sc-page mntl-block')

                recipes.append({
                    'title': title,
                    'ingredients': ', '.join(ingredients),
                    'instructions': instructions
                })
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html,'html.parser')
    return soup.get_text(separator=' ').strip()

df = pd.read_csv('recipes.csv')
df['instructions'] = df['instructions'].apply(clean_html)
df.to_csv('cleaned_recipes.csv', index=False)

#print(category_links)

#print(recipes)