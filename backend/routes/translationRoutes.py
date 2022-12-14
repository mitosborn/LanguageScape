from datetime import datetime

from flask import Blueprint, request

from exceptions.request_exceptions import MissingParameterException
from model.Learnset import Learnset
from model.Translation import Translation
from model.User import User
from model.UserLearnsetProgress import UserLearnsetProgress
import json

from model.UserTranslationProgress import UserTranslationProgress

translation_routes = Blueprint('question', __name__)


@translation_routes.route("", methods=["GET"])
def get_translation_set():
    for param in ['username', 'learnset', 'num_translations']:
        if param not in request.args:
            raise MissingParameterException(action='GetTranslation', param=param)

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
    num_available_translations = len(user_learnset_progress.untried_translations)
    print(requested_num_translations, num_available_translations)
    if requested_num_translations > num_available_translations:
        num_translations_found = num_available_translations
    else:
        num_translations_found = requested_num_translations

    if num_translations_found == 0:
        return list()

    question_set = list(user_learnset_progress.untried_translations)[:num_translations_found]
    response = Translation.query(requested_learnset,
                                 Translation.translation_id.between(float(question_set[0]),
                                                                    float(question_set[-1])))
    return json.dumps([translation.attribute_values for translation in response], cls=SetEncoder)


@translation_routes.route("", methods=["POST"])
def answer_question():
    for param in ['username', 'learnset', 'translation_id', 'result']:
        if param not in request.args:
            raise MissingParameterException(action='AnswerTranslation', param=param)

    username = request.args.get('username')
    translation_id = int(request.args.get('translation_id'))
    learnset = request.args.get('learnset')
    translation_result = 1 if request.args.get('result') == 'true' else 0
    User.get_item(username)
    user_translation_progress = UserTranslationProgress.safe_get(learnset + username, translation_id)
    if not user_translation_progress:
        user_translation_progress = UserTranslationProgress(learnset + username,
                                                            translation_id,
                                                            number_attempts=1,
                                                            number_correct=translation_result,
                                                            last_attempted=datetime.utcnow())
        user_translation_progress.save()
    else:
        user_translation_progress.update(
            actions=[
                UserTranslationProgress.number_attempts.add(1),
                UserTranslationProgress.number_correct.add(translation_result),
                UserTranslationProgress.last_attempted.set(datetime.utcnow())
            ]
        )

    return user_translation_progress.to_json()


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
