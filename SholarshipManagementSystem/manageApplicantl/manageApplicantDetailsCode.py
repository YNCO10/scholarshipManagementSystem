
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
import requests

import Sessions
from SholarshipManagementSystem.manageApplicantl.manageApplicantDetailsPage import Ui_Form
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.applicantTracking.getApplicantData import GetApplicantData
from SholarshipManagementSystem.classes.admin import Admin


class ManageApplicantDetails(QWidget, Ui_Form):
    def __init__(self, email):
        super().__init__()
        self.setupUi(self)
        self.admin = Admin(
            f"{Sessions.adminName}",
            f"{Sessions.seshEmail}",
            "*********"
        )
        self.setWindowTitle("Applicant Details")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.regCode = RegCode()
        self.email = email
        self.getApplicantData = GetApplicantData(self.email)
        self.populateApplicantDetails()
        self.btnClicks()

        #convert values in comboBox
        items = [
            5.0,
            4.5,
            4.0,
            3.5,
            3.0,
            2.5,
            2.0,
            1.5,
            1.0
        ]
        stringItems = [f"{i:.1f}" for i in items]

        self.academicWeightCombo.addItems(stringItems)
        self.financialWeightCombo.addItems(stringItems)
        self.assessmentWeightCombo.addItems(stringItems)

        self.stackedWidget.setCurrentIndex(0)

########################################################################################################################
    def btnClicks(self):
        self.goToApplicantDetialsBtn.clicked.connect(self.goToApplicantDetails)

        self.goToApplicantCriteriaBtn.clicked.connect(self.goToApplicantCriteria)
        #accept
        self.acceptBtn.clicked.connect(
            lambda: self.changeApplicantStatus("ACCEPTED")
        )
        #reject
        self.rejectBtn.clicked.connect(
            lambda: self.changeApplicantStatus("REJECTED")
        )
        #mark as reviewed
        self.markAsReviewedBtn.clicked.connect(
            lambda: self.changeApplicantStatus("Reviewed")
        )

        self.cancelBtn.clicked.connect(self.closeWindow)
        self.cancelBtn_2.clicked.connect(self.closeWindow)

        self.changeWeightsBtn.clicked.connect(self.updateWeights)

########################################################################################################################
    def goToApplicantCriteria(self):
        self.getApplicantData = GetApplicantData(self.email)
        self.stackedWidget.setCurrentIndex(1)
        self.populateApplicantCriteria()

########################################################################################################################
    def goToApplicantDetails(self):
        self.stackedWidget.setCurrentIndex(0)
        self.populateApplicantDetails()

########################################################################################################################
    def populateApplicantDetails(self):
        try:
            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/applicant/allApplicantDetails.php",
                data={
                    "email": self.email
                }
            )
            print(f"RAW RESPONSE(manageApplicant): {response.text}")
            result = response.json()
            msg = result.get("message")

            if result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                print(f"Error: {msg}")

            #populate applicant details page
            dbContent = result.get("data", [])
            item = dbContent[0]
            self.applicantEmail = item.get("email")


            self.nameLabel.setText(f"NAME:  {item.get("name", "")}")
            self.ageLabel.setText(f"AGE:  {str(item.get("age", ""))}")
            self.dateJoinedLabel.setText(f"DATE REGISTERED: {item.get("date_registered", "")}")
            self.eduLevelLabel.setText(f"EDUCATION LEVEL:  {item.get("education_level", "")}")
            self.formerSchoolLabel.setText(F"FORMER SCHOOL:  {item.get("school_attended", "")}")
            self.phoneNumLabel.setText(F"PHONE NUMBER:  {item.get("phone_num", "")}")
            self.nationalityLabel.setText(F"NATIONALITY:  {item.get("nationality", "")}")
            self.gpaLabel.setText(F" GPA:  {str(item.get("gpa", "") or "0")}")
            self.incomeBracketLabel.setText(f"INCOME BRACKET:  {item.get("income_bracket", "") or "Not Specified"}")
            # self.applicationSubmittedLabel.setText(f"APPLICATION SUBMISSION DATE:  {item.get("date_submitted", "")}")
            self.ApplicantScoreLabel.setText(f"APPLICANT SCORE:  {str(item.get("applicant_score", "") or "0")}")
            self.AssessmentScoreLabel.setText(f"ASSESSMENT SCORE:  {str(item.get("assessment_score", "")) or "0"}")


        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(populateApplicantDetails): {e}"
            )
            print(f"Exception(populateApplicantDetails): {e}")

