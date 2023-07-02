from modules.helpers.sanitize import *
from transformers import BartTokenizer, BartForConditionalGeneration

# Load the BART model for summarization
model_name = "facebook/bart-base"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

async def summarize_abstractive(text, min_length, max_length):
    sanitized_text = sanitize_text(text)

    # Tokenize the input text
    tokenized_text = tokenizer([sanitized_text], truncation=True, max_length=max_length, return_tensors="pt")

    # Generate the summary
    summary_ids = model.generate(tokenized_text["input_ids"], 
                                 attention_mask=tokenized_text["attention_mask"],
                                 max_length=max_length, 
                                 min_length=min_length, 
                                 num_beams=4, 
                                 early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
