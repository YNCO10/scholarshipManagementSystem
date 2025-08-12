import sys

from PyQt6.QtWidgets import QApplication
from SholarshipManagementSystem.authentications.loginValidationPHP import LoginCode

app = QApplication(sys.argv)
win = LoginCode()
win.show()
app.exec()