from flask import jsonify, request, Blueprint, Response
from werkzeug.exceptions import BadRequest
from modules.summarization.abstractive import * 
from modules.helpers.fetch import *
from modules.language.translate import *
from modules.helpers.file import *
from modules.language.detectlang import *
import validators
import json

summarize_abs_blueprint = Blueprint('summarize_abstractive', __name__)

## ABSTRACTIVE TEXT ##
@summarize_abs_blueprint.route("/summarizeAbstractive", methods=["POST"])
async def summarize_text_abstractive():
    content = request.json.get("content")
    resp = None
    if not content:
        raise BadRequest("Missing or empty 'content' parameter")
    try:
        # check if content is url
        if validators.url(content):
            # content is a url
            text = await get_texts_from_url(content)
            resp = await abstractive_handler(text)
        # check if content is a file
        elif is_filename(content):
            # content is file
            # Extract text from the URL
            text = await read_file(content)
            resp = await abstractive_handler(text)
        else:
            # content is text
            resp = await abstractive_handler(content)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

async def abstractive_handler(text):
    min_length_param =  request.json.get("min")
    max_length_param = request.json.get("max")
    to_language = request.json.get("to_language")

    try:
        language = await detect_language_of_text(text)

        if not min_length_param: 
            min_length_param = 50 # default min length
        if not max_length_param : 
            max_length_param = 100 # default max length

        if int(min_length_param) > 100: # min length can be maximum 100
            min_length_param = 100
        if  int(max_length_param) > 200: # max length can be maximum 200
            max_length_param = 200

        if not to_language:
            # summarize text without translating
            summary = await summarize_abstractive(text, int(min_length_param), int(max_length_param))
            data = {
            "summarized_text": summary,
            "text_language": language.name.lower(),
            }
            json_string = json.dumps(data, ensure_ascii=False)
            response = Response(json_string, content_type="application/json; charset=utf-8" )
            return response
        else:
            # summarize text after translating
            translated_text = await translate(text, to_language)
            sanitized_text = sanitize_text(translated_text) # sanitize text after translation
            summary = await summarize_abstractive(sanitized_text, int(min_length_param), int(max_length_param))
            data = {
            "summarized_text": summary,
            "from_language": language.name.lower(),
            "to_language": to_language
            }
            json_string = json.dumps(data, ensure_ascii=False)
            response = Response(json_string, content_type="application/json; charset=utf-8" )
            return response
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500
    
@summarize_abs_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    error_response = jsonify(error=str(e))
    return error_response, 400