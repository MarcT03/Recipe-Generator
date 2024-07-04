import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.allrecipes.com/'
main_url = f'{base_url}/recipes-a-z-6735880'
headers = {'User-Agent': 'Mozilla/5.0'}

def recipe_scraper():
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
                    title_tag= recipe_soup.find('h1')
                    title = title_tag.text.strip() if title_tag else None

                    ingredients = [li.text.strip() for li in recipe_soup.find_all('li', class_='mm-recipes-structured-ingredients__list-item')]
                    ingredients = ', '.join(ingredients) if ingredients else None

                    instructions_div = recipe_soup.find('div', class_='comp mm-recipes-steps__content mntl-sc-page mntl-block')
                    instructions = instructions_div.get_text(separator=' ').strip() if instructions_div else None

                    #Entry is skipped if any fields are missing
                    if not title or not ingredients or not instructions:
                        continue

                    recipes.append({
                        'title': title,
                        'ingredients': ingredients,
                        'instructions': instructions
                    })

    df = pd.DataFrame(recipes)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/recipes.csv', index = False)

    # Uses clean_html and transfers clean text from original csv to new csv
    df['instructions'] = df['instructions'].apply(clean_html)
    df.to_csv('data/cleaned_recipes.csv', index=False)

    # Creates and transfers the into formatted into a .txt file
    with open('data/recipes.txt', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            f.write(f"Title: {row['title']}\nIngredients: {row['ingredients']}\nInstructions: {row['instructions']}\n\n")

    return df      


def clean_html(raw_html):
    if isinstance(raw_html, float):
        return ""
    soup = BeautifulSoup(str(raw_html),'html.parser')
    text = soup.get_text(separator=' ').strip()
    text = ' '.join(text.split())
    return text