import sys

from PyQt6.QtWidgets import QApplication
from SholarshipManagementSystem.welcomePage.welcomePageCode import WelcomePageCode


app = QApplication(sys.argv)
win = WelcomePageCode()
win.show()
app.exec()