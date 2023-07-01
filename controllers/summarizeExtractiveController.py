from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest
from modules.summarization.extractive import * 
from modules.helpers.fetch import *
from modules.helpers.file import *
from modules.language.translate import *
from modules.language.detectlang import *
import validators

summarize_ext_blueprint = Blueprint('summarize_extractive', __name__)

## EXTRACTIVE TEXT ##
@summarize_ext_blueprint.route("/summarizeExtractive", methods=["POST"])
async def summarize_text_extractive():
    content_param = request.args.get("content")
    resp = None
    if not content_param:
        raise BadRequest("Missing or empty 'content' parameter")
    
    try:
        # check if content is url
        if validators.url(content_param):
            # content is a url
            text = await get_texts_from_url(content_param)
            resp = await extractive_handler(text)
        # check if content is a file
        elif is_filename(content_param):
            # content is file
            # Extract text from the URL
            text = await read_file(content_param)
            resp = await extractive_handler(text)
        else:
            # content is text
            resp = await extractive_handler(content_param)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

async def extractive_handler(text):
    try:
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
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500
    
@summarize_ext_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    error_response = jsonify(error=str(e))
    return error_response, 400