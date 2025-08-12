import sys

from PyQt6.QtWidgets import QApplication
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode


app = QApplication(sys.argv)
win = RegCode()
win.show()
app.exec()