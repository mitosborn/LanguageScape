from datetime import datetime

from flask import Flask, after_this_request, jsonify, request
from os import environ
from requests import get

from exceptions.request_exceptions import MalformedRequestException, MissingParameterException
from model.User import User
from pynamodb.exceptions import (DeleteError)

IS_DEV = environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://localhost:3000"

app = Flask(__name__)

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

@app.route("/user", methods=["GET", "POST", "DELETE"])
def create_user():
    if request.method == 'GET':
        if 'username' not in request.args:
            raise MissingParameterException(action='GetUser', param='username')
        username = request.args.get('username')
        try:
            user = User.get(hash_key=username)
            return jsonify(isError=True,
                           message="Found user",
                           statusCode=200,
                           data=str(user)), 200
        except User.DoesNotExist:
            return jsonify(isError=True,
                           message="User not found",
                           statusCode=200), 200
    if request.method == 'POST':
        json = request.get_json(force=True, silent=True)
        if not json:
            raise MalformedRequestException(f'CreateUser Error: JSON payload is malformed')

        try:
            for param in ['username', 'email', 'preferred_language']:
                if param not in json:
                    raise MissingParameterException(action='CreateUser', param=param)
            User.get(hash_key=json['username'])
            return jsonify(isError=True,
                           message="Error: User already exists",
                           statusCode=200,
                           data=json), 200
        except User.DoesNotExist:
            try:
                new_user = User(json['username'],
                                email=json['email'],
                                preferred_language=json['preferred_language'],
                                # learn_sets={'deu-eng': [123]},
                                languages_spoken={json['preferred_language']},
                                account_created=datetime.utcnow())
                new_user.save()
                return jsonify(isError=False,
                               message="Success",
                               statusCode=200,
                               data=new_user.to_json()), 200
            except Exception as e:
                print(e)
                return jsonify(isError=True,
                               message="Error creating user",
                               statusCode=400), 400
    if request.method == 'DELETE':
        if 'username' not in request.args:
            raise MissingParameterException(action='DeleteUser', param='username')
        username = request.args.get('username')

        try:
            User.get(hash_key=username).delete()
            return jsonify(isError=False,
                           message=f'User {username} deleted successfully',
                           statusCode=200), 200
        except DeleteError:
            return jsonify(isError=True,
                           message="Error: Error deleting user",
                           statusCode=404), 404
        except User.DoesNotExist:
            return jsonify(isError=True,
                           message="DeleteUser Error: User does not exist",
                           statusCode=404), 404


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
