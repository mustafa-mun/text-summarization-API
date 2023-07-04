from flask import jsonify, request, Blueprint, Response
from werkzeug.exceptions import BadRequest
from modules.helpers.fetch import *
from modules.helpers.file import *
from modules.language.translate import *
from modules.language.detectlang import *
import validators
import json

translate_blueprint = Blueprint('translate', __name__)

@translate_blueprint.route("/supportedLanguages", methods=["GET"])
def get_supported_languages():
    try:
        supported_languages = return_supported_languages()
        resp = jsonify(supported_languages)
        resp.headers.add('Content-Type', 'application/json; charset=utf-8')
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

@translate_blueprint.route("/translate", methods=["POST"])
async def translate_text():
    target_param = request.json.get("target")
    content_param = request.json.get("content")
    if not target_param:
        raise BadRequest("Missing or empty 'target' parameter")
    if not content_param:
        raise BadRequest("Missing or empty 'content' parameter")
    
    try:
         # check if content is url
        if validators.url(content_param):
            # content is a url
            text = await get_texts_from_url(content_param)
            resp = await translate_handler(text, target_param)
        # check if content is a file
        elif is_filename(content_param):
            # content is file
            # Extract text from the URL
            text = await read_file(content_param)
            resp = await translate_handler(text, target_param)
        else:
            # content is text
            resp = await translate_handler(content_param, target_param)
        return resp
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500


@translate_blueprint.route("/contentLanguage", methods=["GET"])
async def get_language_of_content():
    content_param = request.args.get("content")
    language = None
    if not content_param:
        raise BadRequest("Missing or empty 'content' parameter")
    
    try:
         # check if content is url
        if validators.url(content_param):
            # content is a url
            text = await get_texts_from_url(content_param)
            language = await detect_language_of_text(text)
        # check if content is a file
        elif is_filename(content_param):
            # content is file
            # Extract text from the file
            text = await read_file(content_param)
            language = await detect_language_of_text(text)
        else:
            # content is text
            language = await detect_language_of_text(content_param)

        supported_langs = return_supported_languages()
        language_code = supported_langs[language.name.lower()]
        data = {
            "language": language.name.lower(),
            "language_code": language_code,
        }
        json_string = json.dumps(data, ensure_ascii=False)
        response = Response(json_string, content_type="application/json; charset=utf-8" )
        return response
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500    

async def translate_handler(text, target_param):
    try:
        text_language = await detect_language_of_text(text)
        translated_text = await translate(text, target_param)
        sanitized_text = sanitize_text(translated_text)

        if not translated_text:
            error_response = jsonify(error="Target language not found")
            return error_response, 404

        data = {
            "translated_text": sanitized_text,
            "from_language": text_language.name.lower(),
            "to_language": target_param
        }
        json_string = json.dumps(data, ensure_ascii=False)
        response = Response(json_string, content_type="application/json; charset=utf-8" )
        return response
    except Exception as e:
        error_response = jsonify(error=str(e))
        return error_response, 500

@translate_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    error_response = jsonify(error=str(e))
    return error_response, 400