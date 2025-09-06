import sys
from PyQt6.QtWidgets import QApplication
from pageController import Controller

class ManageWindow:
    def __init__(self):
        app = QApplication(sys.argv)
        controller = Controller()
        controller.showIntroPage()
        app.exec()

manageWin = ManageWindow()