import re

def separate_ingredients_quantity(text):
    # Define a pattern for quantities and ingredients
    pattern = re.compile(r'(.+?)(?:\s?-\s?)?(.+)')

    # Match the pattern in the given text
    match = pattern.match(text)

    if match:
        # Extract quantity and ingredient
        quantity = match.group(1).strip()
        ingredient = match.group(2).strip()
        return quantity, ingredient
    else:
        # If no match, return None
        return None, text

# Example usage
example_text = "(90g / 6 tbsp butter)"
quantity, ingredient = separate_ingredients_quantity(example_text)

print("Quantity:", quantity)
print("Ingredient:", ingredient)
