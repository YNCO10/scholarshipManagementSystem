import sys

from PyQt6.QtWidgets import QApplication
from registrationCode import Validations


app = QApplication(sys.argv)
win = Validations()
win.show()
app.exec()