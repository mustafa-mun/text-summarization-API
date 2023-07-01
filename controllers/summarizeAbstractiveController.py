from flask import jsonify, request, Blueprint
from modules.summarization.abstractive import * 
from modules.helpers.fetch import *
from modules.language.translate import *
from modules.language.detectlang import *
from flask_caching import Cache

summarize_abs_blueprint = Blueprint('summarize_abstractive', __name__)
cache = Cache()
## ABSTRACTIVE TEXT ##
@summarize_abs_blueprint.route("/summarizeTextAbstractive", methods=["POST"])
@cache.cached()
async def summarize_text_abstractive():
    text_param = request.args.get("text")
    if not text_param:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    resp = await abstractive_handler(text_param)
    return resp

## ABSTRACTIVE URL ##
@summarize_abs_blueprint.route("/summarizeUrlAbstractive", methods=["POST"])
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

## ABSTRACTIVE FILE ##
@summarize_abs_blueprint.route("/summarizeFileAbstractive", methods=["POST"])
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