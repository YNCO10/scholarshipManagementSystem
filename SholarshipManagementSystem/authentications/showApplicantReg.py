import sys

from PyQt6.QtWidgets import QApplication
from SholarshipManagementSystem.authentications.regApplicantValidationPHP import AppValCode


app = QApplication(sys.argv)
win = AppValCode()
win.show()
app.exec()