from datetime import datetime

from flask import Blueprint, request

from exceptions.request_exceptions import MissingParameterException
from model.Learnset import Learnset
from model.UserLearnsetProgress import UserLearnsetProgress

question_routes = Blueprint('question', __name__)


@question_routes.route("", methods=["GET"])
def get_question_set():
    for param in ['username', 'learnset', 'num_translations']:
        if param not in request.args:
            raise MissingParameterException(action='GetQuestion', param=param)

    username = request.args.get('username')
    learnset = request.args.get('learnset')
    requested_num_translations = int(request.args.get('num_translations'))
    user_learnset_progress = UserLearnsetProgress.safe_get(learnset, UserLearnsetProgress.username.equals(username))
    if not user_learnset_progress:
        learnset = Learnset.get_item(learnset)
        learnset_num_translations = learnset.number_translations
        user_learnset_progress = UserLearnsetProgress(learnset,
                                                      username,
                                                      untried_translations=set(range(learnset_num_translations)),
                                                      attempted_translations=set(), mastered_translations=set(),
                                                      number_translations=learnset_num_translations,
                                                      last_attempted=datetime.utcnow())

    untried_translations_available = len(user_learnset_progress.untried_translations)
    attempted_translations_available = len(user_learnset_progress.attempted_translations)

    if requested_num_translations > untried_translations_available:
        question_set = list(user_learnset_progress.untried_translations)[:requested_num_translations]
        untried_translations_available = list(user_learnset_progress.untried_translations)[requested_num_translations:]






