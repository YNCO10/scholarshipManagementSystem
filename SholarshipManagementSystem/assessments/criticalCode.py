from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QButtonGroup

from SholarshipManagementSystem.assessments.criticalPage import Ui_criticalReasoningForm
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.classes.assessment import Assessment
import Sessions
import json
import requests

class CriticalCode(QWidget, Ui_criticalReasoningForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Critical Reasoning")
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.regCode = RegCode()
        self.assess = None
        self.controller = None


        self.btnCLicks()


        self.criticalReasoningStackedWidget.setCurrentIndex(0)

#######################################################################################################################

    def btnCLicks(self):
        self.startBtn.clicked.connect(self.startAssessment)
        self.qNextBtn.clicked.connect(self.nextQuestion)

#######################################################################################################################

    def loadQuestions(self, question):
    # populate labels with questions & options
        self.question_txt.setText(question.get("question_txt"))

#######################################################################################################################

    def nextQuestion(self):
        if self.yesBtn.isChecked():
            userAns = "a"

        elif self.noBtn.isChecked():
            userAns = "b"


        else:
            userAns = None
            self.regCode.msgBox(
                "No answer",
                'Please choose "Yes" or "No"'
            )

        if userAns:
            # check user ans
            self.assess.checkAns(userAns)
            # change/switch question
            nextQuestion = self.assess.nextQuestion()

            if nextQuestion:
                self.loadQuestions(nextQuestion)
                return
            else:
                try:
                    Sessions.criticalReasoningScore = self.assess.finalScore()
                    self.getFinalScore()

                    finalGrade = self.assess.finalGrade(
                        Sessions.numericalReasoningScore,
                        Sessions.verbalReasoningScore,
                        Sessions.logicalReasoningScore,
                        Sessions.criticalReasoningScore
                    )
                    print(
                        f"Numerical Score: {Sessions.numericalReasoningScore}\n"
                        f"Verbal Score: {Sessions.verbalReasoningScore}\n"
                        f"Logical Score: {Sessions.logicalReasoningScore}\n"
                        f"Verbal Score: {Sessions.criticalReasoningScore}\n"
                    )
                    self.regCode.msgBox(
                        "Session complete",
                        f"Your overall score is {finalGrade:.0f}"
                    )
                    print(f"final grade: {finalGrade}%")
                except Exception as e:
                    print(f"Exception Error: {e}")

#######################################################################################################################

    def getDataFromDB(self, category):
        url = "http://localhost/BackEnd/scholarshipManagement/assessments/assessmentValidation.php"
        # category = "numerical"
        response = requests.post(
            url,
            data={
                "category": category
            }
        )
        print(f"RAW RESPONSE: {response.text}")
        result = json.loads(response.text)
        msg = result.get("Message", "Unknown Response")

        if result.get("status") == "success":
            dbContent = result.get("data", [])
            self.assess = Assessment(dbContent)

            firstQuestion = self.assess.getQuestion()
            self.loadQuestions(firstQuestion)

        elif result.get("status") == "error":
            self.regCode.msgBox(
                "Error(Critical)",
                msg
            )

    def getFinalScore(self):
        perc = (self.assess.score / 5) * 100
        self.regCode.msgBox(
            "Sub-test complete",
            f'You scored {self.assess.finalScore()}/5\n{perc:.0f}%\nClick "ok" to check out your overall grade.'
        )

#######################################################################################################################
    def startAssessment(self):
        self.criticalReasoningStackedWidget.setCurrentIndex(1)
        self.getDataFromDB("critical")

########################################################################################################################
    def hideWindow(self):
        self.hide()