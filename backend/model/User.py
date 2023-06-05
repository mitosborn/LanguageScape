from flask_login import UserMixin
from pynamodb.attributes import (
    UTCDateTimeAttribute, UnicodeAttribute, MapAttribute, UnicodeSetAttribute
)

from model.LangModel import LangModel


class User(LangModel, UserMixin):
    class Meta(LangModel.Meta):
        table_name = 'users'

    username = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute(null=False)
    learn_sets = MapAttribute(null=True)  # {Language: [learn_set_id]}
    account_created = UTCDateTimeAttribute(null=False)
    preferred_language = UnicodeAttribute(null=False)
    languages_spoken = UnicodeSetAttribute(null=False)
    languages_learning = UnicodeSetAttribute(null=True)
    profile_img_url = UnicodeAttribute(null=True)

    # @property
    # def is_active(self):
    #     return True
    #
    # @property
    # def is_authenticated(self):
    #     return self.is_active
    #
    @property
    def user_id(self):
        return self.username

    def get_id(self):
        try:
            return str(self.username)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, User):
            return self.get_id() == other.get_id()
        return NotImplemented
