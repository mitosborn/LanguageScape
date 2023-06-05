import json
import random
import time
from datetime import datetime
import logging
import spacy
from deep_translator import GoogleTranslator
from typing import List

from constants import DEFAULT_READ_CAPACITY_UNITS, DEFAULT_WRITE_CAPACITY_UNITS
from exceptions.model_exceptions import InvalidTranslationException
from model.DynamoDBOAuthStorage import OAuth
from model.LangModel import LangModel
from model.Learnset import Learnset
from model.Translation import Translation
from model.User import User
from model.UserLearnsetProgress import UserLearnsetProgress
from model.UserTranslationProgress import UserTranslationProgress
from wonderwords import RandomWord, NoWordsToChoseFrom

TABLES: List[LangModel] = [Learnset, Translation, User, UserLearnsetProgress, UserTranslationProgress, OAuth]
LEARN_SET_NAME = '20 German Sentences'
ORIGINAL_TEXT_LANGUAGE = 'deu'
TRANSLATION_LANGUAGE = 'eng'
DATE = datetime.utcnow()
proxy = {
    "https": "205.185.126.246"
}
w = RandomWord()
NUM_RANDOM_OPTIONS = 4
BATCH_SIZE = 50
pos_map = {'NOUN': 'nouns', 'VERB': 'verbs', 'ADJ': 'adjectives'}  # 'ADV': 'adverbs', 'AUX': ''}
allowed_pos = {'NOUN', 'VERB', 'ADJ'}
logging.getLogger().setLevel(logging.INFO)


def create_table(table_cls: LangModel):
    if not table_cls.exists():
        table_cls.create_table(read_capacity_units=DEFAULT_READ_CAPACITY_UNITS,
                               write_capacity_units=DEFAULT_WRITE_CAPACITY_UNITS, wait=True)


def create_default_user():
    default_user = {"email": "mbo2@rice.edu", "username": "liebe", "preferred_language": "eng"}
    print("Within create_default_user()")
    if not User.entry_exists(default_user['username']):
        print("User does not exist")
        logging.info("Creating default user")
        # User(default_user['username'],
        #      email=default_user['email'],
        #      preferred_language=default_user['preferred_language'],
        #      languages_spoken={default_user['preferred_language']},
        #      account_created=datetime.utcnow()).safe_save()
    else:
        print("User exists")
        logging.info("Default user exists")


def create_default_learnset():
    return Learnset(name=LEARN_SET_NAME,
                    original_translated_language=f"{ORIGINAL_TEXT_LANGUAGE}_{TRANSLATION_LANGUAGE}",
                    original_text_language=ORIGINAL_TEXT_LANGUAGE,
                    translation_language=TRANSLATION_LANGUAGE,
                    number_translations=20,
                    last_updated=datetime.utcnow(),
                    date_created=datetime.utcnow()).save()


def read_data(file_name: str, num_entries: int = 20, max_original_text_length: int = 80):
    data = list()
    with open(file_name) as json_data:
        tmp = json.load(json_data)
        for i, translation_json in enumerate(tmp):
            if len(translation_json['original_text']) <= max_original_text_length:
                data.append(tmp[i])
            if len(data) == num_entries:
                break

    return data


def create_default_learnset_translations(spacy_model, data_file_name, debug=False):
    nlp = spacy.load(spacy_model)
    data = read_data(data_file_name)
    total_translations = list()
    question_num = 0
    for batch in split(data, BATCH_SIZE):
        translations = dict()
        word_choices = list()
        starting_question_num = question_num
        for item in batch:
            doc = nlp(capitalize_words(item['original_text']))
            tokens = list()
            for j, token in enumerate(doc):
                if token.pos_ in allowed_pos and token.text != '%':
                    tokens.append(token)
                if debug:
                    print((j, token.text, token.pos_, token.dep_))

            word_to_token = {t.text: t for t in tokens}
            for ee in doc.ents:
                if ee.label_ == 'PER' and ee.text in word_to_token.keys():
                    word_to_token.pop(ee.text)

            if debug:
                print(f"Compatible tokens found: {str(list(word_to_token.keys()))}")
                print(f"Entities in document: {str([ee.label_ for ee in doc.ents])}")

            # Generate synonyms
            if len(list(word_to_token.keys())) > 0:
                chosen_word = random.choice(list(word_to_token.keys()))
                part_of_speech = word_to_token[chosen_word].pos_
                try:
                    random_words = w.random_words(NUM_RANDOM_OPTIONS, include_categories=[pos_map[part_of_speech]])
                    word_choices.extend(random_words)
                    translations[question_num] = item
                    translations[question_num]['chosen_word'] = chosen_word
                    question_num += 1
                except NoWordsToChoseFrom:
                    print("Returned fewer than expected random words")
            else:
                print(f"No compatible tokens found within text: {item['original_text']}")
                continue

        print(spacy.explain('oc'))

        ## len <= 80
        if debug:
            print(translations)
        start = time.time()
        result = GoogleTranslator('en', 'de').translate(', '.join(word_choices), proxies=proxy).split(", ")
        print(time.time() - start)
        # Easy = PRON
        # Medium = NOUN

        for i, random_wrd_lst in enumerate(split(result, NUM_RANDOM_OPTIONS)):
            translation_id = starting_question_num + i
            total_translations.append(create_translation(translations[starting_question_num + i], random_wrd_lst,
                                                         translation_id))

    print(question_num, len(total_translations))
    validate_translations(total_translations)
    print(list(map(lambda x: x.to_dict(), total_translations)))
    return total_translations


def create_translation(translation_dict, random_wrd_lst, translation_id):
    chosen_word = translation_dict['chosen_word']
    chosen_word_idx = random.randint(0, NUM_RANDOM_OPTIONS - 1)  # 0, 1, 2, 3
    choices = [wrd for wrd in random_wrd_lst if wrd != chosen_word][0:3]  # Extra word generated cut out
    choices.insert(chosen_word_idx, chosen_word)
    # choices = choices[:chosen_word_idx] + [chosen_word] + choices[chosen_word_idx:]
    return Translation(learn_set_name=LEARN_SET_NAME, translation_id=translation_id,
                       original_text_language=ORIGINAL_TEXT_LANGUAGE,
                       translation_language=TRANSLATION_LANGUAGE,
                       original_text=translation_dict['original_text'],
                       translation=set(translation_dict['eng_translation']),
                       choices=choices,
                       answer=chosen_word_idx)


def validate_translations(translations: List[Translation]):
    for translation in translations:
        validate_translation(translation)


def validate_translation(translation: Translation):
    if translation.choices[translation.answer] not in translation.original_text:
        raise InvalidTranslationException(translation)


def upload_translations(translations_to_upload: List[Translation]):
    with Translation.batch_write() as batch:
        for item in translations_to_upload:
            batch.save(item)


def capitalize_words(text):
    newText = ''
    for sentence in text.split('.'):
        newSentence = ''
        for word in sentence.split():
            newSentence += word + ' '
        newText += newSentence + '\n'

    return newText


def split(lst, n):
    return [lst[idx:idx + n] for idx in range(0, len(lst), n)]


def create_tables():
    for table_cls in TABLES:
        create_table(table_cls)
        if not table_cls.exists():
            print("Could not create DDB Table: " + table_cls.Meta.__name__)
        else:
            print("DDB Table: " + table_cls.__name__ + " exists")


create_tables()
# create_default_user()
# create_default_learnset()
# translations = create_default_learnset_translations(spacy_model="de_core_news_sm",
#                                                     data_file_name="groupedByTranslations.json", debug=False)
# upload_translations(translations) A comment
