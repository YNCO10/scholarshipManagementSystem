import sys


from PyQt6.QtWidgets import QApplication

from myDash import Dash

app = QApplication(sys.argv)
win = Dash()
win.show()
app.exec()
