# Define the dictionary with key-value pairs
expense_categories = {
    "C1": "Computer expenses",
    "C2": "Professional fee",
    "C3": "Tele communication",
    "C4": "Advertising & promotion",
    "C5": "Membership",
    "C6": "Registration fee",
    "C7": "Incorporation cost",
    "C8": "Parking",
    "C9": "Business travel",
    "C10": "Office supplies",
    "C11": "Training",
    "C12": "Meals & entertainment",
    "C13": "Software"
}

def get_cts_from_key( key: str) -> str:
    """
    Retrieve the value corresponding to a given key in the dictionary.

    Args:
        categories (dict): The dictionary of categories.
        key (str): The key to look up.

    Returns:
        str: The corresponding value, or an error message if the key is not found.
    """
    return expense_categories.get(key, "Key not found")

def get_key_from_cts( category: str) -> str:
    """
    Retrieve the key corresponding to a given value in the dictionary.

    Args:
        categories (dict): The dictionary of categories.
        value (str): The value to look up.

    Returns:
        str: The corresponding key, or an error message if the value is not found.
    """
    for k, v in expense_categories.items():
        if v.lower() == category.lower():  # Case-insensitive comparison
            return k
    return "Value not found"

# Test the dictionary and functions
print(get_cts_from_key("C1"))  # Output: Computer expenses
print(get_cts_from_key("C9"))  # Output: Business travel
print(get_cts_from_key("C20"))  # Output: Key not found

#print(get_key_from_value(expense_categories, "Software"))  # Output: C13
print(get_key_from_cts("Tele communication"))  # Output: C3
print(get_key_from_cts("Unknown Category"))  # Output: Value not found

