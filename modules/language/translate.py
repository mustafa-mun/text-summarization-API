from deep_translator import GoogleTranslator
from modules.helpers.sanitize import *

async def translate(text, target_language):
    tl = target_language.lower()
    translated_text = ""
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    if tl not in langs_dict.values():
        return None
    translator = GoogleTranslator(source='auto', target=tl)
    if len(text) > 5000:
        # split the string into parts and append it into a new string
        splitted_string = split_string(text)
        for part in splitted_string:
            sanitized_part = sanitize_text(part)
            translated_text += translator.translate(sanitized_part)
        return translated_text
    else:
        sanitized_text = sanitize_text(text)
        return translator.translate(sanitized_text)

def return_supported_languages():
    return GoogleTranslator().get_supported_languages(as_dict=True)

def split_string(string):
    max_part_length = 5000
    num_parts = len(string) // max_part_length + 1
    split_parts = []

    for i in range(num_parts):
        start = i * max_part_length
        end = (i + 1) * max_part_length
        split_parts.append(string[start:end])

    return split_parts