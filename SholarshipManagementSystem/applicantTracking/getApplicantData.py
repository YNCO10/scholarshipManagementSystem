from SholarshipManagementSystem.classes.applicantTracking import ApplicantTracker
import Sessions
from SholarshipManagementSystem.classes.scoreHandler import ScoreHandler

import requests

class GetApplicantData:
    def __init__(self, email):
        self.applicantName = None
        self.assessmentScore = None
        self.totalQuest = None
        self.score = None
        self.requiredDocs = None
        self.uploadedDocs = None
        self.financialProof = None
        self.need = None
        self.transcript = None
        self.gpa = None
        self.incomeBracket = None
        self.email = email

        # print("Checkpoint1")
        self.applicantTracker = ApplicantTracker(
            self.email,
            "http://localhost/BackEnd/scholarshipManagement/applicantTracking/getApplicantDataForPage.php"
        )

        # get weights----------------------------------------------------------------------
        response = requests.get(
            "http://localhost/BackEnd/scholarshipManagement/applicantTracking/getWeights.php"
        )

        result = response.json()
        msg = result.get("message", "Unknown Msg")
        if result.get("status") == "error":
            print(f"Error(getWeights): {msg}")

        dbContent = result.get("data", [])
        weight = dbContent[0]

        self.academicWeight = weight.get("academic")
        self.assessmentWeight = weight.get("assessment")
        self.financialWeight = weight.get("financial")

        print(f"academicWeight: {self.academicWeight}")
        print(f"assessmentWeight: {self.assessmentWeight}")
        print(f"financialWeight: {self.financialWeight}")
        #use weights
        self.scoreHandler = ScoreHandler(
            self.academicWeight,
            self.financialWeight,
            self.assessmentWeight,
        )
        #get scores-------------------------------------------------------------------------
        response = requests.get(
            "http://localhost/BackEnd/scholarshipManagement/applicantTracking/getScore.php"
        )

        result = response.json()
        msg = result.get("message", "Unknown Msg")
        if result.get("status") == "error":
            print(f"Error(getScores): {msg}")

        scores = result.get("scores", [])
        self.intScores = []
        for score in scores:
            self.intScores.append(int(score))

        self.sumOfScores = sum(self.intScores)
        # print(sumOfScores)
        # self.scoreApplicant()

########################################################################################################################
    def scoreApplicant(self):
        try:

            dbContent = self.applicantTracker.getApplicantData()
            # msg = dbContent.get("message", "Unknown Msg")
            allContent = dbContent.get("data")
            result = allContent[0]

            if dbContent.get("status") == "success":

                if result.get("income_bracket") == "less than MWK150,000":
                    self.incomeBracket = "veryLow"
                elif result.get("income_bracket") == "Between MWK150,000 - MWK250,000":
                    self.incomeBracket = "low"
                elif result.get("income_bracket") == "Between MKW250,000 - MWK500,000":
                    self.incomeBracket = "average"
                elif result.get("income_bracket") == "Between MWK500,00 - MWK1,000,000":
                    self.incomeBracket = "aboveAverage"
                elif result.get("income_bracket") == "Between MWK1,000,000 - MWK2,000,000":
                    self.incomeBracket = "high"
                elif result.get("income_bracket") == "More than MWK2,000,000":
                    self.incomeBracket = "veryHigh"

                self.gpa = result.get("gpa")
                self.need = result.get("fin_assistance")
                self.uploadedDocs = result.get("uploadedDocs")
                self.requiredDocs = ["Recommendation Letter", "Proof Of Need", "National ID", "Transcript"]
                self.assessmentScore = result.get("assessment_score")
                self.totalQuest = 40
                self.applicantName = result.get("name")

                print(f"GPA: {self.gpa}")

                applicant_data = {
                    "gpa": self.gpa,
                    "need": self.need,
                    "incomeBracket": self.incomeBracket,
                    "assessmentScore": self.assessmentScore,
                    "totalQuest": 40
                }

                score = self.scoreHandler.applicantScore(applicant_data)
                print(f"Applicant overall score is {int(score)}")

                response = requests.post(
                    url="http://localhost/BackEnd/scholarshipManagement/applicant/insertScore.php",
                    data={
                        "email": self.email,
                        "score": int(score)
                    }
                )

                print(f"RAW RESPONSE: {response.text}")
                result = response.json()
                msg = result.get("message", "Unknown Msg")

                if result.get("status") == "success":
                    print(f"Applicant overall score for ranking has been recorded\n{msg}")
                    return

                elif result.get("status") == "error":
                    print(f"Error(Update failed): {msg}")
                    return

            elif result.get("status") == "error":
                print(f"Error(scoreApplicant)")
                # print(f"Error(scoreApplicant): {msg}")
                return

        except Exception as e:
            print(f"Exception (scoreApplicant): {e}")
