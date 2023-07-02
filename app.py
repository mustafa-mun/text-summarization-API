from flask import Flask, Blueprint
from controllers import summarizeExtractiveController, summarizeAbstractiveController, translateController

app = Flask(__name__)

# Create a Blueprint for v1
v1_blueprint = Blueprint('v1', __name__, url_prefix='/v1')

# Register the blueprints to the v1 blueprint
v1_blueprint.register_blueprint(summarizeExtractiveController.summarize_ext_blueprint)
v1_blueprint.register_blueprint(summarizeAbstractiveController.summarize_abs_blueprint)
v1_blueprint.register_blueprint(translateController.translate_blueprint)

# Register the v1 blueprint to the app
app.register_blueprint(v1_blueprint)

@app.route("/")
def index():
    resp, status = healthz()
    return resp, status

@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
