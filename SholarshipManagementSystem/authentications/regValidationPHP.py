import re
import sys


from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox, QLineEdit, QApplication
import requests
import json
from SholarshipManagementSystem.authentications.adminReg import Ui_adminRegistrationPage



class RegCode(QWidget, Ui_adminRegistrationPage):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.setupUi(self)

        self.url = "http://localhost/BackEnd/scholarshipManagement/authentications/regValidation.php"

        self.errorMsgLabelReg.setText("")
        self.btnClicks()

    def btnClicks(self):
        #signUp
        self.signUpBtn.clicked.connect(self.register)

        #showHide pass
        self.showHidePassBtn.clicked.connect(
            lambda : self.togglePassword(
                self.passTxt,
                self.showHidePassBtn
            )
        )
        self.showHideConfirmPassBtn.clicked.connect(
        lambda : self.togglePassword(
            self.confirmPassTxt,
            self.showHideConfirmPassBtn
        ))

         # switch pages
        self.goToLoginPageBtn.clicked.connect(self.goTologinPage)

    def register(self):
        if self.nameTxt.text() == "" or self.passTxt.text() == "" or self.emailTxt.text() == "" or self.confirmPassTxt.text() == "":
            self.msgBox("Blank Fields", "Please fill in all blank fields.")
            return

        if not self.validateEmailField(self.emailTxt.text().strip()):
            self.errorMsgLabelReg.setText("Please enter valid Email")
            return

        if self.passTxt.text().strip() != self.confirmPassTxt.text().strip():
            self.msgBox("Password Mismatch", "The passwords do not match.")
            return

        #     validate password field
        if not self.validatePassField(self.passTxt.text().strip()):
            self.errorMsgLabelReg.setText("Password must be 8 characters long\nMust have at least one number\nAt least one symbol")
            return

        try:
            response = requests.post(
                self.url,
                data={
                    "name":self.nameTxt.text().strip(),
                    "email":self.emailTxt.text().strip(),
                    "pass_word":self.passTxt.text().strip()
                }
            )
            result = json.loads(response.text)
            print(f"Raw response: {response.text}")  # for debugging
            errorMsg = result.get("message", "Unknown error")


            if result.get("status") == "success":
                self.msgBox("Welcome", "Enjoy your experience.")
                print("Registration Successful")
            else:
                self.msgBox("Error", f"Error: {errorMsg}")
                print(f"Something went wrong (Reg): {errorMsg}")

        except Exception as e:
            self.msgBox("Error", f"Oops something went wrong: {e}")
            print(f"Oops something went wrong: {e}")


    def validateEmailField(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return re.match(pattern, email) is not None


    def validatePassField(self, password):
        pattern = r"[^A-Za-z0-9_ ]"

        if len(password) < 8 :
            return False

        if not re.search(f"{pattern}", password):
            return False

        return True


    def togglePassword(self, lineEdit, btn):

        if lineEdit.echoMode() == QLineEdit.EchoMode.Password:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            btn.setIcon(QIcon("../../icons/hideWhite.png"))
        else:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            btn.setIcon(QIcon("../../icons/seeWhiteIcon.png"))

    def goTologinPage(self):
        from loginValidationPHP import LoginCode
        self.win = LoginCode()
        self.hide()
        self.win.show()





    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()