import json
import random
import time
from datetime import datetime

import spacy
from deep_translator import GoogleTranslator
from typing import List
from wonderwords import NoWordsToChoseFrom

from constants import DEFAULT_READ_CAPACITY_UNITS, DEFAULT_WRITE_CAPACITY_UNITS
from model.LangModel import LangModel
from model.Learnset import Learnset
from model.Translation import Translation
from model.User import User
from model.UserLearnsetProgress import UserLearnsetProgress
from model.UserTranslationProgress import UserTranslationProgress
from wonderwords import RandomWord, NoWordsToChoseFrom

TABLES = [Learnset, Translation, User, UserLearnsetProgress, UserTranslationProgress]
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


def create_table(table_cls: LangModel):
    if not table_cls.exists():
        table_cls.create_table(read_capacity_units=DEFAULT_READ_CAPACITY_UNITS,
                               write_capacity_units=DEFAULT_WRITE_CAPACITY_UNITS, wait=True)


def create_default_user():
    pass


def create_default_learnset():
    return Learnset(name=LEARN_SET_NAME,
                    original_translated_language=f"{ORIGINAL_TEXT_LANGUAGE}_{TRANSLATION_LANGUAGE}",
                    original_text_language=ORIGINAL_TEXT_LANGUAGE,
                    translation_language=TRANSLATION_LANGUAGE,
                    number_translations=20,
                    last_updated=datetime.utcnow(),
                    date_created=datetime.utcnow()).save()


def read_data(file_name: str, num_entries: int = 20, max_original_text_length: int = 80):
    data, i = list(), 0
    with open(file_name) as json_data:
        tmp = json.load(json_data)
        while i < min(len(data), num_entries):
            if len(tmp[i]['original_text']) <= max_original_text_length:
                data.append(tmp[i])
            i += 1
    return data


def write_default_learnset(debug=False):
    nlp = spacy.load("de_core_news_sm")
    data = read_data('groupedByTranslations.json')

    total_translations = list()
    question_num = 0
    for batch in split(data, BATCH_SIZE):
        translations = dict()
        word_choices = list()
        starting_question_num = question_num
        for item in batch:
            doc = nlp(capitalizeWords(item['original_text']))
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
        start = time.time()
        result = GoogleTranslator('en', 'de').translate(', '.join(word_choices), proxies=proxy).split(", ")
        print(time.time() - start)
        # Easy = PRON
        # Medium = NOUN

        for i, random_wrd_lst in enumerate(split(result, NUM_RANDOM_OPTIONS)):
            curr_translation = translations[starting_question_num + i]
            chosen_word = curr_translation['chosen_word']
            chosen_word_idx = random.randint(0, NUM_RANDOM_OPTIONS - 1)  # 0, 1, 2, 3
            choices = [wrd for wrd in random_wrd_lst if wrd != chosen_word][0:3]  # Extra word generated cut out
            choices.insert(chosen_word_idx, chosen_word)
            # choices = choices[:chosen_word_idx] + [chosen_word] + choices[chosen_word_idx:]
            total_translations.append(
                Translation(learn_set_name=LEARN_SET_NAME, translation_id=starting_question_num + i,
                            original_text_language=ORIGINAL_TEXT_LANGUAGE,
                            translation_language=TRANSLATION_LANGUAGE,
                            original_text=curr_translation['original_text'],
                            translation=set(curr_translation['eng_translation']),
                            choices=choices,
                            answer=chosen_word_idx))

    print(question_num, len(total_translations))
    # for item in total_translations:
    #     print(item.choices, item.original_text, item.answer)
    #     if item.choices[item.answer] not in item.original_text:
    #         print(item.choices, item.answer, item.choices[item.answer], item.original_text)
    #         exit(-1)
    # upload_translations(total_translations)


def upload_translations(translations: List[Translation]):
    with Translation.batch_write() as batch:
        for item in translations:
            batch.save(item)


def capitalizeWords(text):
    newText = ''
    for sentence in text.split('.'):
        newSentence = ''
        for word in sentence.split():
            newSentence += word + ' '
        newText += newSentence + '\n'

    return newText


def split(lst, n):
    return [lst[idx:idx + n] for idx in range(0, len(lst), n)]
