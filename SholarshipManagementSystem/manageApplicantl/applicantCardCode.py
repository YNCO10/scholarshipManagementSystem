import json

import requests
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.manageApplicantl.applicantCardTemp import Ui_ApplicantCardForm



class ApplicantCard(QWidget, Ui_ApplicantCardForm):
    def __init__(self, name, email):
        super().__init__()
        self.manage = None
        self.email = email
        self.regCode = RegCode()
        self.name = name
        self.setupUi(self)
        self.nameLabel.setText(f"Applicant Name: {self.name}")
        self.emailLabel.setText(f"Applicant Email: {self.email}")

        self.viewBtn.setStyleSheet("""
        border: 1px solid black;
        paddling:10px;
        """)
        self.delBtn.setStyleSheet("""
        border: 1px solid black;
        paddling:7px;
        """)
        self.viewBtn.clicked.connect(self.viewApplicant)
        self.delBtn.clicked.connect(self.delApplicant)

    def viewApplicant(self):
        from SholarshipManagementSystem.manageApplicantl.manageApplicantDetailsCode import ManageApplicantDetails
        self.manage = ManageApplicantDetails(self.email)
        self.manage.show()

    def delApplicant(self):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/applicant/deleteApplicant.php",
                data={
                    "email": self.email
                }
            )

            result = json.loads(response.text)
            msg = result.get("message")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    f"{msg}"
                )
                print(f"Delete successful: {msg}")

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "delete failed(dash)",
                    f"{msg}"
                )
                print(f"deleting(dash): {msg}")
        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Something went wrong while Deleting Applicant(dash): {e}"
            )
            print(f"Exception: {e}")
