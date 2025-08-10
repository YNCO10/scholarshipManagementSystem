from traceback import print_tb

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox, QLineEdit
from SholarshipManagementSystem.authentications.adminReg import Ui_Form
from SholarshipManagementSystem.databaseHandler.dbHandler import databaseHandler
# from SholarshipManagementSystem.authentications.loginCode import LoginCode


class Validations(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("REGISTER")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        # self.loginCode = LoginCode()
        self. myDb = databaseHandler("localhost","root","","scholarship_management_sys_db")

        self.btnClicks()

    def showValues(self):
        print("Name:", self.nameTxt.text())
        print("Email:", self.emailTxt.text())
        print("Password:", self.passTxt.text())


    def btnClicks(self):
        # registration
        self.showHidePassBtn.clicked.connect(lambda : self.togglePasswordBtn(self.passTxt, self.showHidePassBtn))
        self.showHideConfirmPassBtn.clicked.connect(lambda : self.togglePasswordBtn(self.confirmPassTxt, self.showHideConfirmPassBtn))


        self.signUpBtn.clicked.connect(self.signUp)
        # self.signUpBtn.clicked.connect(self.showValues)

        self.goToLoginPageBtn.clicked.connect(self.goToLoginPage)

    def signUp(self):

        if self.nameTxt.text() == "" or self.emailTxt.text() == "" or self.passTxt.text() == "" or self.confirmPassTxt.text() == "":
            self.msgBox("Empty Fields", "Fill in all the empty fields")
            return

        if self.myDb.checkEmailExists("SELECT * FROM admin WHERE email = %s", (self.emailTxt.text().strip())):
            self.msgBox("Existing Email","Email Already Exists.")
            print("Email Already Exists.")
            return

        if self.passTxt.text() != self.confirmPassTxt.text():
            self.msgBox("Error", "Passwords do Not Match!")
            return


        query = "INSERT INTO admin (name, email, pass_word) VALUES (%s, %s, %s)"

        self.myDb.insert(query, (self.nameTxt.text().strip(), self.emailTxt.text().strip(), self.passTxt.text().strip()))
        # self.myDb.insert(query, ("Test user", "y@gmail.com", "mypassword"))



    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()


    def togglePasswordBtn(self, lineEdit, Btn):
        if lineEdit.echoMode() == QLineEdit.EchoMode.Normal:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            Btn.setIcon(QIcon("../../icons/seeWhiteIcon.png"))
        else:
            lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            Btn.setIcon(QIcon("../../icons/hideWhite.png"))


    def goToLoginPage(self):
        from SholarshipManagementSystem.authentications.loginCode import LoginCode
        loginCode = LoginCode()
        self.hide()
        loginCode.show()