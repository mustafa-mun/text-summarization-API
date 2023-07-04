from flask import Flask
from controllers import summarizeExtractiveController, summarizeAbstractiveController, translateController

app = Flask(__name__)
app.register_blueprint(summarizeExtractiveController.summarize_ext_blueprint)
app.register_blueprint(summarizeAbstractiveController.summarize_abs_blueprint)
app.register_blueprint(translateController.translate_blueprint)

@app.route("/")
def index():
    resp, status = healthz()
    return resp, status

@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == '__main__': app.run(host='0.0.0.0')
