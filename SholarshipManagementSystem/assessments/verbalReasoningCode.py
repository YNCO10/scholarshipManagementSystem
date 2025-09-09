from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

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
        self.controller = None
        self.regCode = RegCode()
        self.numCode = NumericalReasoningCode()

        self.timeLimit = 15
        self.remainingTime = self.timeLimit

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)

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
                self.timer.stop()
                self.close()


                self.goToLogical()

########################################################################################################################
    def loadQuestions(self, question):
        # populate labels with questions & options
        self.qTimer.setStyleSheet("color:white;")
        self.question_txt.setText(question.get("question_txt"))

        self.qOptionA.setText(question.get("option_a", "None of the above"))
        self.qOptionB.setText(question.get("option_b", "None of the above"))
        self.qOptionC.setText(question.get("option_c", "None of the above"))
        self.qOptionD.setText(question.get("option_d", "None of the above"))

        self.remainingTime = self.timeLimit
        self.qTimer.setText(str(self.remainingTime))
        self.timer.start(1000)

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
                "Error(verbal)",
                msg
            )

########################################################################################################################
    def startAssessment(self):
        self.getDataFromDB("verbal")
        self.verbalReasoninStackedWidget.setCurrentIndex(1)

########################################################################################################################
    def hideWindow(self):
        self.close()

########################################################################################################################
    def getFinalScore(self):
        perc = (self.assess.score / 10) * 100
        self.regCode.msgBox(
            "Sub-test complete",
            f"You scored {self.assess.finalScore()}/10 \n{perc:.0f}% \nNext test is on Logical Reasoning"
        )

########################################################################################################################
    def goToLogical(self):
        from pageController import Controller
        self.controller = Controller()
        self.controller.showLogicalReasoning()
        self.close()

########################################################################################################################
    def updateTimer(self):
        self.remainingTime -= 1
        self.qTimer.setText(str(self.remainingTime))

        if self.remainingTime < 6:
            self.qTimer.setStyleSheet("color:Red;")

        if str(self.remainingTime) == "0":
            self.timer.stop()

            nextQuestion = self.assess.nextQuestion()

            if nextQuestion:
                self.loadQuestions(nextQuestion)
                return
            else:
                self.getFinalScore()
########################################################################################################################