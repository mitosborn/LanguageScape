from datetime import datetime

from flask import Blueprint, jsonify, request
from pynamodb.exceptions import DeleteError, PutError

from exceptions.request_exceptions import MissingParameterException, MalformedRequestException
from model.User import User

user_routes = Blueprint('user', __name__)


@user_routes.route("", methods=["GET"])
def get_user():
    if 'username' not in request.args:
        raise MissingParameterException(action='GetUser', param='username')
    username = request.args.get('username')
    return User.get_item_json_response(username)


@user_routes.route("", methods=["POST"])
def create_user():
    json = request.get_json(force=True, silent=True)
    if not json:
        raise MalformedRequestException(f'CreateUser Error: JSON payload is malformed')

    for param in ['username', 'email', 'preferred_language']:
        if param not in json:
            raise MissingParameterException(action='CreateUser', param=param)

    user = User.safe_get(json['username'])
    if user:
        return jsonify(isError=True,
                       message="Error: User already exists",
                       statusCode=400,
                       data=user.to_json()), 400
    else:
        new_user = User(json['username'],
                        email=json['email'],
                        preferred_language=json['preferred_language'],
                        languages_spoken={json['preferred_language']},
                        account_created=datetime.utcnow())
        return new_user.save_item_json_response()


@user_routes.route("", methods=["DELETE"])
def delete_user():
    if 'username' not in request.args:
        raise MissingParameterException(action='DeleteUser', param='username')
    username = request.args.get('username')
    return User.delete_item_json_response(username)
