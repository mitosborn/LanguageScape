from datetime import datetime

from flask import Blueprint, request

from exceptions.request_exceptions import MissingParameterException
from model.Learnset import Learnset
from model.Translation import Translation
from model.User import User
from model.UserLearnsetProgress import UserLearnsetProgress
import json

translation_routes = Blueprint('question', __name__)


@translation_routes.route("", methods=["GET"])
def get_translation_set():
    for param in ['username', 'learnset', 'num_translations']:
        if param not in request.args:
            raise MissingParameterException(action='GetQuestion', param=param)

    username = request.args.get('username')
    requested_learnset = request.args.get('learnset')
    User.get_item(username)
    requested_num_translations = int(request.args.get('num_translations'))
    print(username)
    user_learnset_progress = UserLearnsetProgress.safe_get(requested_learnset, username)
    if not user_learnset_progress:
        print("here")
        learnset = Learnset.get_item(requested_learnset)
        learnset_num_translations = learnset.number_translations
        user_learnset_progress = UserLearnsetProgress(requested_learnset,
                                                      username,
                                                      untried_translations=set(range(learnset_num_translations)),
                                                      attempted_translations=set(), mastered_translations=set(),
                                                      number_translations=learnset_num_translations,
                                                      last_attempted=datetime.utcnow())
        user_learnset_progress.safe_save()

    untried_translations_available = len(user_learnset_progress.untried_translations)
    # if user_learnset_progress.attempted_translations:
    #     attempted_translations_available = len(user_learnset_progress.attempted_translations)
    # else:
    #     attempted_translations_available = 0
    print(requested_num_translations, untried_translations_available)
    if requested_num_translations < untried_translations_available:
        question_set = list(user_learnset_progress.untried_translations)[:requested_num_translations]
        untried_translations_available = list(user_learnset_progress.untried_translations)[requested_num_translations:]
        response = Translation.query(requested_learnset,
                                     Translation.translation_id.between(float(question_set[0]), float(
                                         question_set[-1])))
        return json.dumps([translation.attribute_values for translation in response], cls=SetEncoder)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
