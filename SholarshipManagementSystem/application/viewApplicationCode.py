import os
import subprocess
import sys
from datetime import datetime

import requests
from PyQt6.QtWidgets import QWidget, QPushButton, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QIcon

import Sessions
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.application.viewApplicationsPage import Ui_ViewApplicantForm

class ViewApplication(QWidget, Ui_ViewApplicantForm):
    def __init__(self, Id):
        super().__init__()
        self.setupUi(self)
        self.regCode = RegCode()
        self.Id = Id
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.setWindowTitle("Application")
        self.btnClicks()

    def btnClicks(self):
        # accept
        self.acceptBtn.clicked.connect(
            lambda: self.changeApplicationStatus("ACCEPTED")
        )
        # reject
        self.rejectBtn.clicked.connect(
            lambda: self.changeApplicationStatus("REJECTED")
        )
        # mark as reviewed
        self.markAsReviewedBtn.clicked.connect(
            lambda: self.changeApplicationStatus("Reviwed")
        )
        #cancel btn
        self.cancelBtn.clicked.connect(self.closeWindow)

    def populateApplicationsDetails(self, applicationID, userID):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/application/applicationDataForApplicationPage.php",
                data={
                    "applicationID": applicationID,
                    "userID": userID
                }
            )
            result = response.json()
            print(f"RAW RESPONSE(populateApplicationsDetails): {response.text}")
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                print(f"Error(populateApplicationsDetails): {msg}")
                return

            dbContent = result.get("data", [])
            item = dbContent[0]

            dateSubmitted = item.get("date_submitted")
            deadline = item.get("deadline")

            parsedSubmittedDated = datetime.strptime(dateSubmitted, "%Y-%m-%d")
            parsedDeadline = datetime.strptime(deadline, "%Y-%m-%d")

            if parsedSubmittedDated < parsedDeadline:
                self.dateSubmittedLabel.setText(f"Application was submitted on {dateSubmitted}\n"
                                                f"Deadline: {deadline}\n"
                                                f"Submitted before deadline")
            else:
                self.dateSubmittedLabel.setText(f"Application was submitted on {dateSubmitted}\n"
                                                f"Deadline: {deadline}\n"
                                                f"Submitted After deadline")

            self.applicanNameLabel.setText(f"Applicant Name: {item.get("applicant_name")}")
            self.scholarshipNameLabel.setText(f"Scholarship Name: {item.get("scholarship_name")}")
            self.incomeBracketLabel.setText(f"Income Bracket: {item.get("income_bracket")}")
            self.reasonForApplicationLabel.setText(item.get("reason_for_applying"))
            self.applicationStatusLabel.setText(f"Application Status: {item.get("application_status")}")

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(populateApplicationsDetails): {e}"
            )
            print(f"Exception(populateApplicationsDetails): {e}")

########################################################################################################################
    def changeApplicationStatus(self, status):
        try:

            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/application/updateStatus.php",
                data={
                    "id": self.Id,
                    "status": status
                }
            )
            print(f"RAW RESPONSE(changeApplicantStatus): {response.text}")
            result = response.json()
            msg = result.get("message", "Unknown MSG")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )
                return

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                print(f"Error: {msg}")
                return

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(changeApplicationStatus): {e}"
            )
            print(f"Exception(changeApplicationStatus): {e}")

########################################################################################################################
    def populateDocumentTbl(self,userID, applicationID):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/documentsTbl/getDocs.php",
                data={
                    "applicationID": applicationID,
                    "userID": userID
                }
            )
            result = response.json()
            print(f"RAW RESPONSE(populateDocumentsTbl): {response.text}")
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                print(f"Error: {msg}")
                return

            dbContent = result.get("data", [])

            self.viewDocsTableWidget.setColumnCount(6)
            self.viewDocsTableWidget.setRowCount(len(dbContent))
            self.viewDocsTableWidget.setHorizontalHeaderLabels(
                [
                    "Actions",
                    "Doc Name",
                    "Date Submitted",
                    "Filepath",
                    "User ID",
                    "Application ID"
                ]
            )

            for rowIndx, rowData in enumerate(dbContent):
                self.viewDocsTableWidget.setItem(rowIndx, 1, QTableWidgetItem(rowData.get("doc_type", "")))
                self.viewDocsTableWidget.setItem(rowIndx, 2, QTableWidgetItem(rowData.get("date_uploaded", "")))
                self.viewDocsTableWidget.setItem(rowIndx, 3, QTableWidgetItem(rowData.get("file_path", "")))
                self.viewDocsTableWidget.setItem(rowIndx, 4, QTableWidgetItem(str(rowData.get("user_id", ""))))
                self.viewDocsTableWidget.setItem(rowIndx, 5, QTableWidgetItem(str(rowData.get("application_ID", ""))))

                #       create View & del btn
                viewBtn = QPushButton("View")
                delBtn = QPushButton("Delete")

                viewBtn.setStyleSheet("QPushButton { "
                                      "color: white;"
                                      "padding:3px;"
                                      "margin:0px;"
                                      "border-radius:3px;"
                                      "}")
                delBtn.setStyleSheet("QPushButton { "
                                     "color: white;"
                                     "padding:3px;"
                                     "margin:0px;"
                                     "border-radius:3px;"
                                     "}")

                viewBtn.clicked.connect(
                    lambda _, filePath=rowData.get("file_path"): self.displayDoc(filePath)
                )
                # delBtn.clicked.connect(
                #     lambda _, Id=rowData.get("file_path"): self.displayDoc(Id)
                # )

                #   align horizontally
                btnWidget = QWidget()
                layout = QHBoxLayout(btnWidget)
                layout.addWidget(viewBtn)
                layout.addWidget(delBtn)
                layout.setContentsMargins(0, 0, 0, 0)
                self.viewDocsTableWidget.setCellWidget(rowIndx, 0, btnWidget)

                requiredDocs = ["Recommendation Letter", "Proof Of Need", "National ID", "Transcript"]
                self.documentsUploadedLabel.setText(f"Documents uploaded {len(dbContent)}/{len(requiredDocs)}")

        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(populateDocumentTbl): {e}"
            )
            print(f"Exception(populateDocumentTbl): {e}")

### DISPLAY SCHOLARSHIPS########################################################################################
    def displayDoc(self, path):

        print(repr(path))
        # referenceDir = "C:/XAMPP/htdocs/BackEnd/scholarshipManagement/uploadScholarships/docs/uploadedFiles"
        xamppDir = r"C:/XAMPP/htdocs/BackEnd/scholarshipManagement/application/docs/uploadedFiles"

        fullPath = os.path.join(xamppDir, path)

        fullPath = os.path.normpath(fullPath)

        print(fullPath)
        os.startfile(fullPath)

        if not os.path.isfile(fullPath):
            self.regCode.msgBox("Error", f"File not found: {fullPath}")
            return

        try:
            if sys.platform.startswith('win'):
                os.startfile(fullPath)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', fullPath])
            else:  # Linux
                subprocess.Popen(['xdg-open', fullPath])
        except Exception as e:
            self.regCode.msgBox("Error", f"Cannot open file: {e}")

########################################################################################################################
    def closeWindow(self):
        self.close()