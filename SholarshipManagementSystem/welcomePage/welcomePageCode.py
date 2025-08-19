from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.welcomePage.WelcomePage import Ui_WelcomePage

class WelcomePageCode(QWidget, Ui_WelcomePage):
    def __init__(self):
        super().__init__()
        self.winReg = None
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.setupUi(self)

        # self.btnClicks()

    # def btnClicks(self):
    #     self.goToAdminRegBtn.clicked.connect(self.goToAdminReg)
    #     self.goToLoginBtn.clicked.connect(self.goToLoginPage)
    #     self.goToApplicantRegBtn.clicked.connect(self.goToApplicantReg)
    #
    #
    # def goToAdminReg(self):
    #     from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
    #     self.winReg = RegCode()
    #     self.winReg.show()
    #     self.hide()
    #
    # def goToApplicantReg(self):
    #     from SholarshipManagementSystem.authentications.regApplicantValidationPHP import AppValCode
    #     self.winApp = AppValCode()
    #     self.winApp.show()
    #     self.hide()
    #
    # def goToLoginPage(self):
    #     from SholarshipManagementSystem.authentications.loginValidationPHP import LoginCode
    #     self.winLog = LoginCode()
    #     self.winLog.show()
    #     self.hide()

    def hideWindow(self):
        self.hide()