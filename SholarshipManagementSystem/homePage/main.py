import sys


from PyQt6.QtWidgets import QApplication
from myMainDisplay import Dash

app = QApplication(sys.argv)
win = Dash()
win.showMaximized()
app.exec()