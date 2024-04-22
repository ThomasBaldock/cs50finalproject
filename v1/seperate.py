from bs4 import BeautifulSoup
import requests
import re

def remove_notes_from_ingredient(ingredient):
    # Remove any (Note x) from the end of the ingredient
    return re.sub(r'\(Note \d\)', '', ingredient).strip()

def remove_punctuation_from_ingredient(text):
    # Remove any , or / from the beginning of the ingredient.
    if text.startswith('/') or text.startswith(','):
        return text[1:]
    return text

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
        ingredient = ' '.join(li.stripped_strings).replace('▢', '')
        ingredient = remove_notes_from_ingredient(ingredient)
        ingredients.append(ingredient)

    return ingredients

def remove_after_comma(text):
    if ',' in text:
        text = text.split(',')[0].strip()
    return text
def remove_after_parentheses(text):
    if '(' in text:
        # Split text at the first '(' and get the first part
        trimmed_text = text.split('(', 1)[0].strip()
        # Check if the resulting text after trimming is not blank
        if trimmed_text:
            return trimmed_text
    return text

def remove_unit(text):
    pattern = r'^\s*\d+\s*(tbsp|tsp|lb|oz)\s*'
    return re.sub(pattern, '', text)

def clean_names(names):

    names_cleaned = []

    for name in names:
        name = remove_punctuation_from_ingredient(name)
        name = name.lstrip()
        name = remove_after_comma(name)
        name = remove_after_parentheses(name)
        name = remove_unit(name)
        names_cleaned.append(name)

    return names_cleaned

def seperate(ingredients):
    quantities = []
    names = []
    for ingredient in ingredients:
        match = re.match(r'^([\d\/\.\s]+[a-zA-Z]*)(.*)$', ingredient)
        if match:
            quantity, item = match.groups()
            quantities.append(quantity.strip())
            names.append(item.strip())
        else:
            quantities.append('')
            names.append(ingredient.strip())
    return quantities, names

standard_units = ['tbsp', 'tsp', 'cup', 'g', 'oz', 'lb', 'kg', 'mg', 'ml', 'liter', 'litre', 'small', 'large', 'sheets', 'pinch', 'Pinch', 'cups', 'liters', 'litres']

def no_unit_fix(quantities, names):
    
    # Initialize refined lists
    refined_quantities = []
    refined_names = []

    # Iterate through quantities and names simultaneously
    for quantity, name in zip(quantities, names):
        # Find the index of the first alphabetical character after initial numerical values
        alpha_index = next((i for i, char in enumerate(quantity) if char.isalpha() or char in ['.', '-']), None)
        if alpha_index is not None:
            # Extract the unit part
            unit = quantity[alpha_index:].strip()
            # Check if the unit is not a standard unit of measurement
            if unit.lower() not in standard_units:
                # Move the unit part to the beginning of the name
                refined_names.append(unit + " " + name)
                refined_quantities.append(quantity[:alpha_index].strip())
            else:
                refined_quantities.append(quantity)
                refined_names.append(name)
        else:
            # No alphabetic character found, treat as if it's a name
            refined_quantities.append("")
            refined_names.append(quantity + " " + name)
    return refined_quantities, refined_names

def move_quantities(Quantities, Names, standard_units):
    for i, name in enumerate(Names):
        for unit in standard_units:
            if unit in name:
                quantity_str, rest = name.split(unit, 1)
                quantity_str = quantity_str.strip()
                if Quantities[i] == '':
                    Quantities[i] = quantity_str + ' ' + unit
                    Names[i] = rest.strip()
                break

url = 'https://www.recipetineats.com/spicy-maple-roast-carrots-with-crispy-chickpeas/'

ingredients = get_ingredients(url)
quantities, names = seperate(ingredients)
names = clean_names(names)
quantities, names = no_unit_fix(quantities, names)
move_quantities(quantities, names, standard_units)

for i in range(len(names)):
    for unit in standard_units:
        if unit in names[i]:
            # Use regular expression to match numerical values with or without decimal points
            names[i] = re.sub(r'\b\d+(?:\.\d+)?\s*' + re.escape(unit), '', names[i])

names = [name.strip() for name in names]
names = [re.sub(r'^of\s+', '', name) for name in names]
names = [name.capitalize() if name[0].isalpha() else name for name in names]

for quantity, name in zip(quantities, names):
    print(quantity + ": " + name)
