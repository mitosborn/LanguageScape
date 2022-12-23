import json

from flask import jsonify

from model.Learnset import Learnset
from model.Translation import Translation
from model.UserLearnsetProgress import UserLearnsetProgress
from model.UserTranslationProgress import UserTranslationProgress
from nltk.corpus import wordnet as wn
import spacy
from spacy.lang.de.examples import sentences

LEARN_SET_NAME = '20 German Sentences'
ORIGINAL_TEXT_LANGUAGE = 'deu'
TRANSLATION_LANGUAGE = 'eng'
#
# if not Translation.exists():
#     Translation.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)
# if not Learnset.exists():
#     Learnset.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)
# if not UserTranslationProgress.exists():
#     UserTranslationProgress.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)
# if not UserLearnsetProgress.exists():
#     UserLearnsetProgress.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)


# new_learn_set = LearnSet(learn_set_name=LEARN_SET_NAME, original_text_language=ORIGINAL_TEXT_LANGUAGE,
#                          translation_language=TRANSLATION_LANGUAGE, number_translations=20)
# print(new_learn_set.save())

with open('groupedByTranslations.json') as json_data:
    to_write = json.load(json_data)[0:5]

    with Translation.batch_write() as batch:
        items = [Translation(learn_set_name=LEARN_SET_NAME, translation_id=i,
                             original_text_language=ORIGINAL_TEXT_LANGUAGE, translation_language=TRANSLATION_LANGUAGE,
                             original_text=item['original_text'],
                             translation=set(item['eng_translation'])) for i, item in enumerate(to_write)]
        items = list(set(items))

        # for item in items:
        #     batch.save(item)

# print(Learnset.get_item(LEARN_SET_NAME))
# print(Learnset.get_item_json_response(LEARN_SET_NAME, item_name='LearnSet'))

print([item.original_text for item in items])


nlp = spacy.load("de_core_news_sm")
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)