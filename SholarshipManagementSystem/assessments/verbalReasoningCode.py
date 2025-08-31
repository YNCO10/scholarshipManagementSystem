from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

from Sessions import verbalReasoningScore
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.assessments.verbalPage import Ui_VerbalReasoningFrom
from SholarshipManagementSystem.assessments.numericalCode import NumericalReasoningCode
from SholarshipManagementSystem.classes.assessment import Assessment
import json
import requests
import Sessions



class VerbalReasoning(QWidget, Ui_VerbalReasoningFrom):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.setWindowTitle("Verbal Reasoning")
        self.assess = None
        self.regCode = RegCode()
        self.numCode = NumericalReasoningCode()

        self.btnClicks()

        self.verbalReasoninStackedWidget.setCurrentIndex(0)

########################################################################################################################
    def btnClicks(self):
        self.startBtn.clicked.connect(self.startAssessment)
        self.qNextBtn.clicked.connect(self.nextQuestion)

########################################################################################################################
    def nextQuestion(self):
        if self.qOptionA.isChecked():
            choice = "a"
        elif self.qOptionB.isChecked():
            choice = "b"
        elif self.qOptionC.isChecked():
            choice = "c"
        elif self.qOptionD.isChecked():
            choice = "d"
        else:
            choice = None
            self.regCode.msgBox(
                "No answer",
                "Please select one answer"
            )

        if choice:
            # check user ans
            self.assess.checkAns(choice)
            # change/switch question
            nextQuestion = self.assess.nextQuestion()

            if nextQuestion:
                self.loadQuestions(nextQuestion)
                return
            else:
                self.getFinalScore()
                Sessions.verbalReasoningScore = self.assess.finalScore()
                self.close()
                print(f"Numerical Score: {Sessions.numericalReasoningScore}\nVerbal Score: {Sessions.verbalReasoningScore}\n")

########################################################################################################################
    def loadQuestions(self, question):
        # populate labels with questions & options
        self.question_txt.setText(question.get("question_txt"))

        self.qOptionA.setText(question.get("option_a", "None of the above"))
        self.qOptionB.setText(question.get("option_b", "None of the above"))
        self.qOptionC.setText(question.get("option_c", "None of the above"))
        self.qOptionD.setText(question.get("option_d", "None of the above"))

########################################################################################################################
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
                "Error(NumCode)",
                msg
            )

########################################################################################################################
    def startAssessment(self):
        self.getDataFromDB("verbal")
        self.verbalReasoninStackedWidget.setCurrentIndex(1)

########################################################################################################################
    def hideWindow(self):
        self.hide()

########################################################################################################################
    def getFinalScore(self):
        perc = (self.assess.score / 5) * 100
        self.regCode.msgBox(
            "Sub-test complete",
            f"You scored {self.assess.finalScore()}/5 \n{perc:.0f}% \nNext test is on Logical Reasoning"
        )