import PyQt5.QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from wordcloudwidget import WordCloudWidget
from wordgraphicwidget import WordGraphicWidget
from emailhandler import EmailHandler

GRAPHIC_SIZE = 400


class MainForm(QWidget):
    """Основной класс приложения. Основная форма"""

    def __init__(self):

        """Конструктор. Инициализация GUI"""
        super(MainForm, self).__init__()

        self.emailHandler = EmailHandler(username="login", ext_password="pass")

        self.listOfMessages = []

        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setText('По данному тегу сообщений не найдено!')

        self.setWindowTitle("Анализ текста")
        self.setGeometry(300, 300, 1000, 500)

        toolsLayout = QtWidgets.QVBoxLayout()
        self.comboBoxWork = QtWidgets.QComboBox()

        self.comboBoxWork.currentIndexChanged.connect(self.onCurrentIndexChanged)

        self.lineEditMailTag = QtWidgets.QLineEdit()

        self.lineEditMailTag.textChanged.connect(self.onTagTextEdit)

        toolsLayout.addWidget(self.comboBoxWork)
        toolsLayout.addWidget(self.lineEditMailTag)

        self.comboBoxWork.setMinimumWidth(300)

        self.btnSearchMail = PyQt5.QtWidgets.QPushButton()
        self.btnSearchMail.setText("Найти")
        self.btnSearchMail.clicked.connect(self.onSearchButtonClicked)
        self.btnSearchMail.setEnabled(False)

        toolsLayout.addWidget(self.btnSearchMail)

        self.textEditor = QtWidgets.QTextEdit()
        toolsLayout.addWidget(self.textEditor)

        self.btnAnalysisCurText = QtWidgets.QPushButton()
        self.btnAnalysisCurText.setText("Анализ")
        self.btnAnalysisCurText.clicked.connect(self.onAnalysisCurTextButtonClicked)

        toolsLayout.addWidget(self.btnAnalysisCurText)

        toolsLayout.addStretch(0)

        mainLayout = QtWidgets.QHBoxLayout()

        self.wordPlotGB = QtWidgets.QGroupBox("График")
        wordPlotLO = QtWidgets.QGridLayout()
        self.wordPlot = WordGraphicWidget(GRAPHIC_SIZE)
        wordPlotLO.addWidget(self.wordPlot, 0, 0)
        self.wordPlotGB.setLayout(wordPlotLO)

        self.wordCloudGB = QtWidgets.QGroupBox("Облако")
        wordCloudLO = QtWidgets.QGridLayout()
        self.wordCloud = WordCloudWidget(GRAPHIC_SIZE)
        wordCloudLO.addWidget(self.wordCloud, 0, 0)
        self.wordCloudGB.setLayout(wordCloudLO)

        # self.wordCloud.setWordCloud(r"output/output.png")
        # self.wordCloud.setWordCloud(r"../media/output.png")

        mainLayout.addLayout(toolsLayout)
        # mainLayout.addStretch(5)
        mainLayout.addWidget(self.wordPlotGB)
        mainLayout.addSpacing(50)
        mainLayout.addWidget(self.wordCloudGB)

        self.setLayout(mainLayout)

    ##!< Здесь текст студента с уже отпаршенной фамилией и номером группы. Т.е. уже тупо чистый текст для анализа
    def calculate(self, text):
        """Анализ заданного текста. Автоматически обновляет график, облако слов и текст в TextEditor'e

        :param text: ИСХОДНЫЙ текст
        """

        # Здесь твой выход, Димас. Прогоняем текст через анализатор и ставим все слова в начальную форму.
        # Удаляем все стоп-слова.
        # Мечтаю получить на выходе текст (str). Если у тебя на выходе получается список [],
        # то просто сделай .join и дай мне текст <3
        #
        # goodText = textProcessing( text )
        self.wordCloud.calculate(text)
        self.wordCloud.setWordCloud()
        self.wordPlot.calculate(text)

        self.textEditor.clear()
        self.textEditor.setText(text)

    def onSearchButtonClicked(self):
        """Реакция на нажатие кнопки 'Найти'"""

        self.listOfMessages = self.emailHandler.get_messages(self.lineEditMailTag.text())

        if self.listOfMessages is None:
            self.error_dialog.show()
            return

        self.comboBoxWork.clear()
        for work in self.listOfMessages:
            self.comboBoxWork.addItem(work.split('\n')[0])

        self.calculate(self.listOfMessages[0])

    def onAnalysisCurTextButtonClicked(self):
        """Реакция на нажатие кнопки Анализ"""

        self.calculate(self.textEditor.toPlainText())

    def onTagTextEdit(self):
        """Реакция на изменение поля для ввода тега"""

        if len(self.lineEditMailTag.text()) == 0:
            self.btnSearchMail.setEnabled(False)
        else:
            self.btnSearchMail.setEnabled(True)

    def onCurrentIndexChanged(self):
        """Реакция на изменение выбранного письма в ComboBox"""

        self.calculate(self.listOfMessages[self.comboBoxWork.currentIndex()])

    def closeEvent(self, a0: PyQt5.QtGui.QCloseEvent) -> None:
        print("Bye!")
        self.emailHandler.close()

    # def resizeEvent(self, event):
    #     if self.wordCloudGB.height() > self.wordCloudGB.width():
    #         self.wordCloudGB.resize(self.wordCloudGB.width(), self.wordCloudGB.width())
    #         self.wordPlotGB.resize(self.wordCloudGB.width(), self.wordCloudGB.width())
    #     else:
    #         self.wordCloudGB.resize(self.wordCloudGB.height(), self.wordCloudGB.height())
    #         self.wordPlotGB.resize(self.wordCloudGB.height(), self.wordCloudGB.height())