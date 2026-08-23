import re 

def extract_number(text):
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    
    word_to_num = {
        "zero": 0, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40,
        "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
        "ninety": 90, "hundred": 100
    }
    for word, num in word_to_num.items():
        if word in text:
            return num
    return None

def extract_category(command):
    categories = ["food", "groceries", "transport", "shopping", "entertainment", "bills", "rent", "medical", "education"]
    for cat in categories:
        if cat in command:
            return cat
    return "general"