########################################################################################################################
    def applicantCriteriaTemplate(self,
                                  academicScoreLabel,
                                  incomeBracketLabel_2,
                                  financialScoreLabel,
                                  assessmentScoreLabel,
                                  academicWeightCombo,
                                  financialWeightCombo,
                                  assessmentWeightCombo,
                                  finalScoreFormulaLabel,
                                  finalScoreLabel,
                                  needLabel,
                                  gpaScoreLabel,
                                  overallAvgScoreLabel,
                                  applicantEligibilityLabel,
                                  successPredictionLabel):
        try:
            # Academic section----------------------------------------------
            gpaScoreLabel.setText(f"{self.gpa}/5 * 100")

            # academic score
            academicScore = self.scoreHandler.AcademicScore(self.gpa)
            academicScoreLabel.setText(f"Score: {academicScore} Points.")

            # Financial section---------------------------------------------
            if self.need == 0:
                needLabel.setText("Financial Assistance was requested")
            else:
                needLabel.setText("Financial Assistance was NOT requested")

            # income bracket
            incomeBracketLabel_2.setText(f"Income Bracket: {self.incomeBracket}")

            # financial score
            financialScore = self.scoreHandler.financialScore(self.need, self.incomeBracket)
            financialScoreLabel.setText(f"Score: {financialScore} Points.")

            # Assessment section---------------------------------------------
            assessmentScore = self.scoreHandler.assessmentScore(self.assessmentScore, self.totalQuest)
            assessmentScoreLabel.setText(f"Score: {assessmentScore:.0f} Points.")

            # Weights section------------------------------------------------
            academicWeightCombo.setCurrentText(f"{float(self.academicWeight):.1f}")
            assessmentWeightCombo.setCurrentText(f"{float(self.assessmentWeight):.1f}")
            financialWeightCombo.setCurrentText(f"{float(self.financialWeight):.1f}")

            # Final score section---------------------------------------------
            sumOfWeights = self.academicWeight + self.assessmentWeight + self.financialWeight
            finalScoreFormulaLabel.setText(
                f"(({academicScore}*{self.academicWeight})+({financialScore}*{self.financialWeight})+({assessmentScore}*{self.assessmentWeight}))/{sumOfWeights}")
            finalScore = ((academicScore * self.academicWeight) + (financialScore * self.financialWeight) + (assessmentScore * self.assessmentWeight)) / sumOfWeights
            finalScoreLabel.setText(f"Applicant score: {finalScore:.0f}")

            #Average and eligibility section ---------------------------------
            avgScore = self.scoreHandler.overallAvgScore(self.sumOfScores, len(self.intScores))
            successPred = self.scoreHandler.calculateSuccessPrediction(finalScore)
            eligibility = self.scoreHandler.calculateEligibility(avgScore, finalScore)

            overallAvgScoreLabel.setText(f"System Threshold = {avgScore:.2f}")
            successPredictionLabel.setText(f"{self.applicantName} is {successPred} to be accepted for a scholarship.")
            applicantEligibilityLabel.setText(f"{self.applicantName} is {eligibility}")

        except Exception as error:
            print(f"Exception(applicantCriteriaTemplate): {error}")

try:
    exe = GetApplicantData(
        "test9@gmail.com"
    )
except Exception as e:
    print(f"Exception(GetApplicantData): {e}")