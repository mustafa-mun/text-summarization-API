from flask import Flask, Blueprint
from controllers import summarizeExtractiveController, summarizeAbstractiveController, translateController
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
}

app = Flask(__name__)

# Create a Blueprint for v1
v1_blueprint = Blueprint('v1', __name__, url_prefix='/v1')

# Register the blueprints to the v1 blueprint
v1_blueprint.register_blueprint(summarizeExtractiveController.summarize_ext_blueprint)
v1_blueprint.register_blueprint(summarizeAbstractiveController.summarize_abs_blueprint)
v1_blueprint.register_blueprint(translateController.translate_blueprint)

# Register the v1 blueprint to the app
app.register_blueprint(v1_blueprint)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

summarizeExtractiveController.cache.init_app(app, config=config)
summarizeAbstractiveController.cache.init_app(app, config=config)
translateController.cache.init_app(app, config=config)


@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
