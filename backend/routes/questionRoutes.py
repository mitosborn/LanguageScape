from datetime import datetime

from flask import Blueprint, jsonify, request
from pynamodb.exceptions import DeleteError

from exceptions.request_exceptions import MissingParameterException, MalformedRequestException
from model import UserLearnsetProgress
from model.User import User

question_routes = Blueprint('question', __name__)


@question_routes.route("", methods=["GET"])
def get_question_set():
    for param in ['username', 'learnset', 'num_questions']:
        if param not in request.args:
            raise MissingParameterException(action='GetQuestion', param=param)

    username = request.args.get('username')
    learnset = request.args.get('learnset')
    num_questions = request.args.get('num_questions')

    user_learnset_progress = UserLearnsetProgress.get_item([learnset, UserLearnsetProgress.username.equals(username)])

