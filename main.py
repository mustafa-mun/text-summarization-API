from flask import Flask, jsonify, Blueprint

app = Flask(__name__)

api_router = Blueprint('api', __name__)

@app.route("/")
def hello_world():
    return jsonify(
        status="OK"
    )

@api_router.route("/")
def apiStatus():
    return jsonify(
        api="OK"
    )

# Register the Blueprint with the Flask app
app.register_blueprint(api_router, url_prefix='/api')