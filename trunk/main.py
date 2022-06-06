# Инфа для будущей сборки
# pyinstaller --onedir --windowed -i "D:\PythonProjects\EmailWordCloud\icon.ico" -n "WordCloud" trunk/main.py
# + output + resources + wordcloud + pymorphy2(all) + icon TO DIST

import sys

from PyQt5.QtWidgets import QApplication

from mainform import MainForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())

