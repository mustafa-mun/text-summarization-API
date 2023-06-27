from flask import Flask, jsonify, request
from extractive import * 
from abstractive import *
from fetch import *
from detectlang import *

app = Flask(__name__)

@app.route("/")
def apiStatus():
    resp = jsonify(api="OK")
    resp.status_code = 200
    resp.mimetype = 'application/json'
    return resp

@app.route("/summarizeText", methods=["POST"])
def summarizeText():
    text = request.args.get("text")
    language = detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    method = request.args.get("method")
    summary = None

    if not text:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    
    if not num_sentences:
        num_sentences = 3 # default num sentences

    if not method:
        method = "extractive" # default method

    num_sentences = int(num_sentences)
    if method == "extractive":
        summary = summarize_extractive(text, num_sentences, language)
    elif method == "abstractive":
        summary = summarize_abstractive(text)
    else:
        error_response = jsonify(error="Method not allowed")
        return error_response, 400

    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp
    
@app.route("/summarizeUrl", methods=["POST"])
def summarizeUrl():
    url = request.args.get("url")
    text = get_texts_from_url(url)
    language = detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    method = request.args.get("method")
    summary = None
    
    if not url:
        error_response = jsonify(error="Missing or empty 'url' parameter")
        return error_response, 400
    
    if not num_sentences:
            num_sentences = 3 # default num sentences

    if not method:
        method = "extractive" # default method

    num_sentences = int(num_sentences)
    if method == "extractive":
        summary = summarize_extractive(text, num_sentences, language)
    elif method == "abstractive":
        summary = summarize_abstractive(text)
    else:
        error_response = jsonify(error="Method not allowed")
        return error_response, 400
    

    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)