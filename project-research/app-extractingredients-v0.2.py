from bs4 import BeautifulSoup
import requests
import re

def remove_notes_from_ingredient(ingredient):
    # Remove any (Note x) from the end of the ingredient
    return re.sub(r'\(Note \d\)', '', ingredient).strip()

def get_ingredients(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div by class containing ingredients
    div = soup.find('div', {'class': 'wprm-recipe-ingredients-container'})

    # Find all list items within the ingredients div
    ingredients_list_items = div.find_all('li')

    ingredients = []
    for li in ingredients_list_items:
        # Extract the text of each ingredient and add a space between quantity and name
        ingredient_text = ' '.join(li.stripped_strings).replace('▢', '')
        cleaned_ingredient = remove_notes_from_ingredient(ingredient_text)
        ingredients.append(cleaned_ingredient)

    return ingredients

def print_ingredients_table(ingredients):
    # Print table header
    print("+-------------------+------------------------------------------+")
    print("|      Quantity     |               Ingredient                   |")
    print("+-------------------+------------------------------------------+")

    # Print each ingredient in the table format
    for ingredient in ingredients:
        # Improved regular expression to handle various quantity formats
        match = re.match(r'^([\d\/\.\s]+[a-zA-Z]*)(.*)$', ingredient)
        if match:
            quantity, item = match.groups()
            print(f"|{quantity.strip().ljust(18)}|{item.strip().ljust(42)}|")
        else:
            print(f"|{''.ljust(18)}|{ingredient.strip().ljust(42)}|")

    # Print table footer
    print("+-------------------+------------------------------------------+")

# Example usage:
url = 'https://www.recipetineats.com/grilled-shrimp-with-lemon-garlic-butter/#wprm-recipe-container-37243'
ingredients = get_ingredients(url)
print_ingredients_table(ingredients)
