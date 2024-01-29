import sqlite3
from bs4 import BeautifulSoup
import requests
import re

def remove_notes_from_ingredient(ingredient):
    # Remove any (Note x) from the end of the ingredient
    return re.sub(r'\(Note \d\)', '', ingredient).strip()

def get_ingredients(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all ingredient groups
    ingredient_groups = soup.find_all('div', {'class': 'wprm-recipe-ingredient-group'})

    ingredients = []
    for group in ingredient_groups:
        # Extract group name if available, otherwise use an empty string
        group_name_tag = group.find('h4', {'class': 'wprm-recipe-group-name'})
        group_name = group_name_tag.text.strip() if group_name_tag else ''

        # Find all list items within the group
        ingredients_list_items = group.find_all('li', {'class': 'wprm-recipe-ingredient'})

        for li in ingredients_list_items:
            # Extract the amount, unit, name, and notes of each ingredient
            amount_tag = li.find('span', {'class': 'wprm-recipe-ingredient-amount'})
            amount = amount_tag.text.strip() if amount_tag else ''

            unit_tag = li.find('span', {'class': 'wprm-recipe-ingredient-unit'})
            unit = unit_tag.text.strip() if unit_tag else ''

            name_tag = li.find('span', {'class': 'wprm-recipe-ingredient-name'})
            name = name_tag.text.strip() if name_tag else ''

            notes_tag = li.find('span', {'class': 'wprm-recipe-ingredient-notes'})
            notes = notes_tag.text.strip() if notes_tag else ''

            # Combine the components to form the ingredient string
            ingredient_text = f"{amount} {unit} {name}, {notes}"

            cleaned_ingredient = remove_notes_from_ingredient(ingredient_text)

            # Append the ingredient to the list
            ingredients.append((group_name, cleaned_ingredient))

    return ingredients

def store_ingredients_in_database(url, recipe_title):
    ingredients = get_ingredients(url)

    # Connect to SQLite3 database
    conn = sqlite3.connect('/Users/Tommy/Documents/python-projects/website parser/data/recipes.db')
    cursor = conn.cursor()

    # Insert ingredients into the database
    for group_name, ingredient in ingredients:
        # Extract quantity and ingredient name
        match = re.match(r'([\d\/.]+) ?([a-zA-Z]+) (.+)', ingredient)
        if match:
            quantity, unit, name = match.groups()
        else:
            quantity, unit, name = '', '', ingredient

        # Insert into the ingredients table
        cursor.execute("INSERT INTO ingredients (quantity, unit, name, group_name, recipe) VALUES (?, ?, ?, ?, ?)",
                       (quantity, unit, name, group_name, recipe_title))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Example usage:
url = 'https://www.recipetineats.com/caramelised-vietnamese-shredded-beef/#wprm-recipe-container-36120'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the recipe title in the h1 element within the entry-header
recipe_title = soup.find('header', class_='entry-header').h1.text.strip()

# Store ingredients in the database
store_ingredients_in_database(url, recipe_title)
