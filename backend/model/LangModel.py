from flask import jsonify
from pynamodb.models import Model


class LangModel(Model):

    @classmethod
    def safe_get(cls, *args):
        try:
            entity = cls.get(*args)
            return entity

        except cls.DoesNotExist:
            return None

    @classmethod
    def get_item_json_response(cls, *args):
        item = cls.safe_get(*args)
        if item:
            return jsonify(isError=True,
                           message=f"Found {cls.__name__}",
                           statusCode=200,
                           data=item.to_json()), 200
        else:
            return jsonify(isError=True,
                           message=f"{cls.__name__} not found",
                           statusCode=404), 404


