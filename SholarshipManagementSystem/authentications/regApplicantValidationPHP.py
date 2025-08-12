from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox, QLineEdit, QApplication
import requests
import json
from SholarshipManagementSystem.authentications.applicantReg import Ui_applicantRegistration
from regValidationPHP import RegCode



class AppValCode(QWidget, Ui_applicantRegistration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("REGISTER")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.regCode = RegCode()


        #initialise errorMsgTxt
        self.errorMsgLog.setText("")


        #values for educationLevelComboBox

        self.educationLevels = [
            "No formal education",
            "Secondary School",
            "Diploma",
            "Bachelor's Degree",
            "Master's Degree",
            "Doctorate (PhD)"
        ]
        #add education levels
        self.educationCombo.addItems(self.educationLevels)

        self.btnClicks()

    def btnClicks(self):
        self.showHidePassBtn.clicked.connect(
            lambda : self.regCode.togglePassword(
                self.passTxt,
                self.showHidePassBtn
            )
        )

        self.showHideConfirmPassBtn.clicked.connect(
            lambda : self.regCode.togglePassword(
                self.confirmPassTxt,
                self.showHideConfirmPassBtn
            )
        )

    def goTologinPage(self):
        pass #CONVERT A LOGIN PAGE FROM LOGIN.UI AND NAME IT APPLICANT_LOGIN
        # from loginValidationPHP import LoginCode
        # self.win = LoginCode()
        # self.hide()
        # self.win.show()

