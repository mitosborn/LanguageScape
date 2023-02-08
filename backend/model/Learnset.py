from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)
from model.LangModel import LangModel


class Learnset(LangModel):
    class Meta:
        table_name = 'learn_sets'
        region = 'us-east-1'
        write_capacity_units = 10
        read_capacity_units = 10

    original_translated_language = UnicodeAttribute(hash_key=True)
    # Add ID field; request deu_eng, ls_ID (language, learnset_id)
    learn_set_name = UnicodeAttribute(range_key=True)
    original_text_language = UnicodeAttribute()
    translation_language = UnicodeAttribute()
    number_translations = NumberAttribute()
    date_created = UTCDateTimeAttribute()
    last_updated = UTCDateTimeAttribute()
    difficulty = UnicodeAttribute(null=True)
