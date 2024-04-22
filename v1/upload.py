import sqlite3
from bs4 import BeautifulSoup
import requests
import re

def store_ingredients_in_database(url, recipe_title):
    ingredients = get_ingredients(url)

    # Connect to SQLite3 database
    conn = sqlite3.connect('sample.db')
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
        cursor.execute("INSERT INTO ingredients (quantity, unit, name, group_name, recipe) VALUES (?, ?, ?, ?, ?)", (quantity, unit, name, group_name, recipe_title))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Example usage:

###TO DO: WRITE CODE WHICH GETS ALL URLS FROM SQL Database###

url = 'https://www.recipetineats.com/caramelised-vietnamese-shredded-beef/#wprm-recipe-container-36120'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the recipe title in the h1 element within the entry-header
recipe_title = soup.find('header', class_='entry-header').h1.text.strip()

# Store ingredients in the database
store_ingredients_in_database(url, recipe_title)
