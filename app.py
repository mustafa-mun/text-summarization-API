from flask import Flask, jsonify
from controllers import summarizeExtractiveController, summarizeAbstractiveController, translateController
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
}
app = Flask(__name__)
app.register_blueprint(summarizeExtractiveController.summarize_ext_blueprint)
app.register_blueprint(summarizeAbstractiveController.summarize_abs_blueprint)
app.register_blueprint(translateController.translate_blueprint)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)
summarizeExtractiveController.cache.init_app(app, config=config)
summarizeAbstractiveController.cache.init_app(app, config=config)
translateController.cache.init_app(app, config=config)


@app.route("/healthz")
def healthz():
    return "OK", 200

@app.errorhandler(Exception)
def handle_exception(error):
    # Handle the exception
    error_response = jsonify(error=str(error))
    return error_response, 500