import json
import requests
import Sessions
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QFileDialog, QCompleter

from Sessions import seshEmail
from SholarshipManagementSystem.manageScholarshipsPage.uploadScholarships import Ui_Dialog
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode

from SholarshipManagementSystem.homePage.myMainDisplay import Dash
from SholarshipManagementSystem.classes.scholarships import Scholarships


class UploadingCode(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("UPLOAD SCHOLARSHIP")
        self.setWindowIcon(QIcon(":icons/Sms"))
        self.regCode = RegCode()

        self.btnClicks()
        self.subjectLiveFiltering()

# BTN CLICKS############################################################################################################
    def btnClicks(self):
        self.browseBtn.clicked.connect(
            lambda : self.browseBtn(self.scholarshipFilepathTxt)
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
        type = self.typeCombo.currentText()
        descrip = self.descripTxt.text()
        provider = self.providerTxt.text()
        deadline = self.deadlineDateEdit.date().toPyDate()
        filePath = self.scholarshipFilepathTxt.text()
        financialAmount = self.financialCombo.currentText()
        applicationLink = self.linkTxt.text()
        providerEmail = self.providerEmailTxt.text()
        subject = self.subjectTxt.text()
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



        if not all([name, descrip, deadline, filePath, applicationLink, providerEmail, subject]):
            self.regCode.msgBox(
                "Blank Fields",
                "Please fill in all fields"
            )
            print("Please fill in all fields")
            return

        print(f"{name}\n"
              f"{type}\n"
              f"{filePath}\n"
              f"{deadline}\n"
              f"{descrip}\n"
              f"{provider}\n"
              f"{financialAmount}\n"
              f"{applicationLink}\n"
              f"{providerEmail}\n"
              f"{subject}\n"
              f"{selectedPerks}\n"
              f"{Sessions.seshEmail}\n")

        try:
            scholar = Scholarships(
                name,
                type,
                filePath,
                deadline,
                descrip,
                provider,
                financialAmount,
                applicationLink,
                providerEmail,
                subject
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
                dash = Dash()
                dash.populateTableWidget()

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
    def subjectLiveFiltering(self):
        subjects = [
            "Agriculture", "Architecture", "Arts & Humanities", "Business & Management",
            "Communications & Media Studies", "Computer Science & IT", "Dentistry",
            "Design & Creative Arts", "Economics", "Education", "Engineering & Technology",
            "Environmental Science", "Finance & Accounting", "Health Sciences", "History",
            "Hospitality & Tourism", "International Relations", "Journalism", "Law",
            "Linguistics & Languages", "Literature", "Mathematics", "Medicine", "Music",
            "Nursing & Midwifery", "Pharmacy", "Philosophy", "Physics", "Political Science",
            "Psychology", "Public Health", "Social Sciences", "Sociology", "Sports Science",
            "Theology & Religious Studies", "Veterinary Science"
        ]

        self.subjectTxt.setPlaceholderText("e.g. Medicine, Engineering, Business etc...")
    #     add completer
        completer = QCompleter(subjects, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)#live filter anywhere in the string
        completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)

        self.subjectTxt.setCompleter(completer)


    # CLOSE WINDOW##########################################################################################################
    def closeWindow(self):
        self.close()