from flask import Flask, jsonify, request
from extractive import * 
from abstractive import *
from fetch import *
from detectlang import *

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return "OK", 200

@app.route("/summarizeExtractive", methods=["POST"])
def summarize_text():
    textParam = request.args.get("text")
    urlParam = request.args.get("url")
    text = None
    if not textParam and not urlParam:
        error_response = jsonify(error="Missing or empty 'text' or 'url' parameter")
        return error_response, 400
    if textParam and urlParam:
        error_response = jsonify(error="Choose between 'text' or 'url' parameter")
        return error_response, 400
    
    if textParam:
        text = textParam
    if urlParam:
        # Extract text from the URL
        text = get_texts_from_url(urlParam)

    language = detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    
    
    if not num_sentences:
        num_sentences = 3 # default num sentences

    summary = summarize_extractive(text, num_sentences, language)


    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp
    
@app.route("/summarizeAbstractive", methods=["POST"])
def summarize_abstractive():
    textParam = request.args.get("text")
    urlParam = request.args.get("url")
    text = None
    if not textParam and not urlParam:
        error_response = jsonify(error="Missing or empty 'text' or 'url' parameter")
        return error_response, 400
    if textParam and urlParam:
        error_response = jsonify(error="Choose between 'text' or 'url' parameter")
        return error_response, 400
    
    if textParam:
        text = textParam
    if urlParam:
        # Extract text from the URL
        text = get_texts_from_url(urlParam)

    language = detect_language_of_text(text)
    num_sentences = request.args.get("num_sentences")
    
    if not num_sentences:
        num_sentences = 3 # default num sentences

    summary = summarize_abstractive(text)

    resp = jsonify(summarized_text = summary, text_language = language.name)
    resp.mimetype = 'application/json'
    return resp
    

if __name__ == '__main__':
    app.run()