import re
import html
import unicodedata

def sanitize_text(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Handle special characters
    text = html.unescape(text)

    # Normalize text
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

    # Replace special characters
    text = text.replace("ı", "i").replace("ğ", "g").replace("ö", "o").replace("ü", "u").replace("ç", "c")

    # Remove noisy data
    # For example, removing consecutive whitespace, extra newlines, or special characters
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[^a-zA-Z0-9\n.,?! ]", "", text)

    return text
