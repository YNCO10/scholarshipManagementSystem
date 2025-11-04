import sys

import requests

import Sessions

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QFileDialog, QApplication
from SholarshipManagementSystem.manageScholarshipsPage.uploadScholarships import Ui_Dialog
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.classes.admin import Admin
from SholarshipManagementSystem.homePage.myMainDisplay import Dash
from SholarshipManagementSystem.classes.scholarships import Scholarships


class UploadingCode(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("UPLOAD SCHOLARSHIP")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.regCode = RegCode()
        self.admin = Admin(Sessions.adminName, Sessions.seshEmail, "*********")
        self.wrkShopCheckBox.setStyleSheet("QCheckBox::indicator:checked {"
                                           "background-color: white;"
                                           "border: 2px solid #666;"
                                           "border-radius: 3px;"
                                           "}")
        self.insuranceCheckBox.setStyleSheet("QCheckBox::indicator:checked {"
                                           "background-color: white;"
                                           "border: 2px solid #666;"
                                           "border-radius: 3px;"
                                           "}")
        self.jobOrppotunitiesCheckBox.setStyleSheet("QCheckBox::indicator:checked {"
                                           "background-color: white;"
                                           "border: 2px solid #666;"
                                           "border-radius: 3px;"
                                           "}")
        self.travelAllawanceCheckBox.setStyleSheet("QCheckBox::indicator:checked {"
                                           "background-color: white;"
                                           "border: 2px solid #666;"
                                           "border-radius: 3px;"
                                           "}")
        self.AccomodationCheckBox.setStyleSheet("QCheckBox::indicator:checked {"
                                           "background-color: white;"
                                           "border: 2px solid #666;"
                                           "border-radius: 3px;"
                                           "}")

        self.btnClicks()

# BTN CLICKS############################################################################################################
    def btnClicks(self):
        self.browseBtn.clicked.connect(
            lambda : self.browseFile(self.scholarshipFilepathTxt)
        )

        self.cancelBtn.clicked.connect(self.closeWindow)

        self.uploadBtn.clicked.connect(self.uploadDocument)


    # BROWSE FILE#######################################################################################################
    def browseFile(self,lineEdit):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if filePath:
            lineEdit.setText(filePath)

#     UPLOAD DOCUMENT###################################################################################################
    def uploadDocument(self):
        name = self.scholarshipNameTxt.text()
        scheme = self.schemeComboBox.currentText().strip()
        descrip = self.descripTxt.text()
        provider = self.providerTxt.text()
        deadline = self.deadlineDateEdit.date().toPyDate()
        filePath = self.scholarshipFilepathTxt.text()
        financialAmount = self.financialCombo.currentText()
        applicationLink = self.linkTxt.text()
        providerEmail = self.providerEmailTxt.text()
        url = "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/uploadScholarshipCode.php"

        selectedPerks = []
        if self.jobOrppotunitiesCheckBox.isChecked():
            selectedPerks.append("Job Opportunities")

        if self.AccomodationCheckBox.isChecked():
            selectedPerks.append("Accommodation")

        if self.insuranceCheckBox.isChecked():
            selectedPerks.append("Insurance")

        if self.travelAllawanceCheckBox.isChecked():
            selectedPerks.append("Travel Allowance")

        if self.wrkShopCheckBox.isChecked():
            selectedPerks.append("Workshop Access")



        if not all([name, descrip, deadline, filePath, applicationLink, providerEmail]):
            self.regCode.msgBox(
                "Blank Fields",
                "Please fill in all fields"
            )
            print("Please fill in all fields")
            return

        print(f"{name}\n"
              f"{scheme}\n"
              f"{filePath}\n"
              f"{deadline}\n"
              f"{descrip}\n"
              f"{provider}\n"
              f"{financialAmount}\n"
              f"{applicationLink}\n"
              f"{providerEmail}\n"
              f"{selectedPerks}\n"
              f"{Sessions.seshEmail}\n")

        try:
            scholar = Scholarships(
                name,
                scheme,
                filePath,
                deadline,
                descrip,
                provider,
                financialAmount,
                applicationLink,
                providerEmail
            )
            result = scholar.execute(
                url,
                filePath,
                selectedPerks,
                Sessions.seshEmail
            )
            msg = result.get("message", "Unknown Message")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "File Uploaded",
                    f"{msg}"
                )
                print(f"File Upload: {msg}")
                print(result.get("main_file_path"))
                self.closeWindow()
                dash = Dash()
                dash.populateTableWidget("")
                #get emails
                emails = self.getEmails()
                #send notifications
                print("Sending Notifications...")
                notifications = self.admin.bulkNotificationsForApplicants(
                    f"{Sessions.seshEmail}",
                    "New Scholarship has been uploaded",
                    f"A new scholarship from {provider} has been uploaded. Check it out!",
                    emails
                )
                #response
                notiMsg = notifications.get("message")
                if notifications.get("status") == "success":
                    print("Notifications about scholarship update have been successfully sent to every applicant")

                elif notifications.get("status") == "error":
                    print(f"Notifications did not send\n{notiMsg}")

                elif notifications.get("status") == "notVerified":
                    print(f"Notifications did not send\n{notiMsg}")

                elif notifications.get("status") == "completed":
                    print(f"Notifications did not send\n{notiMsg}")

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Error(scholarUpload)",
                    f"Upload Error: {msg}"
                )
                print(f"Upload Error: {msg}")


        except Exception as e:
            self.regCode.msgBox(
                "Error(scholarUpload)",
                f"Exception(scholarUpload): {e}"
            )
            print(f"Exception(scholarUpload): {e}")

##### filtering line edit###############################################################################################
    def populateSchemeCombo(self):
        schemes = [
            "Merit-Based Scheme",
            "Need-Based Scheme",
            "STEM Scheme",
            "Sports Scholarship Scheme",
            "Community Service Scheme",
            "Research and Innovation Scheme",
            "Disability Support Scheme",
            "Female Empowerment Scheme",
            "Alumni-Funded Scheme",
            "International Student Scheme",
            "Cultural or Arts Scheme",
            "Leadership Development Scheme",
            "Rural or Underprivileged Scheme",
            "Partner Organization Scheme",
            "Government-Funded Scheme"
        ]
        
        self.schemeComboBox.addItems(schemes)

########################################################################################################################
    def getEmails(self):
        try:
            response = requests.get(
                "http://localhost/BackEnd/scholarshipManagement/applicant/getApplicantEmails.php"
            )
            result = response.json()
            msg = result.get("message", "Unknown Msg")

            if result["status"] == "error":
                self.regCode.msgBox(
                    "Error",
                    f"Something went wrong(getEmails):\n{msg}"
                )
                print(f"Something went wrong(getEmails):\n{msg}")
                return

            elif result["status"] == "success":
                return result["data"]

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception Error(getEmails):\n{e}"
            )
            print(f"Exception Error(getEmails):\n{e}")

######### CLOSE WINDOW #################################################################################################
    def closeWindow(self):
        self.close()

# app = QApplication(sys.argv)
# win = UploadingCode()
# win.show()
# app.exec()