########################################################################################################################
    def convertComboToFloats(self,comboBox):
        items = [float(comboBox.itemText(i)) for i in range(comboBox.count())]
        comboBox.clear()
        for val in items:
            comboBox.addItem(f"{val:.1f}", val)  # stores float as userData too

########################################################################################################################
    def populateApplicantCriteria(self):
        self.getApplicantData.scoreApplicant()

        self.getApplicantData.applicantCriteriaTemplate(
            self.academicScoreLabel,
            self.incomeBracketLabel_2,
            self.financialScoreLabel,
            self.assessmentScoreLabel,
            self.academicWeightCombo,
            self.financialWeightCombo,
            self.assessmentWeightCombo,
            self.finalScoreFormulaLabel,
            self.finalScoreLabel,
            self.needLabel,
            self.gpaScoreLabel,
            self.overallAvgScoreLabel,
            self.applicantEligibilityLabel,
            self.successPredictionLabel
        )

        print("APPLICANT CRITERIA HAS BEEN POPULATED...")
        print(f"Email(populateApplicantCriteria): {self.email}")

########################################################################################################################
    def updateWeights(self):
        try:
            academicWeight = float(self.academicWeightCombo.currentText().strip()),
            financialWeight = float(self.financialWeightCombo.currentText().strip())
            assessmentWeight = float(self.assessmentWeightCombo.currentText().strip())

            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/applicantTracking/updateWeights.php",
                data={
                    "academic": academicWeight,
                    "financial": financialWeight,
                    "assessment": assessmentWeight
                }
            )
            print(f"RAW RESPONSE: {response.text}")
            result = response.json()
            msg = result.get("message", "Unknown Msg")
            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )
                print(f"Process Complete: {msg}")
                self.getApplicantData.scoreApplicant()
                self.getApplicantData = GetApplicantData(self.email)
                self.goToApplicantCriteria()

            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Error",
                    msg
                )
                print(f"Error: {msg}")


        except Exception as e:
            self.regCode.msgBox(
                "Error",
                f"Exception(updateWeights): {e}"
            )
            print(f"Exception(updateWeights): {e}")

########################################################################################################################
    def changeApplicantStatus(self, status):
        try:
            if status == "ACCEPTED":
                if Sessions.overallAverageScore > Sessions.applicantScore:
                    self.regCode.msgBox(
                        "Warning!",
                        "Applicant is Not Eligible."
                    )
                    return

            response = requests.post(
                "http://localhost/BackEnd/scholarshipManagement/manageApplicant/updateStatus.php",
                data={
                    "email" : self.email,
                    "status": status
                }
            )
            print(f"RAW RESPONSE: {response.text}")
            result = response.json()
            msg = result.get("message", "Unknown MSG")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )
                if status == "ACCEPTED":
                    self.admin.sendSingleNotification(
                        f"{self.applicantEmail}",
                        f"Your profile has been Accepted!",
                        f"You have been Accepted into our system. We will keep you updated on any new activities."
                    )
                    return
                elif status == "Reviewed":
                    self.admin.sendSingleNotification(
                        f"{self.applicantEmail}",
                        f"Your profile has been Reviewed!",
                        f"You have been Reviewed by {Sessions.adminName}. We will keep you updated on any new activities."
                    )
                elif status == "REJECTED":
                    self.admin.sendSingleNotification(
                        f"{self.applicantEmail}",
                        f"Your profile has been Rejected!",
                        f"You have been rejected from our system. Your applications will NOT be reviewed."
                    )

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
                f"Exception(changeApplicantStatus): {e}"
            )
            print(f"Exception(changeApplicantStatus): {e}")

########################################################################################################################
    def closeWindow(self):
        self.close()