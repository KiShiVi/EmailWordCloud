import os
import sys
from os import path

import PyQt5.QtWidgets
import numpy as np
import pyqtgraph as pg
from PIL import Image
from PyQt5.QtWidgets import QWidget
from wordcloud import WordCloud


class WordCloudWidget(QWidget):
    """Класс виджета облака слов"""

    def __init__(self, GRAPHIC_SIZE=600):
        """Конструктор. Инициализация GUI

        :param GRAPHIC_SIZE: Изначальный размер виджета
        """

        super(WordCloudWidget, self).__init__()

        # Это не надо разкоменчивать - ожидается что и так будет подаваться отформатированный текст
        # stopwords = set(STOPWORDS)

        self.currdir = path.dirname(__file__)
        mask = np.array(Image.open(os.path.join(os.path.dirname(sys.executable),  r"resources/cloud.jpg")))
        self.wc = WordCloud(background_color="white",
                            max_words=500,
                            mask=mask,
                            # stopwords=stopwords,
                            prefer_horizontal=1,
                            width=1920,
                            height=1920,
                            scale=1
                            )

        self.setMinimumSize(GRAPHIC_SIZE, GRAPHIC_SIZE)

        self.windowSize = GRAPHIC_SIZE

        self.win = pg.PlotWidget()

        layout = PyQt5.QtWidgets.QHBoxLayout()
        layout.addWidget(self.win)

        # self.img = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(r"../media/output.png"))
        # self.img.scale(1, -1)
        # self.win.addItem(self.img)

        self.setLayout(layout)

    def setWordCloud(self, imagePath=os.path.join(os.path.dirname(sys.executable),  r"output/output.png")):
        """Метод обновляет облако слов на новое

        :param imagePath: Путь к новому облаку слов
        """

        self.win.clear()
        self.img = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(imagePath))
        self.img.scale(1, -1)
        self.win.addItem(self.img)

    def calculate(self, text):
        """ Сгенерировать новое облако слов

        :param text: Отформатированный текст
        """

        self.wc.generate(text)
        self.wc.to_file(os.path.join(os.path.dirname(sys.executable),  r"output/output.png"))

    def resizeEvent(self, event):
        if self.height() > self.width():
            self.resize(self.width(), self.width())
        else:
            self.resize(self.height(), self.height())
