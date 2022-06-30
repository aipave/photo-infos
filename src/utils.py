import re

def clean_text(input_text):
    return re.sub(r'[^a-zA-Z0-9 ,./]', '', input_text)
