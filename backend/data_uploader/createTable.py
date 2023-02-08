from datetime import datetime

from model.Learnset import Learnset

LEARN_SET_NAME = '20 German Sentences'
ORIGINAL_TEXT_LANGUAGE = 'deu'
TRANSLATION_LANGUAGE = 'eng'
DATE = datetime.utcnow()
if not Learnset.exists():
    Learnset.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)

new_learn_set = Learnset(original_translated_language=ORIGINAL_TEXT_LANGUAGE + '_' + TRANSLATION_LANGUAGE,
                         learn_set_name=LEARN_SET_NAME, original_text_language=ORIGINAL_TEXT_LANGUAGE,
                         translation_language=TRANSLATION_LANGUAGE, number_translations=20,
                         date_created=DATE, last_updated=DATE)
print(new_learn_set.save())

# Language mappings endpoint - website language
