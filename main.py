from flask import Flask, jsonify, Blueprint, request
from summarize import * 

app = Flask(__name__)

api_router = Blueprint('api', __name__)

@app.route("/")
def hello_world():
    return jsonify(
        status="OK"
    )

@api_router.route("/")
def apiStatus():
    resp = jsonify(api="OK")
    resp.status_code = 200
    resp.mimetype = 'application/json'
    return resp

@api_router.route("/summarizeText", methods=["POST"])
def summarizeText():
    text = request.args.get("text")
    num_sentences = request.args.get("num_sentences")
    if not text:
        error_response = jsonify(error="Missing or empty 'text' parameter")
        return error_response, 400
    
    if not num_sentences:
        num_sentences = 3
    
    num_sentences = int(num_sentences)
    preprocessed_text, sentences_list = Preprocess_text(text)

    similarit_matrix_calculated_score = Calculate_similarity_matrix(preprocessed_text)

    summary = Generate_summarized_text(similarit_matrix_calculated_score, num_sentences, sentences_list)
    resp = jsonify(summarized_text = summary)
    resp.mimetype = 'application/json'
    return resp

# Register the Blueprint with the Flask app
app.register_blueprint(api_router, url_prefix='/api')