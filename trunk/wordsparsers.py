import codecs
from os import path
import os, sys
import re

CURRENT_DIRECTORY = os.path.dirname(sys.executable)

conjunctionPath = CURRENT_DIRECTORY + r'/resources/dictionaries/conjunctions.txt'
prepositionPath = CURRENT_DIRECTORY + r'/resources/dictionaries/prepositions.txt'
particlePath = CURRENT_DIRECTORY + r'/resources/dictionaries/particles.txt'
interjectionPath = CURRENT_DIRECTORY + r'/resources/dictionaries/interjections.txt'
pronouncePath = CURRENT_DIRECTORY + r'/resources/dictionaries/pronounce.txt'
punctuationPath = CURRENT_DIRECTORY + r'/resources/dictionaries/punctuation.txt'

stopWordsPath = CURRENT_DIRECTORY + r'/resources/dictionaries/stopwords.txt'


# Требутеся добавить реализацию addWords // kish
# # user-defined unstopped words
# additionalAddWordsPath = r'/addwords.txt'


def getDictList(*paths) -> list:
    listOfStopWords = []
    for path in paths:
        file = codecs.open(path, encoding='utf-8')
        listOfStopWords += file.read().replace('\r', '').split('\n')
        file.close()
    return listOfStopWords


def processText(in_text, hasTitle: bool = True):
    setOfStopWords = set(getDictList(conjunctionPath, prepositionPath,
                                     particlePath, interjectionPath,
                                     pronouncePath, stopWordsPath))

    text = in_text.replace('\r', ' ').replace('\t', ' ')

    punctuationWords = set(getDictList(punctuationPath))
    for sign in punctuationWords:
        text = text.replace(sign, ' ')

    if hasTitle:
        resultText = ' '.join(text.split('\n')[1:]).split(' ')
    else:
        resultText = ' '.join(text.split('\n')).split(' ')

    while len(resultText) > 0 and len(re.findall(r'\S', resultText[0])) == 0:
        resultText = resultText[1:]

    if len(resultText) == 0:
        return "ошибка"



    while resultText.__contains__(''):
        resultText.remove('')

    for i in range(0, len(resultText)):
        if resultText[i].lower().replace('\r', '').replace('\n', '').replace(' ', '') in setOfStopWords:
            resultText[i] = ''
    return ' '.join([value for value in resultText if value != ''])
