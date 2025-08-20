from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox
import requests
import json

from SholarshipManagementSystem.authentications.loginPage import Ui_loginPage
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
import Sessions



class LoginCode(QWidget, Ui_loginPage):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.setupUi(self)

        self.regCode = RegCode()

        self.url = "http://localhost/BackEnd/scholarshipManagement/authentications/loginValidation.php"
        self.btnClicks()

    def btnClicks(self):
        self.signInBtn.clicked.connect(self.login)
        # self.goToRegistrationPageBtn.clicked.connect(self.goToWelcomePage)
        self.loginShowHidePassBtn.clicked.connect(
            lambda : self.regCode.togglePassword(self.loginPassTxt, self.loginShowHidePassBtn)
        )


    def login(self):

        print(f"{self.loginEmailTxt.text()} : {self.loginPassTxt.text()}")

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

            print(response.text)
            result = json.loads(response.text)
            errorMsg = result.get("message", "Unknown Error")


            if result.get("status") == "admin":
                self.msgBox("Welcome", f"Enjoy your experience, {result.get('adminName', 'Admin')}")
                print("Login Successful")

                Sessions.seshEmail = self.loginEmailTxt.text().strip()

                from pageController import Controller
                self.controller = Controller()
                self.controller.showAdinDash()
                self.hideWindow()


            elif result.get("status") == "applicant":
                self.msgBox("Welcome", f"Enjoy your experience, {result.get('applicantName', 'Applicant')}")
                print("Login Successful")




            else:
                self.msgBox("Error", f"Error: {errorMsg}")
                print(f"Login Failed {errorMsg}")


        except Exception as e:
            self.msgBox("Error", f"Oops something went wrong(login): {e}")
            print(e)


    def hideWindow(self):
        self.hide()


    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()


