from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox

from SholarshipManagementSystem.authentications.loginPage import Ui_loginPage
from SholarshipManagementSystem.databaseHandler.dbHandler import databaseHandler
from registrationCode import Validations

class LoginCode(QWidget, Ui_loginPage):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.setupUi(self)
        self.regPage = Validations()
        self.myDb = databaseHandler("localhost","root","","scholarship_management_sys_db")

        self.btnClicks()


    def showValues(self):
        print("Name:", self.loginEmailTxt.text())
        print("Email:", self.loginPassTxt.text())



    def btnClicks(self):
        self.signInBtn.clicked.connect(self.login)

        self.loginShowHidePassBtn.clicked.connect(
            lambda : self.regPage.togglePasswordBtn(self.loginPassTxt, self.loginShowHidePassBtn)
        )
        self.goToRegistrationPageBtn.clicked.connect(self.goToRegistrationPage)





    def login(self):

        if self.loginPassTxt.text() == "" or self.loginEmailTxt.text() == "":
            self.msgBox("Blank Fields", "Please fill in all blank fields.")
            return

        query = "SELECT * FROM admin WHERE email = %s"

        if self.myDb.checkEmailExists(query, (self.loginEmailTxt.text().strip(),)):
            result = self.myDb.select(
                "SELECT * FROM admin WHERE email = %s AND pass_word = %s",
                (self.loginEmailTxt.text().strip(), self.loginPassTxt.text().strip())
            )

            if result:
                self.msgBox("Welcome","Enjoy your experience.")
                print("Login Successful")
            else:
                self.msgBox("Wrong Credentials", "Wrong Email or Password")
                print("Login Failed")

        else:
            self.msgBox("Account not found", "Email doesn't exist. PLease Register")
            print("Account not found.")


    def goToRegistrationPage(self):
        self.hide()
        self.regPage.show()




    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()