import PyQt5.QtWidgets
from PyQt5.QtChart import (QBarCategoryAxis, QBarSet, QChart,
                           QChartView, QValueAxis, QHorizontalBarSeries)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


class WordGraphicWidget(QWidget):
    """Класс виджета графика слов"""

    def __init__(self, GRAPHIC_SIZE=600):
        """Конструктор. Инициализация GUI

        :param GRAPHIC_SIZE: Исходный размер виджета
        """

        super(WordGraphicWidget, self).__init__()

        self.windowSize = GRAPHIC_SIZE

        self.setMinimumSize(GRAPHIC_SIZE, GRAPHIC_SIZE)
        self.layout = PyQt5.QtWidgets.QHBoxLayout()

        self.isInit = False
        self.chart_view = None

        self.setLayout(self.layout)

    def calculate(self, text):
        """Метод вычисляет новый график слов для текста и обновляет GUI

        :param text: текст
        """

        # словарь из всех слов и их кол-ва. Предполагается, что text уже отформатирован
        result_dict = {}
        for word in text.split(" "):
            if word == '':
                continue
            val = result_dict.get(word, 0)
            result_dict[word.lower()] = val + 1

        sortedWordList = []
        sortedCountWordList = []

        for i in range(10):
            maxValue = 0
            maxKey = 0
            if len(result_dict) == 0:
                break
            for j in result_dict.keys():
                if result_dict[j] > maxValue:
                    maxValue = result_dict[j]
                    maxKey = j
            if maxKey == 0:
                break
            result_dict.pop(maxKey)
            sortedWordList.append(maxKey)
            sortedCountWordList.append(maxValue)

        sortedWordList.reverse()
        sortedCountWordList.reverse()

        set0 = QBarSet("Слово")

        # Сюда добавляем частоту слова
        set0.append(sortedCountWordList)

        bar_series = QHorizontalBarSeries()
        bar_series.append(set0)

        chart = QChart()
        chart.addSeries(bar_series)
        chart.setTitle("График частот слов")

        # Сюда добавляем сами слова
        categories = sortedWordList

        axis_y = QBarCategoryAxis()
        axis_y.append(categories)
        chart.setAxisY(axis_y, bar_series)

        # Здесь не забудем поставить первое и последнее слова
        # self._axis_y.setRange("Jan", "Jun")

        axis_x = QValueAxis()
        axis_x.setTickInterval(1)
        chart.setAxisX(axis_x, bar_series)

        # Здесь не забудем поставить min() и max() кол-ва слов
        # self._axis_x.setRange(0, 20)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        if self.isInit:
            self.layout.removeWidget(self.chart_view)

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.chart_view)

        self.isInit = True

    # def resizeEvent(self, event):
    #     if self.height() > self.width():
    #         self.resize(self.width(), self.width())
    #     else:
    #         self.resize(self.height(), self.height())
