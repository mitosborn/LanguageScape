from pynamodb.attributes import (
    UTCDateTimeAttribute, UnicodeAttribute, NumberAttribute
)

from model.LangModel import LangModel


class UserTranslationProgress(LangModel):
    class Meta(LangModel.Meta):
        table_name = 'user_translation_progress'

    learn_set_username = UnicodeAttribute(hash_key=True)
    translation_id = NumberAttribute(range_key=True)
    number_attempts = NumberAttribute()
    number_correct = NumberAttribute()
    last_attempted = UTCDateTimeAttribute(null=True)
