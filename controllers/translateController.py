from flask import jsonify, request, Blueprint
from modules.helpers.fetch import *
from modules.language.translate import *
from modules.language.detectlang import *
from flask_caching import Cache

translate_blueprint = Blueprint('translate', __name__)
cache = Cache()

@translate_blueprint.route("/getSupportedLanguages", methods=["GET"])
@cache.cached()
def get_supported_languages():
    supported_languages = return_supported_languages()
    resp = jsonify(supported_languages)
    resp.mimetype = 'application/json'
    return resp

@translate_blueprint.route("/translateText", methods=["POST"])
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

@translate_blueprint.route("/translateFile", methods=["POST"])
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

@translate_blueprint.route("/translateUrl", methods=["POST"])
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

