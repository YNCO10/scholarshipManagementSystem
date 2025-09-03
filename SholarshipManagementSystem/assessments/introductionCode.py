from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.assessments.introductionPage import Ui_introduction


class introCode(QWidget, Ui_introduction):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.setWindowTitle("INTRODUCTION")
        self.controller = None

        self.btnClicks()

    def btnClicks(self):
        self.beginBtn.clicked.connect(self.goToNumerical)


    def goToNumerical(self):
        try:
            from pageController import Controller
            self.controller = Controller()
            self.controller.showNumReasoning()
            self.hide()
        except Exception as e:
            print(f"Exception Error: {e}")