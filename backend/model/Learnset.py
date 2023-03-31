from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)
from model.LangModel import LangModel


class Learnset(LangModel):
    class Meta(LangModel.Meta):
        table_name = 'learnsets'

    original_translated_language = UnicodeAttribute(hash_key=True)
    # Add ID field; request deu_eng, ls_ID (language, learnset_id)
    name = UnicodeAttribute(range_key=True)
    original_text_language = UnicodeAttribute()
    translation_language = UnicodeAttribute()
    number_translations = NumberAttribute()
    date_created = UTCDateTimeAttribute()
    last_updated = UTCDateTimeAttribute()
    difficulty = UnicodeAttribute(null=True)
