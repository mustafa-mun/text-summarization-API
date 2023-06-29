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
## EXTRACTIVE TEXT ##
@app.route("/summarizeTextExtractive", methods=["POST"])
@cache.cached()
async def summarize_text_extractive():
    text_param = request.args.get("text")

    if not text_param:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    
    resp = await extractive_handler(text_param)
    return resp
## ABSTRACTIVE TEXT ##
@app.route("/summarizeTextAbstractive", methods=["POST"])
@cache.cached()
async def summarize_text_abstractive():
    text_param = request.args.get("text")
    if not text_param:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    resp = await abstractive_handler(text_param)
    return resp
## EXTRACTIVE URL ##
@app.route("/summarizeUrlExtractive", methods=["POST"])
@cache.cached()
async def summarize_url_extractive():
    url_param = request.args.get("url")
    if not url_param:
        error_response = jsonify(error="Missing or empty 'url' parameter")
        return error_response, 400

     # Extract text from the URL
    text = await get_texts_from_url(url_param)
    resp = await extractive_handler(text)
    return resp
## ABSTRACTIVE URL ##
@app.route("/summarizeUrlAbstractive", methods=["POST"])
@cache.cached()
async def summarize_url_abstractive():
    url_param = request.args.get("url")
    
    if not url_param:
        error_response = jsonify(error="Missing or empty 'url' parameter")
        return error_response, 400

     # Extract text from the URL
    text = await get_texts_from_url(url_param)
    resp = await abstractive_handler(text)
    return resp
## EXTRACTIVE FILE ##
@app.route("/summarizeFileExtractive", methods=["POST"])
@cache.cached()
async def summarize_file_extractive():
    file_param = request.args.get("file")
    if not file_param:
        error_response = jsonify(error="Missing or empty 'file' parameter")
        return error_response, 400

     # Extract text from the file
    text = await read_file(file_param)
    resp = await extractive_handler(text)
    return resp
## ABSTRACTIVE FILE ##
@app.route("/summarizeFileAbstractive", methods=["POST"])
@cache.cached()
async def summarize_file_abstractive():
    file_param = request.args.get("file")
    
    if not file_param:
        error_response = jsonify(error="Missing or empty 'file' parameter")
        return error_response, 400

     # Extract text from the URL
    text = await read_file(file_param)
    resp = await abstractive_handler(text)
    return resp

async def extractive_handler(text):
    language = await detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    
    if not num_sentences:
        num_sentences = 3 # default num sentences

    summary = await summarize_extractive(text, num_sentences, language)

    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp

async def abstractive_handler(text):
    min_length_param = request.args.get("min")
    max_length_param = request.args.get("max")

    language = await detect_language_of_text(text)

    if not min_length_param or int(min_length_param) > 100: # min length can be maximum 100
        min_length_param = 50 # default min length
    if not max_length_param or int(max_length_param) > 200: # max length can be maximum 200
        max_length_param = 80 # default max length

    summary = await summarize_abstractive(text, int(min_length_param), int(max_length_param))

    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp

if __name__ == '__main__':
    app.run(debug=True)