
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
                 careerGoals
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

    def apply(self, url):
        response = requests.post(url, data=self.toDict())
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
            "transcript": self.transcript,
            "nationalID": self.nationalID,
            "recommendation_letter": self.recommendationLetter,
            "careerGoal": self.careerGoals
        }