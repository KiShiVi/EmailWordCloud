from os import path
from PyQt5.QtWidgets import QApplication
from mainform import MainForm
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())

