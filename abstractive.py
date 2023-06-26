from transformers import T5ForConditionalGeneration, T5Tokenizer
from sanitize import *
# Load the pre-trained model and tokenizer
model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def summarize_abstractive(text):
    # Tokenize the input text
    sanitized_text = sanitize_text(text)
    input_ids = tokenizer.encode(sanitized_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate the summary
    summary_ids = model.generate(input_ids, num_beams=4, max_length=150, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
