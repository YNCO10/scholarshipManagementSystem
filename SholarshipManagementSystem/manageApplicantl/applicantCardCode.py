
from PyQt6.QtWidgets import QWidget
from SholarshipManagementSystem.manageApplicantl.applicantCardTemp import Ui_ApplicantCardForm


class ApplicantCard(QWidget, Ui_ApplicantCardForm):
    def __init__(self, name, email):
        super().__init__()
        self.email = email
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

        self.viewBtn.clicked.connect(self.viewBtn)
        # self.delBtn.clicked.connect()

    def viewApplicant(self):
        from SholarshipManagementSystem.manageApplicantl.manageApplicantDetailsCode import ManageApplicantDetails
        manage = ManageApplicantDetails(self.email)
        manage.show()

    def delApplicant(self, email):
        pass