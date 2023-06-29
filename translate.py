from deep_translator import GoogleTranslator
from sanitize import *

async def translate(text, target_language):
    tl = target_language.lower()
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    if tl not in langs_dict.values():
        return None
    translator = GoogleTranslator(source='auto', target=tl)
    sanitized_text = sanitize_text(text)
    return translator.translate(sanitized_text)
