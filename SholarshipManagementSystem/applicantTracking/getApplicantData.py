from SholarshipManagementSystem.classes.applicantTracking import ApplicantTracker
import Sessions
from SholarshipManagementSystem.classes.scoreHandler import ScoreHandler

import requests

class GetApplicantData:
    def __init__(self):
        url = "http://localhost/BackEnd/scholarshipManagement/applicantTracking/getData.php"
        # print("Checkpoint1")
        self.applicantTracker = ApplicantTracker(
            "jeff@gmail.com",
            url
        )
        # print("Checkpoint3")
        self.scoreHandler = ScoreHandler()
        # print("Checkpoint4")
        self.scoreApplicant()


    def scoreApplicant(self):
        result = self.applicantTracker.getApplicantData()
        msg = result.get("message", "Unknown Msg")

        if result.get("status") == "success":
            applicant_data = {
                "gpa": result.get("gpa"),
                "transcript": result.get("transcript"),
                "need": result.get("need"),
                "financialProof": result.get("financialProof"),
                "incomeBracket": result.get("incomeBracket"),
                "uploadedDocs": result.get("uploadedDocs"),
                "requiredDocs": ["NationalID", "transcript", "recommendation", "proofOfNeed"],
                "score": result.get("score"),
                "totalQuest": 20
            }

            score = self.scoreHandler.applicantScore(applicant_data)
            print(f"Applicant overall score is {int(score)}")

            response = requests.post(
                url="http://localhost/BackEnd/scholarshipManagement/applicant/insertScore.php",
                data={
                    "email" : "jeff@gmail.com",
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

try:
    exe = GetApplicantData()
except Exception as e:
    print(f"Exception: {e}")