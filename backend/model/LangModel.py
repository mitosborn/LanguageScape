from flask import jsonify
from pynamodb.exceptions import DeleteError, PutError
from pynamodb.models import Model

from exceptions.request_exceptions import EntityNotFoundException


class LangModel(Model):

    @classmethod
    def safe_get(cls, *args):
        try:
            print(args)
            entity = cls.get(*args)
            return entity

        except cls.DoesNotExist:
            return None

    @classmethod
    def get_item(cls, *args):
        entity = cls.safe_get(*args)
        if entity:
            return entity
        raise EntityNotFoundException(cls.__name__)

    @classmethod
    def get_item_json_response(cls, *args):
        item = cls.safe_get(*args)
        if item:
            return jsonify(isError=False,
                           message=f"Found {cls.__name__}",
                           statusCode=200,
                           data=item.to_json()), 200
        else:
            return jsonify(isError=True,
                           message=f"{cls.__name__} not found",
                           statusCode=404), 404

    @classmethod
    def safe_delete(cls, *args):
        try:
            item = cls.safe_get(*args)
            if item:
                item.delete()
                return 1
            else:
                return 0
        except DeleteError:
            return -1

    @classmethod
    def delete_item_json_response(cls, *args):
        code = cls.safe_delete(*args)
        if code == 1:
            return jsonify(isError=False,
                           message=f'{cls.__name__} deleted successfully',
                           statusCode=200), 200
        elif code == 0:
            return jsonify(isError=True,
                           message=f"Error: {cls.__name__} does not exist",
                           statusCode=404), 404
        else:
            return jsonify(isError=True,
                           message=f"Error deleting {cls.__name__}",
                           statusCode=404), 404

    def safe_save(self, condition=None):
        try:
            self.save(condition)
            return True
        except PutError:
            return False

    def save_item_json_response(self, condition=None):
        if self.safe_save(condition):
            return jsonify(isError=False,
                           message="Success",
                           statusCode=200,
                           data=self.to_json()), 200
        else:
            return jsonify(isError=True,
                           message=f"Error saving {self.__class__.__name__}: {self.to_json()}",
                           statusCode=400), 400
