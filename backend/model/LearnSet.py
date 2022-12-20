from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute
)
from model.LangModel import LangModel


class LearnSet(LangModel):
    class Meta:
        table_name = 'learn_sets'
        region = 'us-east-1'
        write_capacity_units = 10
        read_capacity_units = 10

    learn_set_name = UnicodeAttribute(hash_key=True)
    original_text_language = UnicodeAttribute()
    translation_language = UnicodeAttribute()
    number_translations = NumberAttribute()
    difficulty = UnicodeAttribute(null=True)
