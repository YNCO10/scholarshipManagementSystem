import sys
from PyQt6.QtWidgets import QApplication
from pageController import Controller

app = QApplication(sys.argv)
controller = Controller()
controller.showLogin()
app.exec()
