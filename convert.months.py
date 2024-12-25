import re
def convert_date_to_numeric_old(date_str):
    # Mapping of month abbreviations to numeric equivalents
    month_map = {
        "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
        "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
        "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"
    }
    # Extract month and day
    match = re.match(r"(\w{3})(\d{1,2})", date_str.upper())
    if match:
        month = month_map.get(match.group(1), "00")  # Default to "00" if the month is invalid
        day = f"{int(match.group(2)):02}"  # Format day as two digits
        return f"{month}{day}"
    return None

def convert_date_to_numeric(date_str):
    """
    Replace month abbreviations with numeric equivalents in a string,
    leaving all other content unchanged.
    """
    # Mapping of month abbreviations to numeric equivalents
    month_map = {
        "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
        "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
        "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"
    }
    # Replace month abbreviations with their numeric equivalents
    #return re.sub(r"\b(\w{3})(\d{1,2})\b", 
    #              lambda m: f"{month_map.get(m.group(1).upper(), m.group(1))}{m.group(2)}", 
    #              date_str)
        # Replace month abbreviations with their numeric equivalents
    return re.sub(r"\b([A-Za-z]{3}) (\d{1,2})\b", 
                  lambda m: f"{month_map.get(m.group(1).upper(), m.group(1))}{int(m.group(2)):02}", 
                  date_str)
# Example usage
date_str = "Nov 15,2024"
converted_date = convert_date_to_numeric(date_str)
print(converted_date)  # Output: "1115"

