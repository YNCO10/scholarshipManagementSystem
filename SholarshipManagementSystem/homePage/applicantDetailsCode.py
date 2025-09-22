
import requests
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

from SholarshipManagementSystem.homePage.applicantDetailsPage import Ui_ApplicantDetails
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode



class ApplicantDetails(QWidget, Ui_ApplicantDetails):
    def __init__(self, Id):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Applicant Details")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.regCode = RegCode()
        self.id = Id

        self.displayContent()
        self.btnClicks()

    def btnClicks(self):
        self.backBtn.clicked.connect(self.closeWindow)

    def displayContent(self):
        url = "http://localhost/BackEnd/scholarshipManagement/applicant/loadApplicantDataWithID.php"
        try:
            response = requests.post(
                url=url,
                data={
                    "id" : self.id
                }
            )

            print(f"RAW RESPONSE: {response.text}")

            result = response.json()
            msg = result.get("message", "Unknown Msg")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error(ApplicantDetails)",
                    msg
                )
                print(f"Error(ApplicantDetails): {msg}")
                return

            elif result.get("status") == "success":
                dbContent = result.get("data", [])
                row = dbContent[0]

                self.nameLabel.setText("Name: " + str(row.get("name","Unknown Name")))
                self.emailLabel.setText("Email: " + str(row.get("email")))
                self.ageLabel.setText("Age: " + str(row.get("age")))
                self.genderLabel.setText("Gender: " + str(row.get("gender")))
                # self.nameLabel.setText("Rank: "+result.get("name"))
                self.rankLabel.setText("Rank: Not specified yet")
                self.nationalityLabel.setText("Nationality: " + str(row.get("nationality")))
                self.eduLevelLabel.setText("Education Level: " + str(row.get("education_level")))
                self.dobLabel.setText("DOB: " + str(row.get("dob")))
                self.assessScoreLabel.setText("Assessment Score: " + str(row.get("score")))


        except Exception as e:
            self.regCode.msgBox(
                "Error(ApplicantDetails)",
                f"Exception Error: {e}"
            )
            print(f"Exception Error: {e}")
            return

    def closeWindow(self):
        self.close()