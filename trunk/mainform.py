import PyQt5.QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
# from PyQt5.QtGui import QPixmap
from wordcloudwidget import WordCloudWidget
from wordgraphicwidget import WordGraphicWidget

GRAPHIC_SIZE = 600

class MainForm(QWidget):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setWindowTitle("Анализ текста")
        self.setGeometry(300, 300, 1000, 500)

        toolsLayout = QtWidgets.QVBoxLayout()
        self.comboBoxWork = QtWidgets.QComboBox()
        self.lineEditMailTag = QtWidgets.QLineEdit()

        toolsLayout.addWidget(self.comboBoxWork)
        toolsLayout.addWidget(self.lineEditMailTag)
        toolsLayout.addStretch(0)

        mainLayout = QtWidgets.QHBoxLayout()

        self.wordPlot = WordGraphicWidget(GRAPHIC_SIZE)

        self.wordCloud = WordCloudWidget(GRAPHIC_SIZE)
        # self.wordCloud.setWordCloud(r"output/output.png")
        self.wordCloud.setWordCloud(r"../media/output.png")

        mainLayout.addLayout(toolsLayout)
        mainLayout.addStretch(5)
        mainLayout.addWidget(self.wordPlot)
        mainLayout.addWidget(self.wordCloud)

        self.setLayout(mainLayout)

    def resizeEvent(self, event):
        if self.wordCloud.height() > self.wordCloud.width():
            self.wordCloud.resize(self.wordCloud.width(), self.wordCloud.width())
            self.wordPlot.resize(self.wordCloud.width(), self.wordCloud.width())
        else:
            self.wordCloud.resize(self.wordCloud.height(), self.wordCloud.height())
            self.wordPlot.resize(self.wordCloud.height(), self.wordCloud.height())


