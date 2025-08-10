import sys

from PyQt6.QtWidgets import QApplication
from loginCode import LoginCode

app = QApplication(sys.argv)
win = LoginCode()
win.show()
app.exec()