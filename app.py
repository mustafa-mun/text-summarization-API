from flask import Flask, Blueprint
from controllers import summarizeExtractiveController, summarizeAbstractiveController, translateController

app = Flask(__name__)

@app.route("/")
def index():
    resp, status = healthz()
    return resp, status

@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
