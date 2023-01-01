from pynamodb.attributes import (
    UTCDateTimeAttribute, UnicodeAttribute, NumberAttribute
)

from model.LangModel import LangModel


class UserTranslationProgress(LangModel):
    class Meta:
        table_name = 'user_translation_progress'
        region = 'us-east-1'
        write_capacity_units = 10
        read_capacity_units = 10

    learn_set_username = UnicodeAttribute(hash_key=True)
    translation_id = NumberAttribute(range_key=True)
    number_attempts = NumberAttribute()
    number_correct = NumberAttribute()
    last_attempted = UTCDateTimeAttribute(null=True)
