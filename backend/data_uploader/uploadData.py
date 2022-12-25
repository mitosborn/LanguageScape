import json
import time

from flask import jsonify

from model.Learnset import Learnset
from model.Translation import Translation
from model.UserLearnsetProgress import UserLearnsetProgress
from model.UserTranslationProgress import UserTranslationProgress
from nltk.corpus import wordnet as wn
import spacy
from wonderwords import RandomWord, NoWordsToChoseFrom
import random
from deep_translator import GoogleTranslator

w = RandomWord()
LEARN_SET_NAME = '20 German Sentences'
ORIGINAL_TEXT_LANGUAGE = 'deu'
TRANSLATION_LANGUAGE = 'eng'
NUM_RANDOM_OPTIONS = 4
BATCH_SIZE = 50
pos_map = {'NOUN': 'nouns', 'VERB': 'verbs', 'ADJ': 'adjectives'}  # 'ADV': 'adverbs', 'AUX': ''}
allowed_pos = {'NOUN', 'VERB', 'ADJ'}

# Translation.delete_table()
# quit(-1)
if not Translation.exists():
    Translation.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)
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


def split(lst, n):
    return [lst[idx:idx + n] for idx in range(0, len(lst), n)]


nlp = spacy.load("de_core_news_sm")
with open('groupedByTranslations.json') as json_data:
    data = list()
    tmp = json.load(json_data)
    i = 0
    while len(data) < 20:
        if len(tmp[i]['original_text']) <= 80:
            data.append(tmp[i])
        i += 1
    # data = [t for t in json.load(json_data)[0:200] if len(t['original_text']) <= 80]
    to_write = split(data, BATCH_SIZE)
    total_translations = list()
    question_num = 0
    for batch in to_write:
        translations = dict()
        word_choices = list()
        starting_question_num = question_num
        for item in batch:
            doc = nlp(capitalizeWords(item['original_text']))
            tokens = list()
            pos = list()
            for j, token in enumerate(doc):
                if token.pos_ in allowed_pos and token.text != '%':
                    tokens.append(token)
                pos.append((j, token.text, token.pos_, token.dep_))

            word_to_token = {t.text: t for t in tokens}
            for ee in doc.ents:
                if ee.label_ == 'PER' and ee.text in word_to_token.keys():
                    word_to_token.pop(ee.text)
            print(list(word_to_token.keys()), pos)
            print([ee.label_ for ee in doc.ents])
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

        print(spacy.explain('oc'))
        proxy = {
            "https": "205.185.126.246"
        }
        ## len <= 80
        start = time.time()
        result = GoogleTranslator('en', 'de').translate(', '.join(word_choices), proxies=proxy).split(", ")
        print(time.time() - start)
        # Easy = PRON
        # Medium = NOUN

        for i, random_wrd_lst in enumerate(split(result, NUM_RANDOM_OPTIONS)):
            curr_translation = translations[starting_question_num + i]
            chosen_word = curr_translation['chosen_word']
            chosen_word_idx = random.randint(0, NUM_RANDOM_OPTIONS - 1)
            choices = [wrd for wrd in random_wrd_lst if wrd != chosen_word][0:3]
            choices = choices[:chosen_word_idx] + [chosen_word] + choices[chosen_word_idx:]
            total_translations.append(
                Translation(learn_set_name=LEARN_SET_NAME, translation_id=starting_question_num + i,
                            original_text_language=ORIGINAL_TEXT_LANGUAGE, translation_language=TRANSLATION_LANGUAGE,
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

with Translation.batch_write() as batch:
    for item in total_translations:
        batch.save(item)
