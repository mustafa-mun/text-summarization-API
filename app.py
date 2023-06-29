from flask import Flask, jsonify, request
from extractive import * 
from abstractive import *
from fetch import *
from detectlang import *
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 50
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/healthz")
def healthz():
    return "OK", 200

@app.route("/summarizeExtractive", methods=["POST"])
@cache.cached()
async def summarize_text_extractive():
    text_param = request.args.get("text")
    url_param = request.args.get("url")
    text = None
    if not text_param and not url_param:
        error_response = jsonify(error="Missing or empty 'text' or 'url' parameter")
        return error_response, 400
    if text_param and url_param:
        error_response = jsonify(error="Choose between 'text' or 'url' parameter")
        return error_response, 400
    
    if text_param:
        text = text_param
    if url_param:
        # Extract text from the URL
        text = await get_texts_from_url(url_param)

    language = await detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    
    
    if not num_sentences:
        num_sentences = 3 # default num sentences

    summary = await summarize_extractive(text, num_sentences, language)


    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp
    
@app.route("/summarizeAbstractive", methods=["POST"])
@cache.cached()
async def summarize_text_abstractive():
    text_param = request.args.get("text")
    url_param = request.args.get("url")
    text = None
    min_length_param = request.args.get("min")
    max_length_param = request.args.get("max")

    if not text_param and not url_param:
        error_response = jsonify(error="Missing or empty 'text' or 'url' parameter")
        return error_response, 400
    if text_param and url_param:
        error_response = jsonify(error="Choose between 'text' or 'url' parameter")
        return error_response, 400
    
    if text_param:
        text = text_param
    if url_param:
        # Extract text from the URL
        text = await get_texts_from_url(url_param)

    language = await detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    
    if not num_sentences:
        num_sentences = 3 # default num sentences

    if not min_length_param or min_length_param > 100: # min length can be maximum 100
        min_length_param = 50 # default min length
    if not max_length_param or max_length_param > 200: # max length can be maximum 200
        max_length_param = 80 # default max length

    summary = summarize_abstractive(text, min_length_param, max_length_param)

    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp
    

if __name__ == '__main__':
    app.run(debug=True)