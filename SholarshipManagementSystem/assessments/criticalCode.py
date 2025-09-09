from PyQt6.QtCore import QTimer
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

        self.timeLimit = 15
        self.remainingTime = self.timeLimit

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)


        self.btnCLicks()


        self.criticalReasoningStackedWidget.setCurrentIndex(0)

#######################################################################################################################

    def btnCLicks(self):
        self.startBtn.clicked.connect(self.startAssessment)
        self.qNextBtn.clicked.connect(self.nextQuestion)

#######################################################################################################################

    def loadQuestions(self, question):
    # populate labels with questions & options
        self.qTimer.setStyleSheet("color:white;")
        self.question_txt.setText(question.get("question_txt"))

        self.remainingTime = self.timeLimit
        self.qTimer.setText(str(self.remainingTime))
        self.timer.start(1000)

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
                    self.timer.stop()

                    finalGrade = self.assess.finalGrade(
                        Sessions.numericalReasoningScore,
                        Sessions.verbalReasoningScore,
                        Sessions.logicalReasoningScore,
                        Sessions.criticalReasoningScore
                    )

                    self.regCode.msgBox(
                        "Session complete",
                        f"Your overall score is {finalGrade:.0f}%"
                    )


                    #for debugging
                    print(
                        f"Numerical Score: {Sessions.numericalReasoningScore}\n"
                        f"Verbal Score: {Sessions.verbalReasoningScore}\n"
                        f"Logical Score: {Sessions.logicalReasoningScore}\n"
                        f"Verbal Score: {Sessions.criticalReasoningScore}\n"
                    )
                    self.sendDataToDb(
                        "http://localhost/BackEnd/scholarshipManagement/assessments/insertAssessment.php",
                        "jeff@gmail.com",
                        finalGrade,
                        40
                    )

                    print(f"final grade: {finalGrade}%")
                except Exception as e:
                    print(f"Exception Error: {e}")


#######################################################################################################################

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
                "Error(Critical)",
                msg
            )

#######################################################################################################################
    def getFinalScore(self):
        perc = (self.assess.score / 10) * 100
        self.regCode.msgBox(
            "Sub-test complete",
            f'You scored {self.assess.finalScore()}/10\n{perc:.0f}%\nClick "ok" to check out your overall grade.'
        )

#######################################################################################################################
    def sendDataToDb(self, url, email, score, totalQuest):
        result = self.assess.sendDataToDb(
            score,
            email,
            url,
            totalQuest
        )

        msg = result.get("message", "Unknown Response")

        if result.get("status") == "success":
            self.regCode.msgBox(
                "Process Complete",
                f"{msg}"
            )
        elif result.get("status") == "error":
            self.regCode.msgBox(
                "Process Failed!",
                f"{msg}"
            )

#######################################################################################################################
    def startAssessment(self):
        self.criticalReasoningStackedWidget.setCurrentIndex(1)
        self.getDataFromDB("critical")

########################################################################################################################
    def hideWindow(self):
        self.hide()
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