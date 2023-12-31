from flask import jsonify, request, Blueprint, Response
from werkzeug.exceptions import BadRequest
from modules.summarization.extractive import * 
from modules.helpers.fetch import *
from modules.helpers.file import *
from modules.language.translate import *
from modules.language.detectlang import *
import validators
import json

summarize_ext_blueprint = Blueprint('summarize_extractive', __name__)

## EXTRACTIVE TEXT ##
@summarize_ext_blueprint.route("/summarizeExtractive", methods=["POST"])
async def summarize_text_extractive():
    content = request.json.get("content")
    if not content:
        raise BadRequest("Missing or empty 'content' parameter")
    
    try:
        resp = await extractive_handler(content)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

async def extractive_handler(content):
    try:
        num_sentences = request.json.get("sentences")
        to_language = request.json.get("to_language")

        if not num_sentences:
            num_sentences = 3 # default num sentences
        else:
            num_sentences = int(num_sentences)

        if validators.url(content):
            # content is a url
            url_text = await get_html_from_url(content)
            language = await detect_language_of_text(url_text)
            summary = await summarize_extractive(num_sentences, language.name.lower(), url=content, text=None, file=None)
            resp = await handle_to_language_param(to_language, summary, language)
        # check if content is a file
        elif is_filename(content):
            # content is file
            file_text = await read_file(content)
            language = await detect_language_of_text(file_text)
            summary = await summarize_extractive(num_sentences, language.name.lower(), file=content, text=None, url=None)
            resp = await handle_to_language_param(to_language, summary, language)
        else:
            # content is text
            language = await detect_language_of_text(content)
            summary = await summarize_extractive(num_sentences, language.name.lower(), text=content, url=None, file=None)
            resp = await handle_to_language_param(to_language, summary, language)
        return resp
    
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500
    

async def handle_to_language_param(to_language, summary, language):
    if not to_language:
    # summarize text without translating
        data = {
            "summarized_text": summary,
            "text_language": language.name.lower(),
        }
        json_string = json.dumps(data, ensure_ascii=False)
        response = Response(json_string, content_type="application/json; charset=utf-8" )
        return response
    else:
        # summarize text after translating
        translated_text = await translate(summary, to_language)
        sanitized_text = sanitize_text(translated_text) # sanitize text after translation
        data = {
            "summarized_text": sanitized_text,
            "from_language": language.name.lower(),
            "to_language": to_language
        }
        json_string = json.dumps(data, ensure_ascii=False)
        response = Response(json_string, content_type="application/json; charset=utf-8" )
        return response
    
@summarize_ext_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    error_response = jsonify(error=str(e))
    return error_response, 400