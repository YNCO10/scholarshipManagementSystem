from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
import requests
import json

from SholarshipManagementSystem.authentications.verifyEmailPage import Ui_VerifyEmail
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode



class VerificationCode(QWidget, Ui_VerifyEmail):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verify Email")
        self.setupUi(self)
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.regCode = RegCode()

        self.btnClicks()

########################################################################################################################
    def btnClicks(self):
        self.pushButton_2.clicked.connect(self.verify)

########################################################################################################################
    def verify(self):
        if self.codeTxt.text() == "":
            self.regCode.msgBox(
                "Blank Fields",
                "FIll in all empty"
            )
            return
        url = "http://localhost/BackEnd/scholarshipManagement/authentications/verify.php"
        try:
            response = requests.post(
                url,
                data={
                    "token": self.codeTxt.text().strip()
                }
            )
            print(f"RAW RESPONSE: {response.text}")
            result = json.loads(response.text)
            msg = result.get("message", "Unknown Error.")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Email Verified",
                    f"{msg}"
                )
                print("Email Verified")
                self.goToLogin()

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Verification Failed",
                    f"{msg}"
                )


        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception Error: {e}"
            )
            print(f"Exception Error: {e}")

########################################################################################################################
    def hideWindow(self):
        self.hide()

########################################################################################################################
    def goToLogin(self):
        from pageController import Controller
        self.controller = Controller()
        self.controller.showLogin()
        self.hideWindow()