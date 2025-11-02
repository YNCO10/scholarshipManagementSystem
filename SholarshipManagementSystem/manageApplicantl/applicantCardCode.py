import json
import Sessions
import requests
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.manageApplicantl.applicantCardTemp import Ui_ApplicantCardForm
from SholarshipManagementSystem.classes.admin import Admin



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
        self.admin = Admin(
            f"{Sessions.adminName}",
            f"{Sessions.seshEmail}",
            "*********"
        )

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
            notification = self.admin.sendSingleNotification(
                f"{self.email}",
                "Your profile has been REMOVED!",
                f"You have been removed from our system by {Sessions.adminName}(ADMIN).\nCONTACT them using this email:{Sessions.seshEmail}. to get further clarification."
            )
            if notification.get("status") == "error":
                self.regCode.msgBox(
                    "Notification failed",
                    f"{notification.get("message")}"
                )
                print(f"Error: {notification.get("message")}")
                return

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
