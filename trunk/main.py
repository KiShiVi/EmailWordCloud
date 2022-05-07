import sys

from PyQt5.QtWidgets import QApplication

from mainform import MainForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())

