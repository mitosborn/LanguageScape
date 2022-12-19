from pynamodb.models import Model
from pynamodb.attributes import (
    UTCDateTimeAttribute, UnicodeAttribute, MapAttribute, UnicodeSetAttribute, NumberAttribute
)


class Translation(Model):
    class Meta:
        table_name = 'translations'
        region = 'us-east-1'
        write_capacity_units = 10
        read_capacity_units = 10

    learn_set_name = UnicodeAttribute(hash_key=True)
    translation_id = NumberAttribute(range_key=True)
    original_text_language = UnicodeAttribute()
    translation_language = UnicodeAttribute()
    original_text = UnicodeAttribute()
    translation = UnicodeSetAttribute()
    difficulty = UnicodeAttribute(null=True)
