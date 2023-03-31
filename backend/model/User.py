from pynamodb.attributes import (
    UTCDateTimeAttribute, UnicodeAttribute, MapAttribute, UnicodeSetAttribute
)

from model.LangModel import LangModel


class User(LangModel):
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

