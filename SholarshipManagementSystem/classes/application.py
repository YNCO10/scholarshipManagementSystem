
import requests

class Application:
    def __init__(self,
                 schoolAttended,
                 gpa,
                 financialAssistance,
                 reasonForApplying,
                 transcript,
                 nationalID,
                 recommendationLetter,
                 careerGoals,
                 proofOfNeed,
                 incomeBracket
                 ):
        super().__init__()
        self.schoolAttended = schoolAttended
        self.gpa = gpa
        self.financialAssistance = financialAssistance
        self.reasonForApplying = reasonForApplying
        self.transcript = transcript
        self.nationalID = nationalID
        self.recommendationLetter = recommendationLetter
        self.careerGoals = careerGoals
        self.proofOfNeed = proofOfNeed
        self.incomeBracket = incomeBracket

    def apply(self, url):
        response = requests.post(
            url, 
            data=self.toDict(),
            files={
                "Transcript": open(self.transcript, "rb"),
                "National_ID": open(self.nationalID, "rb"),
                "Recommendation_Letter": open(self.recommendationLetter, "rb"),
                "Proof_Of_Need": open(self.proofOfNeed, "rb")
            }
        )
        try:
            return response.json()
        except ValueError:
            # If backend didn’t return JSON, let’s inspect raw text
            return {"status": "error", "message": response.text}

    def toDict(self):
        return{
            "schoolAttended": self.schoolAttended,
            "gpa": self.gpa,
            "fin_assistance": self.financialAssistance,
            "reasonForApplying": self.reasonForApplying,
            "careerGoal": self.careerGoals
        }