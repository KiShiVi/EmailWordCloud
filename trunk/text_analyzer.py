import pymorphy2


def norm(text):
    resultList = []
    morph = pymorphy2.MorphAnalyzer()
    for word in text.split(' '):
        resultList.append(morph.parse(word)[0].normal_form)
    return ' '.join(resultList)
