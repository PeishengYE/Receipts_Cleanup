import re

def extract_non_digit_info(filename):
    # Regex pattern to match the non-digit info between date and extension
    match = re.search(r'^\d{4}_\d{4}_(\D+?)(?:_\d+)?\.\w+$', filename)
    if match:
        return match.group(1)
    return None

# Test cases
print(extract_non_digit_info("2024_1124_CT_SUPERMARKET.jpg"))  # Output: CT_SUPERMARKET
print(extract_non_digit_info("2024_1119_GAS_01.jpg"))          # Output: GAS
print(extract_non_digit_info("2024_1119_OTHERFILE.png"))       # Output: OTHERFILE

