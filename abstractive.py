from transformers import AutoTokenizer, AutoModelWithLMHead
from sanitize import *

# Load the pre-trained model and tokenizer
model_name = "t5-base"
tokenizer=AutoTokenizer.from_pretrained(model_name)
model=AutoModelWithLMHead.from_pretrained(model_name, return_dict=True)

def summarize_abstractive(text):
    # Tokenize the input text
    sanitized_text = sanitize_text(text)
    inputs = tokenizer.encode("summarize: " + sanitized_text, return_tensors='pt', max_length=512, truncation=True)

    # Generate the summary
    output = model.generate(inputs, min_length=80, max_length=100)
    summary = tokenizer.decode(output[0])
    return summary

