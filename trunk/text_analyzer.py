"""Сейчас файл не используется. Но нужно реализовать морфологический анализ текста,
поэтому пока не удалял. Мб тебе пригодится"""


import pymorphy2


# Singleton
class TextAnalyzer(object):
    instance = None

    def __new__(cls, integer):
        if cls.instance is None:
            cls.instance = super(TextAnalyzer, cls).__new__(cls)
            cls.integer = 0
        return cls.instance

    def __init__(self, integer):
        self.integer = integer

    def print(self):
        print("Instance: " + str(self.instance))
        print("Value in: " + str(self.integer))
