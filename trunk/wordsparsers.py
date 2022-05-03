import re

import multidict as multidict
from os import path
import string

conjunctionPath = r'/resources/dictionaries/conjunctions.txt'
prepositionPath = r'/resources/dictionaries/prepositions.txt'
particlePath = r'/resources/dictionaries/particles.txt'
interjectionPath = r'/resources/dictionaries/interjections.txt'
pronouncePath = r'/resources/dictionaries/pronounce.txt'

# user-defined stop words
additionalStopWordsPath = r'/stopwords.txt'
# user-defined unstopped words
additionalAddWordsPath = r'/addwords.txt'

CURRENT_DIRECTORY = path.dirname(__file__)


class ReaderDocx:
    pass


# plain/text and .txt formats
class ParserWords:
    pass


def read_from_txt(filepath: str) -> str:
    result = ""
    with open(filepath, mode='r', encoding="utf-8") as file:
        result = file.read().replace('\n', ' ').replace('\r', ' ')

    result = _remove_punctuation_marks(result)
    result = result.lower()
# Ошибку чтения файла лучше проверять на методе read # kish
    assert result != "", 'Ошибка чтения файла: ' + filepath

    return result


def get_sorted_dictionary(dict_origin: multidict, sorted_dict_size: int) -> multidict:
    list_items = dict_origin.items()

    # Hard-coded descending sort of dictionary
    list_items = sorted(list_items, key=lambda item: item[1], reverse=True)
    if sorted_dict_size < len(list_items):
        list_items = list_items[:sorted_dict_size]

    return multidict.MultiDict(list_items)


def get_dict_words_count(text: str) -> multidict:
    full_terms_dict = multidict.MultiDict()
    tmp_dict = {}

# А нужна ли нам эта кака? Мб хватит только additionalAddWordsPath? # kish
    stopwords_list = _get_stopwords_list(conjunctionPath, prepositionPath, particlePath,
                                         interjectionPath, pronouncePath, additionalStopWordsPath)

    addwords_list = _get_stopwords_list(additionalAddWordsPath)

    for word in text.split(" "):
        if word not in addwords_list:   # un-skipped words
            if word in stopwords_list:  # skipped words
                continue
# Точно ли здесь нужен match? Вроде findall есть, чтобы точно отсечть инглиш. Иначе может пройти слово кот-obormot # kish
            elif re.match(r"([A-Z])\w*|([a-z])\w*|\d+", word):   # skip english and numbers
                continue
            elif re.match(r"^[ЁёА-я]$", word):  # skip single russian word ('с', 'и')
                continue

        val = tmp_dict.get(word, 0)
        tmp_dict[word.lower()] = val + 1
# Мб есть более элегантный способ приведения обычного словаря к мультиСловарю?)0) # kish
    for key in tmp_dict:
        if len(key) > 0:  # Some strange bug with key = ''
            full_terms_dict.add(key, tmp_dict[key])

    return full_terms_dict


def _get_stopwords_list(*file_directories) -> list:
    paths = []

    for directory in file_directories:
        paths.append(CURRENT_DIRECTORY + directory)

    list_of_stop_words = []
    for filepath in paths:
        with open(filepath, encoding='utf-8') as file:
            list_of_stop_words += file.read().replace('\r', '').split('\n')

    return list_of_stop_words


def _remove_punctuation_marks(text: str) -> str:
# Зачем здесь replace? # kish
    whitespaces_without_space = string.whitespace.replace(' ', '')
    all_marks = string.punctuation + whitespaces_without_space
    # all_marks = string.punctuation
    for mark in all_marks:
        text = text.replace(mark, ' ')
    return text
