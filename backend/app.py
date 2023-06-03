import os
from datetime import datetime

from flask import Flask, after_this_request, jsonify, request, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
from os import environ

from flask_debugtoolbar import DebugToolbarExtension
from requests import get
from flask_cors import CORS
from exceptions.request_exceptions import MalformedRequestException, MissingParameterException, EntityNotFoundException
from model.User import User
from pynamodb.exceptions import (DeleteError, PutError)
from routes.translationRoutes import translation_routes
from routes.userRoutes import user_routes

load_dotenv()
IS_DEV = environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://localhost:3000"
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

print(client_id, client_secret)
app = Flask(__name__)
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
# app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

toolbar = DebugToolbarExtension(app)
CORS(app)

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)
print(blueprint)
app.register_blueprint(blueprint, url_prefix="/login")

app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(translation_routes, url_prefix='/translation')

print("In app.py")
questionNumber = 0
questions = [{
    "id": 1,
    "sentence": "Ich gehe in die Berliner Kirche",
    "answer": 1,
    "choices": ["ins", "in die", "auf der", "zum"]
},
    {
        "id": 2,
        "sentence": "Ich bin stärker als meine Angst",
        "answer": 1,
        "choices": ["besser", "stärker", "schwacher", "großer"]
    }]


def proxy(host, path):
    response = get(f"{host}{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return response.content, response.status_code, headers


# @app.route("/")
# def hello_world():
#     return "<body><p>Hello test, World!</p></body>"


@app.route("/question")
def get_question():
    return jsonify(questions)


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def get_app(path):
    if IS_DEV:
        return proxy(WEBPACK_DEV_SERVER_HOST, request.path)
    if 'assets' in path:
        return app.send_static_file('assets/' + path.split('/')[-1])
    return app.send_static_file(path)


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.errorhandler(MalformedRequestException)
def handle_malformed_request_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(MissingParameterException)
def handle_malformed_request_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(EntityNotFoundException)
def handle_malformed_request_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def all_exception_handler(error):
    if hasattr(error, "code"):
        return "Error: " + str(error.code)
    return str(error)

