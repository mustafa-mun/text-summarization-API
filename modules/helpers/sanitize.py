import re
import html
import unicodedata

def sanitize_text(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Handle special characters
    text = html.unescape(text)

    # Normalize text
    text = unicodedata.normalize("NFKC", text)

    # Replace special characters
    text = re.sub(r"\W+", " ", text)

    # Remove noisy data
    # For example, removing consecutive whitespace, extra newlines
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text
