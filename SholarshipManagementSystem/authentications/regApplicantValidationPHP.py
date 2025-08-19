import re


from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox
import requests
import json
from SholarshipManagementSystem.authentications.applicantReg import Ui_applicantRegistration
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode



class AppValCode(QWidget, Ui_applicantRegistration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("REGISTER")
        self.setWindowIcon(QIcon("../../icons/SMsysIcon.png"))
        self.regCode = RegCode()
        self.url = "http://localhost/BackEnd/scholarshipManagement/authentications/regApplicantValidation.php"


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

        # add values for gender
        self.genders = [
            "Male",
            "Female",
            "Other"
        ]
        self.genderCombo.addItems(self.genders)

        # values for spin box min, max & default
        self.ageSpinBox.setMinimum(18)
        self.ageSpinBox.setMaximum(40)
        self.ageSpinBox.setValue(18)



        # BTN CLICKS
        self.btnClicks()

    # ALL BTN CLICKS BELOW
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

        # go to loginPage
        # self.goToLoginPageBtn.clicked.connect(self.goToLoginPage)

    #     register
        self.signUpBtn.clicked.connect(self.register)


    def register(self):

        if self.nameTxt.text() == "" or self.nationalityTxt.text() == "" or self.passTxt.text() == "" or self.emailTxt.text() == "" or self.confirmPassTxt.text() == "":
            self.msgBox("Blank Fields", "Please fill in all blank fields.")
            return

        if not self.regCode.validatePassField(self.emailTxt.text().strip()):
            self.errorMsgLog.setText("Please enter valid Email")
            return

        if self.passTxt.text().strip() != self.confirmPassTxt.text().strip():
            self.errorMsgLog.setText("The passwords do not match.")
            return

        if not self.regCode.validatePassField(self.passTxt.text().strip()):
            self.errorMsgLog.setText("Password must be 8 characters long\nMust have at least one number\nAt least one symbol")
            return

        if not self.validatePhoneNumberLineEdit(self.phoneNumTxt.text().strip()):
            self.errorMsgLog.setText("Phone number must start with + and contain 7–15 digits.")
            return

        dob = self.DOBdateEdit.date()
        try:
            response = requests.post(
                self.url,
                data={
                    "name":self.nameTxt.text().strip(),
                    "email":self.emailTxt.text().strip(),
                    "nationality":self.nationalityTxt.text().strip(),
                    "pass": self.passTxt.text().strip(),
                    "gender":self.genderCombo.currentText(),
                    "phone_number":self.phoneNumTxt.text().strip(),
                    "age":self.ageSpinBox.text(),
                    "dob":dob.toPyDate(),
                    "education_level":self.educationCombo.currentText()
                }
            )

            result = json.loads(response.text)
            print(f"Raw response: {response.text}")
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


    def validatePhoneNumberLineEdit(self, phoneNum):
        pattern = r"^\+\d{7,15}$"

        return re.match(pattern, phoneNum) is not None


    # def goToLoginPage(self):
    #     from SholarshipManagementSystem.welcomePage.welcomePageCode import WelcomePageCode
    #     self.win = WelcomePageCode()
    #     self.hide()
    #     self.win.show()


    def hideWindow(self):
        self.hide()

    def msgBox(self, title, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()