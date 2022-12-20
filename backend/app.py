from datetime import datetime

from flask import Flask, after_this_request, jsonify, request
from os import environ
from requests import get

from exceptions.request_exceptions import MalformedRequestException, MissingParameterException, EntityNotFoundException
from model.User import User
from pynamodb.exceptions import (DeleteError)

from routes.userRoutes import user_routes

IS_DEV = environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://localhost:3000"

app = Flask(__name__)
app.register_blueprint(user_routes, url_prefix='/user')

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
#     return "<p>Hello test, World!</p>"


@app.route("/question")
def get_question():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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
