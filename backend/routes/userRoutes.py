from datetime import datetime

from flask import Blueprint, jsonify

from model.User import User
from routes.routeHelpers import get_params

user_routes = Blueprint('user', __name__)


@user_routes.route("", methods=["GET"])
def get_user():
    username = get_params(action='GetUser', param_lst=['username'])
    return User.get_item_json_response(username)


@user_routes.route("", methods=["POST"])
def create_user():
    username, email, preferred_language = get_params(action='CreateUser', param_lst=['username', 'email', 'preferred_language'])
    user = User.safe_get(username)
    if user:
        return jsonify(isError=True,
                       message="Error: User already exists",
                       statusCode=400,
                       data=user.to_json()), 400
    else:
        new_user = User(username,
                        email=email,
                        preferred_language=preferred_language,
                        languages_spoken={preferred_language},
                        account_created=datetime.utcnow())
        return new_user.save_item_json_response()


@user_routes.route("", methods=["DELETE"])
def delete_user():
    username = get_params(action='DeleteUser', param_lst=['username'])
    return User.delete_item_json_response(username)


