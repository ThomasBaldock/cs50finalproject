from bs4 import BeautifulSoup
import requests

def get_ingredients(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the divs by their class
    divs = soup.find_all('div', {'class': ['wprm-recipe-ingredients-container', 'wprm-recipe-ingredients-no-images', 'wprm-block-text-normal', 'wprm-ingredient-style-regular', 'wprm-recipe-images-before']})

    ingredients = []
    for div in divs:
        # Extract the text of each ingredient
        ingredients.append(div.text.strip())

    return ingredients

# Example usage:
url = 'https://www.recipetineats.com/grilled-shrimp-with-lemon-garlic-butter/#wprm-recipe-container-37243'
ingredients = get_ingredients(url)
for ingredient in ingredients:
    print(ingredient)
    print("\n")
