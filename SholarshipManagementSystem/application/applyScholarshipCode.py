from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

from SholarshipManagementSystem.application.applyScholarshipPage import Ui_applyScholarshipForm
from SholarshipManagementSystem.classes.application import Application
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.manageScholarshipsPage.uploadScholarCode import UploadingCode



class ApplyScholarship(QWidget, Ui_applyScholarshipForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.setWindowTitle("Apply For Scholarship")
        self.url = "http://localhost/BackEnd/scholarshipManagement/application/applyScholarship.php"
        self.regCode = RegCode()
        self.uploadCode = UploadingCode()

        self.btnClicks()

########################################################################################################################
    def btnClicks(self):
        self.cancelBtn.clicked.connect(self.closeWindow)
        self.applyBtn.clicked.connect(self.applyToScholarship)

        #browse btns
        self.recommBrowseBtn.clicked.connect(
            lambda : self.uploadCode.browseFile(self.recommedationLetterTxt)
        )
        self.transcriptBrowseBtn.clicked.connect(
            lambda : self.uploadCode.browseFile(self.transcriptTxt)
        )
        self.proofBrowseBtn.clicked.connect(
            lambda : self.uploadCode.browseFile(self.proofOfNeedTxt)
        )
        self.nationalBrowseBtn.clicked.connect(
            lambda : self.uploadCode.browseFile(self.nationalIdTxt)
        )

########################################################################################################################
    def applyToScholarship(self):
        try:
            schoolAttended = self.formerSchoolTxt.text()
            gpa = self.gpaSpinbox.text()
            reasonForApplying = self.reasonForApplyingTxt.toPlainText()
            transcript = self.transcriptTxt.text()
            nationalID = self.nationalIdTxt.text()
            recomLetter = self.recommedationLetterTxt.text()
            careerGoals = self.careerGoalsTxt.text()
            proofOfNeed = self.proofOfNeedTxt.text()
            incomeBracket = self.incomeBracketComboBox.currentText()
            financialAssistance = None
            print("Checkpoint 1")
            # CHECK EMPTY FIELDS
            if schoolAttended == "" or reasonForApplying == "" or transcript == "" or nationalID == "" or recomLetter == "":
                self.regCode.msgBox(
                    "Empty field",
                    "Please fill in all required fields"
                )
                return

            if self.yesRadioBtn.isChecked():
                financialAssistance = 0
            elif self.noRadioBtn.isChecked():
                financialAssistance = 1

            if financialAssistance is None:
                self.regCode.msgBox(
                    "Empty fields",
                    'You forgot to check "Yes" or "No" for financial need.'
                )
                return

            print("Checkpoint 2")
            application = Application(
                schoolAttended.strip(),
                gpa.strip(),
                financialAssistance,
                reasonForApplying.strip(),
                transcript.strip(),
                nationalID.strip(),
                recomLetter.strip(),
                careerGoals.strip(),
                proofOfNeed.strip(),
                incomeBracket.strip()
            )
            print("Checkpoint 3")
            result = application.apply(self.url)
            print(f"RAW RESPONSE: {result}")
            msg = result.get("message", "Unknown Response")

            if result.get("status") == "success":
                self.regCode.msgBox(
                    "Process Complete",
                    msg
                )
            elif result.get("status") == "error":
                self.regCode.msgBox(
                    "Application Failed",
                    msg
                )
        except Exception as e:
            self.regCode.msgBox(
                "Error(apply scholar)",
                f"Exception: {e}"
            )
            print(f"Exception: {e}")

########################################################################################################################
    def closeWindow(self):
        self.close()