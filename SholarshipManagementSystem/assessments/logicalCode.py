from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget

from SholarshipManagementSystem.assessments.logicalPage import Ui_logicalReasoningForm
from SholarshipManagementSystem.authentications.regValidationPHP import RegCode
from SholarshipManagementSystem.classes.assessment import Assessment
import json
import requests
import Sessions

class LogicalCode(QWidget, Ui_logicalReasoningForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":icons/SMsysIcon.png"))
        self.setWindowTitle("Logical Reasoning")
        self.regCode = RegCode()
        self.assess = None
        self.controller = None

        self.timeLimit = 20
        self.remainingTime = self.timeLimit

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)


        self.btnClicks()

        self.logicalReasoningStackedWidget.setCurrentIndex(0)

########################################################################################################################
    def btnClicks(self):
        self.startBtn.clicked.connect(self.startAssessment)
        self.qNextBtn.clicked.connect(self.nextQuestion)

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
                Sessions.logicalReasoningScore = self.assess.finalScore()
                self.timer.stop()

                self.goToCritical()

    ########################################################################################################################
    def getDataFromDB(self, category):
        url = "http://localhost/BackEnd/scholarshipManagement/assessments/assessmentValidation.php"

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
    def getFinalScore(self):
        perc = (self.assess.score / 10) * 100
        self.regCode.msgBox(
            "Sub-test complete",
            f"You scored {self.assess.finalScore()}/10\n{perc:.0f}%\nNext test is on Critical Thinking."
        )

########################################################################################################################
    def startAssessment(self):
        self.logicalReasoningStackedWidget.setCurrentIndex(1)
        self.getDataFromDB("logical")

########################################################################################################################
    def hideWindow(self):
        self.close()

########################################################################################################################
    def goToCritical(self):
        from pageController import Controller
        self.controller = Controller()
        self.controller.showCriticalThinking()
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