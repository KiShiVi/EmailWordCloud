import PyQt5.QtWidgets
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtGui import QPixmap


class WordCloudWidget(QWidget):
    def __init__(self, GRAPHIC_SIZE=600):
        super(WordCloudWidget, self).__init__()

        self.setMinimumSize(GRAPHIC_SIZE, GRAPHIC_SIZE)

        self.windowSize = GRAPHIC_SIZE

        self.win = pg.PlotWidget()

        layout = PyQt5.QtWidgets.QHBoxLayout()
        layout.addWidget(self.win)

        self.img = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(r"../media/output.png"))
        self.img.scale(1, -1)
        self.win.addItem(self.img)

        self.setLayout(layout)

    def setWordCloud(self, imagePath=r"../media/output.png"):
        self.win.clear()
        self.img = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(imagePath))
        self.img.scale(1, -1)
        self.win.addItem(self.img)

    def resizeEvent(self, event):
        if self.height() > self.width():
            self.resize(self.width(), self.width())
        else:
            self.resize(self.height(), self.height())







# import PyQt5.QtWidgets
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtGui import QPixmap
#
#
# class WordCloudWidget(QtWidgets.QGraphicsScene):
#     def __init__(self, GRAPHIC_SIZE=600):
#         super(WordCloudWidget, self).__init__()
#         self.windowSize = GRAPHIC_SIZE
#         self.wordCloudView = QtWidgets.QGraphicsView(self)
#         self.wordCloudView.setMaximumSize(self.windowSize, self.windowSize)
#
#     def setWordCloud(self, imagePath=r"../media/output.png"):
#         self.clear()
#         self.addPixmap(QPixmap(imagePath).scaled(self.windowSize, self.windowSize))
