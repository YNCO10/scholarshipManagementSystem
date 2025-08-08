import sys

from PyQt6.QtWidgets import QApplication
from registrationCode import SignUpPage

app = QApplication(sys.argv)
win = SignUpPage()
win.show()
app.exec()