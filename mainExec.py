import sys
from PyQt6.QtWidgets import QApplication
from pageController import Controller

class ManageWindow:
    def __init__(self):
        app = QApplication(sys.argv)
        controller = Controller()
        controller.showAdinDash()
        app.exec()

manageWin = ManageWindow()