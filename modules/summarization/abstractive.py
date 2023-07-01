from transformers import T5TokenizerFast, T5ForConditionalGeneration
from modules.helpers.sanitize import *

# Load the pre-trained model and tokenizer
model_name = "t5-base"
tokenizer=T5TokenizerFast.from_pretrained(model_name)
model=T5ForConditionalGeneration.from_pretrained(model_name, return_dict=True)

async def summarize_abstractive(text, min_length, max_length):
    # Tokenize the input text
    sanitized_text = sanitize_text(text)
    inputs = tokenizer.encode("summarize: " + sanitized_text, return_tensors='pt', max_length=512, padding="max_length", truncation=True)

    # Generate the summary
    output = model.generate(inputs, num_beams=int(2), no_repeat_ngram_size=3, length_penalty=2.0, min_length=min_length, max_length = max_length, early_stopping=True)
    summary = tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return summary

