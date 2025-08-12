from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox
import requests
import json

from SholarshipManagementSystem.authentications.loginPage import Ui_loginPage


class LoginCode(QWidget, Ui_loginPage):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.setupUi(self)

        self.url = "http://localhost/BackEnd/scholarshipManagement/authentications/loginValidation.php"
        self.btnClicks()

    def btnClicks(self):
        self.signInBtn.clicked.connect(self.login)
        self.goToRegistrationPageBtn.clicked.connect(self.goToRegPage)

    def login(self):

        if self.loginPassTxt.text() == "" or self.loginEmailTxt.text() == "":
            self.msgBox("Blank Fields", "Please fill in all blank fields.")
            return

        try:
            response = requests.post(
                self.url,
                data={
                    "email":self.loginEmailTxt.text().strip(),
                    "pass_word":self.loginPassTxt.text().strip()
                }
            )

            result = json.loads(response.text)
            errorMsg = result.get("message", "Unknown Error")

            if result.get("status") == "success":
                self.msgBox("Welcome", "Enjoy your experience.")
                print("Login Successful")
            else:
                self.msgBox("Wrong Credentials", f"Error: {errorMsg}")
                print("Login Failed")
        except Exception as e:
            self.msgBox("Error", f"Oops something went wrong: {e}")



    def goToRegPage(self):
        from regValidationPHP import RegCode
        self.win = RegCode()
        self.win.show()
        self.hide()



    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()


