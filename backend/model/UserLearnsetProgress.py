from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, NumberSetAttribute, UTCDateTimeAttribute
)

from model.LangModel import LangModel


class UserLearnsetProgress(LangModel):
    class Meta(LangModel.Meta):
        table_name = 'user_learnset_progress'

    username_original_translated_language = UnicodeAttribute(hash_key=True)
    learnset_name = UnicodeAttribute(range_key=True)
    untried_translations = NumberSetAttribute()
    attempted_translations = NumberSetAttribute()
    mastered_translations = NumberSetAttribute()
    number_translations = NumberAttribute()
    last_attempted = UTCDateTimeAttribute(null=True)

    def __json__(self):
        dict_obj = self.to_dict()
        if hasattr(dict_obj, "attempted_translations"):
            dict_obj["number_attempted_translations"] = len(dict_obj["attempted_translations"])
        else:
            dict_obj["number_attempted_translations"] = 0

        if hasattr(dict_obj, "mastered_translations"):
            dict_obj["number_mastered_translations"] = len(dict_obj["mastered_translations"])
        else:
            dict_obj["number_mastered_translations"] = 0

        return dict_obj
