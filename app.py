from flask import Flask, jsonify, request
from extractive import * 
from abstractive import *
from fetch import *
from translate import *
from detectlang import *
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
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

@app.route("/getSupportedLanguages", methods=["GET"])
@cache.cached()
def get_supported_languages():
    supported_languages = return_supported_languages()
    resp = jsonify(supported_languages)
    resp.mimetype = 'application/json'
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

@app.route("/translateText", methods=["POST"])
@cache.cached()
async def translate_text():
    target_param = request.args.get("target")
    text_param = request.args.get("text")
    if not target_param:
        error_response = jsonify(error="Missing or empty 'target' parameter")
        return error_response, 400
    if not text_param:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    
    resp = await translate_handler(text_param, target_param)
    return resp

@app.route("/translateFile", methods=["POST"])
@cache.cached()
async def translate_file():
    target_param = request.args.get("target")
    file_param = request.args.get("file")
    if not target_param:
        error_response = jsonify(error="Missing or empty 'target' parameter")
        return error_response, 400
    if not file_param:
        error_response = jsonify(error="Missing or empty 'file' parameter")
        return error_response, 400
    
    text = await read_file(file_param)
    resp = await translate_handler(text, target_param)
    return resp

@app.route("/translateUrl", methods=["POST"])
@cache.cached()
async def translate_url():
    target_param = request.args.get("target")
    url_param = request.args.get("url")
    if not target_param:
        error_response = jsonify(error="Missing or empty 'target' parameter")
        return error_response, 400
    if not url_param:
        error_response = jsonify(error="Missing or empty 'url' parameter")
        return error_response, 400
    
    text = await get_html_from_url(url_param)
    resp = await translate_handler(text, target_param)
    return resp

async def extractive_handler(text):
    language = await detect_language_of_text(text)
    num_sentences = request.args.get("sentences")
    to_language = request.args.get("to_language")

    if not num_sentences:
        num_sentences = 3 # default num sentences
    else:
        num_sentences = int(num_sentences)

    if not to_language:
        # summarize text without translating
        summary = await summarize_extractive(text, num_sentences, language)
        resp = jsonify(summarized_text = summary, text_language = language.name)
        resp.mimetype = 'application/json'
        return resp
    else:
        # summarize text after translating
        translated_text = await translate(text, to_language)
        sanitized_text = sanitize_text(translated_text) # sanitize text after translation
        summary = await summarize_extractive(sanitized_text, num_sentences, language)
        resp = jsonify(summarized_text = summary, from_language = language.name, to_language = to_language)
        resp.mimetype = 'application/json'
        return resp

async def abstractive_handler(text):
    min_length_param = request.args.get("min")
    max_length_param = request.args.get("max")
    to_language = request.args.get("to_language")

    language = await detect_language_of_text(text)

    if not min_length_param or int(min_length_param) > 100: # min length can be maximum 100
        min_length_param = 50 # default min length
    if not max_length_param or int(max_length_param) > 200: # max length can be maximum 200
        max_length_param = 80 # default max length


    if not to_language:
        # summarize text without translating
        summary = await summarize_abstractive(text, int(min_length_param), int(max_length_param))
        resp = jsonify(summarized_text = summary, text_language = language.name)
        resp.mimetype = 'application/json'
        return resp
    else:
        # summarize text after translating
        translated_text = await translate(text, to_language)
        sanitized_text = sanitize_text(translated_text) # sanitize text after translation
        summary = await summarize_abstractive(sanitized_text, int(min_length_param), int(max_length_param))
        resp = jsonify(summarized_text = summary, from_language = language.name, to_language = to_language)
        resp.mimetype = 'application/json'
        return resp

async def translate_handler(text, target_param):
    text_language = await detect_language_of_text(text)
    translated_text = await translate(text, target_param)
    sanitized_text = sanitize_text(translated_text)

    if not translated_text:
        error_response = jsonify(error="Target language not found")
        return error_response, 404
   
    resp = jsonify(translated_text = sanitized_text, from_language = text_language.name, to_language = target_param)
    resp.mimetype = 'application/json'
    return resp

if __name__ == '__main__':
    app.run(debug=True)