import re
import html

def sanitize_text(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Handle special characters
    text = html.unescape(text)


    # remove consecutive whitespace, extra newlines
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text
