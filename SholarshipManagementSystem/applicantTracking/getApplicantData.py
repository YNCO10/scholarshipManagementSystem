from SholarshipManagementSystem.classes.applicantTracking import ApplicantTracker
import Sessions
from SholarshipManagementSystem.classes.scoreHandler import ScoreHandler

import requests

class GetApplicantData:
    def __init__(self, email):
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
            "http://localhost/BackEnd/scholarshipManagement/applicantTracking/getData.php"
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
        self.docWeight = weight.get("doc")
        self.financialWeight = weight.get("financial")

        #use weights
        self.scoreHandler = ScoreHandler(
            self.academicWeight,
            self.financialWeight,
            self.docWeight,
            self.assessmentWeight,
        )
        # print("Checkpoint4")
        self.scoreApplicant()


    def scoreApplicant(self):
        result = self.applicantTracker.getApplicantData()
        msg = result.get("message", "Unknown Msg")

        if result.get("status") == "success":

            if result.get("incomeBracket") == "less than MWK150,000":
                self.incomeBracket = "veryLow"
            elif result.get("incomeBracket") == "Between MWK150,000 - MWK250,000":
                self.incomeBracket = "low"
            elif result.get("incomeBracket") == "Between MKW250,000 - MWK500,000":
                self.incomeBracket = "average"
            elif result.get("incomeBracket") == "Between MWK500,00 - MWK1,000,000":
                self.incomeBracket = "aboveAverage"
            elif result.get("incomeBracket") == "Between MWK1,000,000 - MWK2,000,000":
                self.incomeBracket = "high"
            elif result.get("incomeBracket") == "More than MWK2,000,000":
                self.incomeBracket = "veryHigh"

            self.gpa = result.get("gpa")
            self.transcript = result.get("transcript")
            self.need = result.get("need")
            self.financialProof = result.get("financialProof")
            self.uploadedDocs = result.get("uploadedDocs")
            self.requiredDocs = ["Recommendation Letter", "Proof Of Need", "National ID", "Transcript"]
            self.assessmentScore = result.get("score")
            self.totalQuest = 40


            applicant_data = {
                "gpa": self.gpa,
                "transcript": self.transcript,
                "need": self.need,
                "financialProof": self.financialProof,
                "incomeBracket": self.incomeBracket,
                "uploadedDocs": self.uploadedDocs,
                "requiredDocs": self.requiredDocs,
                "assessmentScore": self.assessmentScore,
                "totalQuest": 40
            }

            score = self.scoreHandler.applicantScore(applicant_data)
            print(f"Applicant overall score is {int(score)}")

            response = requests.post(
                url="http://localhost/BackEnd/scholarshipManagement/applicant/insertScore.php",
                data={
                    "email" : self.email,
                    "score" : int(score)
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
            print(f"Error(Retrieval): {msg}")
            return

    def applicantCriteriaTemplate(self,
                                  transcriptSubmittedLabel,
                                  academicScoreLabel,
                                  proofOfNeedSubmittedLabel,
                                  incomeBracketLabel_2,
                                  financialScoreLabel,
                                  documentsUploadedLabel,
                                  documentScoreLabel,
                                  assessmentScoreLabel,
                                  academicWeightCombo,
                                  financialWeightCombo,
                                  docLabelCombo,
                                  assessmentWeightCombo,
                                  finalScoreFormulaLabel,
                                  finalScoreLabel):
        try:
            # Academic section--------------------------------------------
            if self.transcript:
                transcriptSubmittedLabel.setText("Transcript was Submitted")
            else:
                transcriptSubmittedLabel.setText("Transcript was Not Submitted")

            # academic score
            academicScore = self.scoreHandler.AcademicScore(self.gpa, self.transcript)
            academicScoreLabel.setText(f"Score: {academicScore} Points.")

            # Financial section--------------------------------------------
            if self.financialProof:
                proofOfNeedSubmittedLabel.setText("Proof Of Need was Submitted")
            else:
                proofOfNeedSubmittedLabel.setText("Proof Of Need was Not Submitted")

            # income bracket
            incomeBracketLabel_2.setText(f"Income Bracket: {self.incomeBracket}")

            # financial score
            financialScore = self.scoreHandler.financialScore(self.need, self.financialProof, self.incomeBracket)
            financialScoreLabel.setText(f"Score: {financialScore} Points.")

            # Document section--------------------------------------------
            documentsUploadedLabel.setText(
                f"Number of Documents uploaded: {len(self.uploadedDocs)}/{len(self.requiredDocs)}")
            # doc Score
            docScore = self.scoreHandler.documentScore(self.uploadedDocs, self.requiredDocs)
            documentScoreLabel.setText(f"Score: {docScore} Points.")

            # Assessment section--------------------------------------------
            assessmentScore = self.scoreHandler.assessmentScore(self.assessmentScore, self.totalQuest)
            assessmentScoreLabel.setText(f"Score: {assessmentScore} Points.")

            # Weights section-----------------------------------------------
            academicWeightCombo.setCurrentText(str(self.academicWeight))
            assessmentWeightCombo.setCurrentText(str(self.assessmentWeight))
            docLabelCombo.setCurrentText(str(self.docWeight))
            financialWeightCombo.setCurrentText(str(self.financialWeight))

            # Final score section--------------------------------------------
            sumOfWeights = self.academicWeight + self.assessmentWeight + self.docWeight + self.financialWeight
            finalScoreFormulaLabel.setText(
                f"(({academicScore}*{self.academicWeight})+({financialScore}*{self.financialWeight})+({docScore}*{self.docWeight})+({assessmentScore}*{self.assessmentWeight}))/{sumOfWeights}")
            finalScore = ((academicScore * self.academicWeight) + (financialScore * self.financialWeight) + (
                        docScore * self.docWeight) + (assessmentScore * self.assessmentWeight)) / sumOfWeights
            finalScoreLabel.setText(f"Final score: {finalScore:.0f}")

        except Exception as error:
            print(f"Exception(applicantCriteriaTemplate): {error}")

# try:
#     exe = GetApplicantData()
# except Exception as e:
#     print(f"Exception(GetApplicantData): {e}")