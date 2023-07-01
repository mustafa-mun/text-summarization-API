from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest
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
        raise BadRequest("Missing or empty 'text' parameter")
    try:
        resp = await abstractive_handler(text_param)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

## ABSTRACTIVE URL ##
@summarize_abs_blueprint.route("/summarizeUrlAbstractive", methods=["POST"])
@cache.cached()
async def summarize_url_abstractive():
    url_param = request.args.get("url")
    
    if not url_param:
        raise BadRequest("Missing or empty 'url' parameter")
    
    try:
         # Extract text from the URL
        text = await get_texts_from_url(url_param)
        resp = await abstractive_handler(text)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

## ABSTRACTIVE FILE ##
@summarize_abs_blueprint.route("/summarizeFileAbstractive", methods=["POST"])
@cache.cached()
async def summarize_file_abstractive():
    file_param = request.args.get("file")
    
    if not file_param:
        raise BadRequest("Missing or empty 'file' parameter")

    try:
         # Extract text from the URL
        text = await read_file(file_param)
        resp = await abstractive_handler(text)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

async def abstractive_handler(text):
    min_length_param = request.args.get("min")
    max_length_param = request.args.get("max")
    to_language = request.args.get("to_language")

    try:
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
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500
    
@summarize_abs_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    error_response = jsonify(error=str(e))
    return error_response, 400