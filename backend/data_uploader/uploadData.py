import json

from model.LearnSet import LearnSet
from model.Translation import Translation

new_learn_set = LearnSet()
LEARN_SET_NAME = '20 German Sentences'
ORIGINAL_TEXT_LANGUAGE = 'deu'
TRANSLATION_LANGUAGE = 'eng'
#
# if not Translation.exists():
#     Translation.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)


with open('groupedByTranslations.json') as json_data:
    to_write = json.load(json_data)[0:10]

    with Translation.batch_write() as batch:
        items = [Translation(learn_set_name=LEARN_SET_NAME, translation_id=i,
                             original_text_language=ORIGINAL_TEXT_LANGUAGE, translation_language=TRANSLATION_LANGUAGE,
                             original_text=item['original_text'],
                             translation=item['eng_translation']) for i, item in enumerate(to_write)]
        for item in items:
            batch.save(item)
