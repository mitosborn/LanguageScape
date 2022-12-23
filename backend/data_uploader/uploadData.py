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


def capitalizeWords(text):
    newText = ''

    for sentence in text.split('.'):
        newSentence = ''
        for word in sentence.split():
            newSentence += word + ' '
        newText += newSentence + '\n'

    return newText


with open('groupedByTranslations.json') as json_data:
    to_write = json.load(json_data)[0:25]

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


nlp = spacy.load("de_core_news_sm")
for item in items:
    if len(item.original_text) <= 80:
        doc = nlp(capitalizeWords(item.original_text))
        tokens = list()
        pos = list()
        for i, token in enumerate(doc):
            if (token.pos_ == 'NOUN' or token.pos_ == 'VERB' or token.pos_ == 'ADV' or token.pos_ == 'AUX'
                or token.pos_ == 'PRON') \
                    and token.text != '%':
                tokens.append(token.text)
            pos.append((i, token.text, token.pos_, token.dep_))
        for ee in doc.ents:
            if ee.label_ == 'PER' and ee.text in tokens:
                tokens.remove(ee.text)
        print(tokens, pos)
        print([ee.label_ for ee in doc.ents])

# AUX, NOUN, PRON, VERB, ADV

print(spacy.explain('oc'))

## len <= 80

# Easy = PRON
# Medium = NOUN
