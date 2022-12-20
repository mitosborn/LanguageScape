from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, NumberSetAttribute, UTCDateTimeAttribute
)

from model.LangModel import LangModel


class UserLearnsetProgress(LangModel):
    class Meta:
        table_name = 'user_learnset_progress'
        region = 'us-east-1'
        write_capacity_units = 10
        read_capacity_units = 10

    learnset_name = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute(range_key=True)
    untried_questions = NumberSetAttribute()
    attempted_questions = NumberSetAttribute()
    mastered_questions = NumberSetAttribute()
    number_questions = NumberAttribute()
    last_attempted = UTCDateTimeAttribute(null=True)
