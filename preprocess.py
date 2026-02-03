import re

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove special characters but keep spaces and alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
