from flask import jsonify, request, Blueprint
from modules.summarization.extractive import * 
from modules.helpers.fetch import *
from modules.language.translate import *
from modules.language.detectlang import *
from flask_caching import Cache

summarize_ext_blueprint = Blueprint('summarize_extractive', __name__)
cache = Cache()

## EXTRACTIVE TEXT ##
@summarize_ext_blueprint.route("/summarizeTextExtractive", methods=["POST"])
@cache.cached()
async def summarize_text_extractive():
    text_param = request.args.get("text")

    if not text_param:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    
    resp = await extractive_handler(text_param)
    return resp
## EXTRACTIVE URL ##
@summarize_ext_blueprint.route("/summarizeUrlExtractive", methods=["POST"])
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
## EXTRACTIVE FILE ##
@summarize_ext_blueprint.route("/summarizeFileExtractive", methods=["POST"])
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
    