import PyQt5.QtWidgets
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class WordGraphicWidget(QWidget):
    def __init__(self, GRAPHIC_SIZE=600):
        super(WordGraphicWidget, self).__init__()
        self.windowSize = GRAPHIC_SIZE

        self.setMinimumSize(GRAPHIC_SIZE, GRAPHIC_SIZE)

        self.win = pg.GraphicsWindow()

        layout = PyQt5.QtWidgets.QHBoxLayout()
        layout.addWidget(self.win)

        x = [1, 2, 3, 4, 5, 6, 7]
        y = [1, 0.2, 3, 45, 5, 6]

        plot1 = self.win.addPlot()
        plot1.plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))

        self.setLayout(layout)


    def setWordCloud(self, imagePath=r"../media/output.png"):
        self.clear()
        self.addPixmap(QPixmap(imagePath).scaled(self.windowSize, self.windowSize))

    def resizeEvent(self, event):
        if self.height() > self.width():
            self.resize(self.width(), self.width())
        else:
            self.resize(self.height(), self.height())
