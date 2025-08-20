import json
import requests

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QFileDialog

from SholarshipManagementSystem.manageScholarshipsPage.uploadScholarships import Ui_Dialog
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
import Sessions
from SholarshipManagementSystem.homePage.myMainDisplay import Dash


class UploadingCode(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("UPLOAD SCHOLARSHIP")
        self.setWindowIcon(QIcon(":icons/Sms"))
        self.regCode = RegCode()

        self.btnClicks()

# BTN CLICKS###########################################################
    def btnClicks(self):
        self.browseBtn.clicked.connect(self.browseFile)

        self.cancelBtn.clicked.connect(self.closeWindow)

        self.uploadBtn.clicked.connect(self.uploadDocument)


    # BROWSE FILE########################################################
    def browseFile(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if filePath:
            self.scholarshipFilepathTxt.setText(filePath)

#     UPLOAD DOCUMENT##################################################
    def uploadDocument(self):
        fileName = self.scholarshipNameTxt.text()
        descrip = self.scholarshipDescriptionTxt.text()
        deadline = self.scholarshipDeadlineTxt.text()
        filePath = self.scholarshipFilepathTxt.text()

        if not all([fileName, descrip, deadline, filePath]):
            self.regCode.msgBox(
                "Blank Fields",
                "Please fill in all fields"
            )

        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/uploadScholarships/uploadScholarshipCode.php",
                data={
                    "filename": fileName.strip(),
                    "descrip": descrip.strip(),
                    "deadline": deadline.strip(),
                    "email": Sessions.seshEmail
                },
                files={
                    "document": open(filePath, "rb")
                }
            )
            print(response.text)
            result = json.loads(response.text)
            msg = result.get("message", "Unknown Message")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "File Uploaded",
                    f"{msg}"
                )
                dash = Dash()
                dash.populateTableWidget()

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    f"Upload Error: {msg}"
                )


        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(upload): {e}"
            )

            print("Please fill in all fields")


# CLOSE WINDOW##########################################################
    def closeWindow(self):
        self.close()